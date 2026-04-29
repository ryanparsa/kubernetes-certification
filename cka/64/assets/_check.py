#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

SCRIPT_DIR = os.path.dirname(__file__)
KUBECONFIG = os.environ.get("KUBECONFIG")
if not KUBECONFIG or not os.path.exists(KUBECONFIG):
    local_config = os.path.join(SCRIPT_DIR, "kubeconfig.yaml")
    if os.path.exists(local_config):
        KUBECONFIG = local_config

def kubectl(*args):
    cmd = ["kubectl"]
    if KUBECONFIG:
        cmd += ["--kubeconfig", KUBECONFIG]
    cmd += args
    result = subprocess.run(
        cmd,
        capture_output=True, text=True,
    )
    return result.stdout.strip()

class TestNetworkPolicyLab(unittest.TestCase):
    def test_deployments_exist(self):
        for deploy in ["web", "api", "db"]:
            status = kubectl("get", "deployment", deploy, "-n", "network", "-o", "jsonpath={.status.availableReplicas}")
            try:
                available = int(status)
            except (ValueError, TypeError):
                available = 0
            self.assertTrue(available >= 1, f"Deployment {deploy} should have at least 1 available replica")

    def test_db_env_var(self):
        env = kubectl("get", "deployment", "db", "-n", "network", "-o", "jsonpath={.spec.template.spec.containers[0].env[0].value}")
        self.assertEqual(env, "trust", "POSTGRES_HOST_AUTH_METHOD should be trust")

    def test_web_policy(self):
        out = kubectl("get", "networkpolicy", "web-policy", "-n", "network", "-o", "json")
        policy = json.loads(out)
        self.assertEqual(policy["spec"]["podSelector"]["matchLabels"]["app"], "web")
        self.assertIn("Egress", policy["spec"]["policyTypes"])
        # Check egress allows api
        allowed_api = False
        for egress in policy["spec"].get("egress", []):
            for to in egress.get("to", []):
                if to.get("podSelector", {}).get("matchLabels", {}).get("app") == "api":
                    allowed_api = True
        self.assertTrue(allowed_api, "web-policy should allow egress to api")

    def test_api_policy(self):
        out = kubectl("get", "networkpolicy", "api-policy", "-n", "network", "-o", "json")
        policy = json.loads(out)
        self.assertEqual(policy["spec"]["podSelector"]["matchLabels"]["app"], "api")
        self.assertIn("Ingress", policy["spec"]["policyTypes"])
        self.assertIn("Egress", policy["spec"]["policyTypes"])

        # Check ingress from web
        allowed_web = False
        for ingress in policy["spec"].get("ingress", []):
            for _from in ingress.get("from", []):
                if _from.get("podSelector", {}).get("matchLabels", {}).get("app") == "web":
                    allowed_web = True
        self.assertTrue(allowed_web, "api-policy should allow ingress from web")

        # Check egress to db
        allowed_db = False
        for egress in policy["spec"].get("egress", []):
            for to in egress.get("to", []):
                if to.get("podSelector", {}).get("matchLabels", {}).get("app") == "db":
                    allowed_db = True
        self.assertTrue(allowed_db, "api-policy should allow egress to db")

    def test_db_policy(self):
        out = kubectl("get", "networkpolicy", "db-policy", "-n", "network", "-o", "json")
        policy = json.loads(out)
        self.assertEqual(policy["spec"]["podSelector"]["matchLabels"]["app"], "db")
        self.assertIn("Ingress", policy["spec"]["policyTypes"])

        # Check ingress from api
        allowed_api = False
        for ingress in policy["spec"].get("ingress", []):
            for _from in ingress.get("from", []):
                if _from.get("podSelector", {}).get("matchLabels", {}).get("app") == "api":
                    allowed_api = True
        self.assertTrue(allowed_api, "db-policy should allow ingress from api")

    def test_connectivity(self):
        # This is a more functional check
        web_pod = kubectl("get", "pod", "-n", "network", "-l", "app=web", "-o", "jsonpath={.items[0].metadata.name}")
        api_pod = kubectl("get", "pod", "-n", "network", "-l", "app=api", "-o", "jsonpath={.items[0].metadata.name}")
        db_pod = kubectl("get", "pod", "-n", "network", "-l", "app=db", "-o", "jsonpath={.items[0].metadata.name}")

        api_ip = kubectl("get", "pod", api_pod, "-n", "network", "-o", "jsonpath={.status.podIP}")
        db_ip = kubectl("get", "pod", db_pod, "-n", "network", "-o", "jsonpath={.status.podIP}")

        # Use wget -q -T 2 -O - http://... as it's more likely to be in alpine than curl
        # Web to API should work (nginx on 80)
        cmd = ["kubectl"]
        if KUBECONFIG: cmd += ["--kubeconfig", KUBECONFIG]
        cmd += ["exec", "-n", "network", web_pod, "--", "wget", "-q", "-T", "2", "-O", "-", f"http://{api_ip}"]
        res = subprocess.run(cmd, capture_output=True)
        self.assertEqual(res.returncode, 0, f"Web should be able to connect to API. Error: {res.stderr.decode()}")

        # Web to DB should fail (postgres on 5432)
        # We check that it's NOT a timeout (exit code 1 for wget if it can't connect, but let's be careful)
        # Actually wget will exit with non-zero if it times out or connection refused.
        # To distinguish between "tool missing" and "blocked", we'd need more logic.
        # But let's assume wget is there.
        cmd = ["kubectl"]
        if KUBECONFIG: cmd += ["--kubeconfig", KUBECONFIG]
        cmd += ["exec", "-n", "network", web_pod, "--", "wget", "-q", "-T", "2", "-O", "-", f"http://{db_ip}:5432"]
        res = subprocess.run(cmd, capture_output=True)
        # If it's blocked, it should exit with non-zero.
        # If wget is missing, it will be 127.
        self.assertNotEqual(res.returncode, 0, "Web should NOT be able to connect to DB")
        self.assertNotEqual(res.returncode, 127, "wget missing in web pod")

        # API to DB should work (connection allowed, even if HTTP fails)
        cmd = ["kubectl"]
        if KUBECONFIG: cmd += ["--kubeconfig", KUBECONFIG]
        cmd += ["exec", "-n", "network", api_pod, "--", "wget", "-q", "-T", "2", "-O", "-", f"http://{db_ip}:5432"]
        res = subprocess.run(cmd, capture_output=True)
        # wget on postgres port will likely return 8 (Server error) or 1 (General failure) but NOT timeout if allowed.
        # If it's a timeout, it's usually 4.
        self.assertNotEqual(res.returncode, 4, "API to DB connection timed out (likely blocked)")
        self.assertNotEqual(res.returncode, 127, "wget missing in api pod")

if __name__ == "__main__":
    unittest.main(verbosity=2)

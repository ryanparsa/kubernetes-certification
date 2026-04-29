#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

SCRIPT_DIR = os.path.dirname(__file__)
LOCAL_KUBECONFIG = os.path.join(SCRIPT_DIR, "..", "lab", "kubeconfig.yaml")
KUBECONFIG = LOCAL_KUBECONFIG if os.path.exists(LOCAL_KUBECONFIG) else os.environ.get("KUBECONFIG")

def kubectl(*args):
    cmd = ["kubectl"]
    if KUBECONFIG:
        cmd.extend(["--kubeconfig", KUBECONFIG])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

class TestConfigMapVolume(unittest.TestCase):
    def test_deployment_mounts_configmap(self):
        """Deployment web-server mounts ConfigMap web-server-conf as a volume"""
        deployment_json = kubectl("get", "deployment", "web-server", "-o", "json")
        self.assertTrue(deployment_json, "kubectl get deployment returned nothing")
        deployment = json.loads(deployment_json)

        volumes = deployment["spec"]["template"]["spec"].get("volumes", [])
        found_volume = any(
            v.get("name") == "web-server-conf" and v.get("configMap", {}).get("name") == "web-server-conf"
            for v in volumes
        )
        self.assertTrue(found_volume, "Deployment does not have a volume for ConfigMap web-server-conf")

    def test_volume_mounted_at_path(self):
        """Volume mounted at /etc/nginx/conf.d"""
        deployment_json = kubectl("get", "deployment", "web-server", "-o", "json")
        self.assertTrue(deployment_json, "kubectl get deployment returned nothing")
        deployment = json.loads(deployment_json)

        container = deployment["spec"]["template"]["spec"]["containers"][0]
        volume_mounts = container.get("volumeMounts", [])

        found_mount = any(
            vm.get("name") == "web-server-conf" and vm.get("mountPath") == "/etc/nginx/conf.d"
            for vm in volume_mounts
        )
        self.assertTrue(found_mount, "ConfigMap is not mounted at /etc/nginx/conf.d")

    def test_nginx_config_validation(self):
        """nginx -t inside the container passes validation"""
        pod_name = kubectl("get", "pod", "-l", "app=web-server", "-o", "jsonpath={.items[0].metadata.name}")
        self.assertTrue(pod_name, "No pod found for deployment web-server")

        cmd = ["kubectl"]
        if KUBECONFIG:
            cmd.extend(["--kubeconfig", KUBECONFIG])
        cmd.extend(["exec", pod_name, "--", "nginx", "-t"])

        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"nginx -t failed: {result.stderr}")

class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)

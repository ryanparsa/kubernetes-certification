#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

SCRIPT_DIR = os.path.dirname(__file__)
KUBECONFIG = os.environ.get("KUBECONFIG") or os.path.join(SCRIPT_DIR, "..", "lab", "kubeconfig.yaml")

def kubectl(*args):
    cmd = ["kubectl"]
    if KUBECONFIG:
        cmd.extend(["--kubeconfig", KUBECONFIG])

    result = subprocess.run(
        [*cmd, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()

class TestConfigMapVolume(unittest.TestCase):
    def test_deployment_mounts_configmap(self):
        """Deployment web-server mounts ConfigMap web-server-conf as a volume"""
        deployment_json = kubectl("get", "deployment", "web-server", "-o", "json")
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
        result = subprocess.run(
            ["kubectl", "--kubeconfig", KUBECONFIG, "exec", pod_name, "--", "nginx", "-t"],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, f"nginx -t failed: {result.stderr}")

if __name__ == "__main__":
    unittest.main(verbosity=2)

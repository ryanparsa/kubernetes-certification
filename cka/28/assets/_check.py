#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

SCRIPT_DIR = os.path.dirname(__file__)
KUBECONFIG_FILE = os.path.join(SCRIPT_DIR, "kubeconfig.yaml")

def kubectl(*args):
    cmd = ["kubectl"]
    if os.path.exists(KUBECONFIG_FILE):
        cmd.extend(["--kubeconfig", KUBECONFIG_FILE])
    cmd.extend(args)
    result = subprocess.run(
        cmd,
        capture_output=True, text=True,
    )
    return result.stdout.strip()

class QuietResult(unittest.TextTestResult):
    def addSuccess(self, test):
        pass
    def addError(self, test, err):
        super().addError(test, err)
    def addFailure(self, test, err):
        super().addFailure(test, err)

class TestSecretPod(unittest.TestCase):
    def test_namespace_exists(self):
        """Namespace secret exists"""
        ns = kubectl("get", "ns", "secret", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(ns, "secret")

    def test_secret1_exists(self):
        """Secret secret1 exists in secret namespace"""
        name = kubectl("get", "secret", "secret1", "-n", "secret", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(name, "secret1")

    def test_secret2_exists_and_data(self):
        """Secret secret2 exists and has correct data"""
        data = kubectl("get", "secret", "secret2", "-n", "secret", "-o", "json")
        secret_json = json.loads(data)
        import base64
        self.assertEqual(base64.b64decode(secret_json['data']['user']).decode(), "user1")
        self.assertEqual(base64.b64decode(secret_json['data']['pass']).decode(), "1234")

    def test_pod_exists_and_image(self):
        """Pod secret-pod exists with busybox:1 image"""
        pod_info = kubectl("get", "pod", "secret-pod", "-n", "secret", "-o", "json")
        pod_json = json.loads(pod_info)
        self.assertEqual(pod_json['spec']['containers'][0]['image'], "busybox:1")
        self.assertEqual(len(pod_json['spec']['containers']), 1)

    def test_pod_mounts_secret1_readonly(self):
        """Pod secret-pod mounts secret1 readonly at /tmp/secret1"""
        pod_info = kubectl("get", "pod", "secret-pod", "-n", "secret", "-o", "json")
        pod_json = json.loads(pod_info)

        # Check volume
        volumes = pod_json['spec']['volumes']
        secret1_vol = next((v for v in volumes if v.get('secret', {}).get('secretName') == 'secret1'), None)
        self.assertIsNotNone(secret1_vol)
        vol_name = secret1_vol['name']

        # Check mount
        mounts = pod_json['spec']['containers'][0]['volumeMounts']
        mount = next((m for m in mounts if m['name'] == vol_name), None)
        self.assertIsNotNone(mount)
        self.assertEqual(mount['mountPath'], "/tmp/secret1")
        self.assertTrue(mount.get('readOnly', False))

    def test_pod_has_secret2_env(self):
        """Pod has secret2 env variables APP_USER and APP_PASS"""
        pod_info = kubectl("get", "pod", "secret-pod", "-n", "secret", "-o", "json")
        pod_json = json.loads(pod_info)
        env = pod_json['spec']['containers'][0]['env']

        app_user = next((e for e in env if e['name'] == 'APP_USER'), None)
        self.assertIsNotNone(app_user)
        self.assertEqual(app_user['valueFrom']['secretKeyRef']['name'], 'secret2')
        self.assertEqual(app_user['valueFrom']['secretKeyRef']['key'], 'user')

        app_pass = next((e for e in env if e['name'] == 'APP_PASS'), None)
        self.assertIsNotNone(app_pass)
        self.assertEqual(app_pass['valueFrom']['secretKeyRef']['name'], 'secret2')
        self.assertEqual(app_pass['valueFrom']['secretKeyRef']['key'], 'pass')

if __name__ == "__main__":
    runner = unittest.TextTestRunner(resultclass=QuietResult, verbosity=2)
    unittest.main(testRunner=runner, exit=False)

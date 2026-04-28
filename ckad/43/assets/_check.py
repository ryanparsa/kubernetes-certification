#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

KUBECONFIG_FILE = os.path.join(os.path.dirname(__file__), "kubeconfig.yaml")

def kubectl(*args):
    cmd = ["kubectl"]
    if os.path.exists(KUBECONFIG_FILE) and not os.environ.get("KUBECONFIG"):
        cmd.extend(["--kubeconfig", KUBECONFIG_FILE])

    result = subprocess.run(
        [*cmd, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()

class TestDatabasePersistentStorage(unittest.TestCase):
    def test_namespace_exists(self):
        ns = kubectl("get", "ns", "state", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(ns, "state")

    def test_pv_exists_and_configured(self):
        pv = json.loads(kubectl("get", "pv", "db-pv", "-o", "json"))
        self.assertEqual(pv['spec']['capacity']['storage'], "1Gi")
        self.assertIn("ReadWriteOnce", pv['spec']['accessModes'])
        self.assertEqual(pv['spec']['hostPath']['path'], "/mnt/data")
        self.assertEqual(pv['spec']['persistentVolumeReclaimPolicy'], "Retain")

    def test_pvc_exists_and_configured(self):
        pvc = json.loads(kubectl("get", "pvc", "db-pvc", "-n", "state", "-o", "json"))
        self.assertEqual(pvc['spec']['resources']['requests']['storage'], "500Mi")
        self.assertIn("ReadWriteOnce", pvc['spec']['accessModes'])

    def test_pod_exists_and_image(self):
        pod = json.loads(kubectl("get", "pod", "db-pod", "-n", "state", "-o", "json"))
        self.assertEqual(pod['spec']['containers'][0]['image'], "mysql:5.7")

    def test_pod_mounts_pvc(self):
        pod = json.loads(kubectl("get", "pod", "db-pod", "-n", "state", "-o", "json"))
        mounts = pod['spec']['containers'][0]['volumeMounts']
        mount = next((m for m in mounts if m['mountPath'] == "/var/lib/mysql"), None)
        self.assertIsNotNone(mount)

        volume_name = mount['name']
        volumes = pod['spec']['volumes']
        volume = next((v for v in volumes if v['name'] == volume_name), None)
        self.assertIsNotNone(volume)
        self.assertEqual(volume['persistentVolumeClaim']['claimName'], "db-pvc")

    def test_pod_env_vars(self):
        pod = json.loads(kubectl("get", "pod", "db-pod", "-n", "state", "-o", "json"))
        env = {e['name']: e.get('value') for e in pod['spec']['containers'][0]['env']}
        self.assertEqual(env.get('MYSQL_ROOT_PASSWORD'), "rootpassword")
        self.assertEqual(env.get('MYSQL_DATABASE'), "mydb")
        self.assertEqual(env.get('MYSQL_USER'), "myuser")
        self.assertEqual(env.get('MYSQL_PASSWORD'), "mypassword")

if __name__ == "__main__":
    unittest.main()

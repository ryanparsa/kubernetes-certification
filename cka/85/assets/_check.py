#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

KUBECONFIG = os.path.join(os.path.dirname(__file__), "kubeconfig.yaml")

def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()

class TestSafariStorage(unittest.TestCase):
    def test_pv_exists_and_matches(self):
        """PersistentVolume safari-pv exists with correct specs"""
        pv_json = kubectl("get", "pv", "safari-pv", "-o", "json")
        self.assertTrue(pv_json, "PersistentVolume safari-pv not found")
        pv = json.loads(pv_json)

        self.assertEqual(pv["spec"]["capacity"]["storage"], "2Gi")
        self.assertIn("ReadWriteOnce", pv["spec"]["accessModes"])
        self.assertEqual(pv["spec"]["hostPath"]["path"], "/Volumes/Data")
        self.assertEqual(pv["spec"].get("storageClassName", ""), "")

    def test_pvc_exists_and_bound(self):
        """PersistentVolumeClaim safari-pvc created in namespace project-tiger and bound to safari-pv"""
        pvc_json = kubectl("get", "pvc", "safari-pvc", "-n", "project-tiger", "-o", "json")
        self.assertTrue(pvc_json, "PersistentVolumeClaim safari-pvc not found in project-tiger")
        pvc = json.loads(pvc_json)

        self.assertEqual(pvc["spec"]["resources"]["requests"]["storage"], "2Gi")
        self.assertIn("ReadWriteOnce", pvc["spec"]["accessModes"])
        self.assertEqual(pvc["spec"].get("storageClassName", ""), "")
        self.assertEqual(pvc["spec"]["volumeName"], "safari-pv")
        self.assertEqual(pvc["status"]["phase"], "Bound")

    def test_pod_mounts_pvc(self):
        """Pod safari created in namespace project-tiger mounting safari-pvc at /tmp/safari-data"""
        pod_json = kubectl("get", "pod", "safari", "-n", "project-tiger", "-o", "json")
        self.assertTrue(pod_json, "Pod safari not found in project-tiger")
        pod = json.loads(pod_json)

        # Check volume
        volumes = pod["spec"]["volumes"]
        pvc_volume = next((v for v in volumes if v.get("persistentVolumeClaim") and v["persistentVolumeClaim"]["claimName"] == "safari-pvc"), None)
        self.assertIsNotNone(pvc_volume, "Pod does not have a volume using safari-pvc")
        volume_name = pvc_volume["name"]

        # Check mount
        container = pod["spec"]["containers"][0]
        mount = next((m for m in container["volumeMounts"] if m["name"] == volume_name), None)
        self.assertIsNotNone(mount, f"Volume {volume_name} not mounted in container")
        self.assertEqual(mount["mountPath"], "/tmp/safari-data")

if __name__ == "__main__":
    unittest.main(verbosity=2)

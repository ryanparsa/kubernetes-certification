#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_KUBECONFIG = os.path.join(SCRIPT_DIR, "..", "lab", "kubeconfig.yaml")
KUBECONFIG = LOCAL_KUBECONFIG if os.path.exists(LOCAL_KUBECONFIG) else os.environ.get("KUBECONFIG")

def kubectl(*args):
    cmd = ["kubectl"]
    if KUBECONFIG:
        cmd.extend(["--kubeconfig", KUBECONFIG])
    cmd.extend(args)
    result = subprocess.run(
        cmd,
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()

class TestPersistentVolumeStorage(unittest.TestCase):
    def test_pv_exists_and_config(self):
        # PersistentVolume task-pv-volume exists with capacity 10Mi and ReadWriteOnce
        pv_json = kubectl("get", "pv", "task-pv-volume", "-o", "json")
        self.assertIsNotNone(pv_json, "PV task-pv-volume does not exist")
        pv = json.loads(pv_json)

        self.assertEqual(pv["spec"]["capacity"]["storage"], "10Mi")
        self.assertIn("ReadWriteOnce", pv["spec"]["accessModes"])

    def test_pv_storage_class_and_hostpath(self):
        # PersistentVolume uses storageClassName: manual and hostPath /mnt/data
        pv_json = kubectl("get", "pv", "task-pv-volume", "-o", "json")
        self.assertIsNotNone(pv_json, "PV task-pv-volume does not exist")
        pv = json.loads(pv_json)

        self.assertEqual(pv["spec"]["storageClassName"], "manual")
        self.assertEqual(pv["spec"]["hostPath"]["path"], "/mnt/data")

    def test_pvc_exists_and_storage_class(self):
        # PersistentVolumeClaim task-pv-claim exists with storageClassName: manual
        pvc_json = kubectl("get", "pvc", "task-pv-claim", "-o", "json")
        self.assertIsNotNone(pvc_json, "PVC task-pv-claim does not exist")
        pvc = json.loads(pvc_json)

        self.assertEqual(pvc["spec"]["storageClassName"], "manual")

    def test_pvc_bound_to_pv(self):
        # PVC task-pv-claim is in Bound status bound to task-pv-volume
        pvc_json = kubectl("get", "pvc", "task-pv-claim", "-o", "json")
        self.assertIsNotNone(pvc_json, "PVC task-pv-claim does not exist")
        pvc = json.loads(pvc_json)

        self.assertEqual(pvc["status"]["phase"], "Bound")
        self.assertEqual(pvc["spec"]["volumeName"], "task-pv-volume")

    def test_pod_running_with_nginx(self):
        # Pod task-pv-pod is running using the nginx image
        pod_json = kubectl("get", "pod", "task-pv-pod", "-o", "json")
        self.assertIsNotNone(pod_json, "Pod task-pv-pod does not exist")
        pod = json.loads(pod_json)

        self.assertEqual(pod["status"]["phase"], "Running")
        self.assertEqual(pod["spec"]["containers"][0]["image"], "nginx")

    def test_pod_mounts_pvc(self):
        # Pod task-pv-pod mounts task-pv-claim at /usr/share/nginx/html
        pod_json = kubectl("get", "pod", "task-pv-pod", "-o", "json")
        self.assertIsNotNone(pod_json, "Pod task-pv-pod does not exist")
        pod = json.loads(pod_json)

        # Check volume
        volumes = pod["spec"]["volumes"]
        pvc_volume_name = ""
        for vol in volumes:
            if "persistentVolumeClaim" in vol and vol["persistentVolumeClaim"]["claimName"] == "task-pv-claim":
                pvc_volume_name = vol["name"]
                break
        self.assertNotEqual(pvc_volume_name, "", "Pod does not use PVC task-pv-claim")

        # Check mount
        mounts = pod["spec"]["containers"][0]["volumeMounts"]
        found_mount = False
        for mount in mounts:
            if mount["name"] == pvc_volume_name and mount["mountPath"] == "/usr/share/nginx/html":
                found_mount = True
                break
        self.assertTrue(found_mount, "PVC is not mounted at /usr/share/nginx/html")

if __name__ == "__main__":
    unittest.main(verbosity=2)

#!/usr/bin/env python3
import os
import subprocess
import unittest

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
KUBECONFIG = os.path.join(SCRIPT_DIR, "kubeconfig.yaml")

def kubectl(*args):
    cmd = ["kubectl"]
    if os.path.exists(KUBECONFIG) and "KUBECONFIG" not in os.environ:
        cmd.extend(["--kubeconfig", KUBECONFIG])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

class TestPV_PVCDynamicProvisioning(unittest.TestCase):

    def test_storageclass_exists(self):
        sc = kubectl("get", "sc", "local-backup", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(sc, "local-backup")

    def test_storageclass_provisioner(self):
        provisioner = kubectl("get", "sc", "local-backup", "-o", "jsonpath={.provisioner}")
        self.assertEqual(provisioner, "rancher.io/local-path")

    def test_storageclass_reclaim_policy(self):
        policy = kubectl("get", "sc", "local-backup", "-o", "jsonpath={.reclaimPolicy}")
        self.assertEqual(policy, "Retain")

    def test_storageclass_binding_mode(self):
        mode = kubectl("get", "sc", "local-backup", "-o", "jsonpath={.volumeBindingMode}")
        self.assertEqual(mode, "WaitForFirstConsumer")

    def test_job_uses_pvc(self):
        claim_name = kubectl("get", "job", "backup", "-n", "project-bern", "-o", "jsonpath={.spec.template.spec.volumes[?(@.name=='backup')].persistentVolumeClaim.claimName}")
        self.assertEqual(claim_name, "backup-pvc")

    def test_pvc_exists(self):
        pvc = kubectl("get", "pvc", "backup-pvc", "-n", "project-bern", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(pvc, "backup-pvc")

    def test_pvc_storage_class(self):
        sc = kubectl("get", "pvc", "backup-pvc", "-n", "project-bern", "-o", "jsonpath={.spec.storageClassName}")
        self.assertEqual(sc, "local-backup")

    def test_pvc_requests_storage(self):
        storage = kubectl("get", "pvc", "backup-pvc", "-n", "project-bern", "-o", "jsonpath={.spec.resources.requests.storage}")
        self.assertEqual(storage, "50Mi")

    def test_job_completed(self):
        status = kubectl("get", "job", "backup", "-n", "project-bern", "-o", "jsonpath={.status.succeeded}")
        self.assertEqual(status, "1")

    def test_pvc_bound(self):
        status = kubectl("get", "pvc", "backup-pvc", "-n", "project-bern", "-o", "jsonpath={.status.phase}")
        self.assertEqual(status, "Bound")

if __name__ == "__main__":
    unittest.main(verbosity=2)

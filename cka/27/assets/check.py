#!/usr/bin/env python3

import os
import subprocess
import unittest

KUBECONFIG = os.path.join(os.path.dirname(__file__), "kubeconfig.yaml")

def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()

class TestPVPCProvisioning(unittest.TestCase):

    def test_storageclass_created(self):
        # Check if StorageClass exists and has correct parameters
        sc_name = kubectl("get", "sc", "local-backup", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(sc_name, "local-backup")

        provisioner = kubectl("get", "sc", "local-backup", "-o", "jsonpath={.provisioner}")
        self.assertEqual(provisioner, "rancher.io/local-path")

        reclaim_policy = kubectl("get", "sc", "local-backup", "-o", "jsonpath={.reclaimPolicy}")
        self.assertEqual(reclaim_policy, "Retain")

        binding_mode = kubectl("get", "sc", "local-backup", "-o", "jsonpath={.volumeBindingMode}")
        self.assertEqual(binding_mode, "WaitForFirstConsumer")

    def test_job_uses_pvc(self):
        # Check if Job uses PVC
        volume_type = kubectl("get", "job", "backup", "-n", "project-bern", "-o", "jsonpath={.spec.template.spec.volumes[0].persistentVolumeClaim.claimName}")
        self.assertEqual(volume_type, "backup-pvc")

    def test_pvc_uses_storageclass(self):
        # Check if PVC uses the new StorageClass
        sc_name = kubectl("get", "pvc", "backup-pvc", "-n", "project-bern", "-o", "jsonpath={.spec.storageClassName}")
        self.assertEqual(sc_name, "local-backup")

    def test_pvc_requests_required_storage(self):
        # Check if PVC requests 50Mi
        storage = kubectl("get", "pvc", "backup-pvc", "-n", "project-bern", "-o", "jsonpath={.spec.resources.requests.storage}")
        self.assertEqual(storage, "50Mi")

    def test_job_created_backups_on_pvc(self):
        # Check if Job completed and PVC is bound
        status = kubectl("get", "pvc", "backup-pvc", "-n", "project-bern", "-o", "jsonpath={.status.phase}")
        self.assertEqual(status, "Bound")

        completions = kubectl("get", "job", "backup", "-n", "project-bern", "-o", "jsonpath={.status.succeeded}")
        self.assertEqual(completions, "1")

class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)

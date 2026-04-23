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


class TestPVCPVDynamicProvisioning(unittest.TestCase):

    def test_storage_class_created(self):
        sc = kubectl("get", "sc", "local-backup", "-o", "json")
        self.assertTrue(sc, "StorageClass local-backup does not exist")
        sc_data = json.loads(sc)
        self.assertEqual(sc_data["provisioner"], "rancher.io/local-path")
        self.assertEqual(sc_data["reclaimPolicy"], "Retain")
        self.assertEqual(sc_data["volumeBindingMode"], "WaitForFirstConsumer")

    def test_job_uses_pvc(self):
        volume_source = kubectl("get", "job", "backup", "-n", "project-bern", "-o", "jsonpath={.spec.template.spec.volumes[?(@.name=='backup')].persistentVolumeClaim.claimName}")
        self.assertEqual(volume_source, "backup-pvc")

    def test_pvc_uses_storage_class(self):
        sc_name = kubectl("get", "pvc", "backup-pvc", "-n", "project-bern", "-o", "jsonpath={.spec.storageClassName}")
        self.assertEqual(sc_name, "local-backup")

    def test_pvc_requests_required_storage(self):
        storage = kubectl("get", "pvc", "backup-pvc", "-n", "project-bern", "-o", "jsonpath={.spec.resources.requests.storage}")
        self.assertEqual(storage, "50Mi")

    def test_job_completed(self):
        status = kubectl("get", "job", "backup", "-n", "project-bern", "-o", "jsonpath={.status.succeeded}")
        self.assertEqual(status, "1")

    def test_pvc_is_bound(self):
        status = kubectl("get", "pvc", "backup-pvc", "-n", "project-bern", "-o", "jsonpath={.status.phase}")
        self.assertEqual(status, "Bound")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)

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


class TestPvPvcDynamicProvisioning(unittest.TestCase):

    def test_storageclass_created(self):
        sc = kubectl("get", "sc", "local-backup", "-o", "json")
        self.assertTrue(sc, "StorageClass local-backup does not exist")
        data = json.loads(sc)
        self.assertEqual(data["provisioner"], "rancher.io/local-path")
        self.assertEqual(data["reclaimPolicy"], "Retain")
        self.assertEqual(data["volumeBindingMode"], "WaitForFirstConsumer")

    def test_job_uses_pvc(self):
        claim_name = kubectl("get", "job", "backup", "-n", "project-bern", "-o", "jsonpath={.spec.template.spec.volumes[?(@.name=='backup')].persistentVolumeClaim.claimName}")
        self.assertEqual(claim_name, "backup-pvc")

    def test_pvc_uses_storageclass(self):
        sc_name = kubectl("get", "pvc", "backup-pvc", "-n", "project-bern", "-o", "jsonpath={.spec.storageClassName}")
        self.assertEqual(sc_name, "local-backup")

    def test_pvc_requests_required_storage(self):
        storage = kubectl("get", "pvc", "backup-pvc", "-n", "project-bern", "-o", "jsonpath={.spec.resources.requests.storage}")
        self.assertEqual(storage, "50Mi")

    def test_job_created_backups_on_the_pvc(self):
        # Verify job completed
        status = kubectl("get", "job", "backup", "-n", "project-bern", "-o", "jsonpath={.status.succeeded}")
        self.assertEqual(status, "1")

        # Verify PVC is bound
        phase = kubectl("get", "pvc", "backup-pvc", "-n", "project-bern", "-o", "jsonpath={.status.phase}")
        self.assertEqual(phase, "Bound")

        # Verify PV exists and has Retain policy
        pv_name = kubectl("get", "pvc", "backup-pvc", "-n", "project-bern", "-o", "jsonpath={.spec.volumeName}")
        reclaim_policy = kubectl("get", "pv", pv_name, "-o", "jsonpath={.spec.persistentVolumeReclaimPolicy}")
        self.assertEqual(reclaim_policy, "Retain")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)

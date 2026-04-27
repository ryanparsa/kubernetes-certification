#!/usr/bin/env python3
import os
import subprocess
import unittest

LOCAL_KUBECONFIG = os.path.join(os.path.dirname(__file__), "..", "lab", "kubeconfig.yaml")
KUBECONFIG = LOCAL_KUBECONFIG if os.path.exists(LOCAL_KUBECONFIG) else os.environ.get("KUBECONFIG")


def kubectl(*args):
    cmd = ["kubectl"]
    if KUBECONFIG:
        cmd.extend(["--kubeconfig", KUBECONFIG])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()


class TestStorageClassPVCJob(unittest.TestCase):

    def test_storageclass_created(self):
        provisioner = kubectl("get", "storageclass", "local-backup",
                              "-o", "jsonpath={.provisioner}")
        self.assertEqual(provisioner, "rancher.io/local-path")
        reclaim = kubectl("get", "storageclass", "local-backup",
                          "-o", "jsonpath={.reclaimPolicy}")
        self.assertEqual(reclaim, "Retain")
        binding = kubectl("get", "storageclass", "local-backup",
                          "-o", "jsonpath={.volumeBindingMode}")
        self.assertEqual(binding, "WaitForFirstConsumer")

    def test_job_uses_pvc(self):
        volume_type = kubectl("get", "job", "backup", "-n", "project-bern",
                              "-o",
                              "jsonpath={.spec.template.spec.volumes[?(@.name=='backup')].persistentVolumeClaim.claimName}")
        self.assertEqual(volume_type, "backup-pvc",
                         "Job backup volume is not using PVC 'backup-pvc'")

    def test_pvc_uses_storageclass(self):
        sc = kubectl("get", "pvc", "backup-pvc", "-n", "project-bern",
                     "-o", "jsonpath={.spec.storageClassName}")
        self.assertEqual(sc, "local-backup")

    def test_pvc_requests_required_storage(self):
        storage = kubectl("get", "pvc", "backup-pvc", "-n", "project-bern",
                          "-o", "jsonpath={.spec.resources.requests.storage}")
        self.assertEqual(storage, "50Mi")

    def test_job_created_backups_on_pvc(self):
        # Job must have completed at least once
        succeeded = kubectl("get", "job", "backup", "-n", "project-bern",
                            "-o", "jsonpath={.status.succeeded}")
        self.assertTrue(succeeded and int(succeeded) >= 1,
                        "Job backup has not completed successfully")
        # PVC must be Bound (volume was provisioned and used)
        pvc_status = kubectl("get", "pvc", "backup-pvc", "-n", "project-bern",
                             "-o", "jsonpath={.status.phase}")
        self.assertEqual(pvc_status, "Bound",
                         "PVC backup-pvc is not Bound — backup may not have run on the PVC")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)

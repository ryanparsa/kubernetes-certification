#!/usr/bin/env python3
import os
import subprocess
import unittest

KUBECONFIG = os.path.join(os.path.dirname(__file__), "..", "lab", "kubeconfig.yaml")


def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()


class TestStoragePVPVCPod(unittest.TestCase):

    def test_pv_exists(self):
        name = kubectl("get", "pv", "safari-pv", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(name, "safari-pv")

    def test_pv_capacity(self):
        capacity = kubectl("get", "pv", "safari-pv", "-o", "jsonpath={.spec.capacity.storage}")
        self.assertEqual(capacity, "2Gi")

    def test_pv_access_mode(self):
        modes = kubectl("get", "pv", "safari-pv", "-o", "jsonpath={.spec.accessModes[0]}")
        self.assertEqual(modes, "ReadWriteOnce")

    def test_pv_host_path(self):
        path = kubectl("get", "pv", "safari-pv", "-o", "jsonpath={.spec.hostPath.path}")
        self.assertEqual(path, "/Volumes/Data")

    def test_pv_no_storage_class(self):
        sc = kubectl("get", "pv", "safari-pv", "-o", "jsonpath={.spec.storageClassName}")
        self.assertEqual(sc, "")

    def test_pvc_exists_and_bound(self):
        status = kubectl("get", "pvc", "safari-pvc", "-n", "project-t230", "-o", "jsonpath={.status.phase}")
        self.assertEqual(status, "Bound")

    def test_deployment_exists(self):
        name = kubectl("get", "deploy", "safari", "-n", "project-t230", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(name, "safari")

    def test_deployment_image(self):
        image = kubectl("get", "deploy", "safari", "-n", "project-t230",
                        "-o", "jsonpath={.spec.template.spec.containers[0].image}")
        self.assertEqual(image, "httpd:2-alpine")

    def test_volume_mount_path(self):
        mount = kubectl("get", "deploy", "safari", "-n", "project-t230",
                        "-o", "jsonpath={.spec.template.spec.containers[0].volumeMounts[0].mountPath}")
        self.assertEqual(mount, "/tmp/safari-data")

    def test_volume_uses_pvc(self):
        claim = kubectl("get", "deploy", "safari", "-n", "project-t230",
                        "-o", "jsonpath={.spec.template.spec.volumes[0].persistentVolumeClaim.claimName}")
        self.assertEqual(claim, "safari-pvc")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)

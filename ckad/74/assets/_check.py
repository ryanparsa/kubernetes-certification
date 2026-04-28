#!/usr/bin/env python3
import os
import subprocess
import unittest

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
LOCAL_KUBECONFIG = os.path.join(SCRIPT_DIR, "..", "lab", "kubeconfig.yaml")
KUBECONFIG = LOCAL_KUBECONFIG if os.path.exists(LOCAL_KUBECONFIG) else os.environ.get("KUBECONFIG")


def kubectl(*args):
    cmd = ["kubectl"]
    if KUBECONFIG:
        cmd.extend(["--kubeconfig", KUBECONFIG])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()


class TestSecuredPod(unittest.TestCase):

    def test_pod_running(self):
        phase = kubectl("get", "pod", "secured", "-o", "jsonpath={.status.phase}")
        self.assertEqual(phase, "Running")

    def test_emptydir_volume_mounted_at_data_app(self):
        mount_path = kubectl(
            "get", "pod", "secured",
            "-o", "jsonpath={.spec.containers[0].volumeMounts[?(@.mountPath=='/data/app')].mountPath}",
        )
        self.assertEqual(mount_path, "/data/app")

        volume_type = kubectl(
            "get", "pod", "secured",
            "-o", "jsonpath={.spec.volumes[?(@.name=='data-vol')].emptyDir}",
        )
        self.assertNotEqual(volume_type, "")

    def test_fsgroup_set_to_3000(self):
        fs_group = kubectl("get", "pod", "secured", "-o", "jsonpath={.spec.securityContext.fsGroup}")
        self.assertEqual(fs_group, "3000")

    def test_file_owned_by_group_3000(self):
        # Create a file and check its group ownership
        result = subprocess.run(
            ["kubectl"] + (["--kubeconfig", KUBECONFIG] if KUBECONFIG else []) +
            ["exec", "secured", "--", "sh", "-c",
             "touch /data/app/logs.txt && stat -c '%g' /data/app/logs.txt"],
            capture_output=True, text=True,
        )
        gid = result.stdout.strip()
        self.assertEqual(gid, "3000")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)

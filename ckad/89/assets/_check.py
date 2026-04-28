#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

SCRIPT_DIR = os.path.dirname(__file__)
LOCAL_KUBECONFIG = os.path.join(SCRIPT_DIR, "kubeconfig.yaml")
KUBECONFIG = LOCAL_KUBECONFIG if os.path.exists(LOCAL_KUBECONFIG) else os.environ.get("KUBECONFIG")

def kubectl(*args):
    cmd = ["kubectl"]
    if KUBECONFIG:
        cmd.extend(["--kubeconfig", KUBECONFIG])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

class TestTrauerweide(unittest.TestCase):

    def test_configmap_exists(self):
        val = kubectl("get", "configmap", "trauerweide", "-o", "jsonpath={.data.tree}")
        self.assertEqual(val, "trauerweide")

    def test_pod_exists_and_image(self):
        image = kubectl("get", "pod", "pod-6", "-o", "jsonpath={.spec.containers[0].image}")
        self.assertEqual(image, "busybox:1.31.0")

    def test_pod_command(self):
        # We check both command and args just in case, but fix.sh uses command
        command = kubectl("get", "pod", "pod-6", "-o", "jsonpath={.spec.containers[0].command}")
        self.assertIn("sleep", command)
        self.assertIn("999", command)

    def test_pod_volume_mount(self):
        pod_json = kubectl("get", "pod", "pod-6", "-o", "json")
        self.assertTrue(pod_json, "Pod json should not be empty")
        pod = json.loads(pod_json)

        containers = pod.get("spec", {}).get("containers", [])
        self.assertTrue(len(containers) > 0)

        mounts = containers[0].get("volumeMounts", [])
        mount = next((m for m in mounts if m.get("mountPath") == "/tmp/vols"), None)
        self.assertIsNotNone(mount, "Mount path /tmp/vols not found")

        vol_name = mount.get("name")
        volumes = pod.get("spec", {}).get("volumes", [])
        volume = next((v for v in volumes if v.get("name") == vol_name), None)
        self.assertIsNotNone(volume, f"Volume {vol_name} not found")
        self.assertIn("emptyDir", volume, "Volume should be an emptyDir")

if __name__ == "__main__":
    unittest.main(verbosity=2)

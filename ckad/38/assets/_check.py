#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
KUBECONFIG_FILE = os.path.join(SCRIPT_DIR, "..", "lab", "kubeconfig.yaml")

def kubectl(*args):
    cmd = ["kubectl"]
    if os.path.exists(KUBECONFIG_FILE) and "KUBECONFIG" not in os.environ:
        cmd.extend(["--kubeconfig", KUBECONFIG_FILE])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result

class TestMultiContainerPod(unittest.TestCase):
    def test_namespace_exists(self):
        res = kubectl("get", "namespace", "multi-container")
        self.assertEqual(res.returncode, 0, "Namespace 'multi-container' does not exist")

    def test_pod_exists_with_two_containers(self):
        res = kubectl("get", "pod", "multi-container-pod", "-n", "multi-container", "-o", "json")
        self.assertEqual(res.returncode, 0, "Pod 'multi-container-pod' not found in namespace 'multi-container'")

        pod = json.loads(res.stdout)
        containers = pod.get("spec", {}).get("containers", [])
        self.assertEqual(len(containers), 2, "Pod does not have exactly 2 containers")

        container_names = [c["name"] for c in containers]
        self.assertIn("main-container", container_names)
        self.assertIn("sidecar-container", container_names)

    def test_container_images(self):
        res = kubectl("get", "pod", "multi-container-pod", "-n", "multi-container", "-o", "json")
        pod = json.loads(res.stdout)
        containers = pod.get("spec", {}).get("containers", [])

        images = {c["name"]: c["image"] for c in containers}
        self.assertEqual(images.get("main-container"), "nginx")
        self.assertTrue(images.get("sidecar-container").startswith("busybox"))

    def test_shared_volume_mounts(self):
        res = kubectl("get", "pod", "multi-container-pod", "-n", "multi-container", "-o", "json")
        pod = json.loads(res.stdout)
        containers = pod.get("spec", {}).get("containers", [])

        # Check volume definition
        volumes = pod.get("spec", {}).get("volumes", [])
        self.assertTrue(any(v["name"] == "log-volume" for v in volumes), "Volume 'log-volume' not defined in pod spec")

        # Check mounts in each container
        for container in containers:
            mounts = container.get("volumeMounts", [])
            log_mount = next((m for m in mounts if m["name"] == "log-volume"), None)
            self.assertIsNotNone(log_mount, f"Container {container['name']} does not mount 'log-volume'")
            self.assertEqual(log_mount["mountPath"], "/var/log", f"Container {container['name']} mounts 'log-volume' at incorrect path")

if __name__ == "__main__":
    unittest.main()

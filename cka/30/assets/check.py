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


class TestMultiContainersSharedVolume(unittest.TestCase):

    def test_pod_is_running(self):
        phase = kubectl("get", "pod", "multi-container-playground", "-n", "default", "-o", "jsonpath={.status.phase}")
        self.assertEqual(phase, "Running")

    def test_container_count(self):
        names = kubectl("get", "pod", "multi-container-playground", "-n", "default", "-o", "jsonpath={range .spec.containers[*]}{.name} {end}")
        self.assertEqual(len(names.split()), 3)

    def test_containers_are_ready(self):
        ready_count = kubectl("get", "pod", "multi-container-playground", "-n", "default", "-o", "jsonpath={.status.containerStatuses[*].ready}")
        # count occurrences of 'true'
        self.assertEqual(ready_count.split().count("true"), 3)

    def test_container_c1_spec(self):
        name = kubectl("get", "pod", "multi-container-playground", "-n", "default", "-o", "jsonpath={.spec.containers[0].name}")
        image = kubectl("get", "pod", "multi-container-playground", "-n", "default", "-o", "jsonpath={.spec.containers[0].image}")
        self.assertEqual(name, "c1")
        self.assertEqual(image, "nginx:1-alpine")

    def test_container_c1_env(self):
        env_name = kubectl("get", "pod", "multi-container-playground", "-n", "default", "-o", "jsonpath={.spec.containers[0].env[0].name}")
        field_path = kubectl("get", "pod", "multi-container-playground", "-n", "default", "-o", "jsonpath={.spec.containers[0].env[0].valueFrom.fieldRef.fieldPath}")
        self.assertEqual(env_name, "MY_NODE_NAME")
        self.assertEqual(field_path, "spec.nodeName")

    def test_container_c2_spec(self):
        name = kubectl("get", "pod", "multi-container-playground", "-n", "default", "-o", "jsonpath={.spec.containers[1].name}")
        image = kubectl("get", "pod", "multi-container-playground", "-n", "default", "-o", "jsonpath={.spec.containers[1].image}")
        self.assertEqual(name, "c2")
        self.assertEqual(image, "busybox:1")

    def test_container_c3_spec(self):
        name = kubectl("get", "pod", "multi-container-playground", "-n", "default", "-o", "jsonpath={.spec.containers[2].name}")
        image = kubectl("get", "pod", "multi-container-playground", "-n", "default", "-o", "jsonpath={.spec.containers[2].image}")
        self.assertEqual(name, "c3")
        self.assertEqual(image, "busybox:1")

    def test_all_containers_have_volume_mount(self):
        # We check if all 3 containers have a mount named 'vol'
        for i in range(3):
            mount_name = kubectl("get", "pod", "multi-container-playground", "-n", "default", "-o", f"jsonpath={{.spec.containers[{i}].volumeMounts[?(@.name=='vol')].name}}")
            self.assertEqual(mount_name, "vol")
            mount_path = kubectl("get", "pod", "multi-container-playground", "-n", "default", "-o", f"jsonpath={{.spec.containers[{i}].volumeMounts[?(@.name=='vol')].mountPath}}")
            self.assertEqual(mount_path, "/vol")

    def test_pod_has_emptydir_volume(self):
        vol_type = kubectl("get", "pod", "multi-container-playground", "-n", "default", "-o", "jsonpath={.spec.volumes[?(@.name=='vol')].emptyDir}")
        # If emptyDir exists, jsonpath returns {} (as string) or empty string depending on kubectl version/flags, but if we use jsonpath={.spec.volumes[0]} we can see it.
        # Let's try more specific check
        vols = kubectl("get", "pod", "multi-container-playground", "-n", "default", "-o", "json")
        vols_data = json.loads(vols)
        vol_found = False
        for v in vols_data['spec']['volumes']:
            if v['name'] == 'vol' and 'emptyDir' in v:
                vol_found = True
                break
        self.assertTrue(vol_found)


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)

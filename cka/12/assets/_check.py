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


class TestDeploymentOnAllNodes(unittest.TestCase):

    def test_deployment_exists(self):
        name = kubectl("get", "deploy", "deploy-important", "-n", "project-tiger", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(name, "deploy-important")

    def test_deployment_label(self):
        label = kubectl("get", "deploy", "deploy-important", "-n", "project-tiger", "-o", "jsonpath={.metadata.labels.id}")
        self.assertEqual(label, "very-important")

    def test_pod_label(self):
        label = kubectl("get", "deploy", "deploy-important", "-n", "project-tiger", "-o", "jsonpath={.spec.template.metadata.labels.id}")
        self.assertEqual(label, "very-important")

    def test_replicas(self):
        replicas = kubectl("get", "deploy", "deploy-important", "-n", "project-tiger", "-o", "jsonpath={.spec.replicas}")
        self.assertEqual(replicas, "3")

    def test_container1_name(self):
        name = kubectl("get", "deploy", "deploy-important", "-n", "project-tiger", "-o", "jsonpath={.spec.template.spec.containers[0].name}")
        self.assertEqual(name, "container1")

    def test_container1_image(self):
        image = kubectl("get", "deploy", "deploy-important", "-n", "project-tiger", "-o", "jsonpath={.spec.template.spec.containers[0].image}")
        self.assertEqual(image, "nginx:1-alpine")

    def test_container2_name(self):
        name = kubectl("get", "deploy", "deploy-important", "-n", "project-tiger", "-o", "jsonpath={.spec.template.spec.containers[1].name}")
        self.assertEqual(name, "container2")

    def test_container2_image(self):
        image = kubectl("get", "deploy", "deploy-important", "-n", "project-tiger", "-o", "jsonpath={.spec.template.spec.containers[1].image}")
        self.assertEqual(image, "google/pause")

    def test_scheduling_constraint_exists(self):
        antiaffinity = kubectl("get", "deploy", "deploy-important", "-n", "project-tiger", "-o", "jsonpath={.spec.template.spec.affinity.podAntiAffinity}")
        topologyspread = kubectl("get", "deploy", "deploy-important", "-n", "project-tiger", "-o", "jsonpath={.spec.template.spec.topologySpreadConstraints}")
        self.assertTrue(antiaffinity or topologyspread, "Deployment has no podAntiAffinity or topologySpreadConstraints")

    def test_topology_key(self):
        antiaffinity_key = kubectl("get", "deploy", "deploy-important", "-n", "project-tiger", "-o",
                                   "jsonpath={.spec.template.spec.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[0].topologyKey}")
        topologyspread_key = kubectl("get", "deploy", "deploy-important", "-n", "project-tiger", "-o",
                                     "jsonpath={.spec.template.spec.topologySpreadConstraints[0].topologyKey}")
        self.assertIn("kubernetes.io/hostname", antiaffinity_key + topologyspread_key)


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)

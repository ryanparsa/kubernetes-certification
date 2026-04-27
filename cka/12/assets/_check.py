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


class TestDeploymentOnAllNodes(unittest.TestCase):

    def test_deployment_exists(self):
        """Deployment deploy-important exists in namespace project-tiger"""
        name = kubectl("get", "deploy", "deploy-important", "-n", "project-tiger",
                       "--ignore-not-found", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(name, "deploy-important")

    def test_replicas(self):
        """Deployment has 3 replicas"""
        replicas = kubectl("get", "deploy", "deploy-important", "-n", "project-tiger",
                           "-o", "jsonpath={.spec.replicas}")
        self.assertEqual(replicas, "3")

    def test_two_running_replicas(self):
        """Deployment has 2 running replicas"""
        ready = kubectl("get", "deploy", "deploy-important", "-n", "project-tiger",
                        "-o", "jsonpath={.status.readyReplicas}")
        self.assertEqual(ready, "2", "Expected 2 ready replicas (3rd is Pending due to anti-affinity)")

    def test_two_containers(self):
        """Deployment has two containers"""
        containers = kubectl("get", "deploy", "deploy-important", "-n", "project-tiger",
                             "-o", "jsonpath={range .spec.template.spec.containers[*]}{.name} {end}")
        self.assertEqual(len(containers.split()), 2)

    def test_container1_name(self):
        """First container is named container1"""
        name = kubectl("get", "deploy", "deploy-important", "-n", "project-tiger",
                       "-o", "jsonpath={.spec.template.spec.containers[0].name}")
        self.assertEqual(name, "container1")

    def test_container1_image(self):
        """First container uses image nginx:1-alpine"""
        image = kubectl("get", "deploy", "deploy-important", "-n", "project-tiger",
                        "-o", "jsonpath={.spec.template.spec.containers[0].image}")
        self.assertEqual(image, "nginx:1-alpine")

    def test_container2_name(self):
        """Second container is named container2"""
        name = kubectl("get", "deploy", "deploy-important", "-n", "project-tiger",
                       "-o", "jsonpath={.spec.template.spec.containers[1].name}")
        self.assertEqual(name, "container2")

    def test_container2_image(self):
        """Second container uses image google/pause"""
        image = kubectl("get", "deploy", "deploy-important", "-n", "project-tiger",
                        "-o", "jsonpath={.spec.template.spec.containers[1].image}")
        self.assertEqual(image, "google/pause")

    def test_three_pods_exist(self):
        """Three pods exist for deployment"""
        pods = kubectl("get", "pods", "-n", "project-tiger", "-l", "id=very-important",
                       "-o", "jsonpath={range .items[*]}{.metadata.name} {end}")
        count = len(pods.split()) if pods else 0
        self.assertEqual(count, 3, f"Expected 3 pods, got {count}")

    def test_two_pods_running(self):
        """Two pods for deployment are Running"""
        pods = kubectl("get", "pods", "-n", "project-tiger", "-l", "id=very-important",
                       "-o", "jsonpath={range .items[*]}{.status.phase} {end}")
        running = [p for p in pods.split() if p == "Running"] if pods else []
        self.assertEqual(len(running), 2, f"Expected 2 Running pods, got {len(running)}")

    def test_two_pods_on_different_nodes(self):
        """Two pods of deployment run on different nodes"""
        pods = kubectl("get", "pods", "-n", "project-tiger", "-l", "id=very-important",
                       "-o", "jsonpath={range .items[*]}{.status.phase}:{.spec.nodeName} {end}")
        running_nodes = []
        for entry in pods.split():
            parts = entry.split(":")
            if len(parts) == 2 and parts[0] == "Running":
                running_nodes.append(parts[1])
        self.assertEqual(len(running_nodes), 2, f"Expected 2 Running pods with node info, got {running_nodes}")
        self.assertNotEqual(running_nodes[0], running_nodes[1],
                            f"Both Running pods are on the same node: {running_nodes[0]}")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)

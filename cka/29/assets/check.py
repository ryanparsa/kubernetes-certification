#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
KUBECONFIG = os.path.join(SCRIPT_DIR, "kubeconfig.yaml")

def kubectl(*args):
    cmd = ["kubectl"]
    if os.path.exists(KUBECONFIG):
        cmd.extend(["--kubeconfig", KUBECONFIG])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

class TestDeploymentOnAllNodes(unittest.TestCase):
    def test_deployment_exists(self):
        status = kubectl("get", "deployment", "deploy-important", "-n", "project-tiger", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(status, "deploy-important")

    def test_deployment_labels(self):
        label = kubectl("get", "deployment", "deploy-important", "-n", "project-tiger", "-o", "jsonpath={.metadata.labels.id}")
        self.assertEqual(label, "very-important")

    def test_pod_template_labels(self):
        label = kubectl("get", "deployment", "deploy-important", "-n", "project-tiger", "-o", "jsonpath={.spec.template.metadata.labels.id}")
        self.assertEqual(label, "very-important")

    def test_replicas(self):
        replicas = kubectl("get", "deployment", "deploy-important", "-n", "project-tiger", "-o", "jsonpath={.spec.replicas}")
        self.assertEqual(replicas, "3")

    def test_container1_name(self):
        name = kubectl("get", "deployment", "deploy-important", "-n", "project-tiger", "-o", "jsonpath={.spec.template.spec.containers[0].name}")
        self.assertEqual(name, "container1")

    def test_container1_image(self):
        image = kubectl("get", "deployment", "deploy-important", "-n", "project-tiger", "-o", "jsonpath={.spec.template.spec.containers[0].image}")
        self.assertEqual(image, "nginx:1-alpine")

    def test_container2_name(self):
        name = kubectl("get", "deployment", "deploy-important", "-n", "project-tiger", "-o", "jsonpath={.spec.template.spec.containers[1].name}")
        self.assertEqual(name, "container2")

    def test_container2_image(self):
        image = kubectl("get", "deployment", "deploy-important", "-n", "project-tiger", "-o", "jsonpath={.spec.template.spec.containers[1].image}")
        self.assertEqual(image, "google/pause")

    def test_scheduling_constraint(self):
        # Check for podAntiAffinity or topologySpreadConstraints
        affinity = kubectl("get", "deployment", "deploy-important", "-n", "project-tiger", "-o", "json")
        data = json.loads(affinity)
        spec = data.get("spec", {}).get("template", {}).get("spec", {})

        has_affinity = False
        if "affinity" in spec and "podAntiAffinity" in spec["affinity"]:
            anti_affinity = spec["affinity"]["podAntiAffinity"]
            terms = anti_affinity.get("requiredDuringSchedulingIgnoredDuringExecution", [])
            for term in terms:
                if term.get("topologyKey") == "kubernetes.io/hostname":
                    has_affinity = True

        has_topology_spread = False
        if "topologySpreadConstraints" in spec:
            constraints = spec["topologySpreadConstraints"]
            for constraint in constraints:
                if constraint.get("topologyKey") == "kubernetes.io/hostname":
                    has_topology_spread = True

        self.assertTrue(has_affinity or has_topology_spread)

if __name__ == "__main__":
    unittest.main(verbosity=2)

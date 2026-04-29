#!/usr/bin/env python3
import os
import subprocess
import unittest

KUBECONFIG = os.path.join(os.path.dirname(__file__), "..", "lab", "kubeconfig.yaml")
LAB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "lab")

def kubectl(*args):
    cmd = ["kubectl"]
    if os.path.exists(KUBECONFIG):
        cmd.extend(["--kubeconfig", KUBECONFIG])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

class TestResourcesAndRoles(unittest.TestCase):
    def test_cka_master_namespace(self):
        """Namespace cka-master exists"""
        ns = kubectl("get", "namespace", "cka-master", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(ns, "cka-master")

    def test_resources_txt_content(self):
        """File lab/resources.txt contains namespaced resources"""
        filepath = os.path.join(LAB_DIR, "resources.txt")
        self.assertTrue(os.path.exists(filepath), f"{filepath} does not exist")

        with open(filepath, 'r') as f:
            lines = f.read().splitlines()

        # Check for some common namespaced resources
        self.assertIn("pods", lines)
        self.assertIn("services", lines)
        self.assertIn("deployments.apps", lines)
        self.assertIn("secrets", lines)
        self.assertIn("configmaps", lines)

        # Check that cluster-wide resources are NOT in the list
        self.assertNotIn("nodes", lines)
        self.assertNotIn("namespaces", lines)
        self.assertNotIn("persistentvolumes", lines)

    def test_crowded_namespace_txt_content(self):
        """File lab/crowded-namespace.txt has correct content"""
        filepath = os.path.join(LAB_DIR, "crowded-namespace.txt")
        self.assertTrue(os.path.exists(filepath), f"{filepath} does not exist")

        with open(filepath, 'r') as f:
            content = f.read().strip()

        # Based on setup.sh, project-miami should have 300 roles
        self.assertEqual(content, "project-miami with 300 roles")

if __name__ == "__main__":
    unittest.main(verbosity=2)

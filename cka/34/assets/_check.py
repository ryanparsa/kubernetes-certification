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


class TestOperatorKustomize(unittest.TestCase):

    def test_kustomize_role_updated(self):
        # Check if the role in lab/operator/base/rbac.yaml contains students and classes
        rbac_path = os.path.join(os.path.dirname(__file__), "..", "lab", "operator", "base", "rbac.yaml")
        with open(rbac_path, 'r') as f:
            content = f.read()
        self.assertIn("students", content)
        self.assertIn("classes", content)
        self.assertIn("list", content)

    def test_operator_has_correct_permissions(self):
        # Check live cluster for role permissions
        # Use jsonpath to find the rule with students and classes
        rules = kubectl("get", "role", "operator-role", "-n", "operator-prod", "-o", "json")
        import json
        if not rules:
            self.fail("Role operator-role not found in namespace operator-prod")
        data = json.loads(rules)
        found_students = False
        found_classes = False
        found_list = False
        for rule in data.get("rules", []):
            if "students" in rule.get("resources", []) and "classes" in rule.get("resources", []):
                if "list" in rule.get("verbs", []):
                    found_students = True
                    found_classes = True
                    found_list = True
        self.assertTrue(found_students and found_classes and found_list, "Operator role does not have correct list permissions")

    def test_kustomize_student_added_in_base(self):
        # Check if student4 is in base/students.yaml
        students_path = os.path.join(os.path.dirname(__file__), "..", "lab", "operator", "base", "students.yaml")
        with open(students_path, 'r') as f:
            content = f.read()
        self.assertIn("student4", content)

    def test_student_created(self):
        # Check if student4 is created in the cluster
        # CRDs might be in any namespace depending on kustomize, but usually students are in operator-prod
        name = kubectl("get", "student", "student4", "-n", "operator-prod", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(name, "student4")

    def test_kustomize_build_no_error(self):
        # Check if kustomize build works for both base and prod
        base_dir = os.path.join(os.path.dirname(__file__), "..", "lab", "operator", "base")
        prod_dir = os.path.join(os.path.dirname(__file__), "..", "lab", "operator", "prod")

        res_base = subprocess.run(["kubectl", "kustomize", base_dir], capture_output=True)
        self.assertEqual(res_base.returncode, 0, f"Kustomize build base failed: {res_base.stderr.decode()}")

        res_prod = subprocess.run(["kubectl", "kustomize", prod_dir], capture_output=True)
        self.assertEqual(res_prod.returncode, 0, f"Kustomize build prod failed: {res_prod.stderr.decode()}")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)

#!/usr/bin/env python3
import os
import subprocess
import unittest

KUBECONFIG = os.environ.get("KUBECONFIG") or os.path.join(os.path.dirname(__file__), "..", "lab", "kubeconfig.yaml")


def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()


class TestGatewayAPIIngress(unittest.TestCase):

    def test_httproute_exists(self):
        name = kubectl("get", "httproute", "traffic-director", "-n", "project-r500", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(name, "traffic-director")

    def test_httproute_parent_gateway(self):
        parent = kubectl("get", "httproute", "traffic-director", "-n", "project-r500", "-o", "jsonpath={.spec.parentRefs[0].name}")
        self.assertEqual(parent, "main")

    def test_desktop_route_exists(self):
        rules = kubectl("get", "httproute", "traffic-director", "-n", "project-r500", "-o", "jsonpath={.spec.rules}")
        self.assertIn("web-desktop", rules)
        self.assertIn("/desktop", rules)

    def test_mobile_route_exists(self):
        rules = kubectl("get", "httproute", "traffic-director", "-n", "project-r500", "-o", "jsonpath={.spec.rules}")
        self.assertIn("web-mobile", rules)
        self.assertIn("/mobile", rules)

    def test_auto_route_has_mobile_header_match(self):
        rules = kubectl("get", "httproute", "traffic-director", "-n", "project-r500", "-o", "jsonpath={.spec.rules}")
        self.assertIn("/auto", rules)
        self.assertIn("user-agent", rules)
        self.assertIn("mobile", rules)

    def test_auto_route_has_desktop_fallback(self):
        # There must be at least two rules matching /auto: one conditional, one catch-all
        paths = kubectl("get", "httproute", "traffic-director", "-n", "project-r500",
                        "-o", "jsonpath={range .spec.rules[*]}{.matches[0].path.value} {end}")
        auto_count = paths.split().count("/auto")
        self.assertGreaterEqual(auto_count, 2, "Expected at least 2 rules for /auto (conditional + fallback)")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)

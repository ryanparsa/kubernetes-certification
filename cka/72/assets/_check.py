#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

SCRIPT_DIR = os.path.dirname(__file__)
KUBECONFIG_FILE = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "lab", "kubeconfig.yaml"))

def kubectl(*args):
    env = os.environ.copy()
    if os.path.exists(KUBECONFIG_FILE) and "KUBECONFIG" not in env:
        env["KUBECONFIG"] = KUBECONFIG_FILE

    result = subprocess.run(
        ["kubectl", *args],
        capture_output=True, text=True, env=env
    )
    return result.stdout.strip()

class TestGatewayTraffic(unittest.TestCase):
    def test_httproute_exists(self):
        name = kubectl("get", "httproute", "traffic-director", "-n", "project-r500", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(name, "traffic-director")

    def test_httproute_rules(self):
        rules_json = kubectl("get", "httproute", "traffic-director", "-n", "project-r500", "-o", "json")
        rules = json.loads(rules_json).get("spec", {}).get("rules", [])

        paths = []
        for rule in rules:
            for match in rule.get("matches", []):
                if "path" in match:
                    paths.append(match["path"]["value"])

        self.assertIn("/desktop", paths)
        self.assertIn("/mobile", paths)
        self.assertIn("/api/route", paths)

    def test_httproute_redirect(self):
        rules_json = kubectl("get", "httproute", "traffic-director", "-n", "project-r500", "-o", "json")
        rules = json.loads(rules_json).get("spec", {}).get("rules", [])

        redirect_rule = None
        for rule in rules:
            for match in rule.get("matches", []):
                if match.get("path", {}).get("value") == "/api/route":
                    redirect_rule = rule
                    break

        self.assertIsNotNone(redirect_rule, "Could not find rule for /api/route")

        # Check header match
        header_match = False
        for match in redirect_rule.get("matches", []):
            if match.get("path", {}).get("value") == "/api/route":
                for header in match.get("headers", []):
                    if header.get("name") == "User-Agent" and header.get("value") == "mobile":
                        header_match = True
        self.assertTrue(header_match, "Header match for User-Agent: mobile not found")

        # Check filter
        redirect_filter = False
        for filter in redirect_rule.get("filters", []):
            if filter.get("type") == "RequestRedirect":
                rr = filter.get("requestRedirect", {})
                if rr.get("path", {}).get("type") == "ReplaceFullPath" and rr.get("path", {}).get("replaceFullPath") == "/mobile":
                    redirect_filter = True
        self.assertTrue(redirect_filter, "RequestRedirect filter to /mobile not found")

if __name__ == "__main__":
    unittest.main()

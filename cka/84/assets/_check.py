#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

SCRIPT_DIR = os.path.dirname(__file__)
KUBECONFIG = os.path.join(SCRIPT_DIR, "kubeconfig.yaml")

def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result

class TestApiGatewayHPA(unittest.TestCase):
    def check_namespace(self, ns):
        # 1. ConfigMap should be gone
        res = kubectl("get", "configmap", "api-gateway-autoscaler", "-n", ns)
        self.assertNotEqual(res.returncode, 0, f"ConfigMap api-gateway-autoscaler still exists in {ns}")

        # 2. Deployment replicas should be 0 (in spec)
        res = kubectl("get", "deployment", "api-gateway", "-n", ns, "-o", "json")
        self.assertEqual(res.returncode, 0, f"Deployment api-gateway not found in {ns}")
        deploy = json.loads(res.stdout)
        self.assertEqual(deploy["spec"]["replicas"], 0, f"Deployment api-gateway replicas not 0 in {ns}")

        # 3. HPA should exist with correct settings
        res = kubectl("get", "hpa", "gateway", "-n", ns, "-o", "json")
        self.assertEqual(res.returncode, 0, f"HPA gateway not found in {ns}")
        hpa = json.loads(res.stdout)
        self.assertEqual(hpa["spec"]["minReplicas"], 2, f"HPA minReplicas not 2 in {ns}")
        self.assertEqual(hpa["spec"]["maxReplicas"], 3, f"HPA maxReplicas not 3 in {ns}")

        # Check CPU utilization - support both v1 and v2 HPA if necessary, but v2 is standard now
        metrics = hpa["spec"].get("metrics", [])
        if metrics:
            found_cpu = False
            for m in metrics:
                if m.get("type") == "Resource" and m.get("resource", {}).get("name") == "cpu":
                    target = m["resource"].get("target", {})
                    if target.get("type") == "Utilization":
                        self.assertEqual(target.get("averageUtilization"), 50, f"HPA target CPU not 50% in {ns}")
                        found_cpu = True
            self.assertTrue(found_cpu, f"HPA CPU metric not found in {ns}")
        else:
            # Fallback for older API versions
            self.assertEqual(hpa["spec"].get("targetCPUUtilizationPercentage"), 50, f"HPA target CPU not 50% in {ns}")

        # 4. HPA should target the correct deployment
        self.assertEqual(hpa["spec"]["scaleTargetRef"]["name"], "api-gateway", f"HPA not targeting api-gateway in {ns}")
        self.assertEqual(hpa["spec"]["scaleTargetRef"]["kind"], "Deployment", f"HPA not targeting a Deployment in {ns}")

    def test_staging(self):
        self.check_namespace("api-gateway-staging")

    def test_prod(self):
        self.check_namespace("api-gateway-prod")

if __name__ == "__main__":
    unittest.main(verbosity=2)

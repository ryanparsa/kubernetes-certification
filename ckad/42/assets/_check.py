#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

class TestWebServices(unittest.TestCase):
    def kubectl(self, *args):
        cmd = ["kubectl", *args]
        result = subprocess.run(
            cmd,
            capture_output=True, text=True,
        )
        return result.stdout.strip()

    def test_namespace_exists(self):
        """Verify the 'services' namespace exists."""
        namespaces = self.kubectl("get", "ns", "-o", "jsonpath={.items[*].metadata.name}")
        self.assertIn("services", namespaces.split())

    def test_deployment_config(self):
        """Verify web-app deployment in services namespace."""
        output = self.kubectl("get", "deployment", "web-app", "-n", "services", "-o", "json")
        if not output:
            self.fail("Deployment web-app not found in services namespace")

        deploy = json.loads(output)
        self.assertEqual(deploy["spec"]["replicas"], 3)
        self.assertEqual(deploy["spec"]["template"]["spec"]["containers"][0]["image"], "nginx:alpine")
        self.assertEqual(deploy["spec"]["template"]["metadata"]["labels"]["app"], "web")

    def test_clusterip_service(self):
        """Verify web-svc-cluster service."""
        output = self.kubectl("get", "svc", "web-svc-cluster", "-n", "services", "-o", "json")
        if not output:
            self.fail("Service web-svc-cluster not found")

        svc = json.loads(output)
        self.assertEqual(svc["spec"]["type"], "ClusterIP")
        self.assertEqual(svc["spec"]["ports"][0]["port"], 80)

    def test_nodeport_service(self):
        """Verify web-svc-nodeport service."""
        output = self.kubectl("get", "svc", "web-svc-nodeport", "-n", "services", "-o", "json")
        if not output:
            self.fail("Service web-svc-nodeport not found")

        svc = json.loads(output)
        self.assertEqual(svc["spec"]["type"], "NodePort")
        self.assertEqual(svc["spec"]["ports"][0]["port"], 80)
        self.assertEqual(svc["spec"]["ports"][0]["nodePort"], 30080)

    def test_loadbalancer_service(self):
        """Verify web-svc-lb service."""
        output = self.kubectl("get", "svc", "web-svc-lb", "-n", "services", "-o", "json")
        if not output:
            self.fail("Service web-svc-lb not found")

        svc = json.loads(output)
        self.assertEqual(svc["spec"]["type"], "LoadBalancer")
        self.assertEqual(svc["spec"]["ports"][0]["port"], 80)

if __name__ == "__main__":
    unittest.main()

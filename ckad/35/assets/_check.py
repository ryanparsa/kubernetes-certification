#!/usr/bin/env python3
import os
import subprocess
import unittest

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
KUBECONFIG_FILE = os.path.join(SCRIPT_DIR, "kubeconfig.yaml")

def kubectl(*args):
    cmd = ["kubectl"]
    if os.path.exists(KUBECONFIG_FILE) and "KUBECONFIG" not in os.environ:
        cmd.extend(["--kubeconfig", KUBECONFIG_FILE])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

class TestHelloJob(unittest.TestCase):
    def test_job_exists(self):
        """Job hello-job exists in namespace networking"""
        val = kubectl("get", "job", "hello-job", "-n", "networking", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(val, "hello-job")

    def test_job_spec(self):
        """Job uses image busybox, has activeDeadlineSeconds: 30, and restartPolicy: Never"""
        image = kubectl("get", "job", "hello-job", "-n", "networking", "-o", "jsonpath={.spec.template.spec.containers[0].image}")
        deadline = kubectl("get", "job", "hello-job", "-n", "networking", "-o", "jsonpath={.spec.activeDeadlineSeconds}")
        restart_policy = kubectl("get", "job", "hello-job", "-n", "networking", "-o", "jsonpath={.spec.template.spec.restartPolicy}")

        self.assertEqual(image, "busybox")
        self.assertEqual(deadline, "30")
        self.assertEqual(restart_policy, "Never")

    def test_job_completion_and_logs(self):
        """Job completes successfully and logs show 'Hello from Kubernetes job!'"""
        # Check completion
        status = kubectl("get", "job", "hello-job", "-n", "networking", "-o", "jsonpath={.status.succeeded}")
        self.assertEqual(status, "1")

        # Check logs
        logs = kubectl("logs", "-n", "networking", "-l", "job-name=hello-job")
        self.assertIn("Hello from Kubernetes job!", logs)

if __name__ == "__main__":
    unittest.main(verbosity=2)

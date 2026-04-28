#!/usr/bin/env python3

import os
import subprocess
import unittest

# Try local kubeconfig first (for local dev), then fallback to default (for CI)
LOCAL_KUBECONFIG = os.path.join(os.path.dirname(__file__), "..", "lab", "kubeconfig.yaml")
KUBECONFIG = LOCAL_KUBECONFIG if os.path.exists(LOCAL_KUBECONFIG) else os.environ.get("KUBECONFIG")


def kubectl(*args):
    cmd = ["kubectl"]
    if KUBECONFIG:
        cmd.extend(["--kubeconfig", KUBECONFIG])
    cmd.extend(args)
    result = subprocess.run(
        cmd,
        capture_output=True, text=True,
    )
    return result.stdout.strip()


class TestLogCleanerCronJob(unittest.TestCase):

    def test_cronjob_exists(self):
        name = kubectl("get", "cronjob", "log-cleaner", "-n", "workloads", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(name, "log-cleaner")

    def test_schedule_every_hour(self):
        schedule = kubectl("get", "cronjob", "log-cleaner", "-n", "workloads", "-o", "jsonpath={.spec.schedule}")
        self.assertEqual(schedule, "0 * * * *")

    def test_command(self):
        args = kubectl("get", "cronjob", "log-cleaner", "-n", "workloads",
                       "-o", "jsonpath={.spec.jobTemplate.spec.template.spec.containers[0].args[0]}")
        self.assertIn("find /var/log", args)
        self.assertIn("-name \"*.log\"", args)
        self.assertIn("-mtime +7", args)
        self.assertIn("-delete", args)

    def test_concurrency_policy(self):
        policy = kubectl("get", "cronjob", "log-cleaner", "-n", "workloads", "-o", "jsonpath={.spec.concurrencyPolicy}")
        self.assertEqual(policy, "Forbid")

    def test_successful_jobs_history_limit(self):
        limit = kubectl("get", "cronjob", "log-cleaner", "-n", "workloads",
                        "-o", "jsonpath={.spec.successfulJobsHistoryLimit}")
        self.assertEqual(limit, "3")

    def test_failed_jobs_history_limit(self):
        limit = kubectl("get", "cronjob", "log-cleaner", "-n", "workloads",
                        "-o", "jsonpath={.spec.failedJobsHistoryLimit}")
        self.assertEqual(limit, "1")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)

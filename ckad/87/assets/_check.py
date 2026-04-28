#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

SCRIPT_DIR = os.path.dirname(__file__)
KUBECONFIG = os.path.join(SCRIPT_DIR, "..", "lab", "kubeconfig.yaml")

def kubectl(*args):
    cmd = ["kubectl"]
    if os.path.exists(KUBECONFIG):
        cmd.extend(["--kubeconfig", KUBECONFIG])
    cmd.extend(args)
    result = subprocess.run(
        cmd,
        capture_output=True, text=True,
    )
    return result.stdout.strip()

class TestBackupJob(unittest.TestCase):
    def test_cronjob_exists(self):
        """CronJob backup-job exists in namespace jobs"""
        namespace = kubectl("get", "namespace", "jobs", "-o", "name")
        self.assertEqual(namespace, "namespace/jobs")

        cronjob = kubectl("get", "cronjob", "backup-job", "-n", "jobs", "-o", "name")
        self.assertEqual(cronjob, "cronjob.batch/backup-job")

    def test_cronjob_schedule(self):
        """Schedule is 0 2 * * *"""
        schedule = kubectl("get", "cronjob", "backup-job", "-n", "jobs", "-o", "jsonpath={.spec.schedule}")
        self.assertEqual(schedule, "0 2 * * *")

    def test_concurrency_policy(self):
        """concurrencyPolicy is Forbid"""
        policy = kubectl("get", "cronjob", "backup-job", "-n", "jobs", "-o", "jsonpath={.spec.concurrencyPolicy}")
        self.assertEqual(policy, "Forbid")

    def test_history_limits(self):
        """successfulJobsHistoryLimit: 3 and failedJobsHistoryLimit: 1"""
        successful = kubectl("get", "cronjob", "backup-job", "-n", "jobs", "-o", "jsonpath={.spec.successfulJobsHistoryLimit}")
        failed = kubectl("get", "cronjob", "backup-job", "-n", "jobs", "-o", "jsonpath={.spec.failedJobsHistoryLimit}")
        self.assertEqual(successful, "3")
        self.assertEqual(failed, "1")

if __name__ == "__main__":
    unittest.main(verbosity=2)

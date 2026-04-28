#!/usr/bin/env python3
import unittest
import subprocess
import json

def run_kubectl(args):
    cmd = ["kubectl"] + args + ["-o", "json"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return None
    return json.loads(result.stdout)

class TestCronJob(unittest.TestCase):
    def test_namespace_exists(self):
        ns = run_kubectl(["get", "namespace", "pod-design"])
        self.assertIsNotNone(ns, "Namespace 'pod-design' does not exist")

    def test_cronjob_exists(self):
        cj = run_kubectl(["get", "cronjob", "backup-job", "-n", "pod-design"])
        self.assertIsNotNone(cj, "CronJob 'backup-job' does not exist in 'pod-design' namespace")

    def test_cronjob_schedule(self):
        cj = run_kubectl(["get", "cronjob", "backup-job", "-n", "pod-design"])
        self.assertEqual(cj["spec"]["schedule"], "*/5 * * * *")

    def test_cronjob_image_and_command(self):
        cj = run_kubectl(["get", "cronjob", "backup-job", "-n", "pod-design"])
        container = cj["spec"]["jobTemplate"]["spec"]["template"]["spec"]["containers"][0]
        self.assertEqual(container["image"], "busybox")
        expected_command = ['sh', '-c', 'echo Backup started: $(date); sleep 30; echo Backup completed: $(date)']
        self.assertEqual(container["command"], expected_command)

    def test_cronjob_restart_policy(self):
        cj = run_kubectl(["get", "cronjob", "backup-job", "-n", "pod-design"])
        policy = cj["spec"]["jobTemplate"]["spec"]["template"]["spec"]["restartPolicy"]
        self.assertEqual(policy, "OnFailure")

    def test_cronjob_deadline(self):
        cj = run_kubectl(["get", "cronjob", "backup-job", "-n", "pod-design"])
        deadline = cj["spec"]["jobTemplate"]["spec"]["activeDeadlineSeconds"]
        self.assertEqual(deadline, 100)

if __name__ == "__main__":
    unittest.main()

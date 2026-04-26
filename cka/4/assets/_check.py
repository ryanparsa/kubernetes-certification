#!/usr/bin/env python3
import os
import subprocess
import unittest

KUBECONFIG = os.path.join(os.path.dirname(__file__), "kubeconfig.yaml")
COURSE_DIR = os.path.join(os.path.dirname(__file__), "..", "course")


def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()


class TestPodsTerminatedFirst(unittest.TestCase):

    def test_file_exists(self):
        path = os.path.join(COURSE_DIR, "pods-terminated-first.txt")
        self.assertTrue(os.path.exists(path), "pods-terminated-first.txt not found")

    def test_listed_pods_are_besteffort(self):
        path = os.path.join(COURSE_DIR, "pods-terminated-first.txt")
        with open(path) as f:
            listed = [l.strip() for l in f if l.strip()]
        self.assertGreater(len(listed), 0, "File is empty")
        for pod in listed:
            qos = kubectl("get", "pod", pod, "-n", "project-c13",
                          "-o", "jsonpath={.status.qosClass}")
            self.assertEqual(qos, "BestEffort", f"Pod {pod} is not BestEffort")

    def test_all_besteffort_pods_listed(self):
        path = os.path.join(COURSE_DIR, "pods-terminated-first.txt")
        with open(path) as f:
            listed = {l.strip() for l in f if l.strip()}
        raw = kubectl(
            "get", "pods", "-n", "project-c13",
            "-o", "jsonpath={range .items[?(@.status.qosClass=='BestEffort')]}"
                  "{.metadata.name}{'\\n'}{end}",
        )
        expected = {l for l in raw.splitlines() if l.strip()}
        self.assertEqual(listed, expected)


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)

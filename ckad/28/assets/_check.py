#!/usr/bin/env python3
import json
import os
import subprocess
import unittest

KUBECONFIG = os.path.join(os.path.dirname(__file__), "..", "lab", "kubeconfig.yaml")


def kubectl(*args):
    cmd = ["kubectl"]
    if os.path.exists(KUBECONFIG):
        cmd.extend(["--kubeconfig", KUBECONFIG])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()


class TestPodReaderRBAC(unittest.TestCase):
    def test_clusterrole_pod_reader_verbs(self):
        verbs_json = kubectl(
            "get", "clusterrole", "pod-reader",
            "-o", "jsonpath={.rules[0].verbs}",
        )
        verbs = json.loads(verbs_json)
        for verb in ("get", "watch", "list"):
            self.assertIn(verb, verbs)

    def test_clusterrolebinding_read_pods_roleref(self):
        cr_name = kubectl(
            "get", "clusterrolebinding", "read-pods",
            "-o", "jsonpath={.roleRef.name}",
        )
        self.assertEqual(cr_name, "pod-reader")

    def test_clusterrolebinding_read_pods_subject(self):
        subject_name = kubectl(
            "get", "clusterrolebinding", "read-pods",
            "-o", "jsonpath={.subjects[0].name}",
        )
        self.assertEqual(subject_name, "jane")


if __name__ == "__main__":
    unittest.main(verbosity=2)

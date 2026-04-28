#!/usr/bin/env python3
import os
import subprocess
import unittest

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
KUBECONFIG_FILE = os.path.join(SCRIPT_DIR, "kubeconfig.yaml")


def kubectl(*args):
    cmd = ["kubectl"]
    if "KUBECONFIG" not in os.environ and os.path.exists(KUBECONFIG_FILE):
        cmd.extend(["--kubeconfig", KUBECONFIG_FILE])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()


class TestDeploymentRolloutAndRollback(unittest.TestCase):

    def test_deployment_label_tier_backend(self):
        label = kubectl("get", "deployment", "deploy", "-o", "jsonpath={.metadata.labels.tier}")
        self.assertEqual(label, "backend")

    def test_pod_template_label_app_v1(self):
        label = kubectl("get", "deployment", "deploy", "-o", "jsonpath={.spec.template.metadata.labels.app}")
        self.assertEqual(label, "v1")

    def test_container_name_nginx(self):
        name = kubectl("get", "deployment", "deploy", "-o", "jsonpath={.spec.template.spec.containers[0].name}")
        self.assertEqual(name, "nginx")

    def test_current_image_is_nginx_after_rollback(self):
        image = kubectl("get", "deployment", "deploy", "-o", "jsonpath={.spec.template.spec.containers[0].image}")
        self.assertEqual(image, "nginx")

    def test_rollout_to_nginx_latest_occurred(self):
        # After rollback, a ReplicaSet with nginx:latest should still exist (scaled to 0)
        images = kubectl(
            "get", "replicasets",
            "-l", "app=v1",
            "-o", "jsonpath={range .items[*]}{range .spec.template.spec.containers[*]}{.image}{\" \"}{end}{end}",
        )
        self.assertIn("nginx:latest", images)

    def test_deployment_scaled_to_5_replicas(self):
        replicas = kubectl("get", "deployment", "deploy", "-o", "jsonpath={.spec.replicas}")
        self.assertEqual(replicas, "5")


if __name__ == "__main__":
    unittest.main(verbosity=2)

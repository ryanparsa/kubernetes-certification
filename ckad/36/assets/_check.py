#!/usr/bin/env python3
import os
import subprocess
import unittest

class TestOCIImageExport(unittest.TestCase):
    def test_directory_exists(self):
        """Directory /root/oci-images exists"""
        result = subprocess.run(["sudo", "test", "-d", "/root/oci-images"])
        self.assertEqual(result.returncode, 0, "Directory /root/oci-images does not exist")

    def test_extracted_content(self):
        """Nginx image content is extracted (manifest.json present)"""
        result = subprocess.run(["sudo", "ls", "/root/oci-images"], capture_output=True, text=True)
        files = result.stdout.split()
        self.assertIn("manifest.json", files, "manifest.json missing in /root/oci-images - image might not be extracted")

if __name__ == "__main__":
    unittest.main(verbosity=2)

# Preview Question 3 | Change Service CIDR

> **Solve this question on:** the "cka-lab-37" kind cluster

1.  Create a *Pod* named `check-ip` in *Namespace* `default` using image `httpd:2-alpine`
2.  Expose it on port `80` as a ClusterIP *Service* named `check-ip-service`. Remember/output the IP of that *Service*
3.  Change the Service CIDR to `11.96.0.0/12` for the cluster
4.  Create a second *Service* named `check-ip-service2` pointing to the same *Pod*

> [i] The second *Service* should get an IP address from the new CIDR range

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

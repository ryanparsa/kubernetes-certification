# Question 57

> **Solve this question on:** `cka-lab-57`

Set up basic DNS service discovery in the `dns-config` namespace:

1. Create a deployment named `dns-app` with `2` replicas using the `nginx` image
2. Create a service named `dns-svc` to expose the deployment
3. Create a Pod named `dns-tester` using the `infoblox/dnstools` image that:
   - Runs a command to test DNS resolution of the service
   - Verifies both short service DNS (`dns-svc`) and FQDN (`dns-svc.dns-config.svc.cluster.local`)
   - Stores the test results in `/tmp/dns-test.txt` inside the pod

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

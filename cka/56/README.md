# Question 56

> **Solve this question on:** `cka-lab-56`

Set up a DNS service discovery testing environment in the `dns-debug` namespace:

1. Create a deployment named `web-app` with `3` replicas using the `nginx` image

2. Create a `ClusterIP` service named `web-svc` to expose the deployment

3. Create a Pod named `dns-test` using the `busybox` image that will:
   - Run the command: `wget -qO- http://web-svc && wget -qO- http://web-svc.dns-debug.svc.cluster.local && sleep 36000`
   - Verify it can resolve both the short service DNS (`web-svc`) and the FQDN (`web-svc.dns-debug.svc.cluster.local`)

4. Create a ConfigMap named `dns-config` with custom search domains for the test pod

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

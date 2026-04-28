# Question 22

> **Solve this question on:** `ckad-lab-22`

Users are reporting connectivity issues with an application.

The Service `web-service` in namespace `troubleshooting` is supposed to route traffic to backend pods, but it is not functioning correctly.

Investigate this service and identify what is preventing proper traffic routing. Possible issues could include:

- Mismatched selectors between service and pods
- Incorrect port configurations
- Problems with the underlying pods

After identifying the issue, implement the necessary fixes to ensure the service correctly routes traffic to the appropriate pods.

Verify your fix by ensuring that service endpoints are properly populated and traffic is forwarded as expected.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

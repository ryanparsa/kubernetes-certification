# Question 31

> **Solve this question on:** `ckad-lab-31`

To enhance security through network segmentation, implement a network policy for a web application.

Create a NetworkPolicy named `allow-traffic` in namespace `networking` that allows incoming traffic only from pods with the label `tier=frontend` to pods with the label `app=web` on TCP port `80`.

All other incoming traffic to these pods should be denied.

This implements the principle of least privilege at the network level, ensuring that the web application can only be accessed by authorized frontend components.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

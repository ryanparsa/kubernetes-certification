# Question 32

> **Solve this question on:** `ckad-lab-32`

The microservices architecture requires internal service communication.

Create a ClusterIP service named `internal-app` in namespace `networking` to enable this communication pattern.

Configure the service to route traffic to pods with the label `app=backend`. The service should accept connections on port `80` and forward them to port `8080` on the backend pods.

ClusterIP is the appropriate service type because this communication is entirely internal to the cluster and doesn't need external exposure.

Ensure the selector exactly matches the pod labels and the port configuration correctly maps the service port to the target port on the pods.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

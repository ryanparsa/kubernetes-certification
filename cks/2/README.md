# Question 2

> **Solve this question on:** `cks-lab-2`

Create a TLS-enabled Ingress resource named `secure-app` in the `secure-ingress` namespace for the service `web-service` (port 80).

The Ingress should:
- Respond to the hostname `secure-app.example.com`
- Use a TLS secret named `secure-app-tls`

The TLS secret has already been created in the `secure-ingress` namespace.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

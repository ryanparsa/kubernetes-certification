# Question 34

> **Solve this question on:** `ckad-lab-34`

The API team needs to implement host-based routing for their services.

Create an *Ingress* resource named `api-ingress` in *Namespace* `networking` that implements the following routing rule:

- All HTTP traffic for the hostname `api.example.com` should be directed to the *Service* `api-service` on port `80`.

This *Ingress* will utilize the cluster's *Ingress* controller to provide more sophisticated HTTP routing than is possible with *Services* alone.

Make sure to properly configure the host field with the exact domain name and set up the correct backend *Service* reference.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

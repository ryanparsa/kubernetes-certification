# Question 60

> **Solve this question on:** `cka-lab-60`

Configure Gateway API resources in the `gateway` namespace:

1. Create a Gateway named `main-gateway` listening on port `80`
2. Create an HTTPRoute to route traffic:
   - Path `/app1` should route to service `app1-svc` on port `8080`
   - Path `/app2` should route to service `app2-svc` on port `8080`
3. Create two deployments (`app1` and `app2`) using the `nginx` image with corresponding services to test the routing

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

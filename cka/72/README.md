# Question 72

> **Solve this question on:** the "cka-lab-72" kind cluster

The team from Project-r500 wants to replace their *Ingress* (`networking.k8s.io`) with a *Gateway API* (`gateway.networking.k8s.io`) solution. The old *Ingress* is available at `lab/72-ingress.yaml`.

Perform the following in *Namespace* `project-r500` using the already existing *Gateway*:

1. Create a new *HTTPRoute* named `traffic-director` which replicates the routes from the old *Ingress*

1. Extend the new *HTTPRoute* with path `/api/route` which redirects to `mobile` — match this route using the `User-Agent` header exactly equal to `mobile`

The existing *Gateway* is reachable at `http://72.gateway:30000`. Your implementation should work for these commands:

```bash
curl http://72.gateway:30000/mobile/desktop --resolve 72.gateway:30000:127.0.0.1
curl http://72.gateway:30000/mobile/tools --resolve 72.gateway:30000:127.0.0.1
curl http://72.gateway:30000/api/route -H "User-Agent: mobile" --resolve 72.gateway:30000:127.0.0.1
```

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

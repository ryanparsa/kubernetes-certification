# Question 13

The team from Project r500 wants to replace their *Ingress* (networking.k8s.io) with a *Gateway API* (gateway.networking.k8s.io) solution. The old *Ingress* is available at `cka/13/lab/ingress.yaml`.

> **Solve this question on:** the "cka-lab-13" kind cluster

Perform the following in *Namespace* `project-r500` and for the already existing *Gateway*:

1. Create a new *HTTPRoute* named `traffic-director` which replicates the routes from the old *Ingress*
2. Extend the new *HTTPRoute* with path `/auto` which forwards to mobile backend if the `User-Agent` is exactly `mobile` and to desktop backend otherwise

The existing *Gateway* is reachable at `http://r500.gateway:30080` which means your implementation should work for these commands:

```bash
curl http://r500.gateway:30080/desktop --resolve r500.gateway:30080:127.0.0.1
curl http://r500.gateway:30080/mobile --resolve r500.gateway:30080:127.0.0.1
curl http://r500.gateway:30080/auto -H "User-Agent: mobile" --resolve r500.gateway:30080:127.0.0.1
curl http://r500.gateway:30080/auto --resolve r500.gateway:30080:127.0.0.1
```

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

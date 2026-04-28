# Question 192

> **Solve this question on:** `ssh cka7868`

The team from Project-r500 wants to replace their *Ingress* (`networking.k8s.io`) with a *Gateway API* (`gateway.networking.k8s.io`) solution. The old *Ingress* is available at `/opt/course/13/ingress.yaml`.

Perform the following in *Namespace* `project-r500` using the already existing *Gateway*:

1. Create a new `HTTPRoute` named `traffic-director` which replicates the routes from the old *Ingress*

1. Extend the new `HTTPRoute` with path `/api/route` which redirects to `mobile` — match this route using the `User-Agent` header exactly equal to `mobile`

The existing Gateway is reachable at `http://1580.gateway:30000`. Your implementation should work for these commands:

```bash
curl 1580.gateway:30000/mobile/desktop
curl 1580.gateway:30000/mobile/tools
curl 1580.gateway:30000/api/site --header "User-Agent: mobile"
```

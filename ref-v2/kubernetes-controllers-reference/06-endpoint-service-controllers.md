# Kubernetes Controllers Reference

[← Back to index](../README.md)

---

## Endpoint & Service Controllers

| Controller | Main File | What It Does |
| --- | --- | --- |
| **Endpoint** | `pkg/controller/endpoint/endpoints_controller.go` | `Controller` · `syncEndpoints()` queries Pods matching the Service selector and writes their IPs into the `Endpoints` object |
| **EndpointSlice** | `pkg/controller/endpointslice/endpointslice_controller.go` | `Controller` · `syncEndpointSlices()` splits Pod IPs across `EndpointSlice` objects (max 100 each). Diff logic lives in `reconciler.go` |
| **EndpointSliceMirroring** | `pkg/controller/endpointslicemirroring/endpointslicemirroring_controller.go` | `Controller` · Mirrors hand-crafted `Endpoints` into `EndpointSlice` objects for Services without pod selectors |
| **ServiceCIDRs** | `pkg/controller/servicecidrs/` | Manages `ServiceCIDR` objects that define IP ranges for ClusterIP services |

---

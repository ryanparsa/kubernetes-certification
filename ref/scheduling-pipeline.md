# Scheduling Pipeline

```
1. Filtering (Predicates)
   - NodeSelector / nodeAffinity
   - TaintToleration
   - ResourceFit (requests vs. allocatable)
   - PodTopologySpread
   - ...

2. Scoring (Priorities)
   - LeastAllocated (spread pods evenly)
   - NodeAffinity (preferred rules)
   - PodAffinity / PodAntiAffinity
   - ImageLocality (prefer nodes with image cached)
   - ...

3. Binding
   - Scheduler writes spec.nodeName on the Pod
   - kubelet on that node picks it up and starts the containers
```

---


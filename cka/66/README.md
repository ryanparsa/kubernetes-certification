# Question 66

> **Solve this question on:** `cka-lab-66`

Configure advanced scheduling in the `scheduling` namespace:

1. Create a PriorityClass named `high-priority` with value `1000`
2. Create a PriorityClass named `low-priority` with value `100`
3. Create a pod named `high-priority` using the `nginx` image with `priorityClassName: high-priority`
4. Create a pod named `low-priority` using the `nginx` image with `priorityClassName: low-priority`
5. Configure pod anti-affinity on both pods to ensure they do not run on the same node

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

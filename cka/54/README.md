# Question 54

> **Solve this question on:** `cka-lab-54`

Configure node `k3d-cluster-agent-1` with a taint `key=special-workload`, `value=true` and `effect=NoSchedule`.

Then create a deployment named `toleration-deploy` in the `scheduling` namespace with `2` replicas using the `nginx` image that can tolerate this taint.

Finally, create another deployment named `normal-deploy` in the `scheduling` namespace with `2` replicas using the `nginx` image that should not run on the tainted node.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

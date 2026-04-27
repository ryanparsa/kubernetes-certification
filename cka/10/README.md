# Question 10

> **Solve this question on:** the "cka-lab-10" kind cluster

Create a new *ServiceAccount* `processor` in *Namespace* `project-hamster`. Create a *Role* and *RoleBinding*, both named `processor` as well. These should allow the new *ServiceAccount* to only create *Secrets* and *ConfigMaps* in that *Namespace*.

---

**Setup:** `bash assets/setup.sh` · **Cleanup:** `bash assets/cleanup.sh`

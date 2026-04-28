# Question 124

> **Solve this question on:** `ckad-lab-05`

There are existing *Namespaces* named `sun` and `moon`.

1. Create a *ServiceAccount* named `secret-manager` in *Namespace* `sun`.

2. The new *ServiceAccount* should be bound to the existing *ClusterRole* `secret-manager`. Create the appropriate *ClusterRoleBinding* named `secret-manager` to achieve this.

3. Confirm that the *ServiceAccount* can `get` *Secrets* in *Namespace* `sun` by using `kubectl auth can-i`.

4. Confirm that the *ServiceAccount* cannot `get` *Secrets* in *Namespace* `moon` using `kubectl auth can-i`.

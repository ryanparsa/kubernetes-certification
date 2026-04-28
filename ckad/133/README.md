# Question 133

> **Solve this question on:** `ckad-lab-14`

You need to make some namespace changes on an existing Kubernetes setup. Follow these steps:

1. Create a new *Namespace* named `meerkat`.

2. There is a *Secret* named `meerkat-secret` already in *Namespace* `meerkat`. This *Secret* should only be accessible from within the namespace. Confirm this by listing secrets in the namespace.

3. The *Deployment* `meerkat` in *Namespace* `meerkat` is not running correctly. Investigate and fix the problem by using the correct image. There are two existing *Pods* — check which image they use and why it could be failing.

4. There should also be a Kubernetes *Secret* (non-Docker) with name `meerkat` in *Namespace* `meerkat`. This *Secret* should only be accessible from within the namespace.

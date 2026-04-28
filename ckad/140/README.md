# Question 140

> **Solve this question on:** `ckad-lab-21`

Team Sunny needs to run two *Pods* in *Namespace* `sun`, but only about `readyReplicas`. Both *Deployments* are available:

1. There is a *Deployment* named `sun-1cc` with 1 replica and a `readinessProbe` already configured. Check the current `readyReplicas` count.

2. Create a *PodDisruptionBudget* named `pdb-sun-1cc` in *Namespace* `sun` for *Deployment* `sun-1cc`, with `minAvailable: 1`.

3. Create a *PodDisruptionBudget* named `pdb-sun-2cc-deployment` in *Namespace* `sun` for *Deployment* `sun-2cc`, with a `maxUnavailable` of 40%.

4. The *Deployment* should be `Available` replicas-wise.

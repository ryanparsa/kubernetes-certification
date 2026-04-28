# Question 139

> **Solve this question on:** `ckad-lab-20`

Your manager would like to know how many *Deployments* exist in *Namespace* `project-tiger` and also from *Namespace* `project-snake`. Write the output of `kubectl get deployment` (and only the deployments) for both Namespaces into `/opt/course/20/deployments.txt`.

Both Deployments are manually managed and only about `all` Pods that have the label `app=runner` are relevant. Use `kubectl get pods --all-namespaces -l app=runner` and write the output to `/opt/course/20/pods.txt`.

# Question 138

> **Solve this question on:** `ckad-lab-19`

In *Namespace* `saturn` you'll find a *Deployment* named `saturn-2cc-runner`. There is also a *Service* named `saturn-2cc-runner` in the same *Namespace*.

You can test the *Service* by running, in Namespace `saturn`, running `curl` on `saturn-2cc-runner:8080` using a temporary *Pod*.

Find out on which node the currently running *Pod* is scheduled. Write the node name to `/opt/course/19/pod-on-node.txt`.

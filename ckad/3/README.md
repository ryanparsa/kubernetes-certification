# Question 3

> **Solve this question on:** `ckad-lab-3`

Perform the following tasks:

1. Create three pods named `nginx1`, `nginx2`, and `nginx3`, all using image `nginx` and label `app=v1`.
2. Change the label of pod `nginx2` from `app=v1` to `app=v2`.
3. Add annotation `owner=team-a` to all pods that currently have label `app=v1`.
4. Create a pod named `scheduled` with image `nginx` that will only be scheduled on nodes with the label `kubernetes.io/os=linux` by using a `nodeSelector`.

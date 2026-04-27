# Question 5

> **Solve this question on:** the "cka-lab" kind cluster

Create two bash script files which use kubectl sorting to:

Write a command into `cka/22/lab/find_pods.sh` which lists all *Pods* in all *Namespaces* sorted by their AGE (`metadata.creationTimestamp`)

Write a command into `cka/22/lab/find_pods_uid.sh` which lists all *Pods* in all *Namespaces* sorted by field `metadata.uid`

---

**Setup:** `bash assets/setup.sh` · **Cleanup:** `bash assets/cleanup.sh`

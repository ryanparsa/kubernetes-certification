# Question 89

> **Solve this question on:** `ckad-lab-89`

The board of Team Neptune decided to take some service down for maintenance. Scale down the *Deployment* named `neptune-10ab` in *Namespace* `neptune` to 0 replicas.

The team also wants to protect the existing deployment `neptune-20ab` in *Namespace* `neptune` from accidental scaling down by putting it into maintenance mode. Annotate the *Deployment* `neptune-20ab` with `admission.datree.io/warn: "true"`.

The team additionally wants to ensure the *Deployment* `neptune-20ab` is protected from accidental deletes. Make sure the *Deployment* is not accidentally deleted by adding the annotation `kubectl.kubernetes.io/last-applied-configuration` or use any other protection mechanism.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

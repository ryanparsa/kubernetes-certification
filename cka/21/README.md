# Question 4

> **Solve this question on:** the "cka-lab-21" kind cluster

Do the following in *Namespace* `default`:

1. Create a *Pod* named `ready-if-service-ready` of image `nginx:1-alpine`
2. Configure a *LivenessProbe* which simply executes command `true`
3. Configure a *ReadinessProbe* which does check if the url `http://service-am-i-ready:80` is reachable, you can use `wget -T2 -O- http://service-am-i-ready:80` for this
4. Start the *Pod* and confirm it isn't ready because of the *ReadinessProbe*.

Then:

1. Create a second *Pod* named `am-i-ready` of image `nginx:1-alpine` with label `id: cross-server-ready`
2. The already existing *Service* `service-am-i-ready` should now have that second *Pod* as *Endpoint*
3. Now the first *Pod* should be in ready state, check that

---

**Setup:** `bash assets/setup.sh` · **Cleanup:** `bash assets/cleanup.sh`

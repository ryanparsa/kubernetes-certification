# Question 103

> **Solve this question on:** `kubectl config use-context k8s-c1-H`

Do the following in *Namespace* `default`. Create a single *Pod* named `ready` of image `nginx:1.16.1-alpine`. Configure a *ReadinessProbe* which simply checks the url `http://service-ws:80/`. As this Pod might not be reachable, you can skip `readinessProbe.initialDelaySeconds` so it starts checking immediately.

Create a second *Pod* named `js-l-ready` of image `nginx:1.16.1-alpine` with label `id=cross-server-ready`. The already existing *Service* `service-ws` should be ready.

Now the first *Pod* should be in ready state — confirm that.

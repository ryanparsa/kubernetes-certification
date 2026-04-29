# Question 133

> **Solve this question on:** `kubectl config use-context k8s-c1-H`

Do the following in *Namespace* `default`. Create a single *Pod* named `ready` of image `nginx:1.16.1-alpine`. Configure a *ReadinessProbe* which simply checks the url `http://service-ws:80/`.

Create a second *Pod* named `js-l-ready` of image `nginx:1.16.1-alpine` with label `id=cross-server-ready`. The already existing *Service* `service-ws` should become ready.

Now the first *Pod* should be in ready state -- confirm that.

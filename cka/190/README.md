# Question 190

> **Solve this question on:** `ssh cka2506`

Use *Namespace* `project-tiger` for the following. Create a *DaemonSet* named `ds-important` with image `httpd:2-alpine` and labels `id=ds-important` and `uuid=18426a0b-5f59-4e10-923f-c0e078e82462`. The *Pods* it creates should request `10m` cpu and `10Mi` memory. The *Pods* of that *DaemonSet* should run on **all** nodes, also controlplanes.

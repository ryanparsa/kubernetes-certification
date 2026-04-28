# Question 129

> **Solve this question on:** `ckad-lab-10`

Team Pluto needs a new cluster internal *Service*. Create a *ClusterIP* *Service* named `project-plt-6cc-svc` in *Namespace* `pluto`. This *Service* should expose a single *Pod* named `project-plt-6cc-api` of image `nginx:1.17.3-alpine`.

The *Pod* and its container should be named `project-plt-6cc-api`. The container should listen on port 3333.

Finally call the *Service* from within the cluster. Write the result of the call to `/opt/course/10/service_test.html`. Also check if the *Service* `ClusterIP` works and write the result to `/opt/course/10/service_test2.html`.

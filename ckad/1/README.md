# Question 1

> **Solve this question on:** `ckad-lab-1`

Create a namespace called `mynamespace`.

Create a pod named `nginx` with image `nginx` in the `mynamespace` namespace. Once the pod is running, exec into it and print the value of the `HOSTNAME` environment variable.

Using a YAML manifest, create a second pod named `envpod` in namespace `mynamespace` with image `busybox`, command `env`, and `restartPolicy: Never`. Retrieve the logs of the `envpod` pod and confirm environment variables are printed.

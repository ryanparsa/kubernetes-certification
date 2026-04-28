# Question 2

> **Solve this question on:** `ckad-lab-2`

Create a pod named `web` with the following specification:

- An **init container** named `init` using image `busybox` that writes the string `Hello from init` to `/work-dir/index.html`
- A **main container** named `nginx` using image `nginx:alpine` configured to serve files from `/usr/share/nginx/html`
- Both containers must share an `emptyDir` volume named `html`, mounted at `/work-dir` in the init container and at `/usr/share/nginx/html` in the main container

Verify that after the pod is running, the `nginx` container serves the content written by the init container.

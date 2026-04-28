# Question 33

> **Solve this question on:** `ckad-lab-33`

A public-facing web application needs to be exposed to external users.

Create a NodePort service named `public-web` in namespace `networking` that will expose the `web-frontend` deployment to external users.

Configure the service to accept external traffic on port `80` and forward it to port `8080` on the deployment's pods. Set the NodePort to `30080`.

Using a NodePort service will expose the application on a static port on each node in the cluster, making it accessible via any node's IP address.

Ensure the service selector correctly targets the `web-frontend` deployment pods and that the port configuration is appropriate for a web application.

This setup will enable external users to access the web application through `<node-ip>:30080`.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

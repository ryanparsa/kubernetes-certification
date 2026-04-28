# Question 50

> **Solve this question on:** `ckad-lab-50`

Create a Pod named `app-with-init` in the `init-containers` namespace with the following specifications:

1. Main container using image `nginx`
2. Init container using image `busybox` with command: `['sh', '-c', 'until nslookup myservice; do echo waiting for myservice; sleep 2; done']`
3. Create a service named `myservice` in the same namespace (selector: `app=myservice`)
4. Share a volume named `log-volume` between the init container and main container, mounted at `/shared`

Ensure the namespace exists before creating the resources.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

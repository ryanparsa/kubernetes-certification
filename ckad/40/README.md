# Question 40

> **Solve this question on:** `ckad-lab-40`

Create a ConfigMap named `app-config` in the `configuration` namespace with the following data:

```
DB_HOST=mysql
DB_PORT=3306
DB_NAME=myapp
```

Then create a Secret named `app-secret` with the following data:

```
DB_USER=admin
DB_PASSWORD=s3cr3t
```

Finally, create a Pod named `app-pod` using the `nginx` image that uses both the ConfigMap and Secret.

Mount the ConfigMap as environment variables and the Secret as a volume at `/etc/app-secret`.

Ensure the namespace exists before creating the resources.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

# Question 48

> **Solve this question on:** `ckad-lab-48`

Create a simple Docker image and run it:

1. Create a file `/tmp/Dockerfile` with the following contents:

```dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/
EXPOSE 80
```

2. Create a file `/tmp/index.html` with the following content:

```html
<!DOCTYPE html>
<html>
<body>
<h1>Hello from CKAD Docker Question!</h1>
</body>
</html>
```

3. Build the Docker image with tag `my-nginx:v1`
4. Run a container from this image with name `my-web` and publish port `80` to `8080` on the host

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

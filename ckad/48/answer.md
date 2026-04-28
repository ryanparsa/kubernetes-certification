## Answer

**Reference:** https://docs.docker.com/engine/reference/builder/

### Create the Dockerfile

```bash
cat > /tmp/Dockerfile << 'EOF'
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/
EXPOSE 80
EOF
```

### Create the index.html

```bash
cat > /tmp/index.html << 'EOF'
<!DOCTYPE html>
<html>
<body>
<h1>Hello from CKAD Docker Question!</h1>
</body>
</html>
EOF
```

### Build the Docker image

```bash
docker build -t my-nginx:v1 -f /tmp/Dockerfile /tmp
```

### Run the container

```bash
docker run -d --name my-web -p 8080:80 my-nginx:v1
```

### Verify

```bash
docker ps | grep my-web
docker images | grep my-nginx
curl localhost:8080
```

## Checklist (Score: 0/4)

- [ ] `/tmp/Dockerfile` exists with correct content
- [ ] `/tmp/index.html` exists with correct content
- [ ] Docker image `my-nginx:v1` is built correctly
- [ ] Container `my-web` is running with port `8080` mapped to `80`

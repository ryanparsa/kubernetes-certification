## Answer

**Reference:** <https://docs.docker.com/engine/reference/commandline/build/>

### Update the Dockerfile

Edit `/opt/course/11/Dockerfile` to set the `NODE_NAME` env variable:

```dockerfile
# /opt/course/11/Dockerfile
ENV NODE_NAME $HOSTNAME
```

Or if `$HOSTNAME` returns FQDN, use:

```dockerfile
ENV NODE_NAME $(hostname -s)
```

### Build and push with Docker

```bash
cd /opt/course/11

docker build -t registry.killer.sh:5000/sun-cipher:v1-docker .
docker login registry.killer.sh:5000
docker push registry.killer.sh:5000/sun-cipher:v1-docker
```

### Build and push with Podman

```bash
podman build -t registry.killer.sh:5000/sun-cipher:v1-podman .
podman login registry.killer.sh:5000
podman push registry.killer.sh:5000/sun-cipher:v1-podman
```

### Run container in background and capture logs

```bash
mkdir -p /opt/course/11/logs
podman run -d --name sun-cipher registry.killer.sh:5000/sun-cipher:v1-podman
podman logs sun-cipher > /opt/course/11/logs/container-started.log
```

## Checklist (Score: 0/5)

- [ ] Dockerfile updated with correct `NODE_NAME` env variable
- [ ] Image `registry.killer.sh:5000/sun-cipher:v1-docker` built and pushed
- [ ] Image `registry.killer.sh:5000/sun-cipher:v1-podman` built and pushed
- [ ] Container `sun-cipher` running in background via Podman
- [ ] Logs written to `/opt/course/11/logs/container-started.log`

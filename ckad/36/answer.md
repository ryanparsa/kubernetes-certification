## Answer

**Reference:** https://docs.docker.com/engine/reference/commandline/save/

### Pull the nginx image

```bash
docker pull nginx:latest
```

### Create the OCI images directory

```bash
sudo mkdir -p /root/oci-images
```

### Export and extract the image

```bash
docker save nginx:latest -o /tmp/nginx-image.tar
sudo tar -xf /tmp/nginx-image.tar -C /root/oci-images
rm /tmp/nginx-image.tar
```

### Verify

```bash
sudo ls -la /root/oci-images
```

## Checklist (Score: 0/2)

- [ ] Directory `/root/oci-images` exists
- [ ] Nginx image content is extracted into the directory (manifest.json present)

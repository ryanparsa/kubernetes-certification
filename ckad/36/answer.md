## Answer

**Reference:** https://kubernetes.io/docs/concepts/containers/images/

### Pull the nginx image

```bash
docker pull nginx:latest
```

### Create the OCI images directory

```bash
mkdir -p /root/oci-images
```

### Export the image in OCI format

```bash
docker save nginx:latest -o /tmp/nginx-image.tar
tar -xf /tmp/nginx-image.tar -C /root/oci-images
rm /tmp/nginx-image.tar
```

### Verify

```bash
ls -la /root/oci-images
cat /root/oci-images/index.json
```

## Checklist (Score: 0/2)

- [ ] Directory `/root/oci-images` exists and contains the exported image content
- [ ] Nginx image is properly stored in OCI format (index.json and blobs present)

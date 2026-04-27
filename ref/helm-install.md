# Installing a Chart

```bash
# Basic install — release name + chart
helm install <release-name> <chart>
helm install my-nginx bitnami/nginx

# Install into a specific namespace (creates namespace if it doesn't exist with --create-namespace)
helm install my-nginx bitnami/nginx \
  --namespace ingress \
  --create-namespace

# Install a specific chart version
helm install my-nginx bitnami/nginx --version 15.0.0

# Override values inline (--set)
helm install my-release bitnami/nginx \
  --set replicaCount=3 \
  --set service.type=ClusterIP

# Override values with a file (--values / -f)
helm install my-release bitnami/nginx \
  --values custom-values.yaml

# Combine --set and -f (--set overrides -f values)
helm install my-release bitnami/nginx \
  -f base-values.yaml \
  --set image.tag=1.25

# Dry-run (render templates without installing)
helm install my-release bitnami/nginx --dry-run

# Install a local chart directory
helm install my-release ./my-chart/

# Install a local chart tarball
helm install my-release ./my-chart-1.0.0.tgz
```

### --set value syntax

```bash
--set key=value                          # simple value
--set a=1,b=2                            # multiple values
--set outer.inner=value                  # nested key
--set list[0]=value                      # list item
--set list[0]=val1,list[1]=val2          # multiple list items
--set "key=value with spaces"            # value with spaces (quote)
--set-string numericKey=123              # force string type
--set-json 'key={"a":1}'                 # JSON value (Helm 3.10+)
```

---


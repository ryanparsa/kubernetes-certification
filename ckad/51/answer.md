## Answer

**Reference:** https://helm.sh/docs/intro/using_helm/

### Create the namespace

```bash
kubectl create namespace helm-basics
```

### Add the Bitnami Helm repository

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```

### Install the nginx chart

```bash
helm install nginx-release bitnami/nginx --namespace helm-basics
```

### Save the release notes

```bash
helm get notes nginx-release --namespace helm-basics > /tmp/release-notes.txt
```

### Verify

```bash
helm list -n helm-basics
cat /tmp/release-notes.txt
kubectl get pods -n helm-basics
```

## Checklist (Score: 0/3)

- [ ] Namespace `helm-basics` exists
- [ ] Helm chart `bitnami/nginx` is installed as release `nginx-release` in namespace `helm-basics`
- [ ] Release notes are saved to `/tmp/release-notes.txt`

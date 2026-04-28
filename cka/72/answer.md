## Answer

**Reference:** https://kubernetes.io/docs/reference/kubectl/generated/kubectl_config/

### List contexts

```bash
kubectl config get-contexts -o name > /opt/course/72/contexts
```

### Current context with kubectl

```bash
echo "kubectl config current-context" > /opt/course/72/context_default_kubectl
```

### Current context without kubectl

Assuming standard kubeconfig location at `~/.kube/config`:

```bash
echo "grep 'current-context' ~/.kube/config | awk '{print \$2}'" > /opt/course/72/context_default_sh
```

## Checklist (Score: 0/3)

- [ ] File `/opt/course/72/contexts` contains all context names.
- [ ] File `/opt/course/72/context_default_kubectl` contains the correct `kubectl` command.
- [ ] File `/opt/course/72/context_default_sh` contains a working command not using `kubectl`.

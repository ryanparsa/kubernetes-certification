# Question 88

> **Solve this question on:** `ckad-lab-88`

Create a DaemonSet named `node-monitor` in namespace `default` with the following specification:

- **Image**: `busybox`
- **Command**: `sh -c 'while true; do echo "Node: $(hostname)"; sleep 30; done'`
- **nodeSelector**: `kubernetes.io/os=linux`
- **Resource requests**: `cpu=50m`, `memory=32Mi`
- A **toleration** that allows the DaemonSet to run on control-plane nodes:
  - `key: node-role.kubernetes.io/control-plane`, `operator: Exists`, `effect: NoSchedule`

Verify the DaemonSet has a Pod running on every node:

```bash
kubectl get daemonset node-monitor
kubectl get pods -l app=node-monitor -o wide
```

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

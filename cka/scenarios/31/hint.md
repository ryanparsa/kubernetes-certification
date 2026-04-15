# Hints — Task 31

## Hint 1
`ssh worker-2`
`systemctl status kubelet` — is it running or crash-looping?

## Hint 2
`journalctl -u kubelet` — look for "failed to load kubelet config file".
Note the path it's trying to open.

## Hint 3
`ls /var/lib/kubelet/` — what is the actual config file called?
Compare it to the path in the error message.

## Hint 4
The wrong path is set in `/etc/systemd/system/kubelet.service.d/10-kubeadm.conf`
under `KUBELET_CONFIG_ARGS`.

## Solution

```bash
# on worker-2
vi /etc/systemd/system/kubelet.service.d/10-kubeadm.conf
# change: --config=/var/lib/kubelet/kubelet-config.yaml
#     to: --config=/var/lib/kubelet/config.yaml

systemctl daemon-reload
systemctl restart kubelet
systemctl status kubelet   # verify Active: running
exit

# on controlplane
kubectl get nodes worker-2  # Expected: Ready
```

**⚠️ Watch Out:** Always run `systemctl daemon-reload` before `systemctl restart` after
editing a unit file or drop-in — without it systemd keeps the old config in memory.

**Reflex:** Node NotReady → `systemctl status kubelet` → `journalctl -u kubelet`
→ find config source → fix → `daemon-reload` → `restart` → verify.

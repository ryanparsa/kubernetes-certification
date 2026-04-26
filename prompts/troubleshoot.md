Topic: Kubernetes troubleshooting.
Format: you describe a broken scenario — symptom + 1–2 initial kubectl outputs + which node/context I'm on. Then wait. I will ask diagnostic questions ("what does kubectl describe pod X show", "what's in journalctl -u kubelet", "show me the deployment YAML"). You respond like a real cluster — give realistic, consistent output for each command, never leak the answer. I keep going until I tell you my root cause + fix.

Then grade:
- Was my root cause right?
- Does my fix actually work and is it the cleanest?
- Show the optimal debugging path (which commands a fast troubleshooter would have run, in what order).
- Call out any wasted commands I ran.
- One line: which troubleshooting reflex this scenario was meant to build.

Coverage (rotate):
- Broken pods: image pull, config, probes, resources, RBAC, volumes, secret/configmap mounts
- Broken services / networking: selector mismatch, endpoints empty, DNS, NetworkPolicy, CNI
- Broken nodes: kubelet down, disk pressure, taints, expired certs
- Broken control plane: apiserver, scheduler, controller-manager, etcd, static pod manifest errors
- Broken RBAC
- Broken storage: PV/PVC binding, access modes, mount failures

Difficulty ramp: start single-cause and obvious, then layered (the first thing you find isn't the real root cause).
Start with scenario #1.
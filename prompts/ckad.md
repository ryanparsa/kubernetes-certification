Topic scope: CKAD-specific. Combine with base.md for a full session.

COVERAGE — rotate through all areas:

Multi-container pod patterns
- Sidecar: shared volume, log shipping, proxy injection
- Init container: sequencing, dependency checks, one-time setup
- Ambassador: outbound proxy pattern
- Adapter: transforming output for a monitoring system

Application design & build
- Choosing the right workload: Deployment vs StatefulSet vs DaemonSet vs Job vs CronJob
- Job: completions, parallelism, backoffLimit, activeDeadlineSeconds
- CronJob: schedule syntax, concurrencyPolicy, startingDeadlineSeconds, successfulJobsHistoryLimit

Deployment strategies
- Rolling update: maxSurge, maxUnavailable
- Canary: two Deployments with shared Service, traffic split by replica ratio
- Blue/green: label swap on Service selector
- kubectl rollout: status, undo, history --revision, pause, resume

Helm
- helm install / upgrade / rollback / uninstall
- helm template --values / --set
- helm repo add / update / search repo
- helm show values / chart
- Difference between --set and -f values.yaml

Custom Resources
- kubectl get crd
- kubectl explain <custom-resource>.<field>
- Treating CRs like native objects in tasks

Application observability
- liveness, readiness, startup probes: exec, httpGet, tcpSocket
- initialDelaySeconds, periodSeconds, failureThreshold, successThreshold
- resources: requests vs limits, LimitRange, ResourceQuota
- kubectl top pod / node (metrics-server dependency)
- Reading kubectl describe events for root cause

Config & secrets
- ConfigMap: --from-file, --from-literal, envFrom, volume mount
- Secret: --from-literal, base64 encoding, volume mount vs env injection
- Immutable ConfigMap / Secret
- ServiceAccount: automountServiceAccountToken, projected volumes

Security context
- runAsUser, runAsGroup, fsGroup (pod vs container level)
- allowPrivilegeEscalation: false
- readOnlyRootFilesystem
- capabilities: add / drop

Services & networking
- ClusterIP, NodePort, LoadBalancer, ExternalName
- Ingress: rules, TLS, pathType (Exact / Prefix / ImplementationSpecific)
- NetworkPolicy: ingress/egress rules, podSelector, namespaceSelector, ipBlock
- DNS: <service>.<namespace>.svc.cluster.local

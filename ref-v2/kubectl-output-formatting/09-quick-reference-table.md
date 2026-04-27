# kubectl Output Formatting Reference

[← Back to index](../README.md)

---

## 9. Quick Reference Table

| Task | Command |
|---|---|
| Sort pods by age | `kubectl get pod -A --sort-by=.metadata.creationTimestamp` |
| Sort pods by UID | `kubectl get pod -A --sort-by=.metadata.uid` |
| Get pod's node | `kubectl get pod <p> -o jsonpath='{.spec.nodeName}'` |
| Get node internal IP | `kubectl get node <n> -o jsonpath='{.status.addresses[?(@.type=="InternalIP")].address}'` |
| All images in cluster | `kubectl get pods -A -o jsonpath='{range .items[*]}{.spec.containers[*].image}{"\n"}{end}'` |
| Pod restart counts | `kubectl get pod -A -o custom-columns=NAME:.metadata.name,RESTARTS:.status.containerStatuses[0].restartCount` |
| Services and ClusterIPs | `kubectl get svc -A -o custom-columns=NS:.metadata.namespace,NAME:.metadata.name,IP:.spec.clusterIP` |

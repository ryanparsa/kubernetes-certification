## Answer

First we look at the existing Pods and their labels:

```bash
kubectl -n project-snake get pod
NAME        READY   STATUS    RESTARTS   AGE
backend-0   1/1     Running   0          8d
db1-0       1/1     Running   0          8d
db2-0       1/1     Running   0          8d
vault-0     1/1     Running   0          8d

kubectl -n project-snake get pod -L app
NAME        READY   STATUS    RESTARTS   AGE   APP
backend-0   1/1     Running   0          8d    backend
db1-0       1/1     Running   0          8d    db1
db2-0       1/1     Running   0          8d    db2
vault-0     1/1     Running   0          8d    vault
```

We test the current connection situation and see nothing is restricted:

```bash
kubectl -n project-snake get pod -o wide
NAME        READY   STATUS    RESTARTS   AGE     IP          ...
backend-0   1/1     Running   0          8d      10.44.0.24  ...
db1-0       1/1     Running   0          8d      10.44.0.25  ...
db2-0       1/1     Running   0          8d      10.44.0.23  ...
vault-0     1/1     Running   0          8d      10.44.0.22  ...

kubectl -n project-snake exec backend-0 -- curl -s 10.44.0.25:1111
database one

kubectl -n project-snake exec backend-0 -- curl -s 10.44.0.23:2222
database two

kubectl -n project-snake exec backend-0 -- curl -s 10.44.0.22:3333
vault secret storage
```

Now we create the NP by copying and changing an example from the K8s Docs:

```yaml
# 15_np.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: np-backend
  namespace: project-snake
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
    - Egress                    # policy is only about Egress
  egress:
    -                           # first rule
      to:                           # first condition "to"
      - podSelector:
          matchLabels:
            app: db1
      ports:                        # second condition "port"
      - protocol: TCP
        port: 1111
    -                           # second rule
      to:                           # first condition "to"
      - podSelector:
          matchLabels:
            app: db2
      ports:                        # second condition "port"
      - protocol: TCP
        port: 2222
```

The NP above has two rules with two conditions each, it can be read as:

```
allow outgoing traffic if:
  (destination pod has label app=db1 AND port is 1111)
  OR
  (destination pod has label app=db2 AND port is 2222)
```

### Wrong example

Now let's shortly look at a wrong example:

```yaml
# WRONG
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: np-backend
  namespace: project-snake
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
    - Egress
  egress:
    -                           # first rule
      to:                           # first condition "to"
      - podSelector:                    # first "to" possibility
          matchLabels:
            app: db1
      - podSelector:                    # second "to" possibility
          matchLabels:
            app: db2
      ports:                        # second condition "ports"
      - protocol: TCP                   # first "ports" possibility
        port: 1111
      - protocol: TCP                   # second "ports" possibility
        port: 2222
```

The NP above has one rule with two conditions and two condition-entries each, it can be read as:

```
allow outgoing traffic if:
  (destination pod has label app=db1 OR destination pod has label app=db2)
  AND
  (destination port is 1111 OR destination port is 2222)
```

Using this NP it would still be possible for `backend-*` Pods to connect to `db2-*` Pods on port 1111 for example which should be forbidden.

### Create NetworkPolicy

We create the correct NP:

```bash
kubectl apply -f 15_np.yaml
```

And to verify:

```bash
kubectl -n project-snake exec backend-0 -- curl -s 10.44.0.25:1111
database one

kubectl -n project-snake exec backend-0 -- curl -s 10.44.0.23:2222
database two

kubectl -n project-snake exec backend-0 -- curl --connect-timeout 2 -s 10.44.0.22:3333
# (should timeout or be denied)
```

Also helpful to use `kubectl describe` on the NP to see how K8s has interpreted the policy.

## Killer.sh Checklist (Score: 0/7)

- [ ] NetworkPolicy `np-backend` exists in namespace `project-snake`
- [ ] StatefulSets `backend`, `db1`, `db2` and `vault` exist and are ready
- [ ] Backend can reach `db1` on port `1111`
- [ ] Backend can reach `db1` only on port `1111`
- [ ] Backend can reach `db2` on port `2222`
- [ ] Backend can reach `db2` only on port `2222`
- [ ] Backend cannot reach `vault` on any port

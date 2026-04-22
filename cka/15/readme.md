# Question 15 | NetworkPolicy

> **Solve this question on:** `ssh cka7968`

There was a security incident where an intruder was able to access the whole cluster from a single hacked backend Pod.

To prevent this create a NetworkPolicy called `np-backend` in Namespace `project-snake`. It should allow the `backend-*` Pods only to:

- Connect to `db1-*` Pods on port 1111
- Connect to `db2-*` Pods on port 2222

Use the `app` Pod labels in your policy.

> [!NOTE]
> All Pods in the Namespace run plain Nginx images. This allows simple connectivity tests like: `k -n project-snake exec POD_NAME -- curl POD_IP:PORT`

> [!NOTE]
> For example, connections from `backend-*` Pods to `vault-*` Pods on port 3333 should no longer work

## Answer

First we look at the existing Pods and their labels:

```bash
➜ ssh cka7968

➜ candidate@cka7968:~$ k -n project-snake get pod
NAME        READY   STATUS    RESTARTS   AGE
backend-0   1/1     Running   0          8d
db1-0       1/1     Running   0          8d
db2-0       1/1     Running   0          8d
vault-0     1/1     Running   0          8d

➜ candidate@cka7968:~$ k -n project-snake get pod -L app
NAME        READY   STATUS    RESTARTS   AGE   APP
backend-0   1/1     Running   0          8d    backend
db1-0       1/1     Running   0          8d    db1
db2-0       1/1     Running   0          8d    db2
vault-0     1/1     Running   0          8d    vault
```

We test the current connection situation and see nothing is restricted:

```bash
➜ candidate@cka7968:~$ k -n project-snake get pod -o wide
NAME        READY   STATUS    RESTARTS   AGE     IP          ...
backend-0   1/1     Running   0          8d      10.44.0.24  ...
db1-0       1/1     Running   0          8d      10.44.0.25  ...
db2-0       1/1     Running   0          8d      10.44.0.23  ...
vault-0     1/1     Running   0          8d      10.44.0.22  ...

➜ candidate@cka7968:~$ k -n project-snake exec backend-0 -- curl -s 10.44.0.25:1111
database one

➜ candidate@cka7968:~$ k -n project-snake exec backend-0 -- curl -s 10.44.0.23:2222
database two

➜ candidate@cka7968:~$ k -n project-snake exec backend-0 -- curl -s 10.44.0.22:3333
vault secret storage
```

Now we create the NP by copying and changing an example from the K8s Docs:

```yaml
# cka7968:/home/candidate/15_np.yaml
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
➜ candidate@cka7968:~$ k -f 15_np.yaml create
```

And to verify:

```bash
➜ candidate@cka7968:~$ k -n project-snake exec backend-0 -- curl -s 10.44.0.25:1111
database one

➜ candidate@cka7968:~$ k -n project-snake exec backend-0 -- curl -s 10.44.0.23:2222
database two

➜ candidate@cka7968:~$ k -n project-snake exec backend-0 -- curl -s 10.44.0.22:3333
^C
```

Also helpful to use `kubectl describe` on the NP to see how K8s has interpreted the policy.

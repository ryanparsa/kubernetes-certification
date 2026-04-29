## Answer

### Create Namespace

```bash
kubectl create namespace cka-master
```

### Namespaced Resources

We can get a list of all namespaced resources using `api-resources`:

```bash
kubectl api-resources --namespaced -o name > lab/resources.txt
```

### Namespace with most *Roles*

We can iterate through namespaces and count roles:

```bash
# Example manual check
kubectl -n project-jinan get role --no-headers | wc -l
kubectl -n project-miami get role --no-headers | wc -l
...
```

Finally we write the name and amount into the file:

```bash
# lab/crowded-namespace.txt
project-miami with 300 roles
```


## Checklist (Score: 0/3)

- [ ] Namespace `cka-master` exists
- [ ] File `lab/resources.txt` contains namespaced resources
- [ ] File `lab/crowded-namespace.txt` has correct content

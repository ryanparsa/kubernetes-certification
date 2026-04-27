# What is etcd

etcd is a **distributed, consistent key-value store** built on the **Raft consensus
algorithm**. It provides:

- **Strong consistency**: every read reflects the most recent committed write (linearizable)
- **High availability**: an odd-numbered cluster tolerates `(N-1)/2` node failures
- **Watch API**: clients subscribe to key prefixes and receive change notifications in real time

### Raft consensus basics

```
Leader election:
  - One node is elected leader; all writes go to the leader
  - Leader sends log entries to followers; a write is committed once a quorum
    (majority) of nodes acknowledge it

Quorum (minimum nodes needed to commit a write):
  3-node cluster → 2  (tolerates 1 failure)
  5-node cluster → 3  (tolerates 2 failures)
  7-node cluster → 4  (tolerates 3 failures)
```

> A cluster with an **even** number of members has the same fault tolerance as one
> with `N-1` members (e.g. 4-node = 2-failure tolerance, same as 3-node) but is harder
> to elect a leader. Always use **odd** member counts.

---


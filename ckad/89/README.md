# Question 89

> **Solve this question on:** `ckad-lab-89`

Create a *ConfigMap* named `trauerweide` in *Namespace* `default` with the content:

```
tree=trauerweide
```

Create a *Pod* named `pod-6` in *Namespace* `default` with image `busybox:1.31.0`, which should run `sleep 999`. It should be configured to use an `emptyDir` volume mounted at `/tmp/vols`.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

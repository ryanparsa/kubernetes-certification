# Question 125

> **Solve this question on:** `ckad-lab-06`

Create a *ConfigMap* named `trauerweide` in *Namespace* `default` with the content:

```
tree=trauerweide
```

Create a *Pod* named `pod-6` in *Namespace* `default` with image `busybox:1.31.0`, which should run `sleep 999`. It should be configured to use an `emptyDir` volume mounted at `/tmp/vols`. Create the necessary files to be ready, and then close.

Create the first and confirm a status.

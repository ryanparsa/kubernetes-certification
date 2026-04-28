# Question 118

> **Solve this question on:** `kubectl config use-context k8s-c1-H`

Do the following in a new *Namespace* `secret`. Create a *Pod* named `secret` of image `busybox:1.31.1` which should keep running.

There is an existing *Secret* located at `/opt/course/19/secret1.yaml` — create it in the *Namespace* `secret` and mount it **readonly** into the *Pod* at `/tmp/secret1`.

Create a new *Secret* in *Namespace* `secret` called `secret2` which should contain `user=user1` and `pass=1234`. These values should be available inside the *Pod*'s container as environment variables `APP_USER` and `APP_PASS`.

Confirm everything is working.

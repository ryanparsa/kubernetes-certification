# Question 75

> **Solve this question on:** `ckad-lab-75`

Create a *Pod* named `adapter` with two containers that share an `emptyDir` volume mounted at `/var/logs` in both containers.

- Container **app** uses the image `busybox` and runs the command:
  ```
  /bin/sh -c 'while true; do echo "$(date) | $(du -sh ~)" >> /var/logs/diskspace.txt; sleep 5; done;'
  ```

- Container **transformer** uses the image `busybox` and runs the command:
  ```
  /bin/sh -c 'sleep 20; while true; do while read LINE; do echo "$LINE" | cut -f2 -d"|" >> /tmp/$(date +%Y-%m-%d-%H-%M-%S)-transformed.txt; done < /var/logs/diskspace.txt; sleep 20; done;'
  ```

After the *Pod* is running, shell into the **transformer** container and confirm that transformed files appear in `/tmp` roughly every 20 seconds.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

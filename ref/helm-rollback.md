# Release History and Rollback

```bash
# View revision history of a release
helm history <release-name> -n <namespace>
helm history my-nginx -n ingress
# REVISION  UPDATED                  STATUS     CHART          APP VERSION  DESCRIPTION
# 1         Mon Jan 01 00:00:00 UTC  superseded nginx-15.0.0   1.25.0       Install complete
# 2         Tue Jan 02 00:00:00 UTC  deployed   nginx-15.1.0   1.25.1       Upgrade complete

# Roll back to the previous revision
helm rollback <release-name>
helm rollback my-nginx

# Roll back to a specific revision
helm rollback my-nginx 1 -n ingress
```

---


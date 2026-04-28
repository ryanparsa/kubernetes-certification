# Question 53

> **Solve this question on:** `cka-lab-53`

Configure Pod Security for the `security` namespace and create a secure nginx pod:

1. Create the `security` namespace with Pod Security Admission (PSA) controls:
   - Set the namespace to enforce the `restricted` security profile
   - Use the `latest` version of the security profile

2. Create a secure pod named `secure-pod` in the `security` namespace with the following specifications:
   - Image: `nginx`
   - Pod-level security context:
     - Run as a non-root user with UID `1000`
     - Enable `runAsNonRoot`
     - Use the default seccomp profile (`RuntimeDefault`)
   - Container-level security context:
     - Prevent privilege escalation (`allowPrivilegeEscalation: false`)
     - Run as non-root user (UID `1000`)
     - Drop ALL Linux capabilities
   - Add a volume mount:
     - Create an `emptyDir` volume named `html`
     - Mount the volume at `/usr/share/nginx/html`

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

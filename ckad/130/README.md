# Question 130

> **Solve this question on:** `ckad-lab-11`

During the build, creating on a maintenance (build) process to create a containerized solution. Follow the instructions below:

1. Change the *Dockerfile* at `/opt/course/11/Dockerfile`:
   - The value of the environment variable `NODE_NAME` should be set to the `hostname`-short value. `$HOSTNAME` should only return the short name, not the FQDN.

2. Build the image using *Docker*, tagged `registry.killer.sh:5000/sun-cipher:v1-docker`, logged in to the registry and push it.

3. Build the image using *Podman*, tagged `registry.killer.sh:5000/sun-cipher:v1-podman`, logged in to the registry and push it.

4. Run a container using *Podman* named `sun-cipher` using the image `registry.killer.sh:5000/sun-cipher:v1-podman` in the background, and keep it running. Write the output of the container into `/opt/course/11/logs/container-started.log`.

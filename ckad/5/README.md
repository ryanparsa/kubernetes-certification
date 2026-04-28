# Question 5

> **Solve this question on:** `ckad-lab-5`

Perform the following Job tasks:

1. Create a Job named `pi` with image `perl:5.34` that runs the command `perl -Mbignum=bpi -wle 'print bpi(2000)'`. Wait for it to complete and retrieve the output from its logs.

2. Create a Job named `multi` with image `busybox` that runs `echo done`, configured with `completions: 5` and `parallelism: 2`. Wait for all completions.

3. Create a Job named `deadline` with image `busybox` running command `sleep 60`, with `activeDeadlineSeconds: 30` so it is automatically terminated if it runs longer than 30 seconds.

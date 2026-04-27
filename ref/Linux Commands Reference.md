# Linux Commands Reference

Essential Linux commands for Kubernetes certification exams (CKA, CKAD, CKS):
file editing with vim, text search with grep, file finding with find, and
other commonly needed shell utilities.

---

## 1. vim

### Modes

| Mode | How to enter | Purpose |
|---|---|---|
| Normal | `Esc` | Navigation, copy/paste, delete |
| Insert | `i` (before cursor), `a` (after), `o` (new line below) | Type text |
| Visual | `v` (char), `V` (line), `Ctrl-v` (block) | Select text |
| Command | `:` | Save, quit, search/replace, settings |

### Essential commands

```vim
" Save and quit
:w          " save
:q          " quit (fails if unsaved changes)
:wq         " save and quit
:q!         " quit without saving
:wq!        " force save and quit (read-only files)
ZZ          " save and quit (normal mode shortcut)
ZQ          " quit without saving (normal mode shortcut)

" Navigation
gg          " go to first line
G           " go to last line
:<n>        " go to line n  (e.g. :42)
0           " start of line
$           " end of line
w           " next word
b           " previous word
Ctrl-f      " page down
Ctrl-b      " page up

" Editing
dd          " delete (cut) current line
<n>dd       " delete n lines (e.g. 3dd)
yy          " yank (copy) current line
<n>yy       " yank n lines
p           " paste after cursor / below line
P           " paste before cursor / above line
u           " undo
Ctrl-r      " redo
x           " delete character under cursor
r<c>        " replace character under cursor with c
cw          " change word (delete word and enter insert mode)

" Search
/<pattern>  " search forward
?<pattern>  " search backward
n           " next match
N           " previous match
*           " search for word under cursor (forward)

" Search and replace
:%s/old/new/g      " replace all occurrences in file
:%s/old/new/gc     " replace all, ask for confirmation each time
:10,20s/old/new/g  " replace in lines 10–20

" Indentation (useful for YAML)
>>          " indent line right (normal mode)
<<          " indent line left (normal mode)
>}          " indent paragraph
=G          " auto-indent from cursor to end of file

" Multiple lines — visual block
Ctrl-v      " enter visual block mode
<select lines with j/k>
I           " insert at start of each selected line (press Esc when done)
d           " delete selected block

" Settings (apply for current session)
:set number          " show line numbers
:set nonumber        " hide line numbers
:set paste           " disable auto-indent before pasting from clipboard
:set nopaste         " re-enable auto-indent
:set expandtab       " use spaces instead of tabs
:set tabstop=2       " tab width = 2
:set shiftwidth=2    " indent width = 2
```

### Useful one-liners for exam

```bash
# Open file at a specific line
vim +42 /etc/kubernetes/manifests/kube-apiserver.yaml

# Open file and immediately search
vim +/pattern /path/to/file

# Make vim YAML-friendly (add to ~/.vimrc)
echo 'set expandtab tabstop=2 shiftwidth=2 number' >> ~/.vimrc
```

---

## 2. grep

```bash
# Basic search
grep "pattern" file.txt

# Case-insensitive search
grep -i "pattern" file.txt

# Recursive search in directory
grep -r "pattern" /etc/kubernetes/

# Show line numbers
grep -n "pattern" file.txt

# Show only matching filename (no content)
grep -l "pattern" /etc/kubernetes/manifests/*.yaml

# Invert match (lines that do NOT match)
grep -v "pattern" file.txt

# Extended regex (|, +, ?, groups)
grep -E "error|warning|failed" /var/log/syslog

# Fixed string (no regex — faster for literal matches)
grep -F "192.168.1.1" file.txt

# Count matching lines
grep -c "pattern" file.txt

# Show context around a match
grep -A 3 "pattern" file.txt   # 3 lines after
grep -B 3 "pattern" file.txt   # 3 lines before
grep -C 3 "pattern" file.txt   # 3 lines before and after

# Match whole word only
grep -w "port" file.txt

# Quiet — exit code only (0 = found, 1 = not found)
grep -q "pattern" file.txt && echo "found"

# Multiple patterns
grep -e "pattern1" -e "pattern2" file.txt

# Common exam uses
grep -i "error" /var/log/syslog | tail -20
journalctl -u kubelet | grep -i "fail\|error"
kubectl describe pod mypod | grep -A 5 "Events:"
kubectl get pods -A | grep -v Running
grep -r "image:" /etc/kubernetes/manifests/
```

---

## 3. find

```bash
# Find by name
find /etc -name "*.yaml"

# Case-insensitive name
find /etc -iname "*.conf"

# Find by type (f=file, d=directory, l=symlink)
find /var/lib -type f -name "*.pem"
find /etc/kubernetes -type d

# Find by modification time
find /var/log -mmin -60         # modified in last 60 minutes
find /var/log -mtime -1         # modified in last 1 day
find /var/log -mtime +7         # modified more than 7 days ago

# Find by size
find /var -size +100M           # larger than 100 MB
find /tmp -size -1k             # smaller than 1 KB

# Find and execute a command on results
find /etc/cni -name "*.conf" -exec cat {} \;
find /tmp -name "*.log" -exec rm {} \;

# Find and print with null separator (safe for filenames with spaces)
find /etc -name "*.yaml" -print0 | xargs -0 grep "apiVersion"

# Find by permissions
find /etc/kubernetes/pki -perm 600     # exactly 600
find /usr -perm /111                    # executable by anyone

# Find by owner/group
find /var/lib/kubelet -user root
find /etc/kubernetes -group root

# Limit search depth
find /etc -maxdepth 2 -name "*.yaml"

# Exclude a directory
find /var -name "*.log" -not -path "*/containers/*"

# Common exam uses
find / -name "kubeconfig" 2>/dev/null
find /etc/kubernetes/pki -name "*.crt" -exec openssl x509 -noout -dates -in {} \;
find /var/log -name "*.log" -mmin -30
```

---

## 4. sed

```bash
# Print specific line(s)
sed -n '10p' file.txt           # print line 10
sed -n '10,20p' file.txt        # print lines 10–20

# In-place substitution
sed -i 's/old/new/' file.txt            # replace first occurrence per line
sed -i 's/old/new/g' file.txt           # replace all occurrences

# Delete lines matching a pattern
sed -i '/^#/d' file.txt                 # remove comment lines

# Insert a line before/after a match
sed -i '/pattern/i new line before' file.txt
sed -i '/pattern/a new line after' file.txt

# Remove blank lines
sed -i '/^$/d' file.txt

# Common exam uses
# Change a port number in a config file
sed -i 's/6443/6444/' /etc/kubernetes/manifests/kube-apiserver.yaml
```

---

## 5. awk

```bash
# Print specific column(s)
awk '{print $1}' file.txt          # first column
awk '{print $1, $3}' file.txt      # first and third
kubectl get pods | awk '{print $1, $3}'  # name and status

# Filter rows by column value
awk '$3 > 5 {print}' file.txt
kubectl get pods -A | awk '$5 > 3'  # pods with >3 restarts

# Print with custom delimiter (default is whitespace)
awk -F: '{print $1}' /etc/passwd    # colon-separated, print username

# NR = row number, NF = number of fields
awk 'NR==1{print}' file.txt         # print first line
awk 'NR>1{print}' file.txt          # skip header line
awk '{print NR, $0}' file.txt       # print with line numbers

# Sum a column
kubectl get nodes -o wide | awk '{sum += $1} END {print sum}'
```

---

## 6. tail / head

```bash
# Last N lines
tail -n 50 /var/log/syslog
tail -50 /var/log/syslog           # shorthand

# Follow a log file in real time
tail -f /var/log/syslog
tail -f /var/log/kubernetes/audit.log

# Follow multiple files
tail -f /var/log/syslog /var/log/auth.log

# First N lines
head -n 20 file.txt

# Combined: lines 10–30 of a file
sed -n '10,30p' file.txt
```

---

## 7. cat / less / more

```bash
# Print file to stdout
cat file.txt

# Concatenate files
cat file1.txt file2.txt > combined.txt

# Append to file
cat >> file.txt <<EOF
line 1
line 2
EOF

# View large files page by page (q to quit)
less /var/log/syslog
less +G file.txt          # open at end of file

# Search inside less: /pattern then n/N for next/prev
# Press q to quit
```

---

## 8. Useful shell utilities

```bash
# Check disk usage
df -h                          # filesystem usage
du -sh /var/lib/containerd/    # size of a directory
du -sh /*  | sort -h           # find largest directories

# Check memory
free -h

# Check running processes
ps aux | grep kubelet
ps aux | grep -E "kube|etcd"

# Kill a process by PID
kill <pid>
kill -9 <pid>      # force kill (SIGKILL)

# systemd service management
systemctl status kubelet
systemctl start kubelet
systemctl stop kubelet
systemctl restart kubelet
systemctl enable kubelet       # start on boot
systemctl disable kubelet
systemctl daemon-reload        # reload unit files after edits

# journald log viewing
journalctl -u kubelet                    # all logs for kubelet
journalctl -u kubelet -n 100            # last 100 lines
journalctl -u kubelet --since "10 min ago"
journalctl -u kubelet -f                # follow (live)
journalctl -u kubelet --no-pager | grep -i error

# Network utilities
ss -tlnp                       # listening TCP ports with process info
ss -ulnp                       # listening UDP ports
ip addr show                   # network interfaces and IPs
ip route show                  # routing table
curl -sk https://localhost:6443/healthz   # API server health (skip TLS verify)
wget -qO- https://example.com  # download URL to stdout

# File permissions
chmod 600 file.txt             # owner read/write only
chmod 644 file.txt             # owner rw, group/other r
chmod 755 dir/                 # owner rwx, group/other rx
chown root:root file.txt
chown -R 1000:1000 /data/

# Environment variables
export KUBECONFIG=/tmp/my.kubeconfig
echo $KUBECONFIG
env | grep KUBE

# Redirection
command > /tmp/out.txt         # stdout to file (overwrite)
command >> /tmp/out.txt        # stdout to file (append)
command 2>&1 | tee /tmp/out.txt  # stdout+stderr to file and screen
command 2>/dev/null            # discard stderr
```

---

## 9. Quick reference — exam tips

```bash
# Open vim with YAML-friendly settings immediately
vim -c 'set et ts=2 sw=2 nu' file.yaml

# Extract a certificate subject and SANs quickly
openssl x509 -noout -text -in cert.crt | grep -E "Subject:|DNS:|IP:"

# Check which process is using a port
ss -tlnp | grep :6443

# Find a file anywhere on the system (suppress permission errors)
find / -name "admin.conf" 2>/dev/null

# Confirm a service is listening after changes
systemctl restart kubelet && sleep 3 && systemctl status kubelet

# Count error lines in a log
grep -ic "error" /var/log/syslog

# Replace a YAML value in-place
sed -i 's/image: nginx:1.19/image: nginx:1.25/' deployment.yaml
```

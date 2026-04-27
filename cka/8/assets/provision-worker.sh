#!/usr/bin/env bash
set -euo pipefail

K8S_VERSION="1.31.8"
K8S_MINOR="1.31"

apt-get update -q
apt-get install -y -q containerd apt-transport-https ca-certificates curl gpg

mkdir -p /etc/containerd
containerd config default > /etc/containerd/config.toml
sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml
systemctl restart containerd
systemctl enable containerd

swapoff -a
sed -i '/swap/d' /etc/fstab
modprobe overlay
modprobe br_netfilter
printf 'overlay\nbr_netfilter\n' > /etc/modules-load.d/k8s.conf
printf 'net.bridge.bridge-nf-call-iptables=1\nnet.bridge.bridge-nf-call-ip6tables=1\nnet.ipv4.ip_forward=1\n' \
  > /etc/sysctl.d/k8s.conf
sysctl --system -q

mkdir -p /etc/apt/keyrings
curl -fsSL "https://pkgs.k8s.io/core:/stable:/v${K8S_MINOR}/deb/Release.key" \
  | gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v${K8S_MINOR}/deb/ /" \
  > /etc/apt/sources.list.d/kubernetes.list
apt-get update -q
apt-get install -y -q "kubelet=${K8S_VERSION}-*" "kubeadm=${K8S_VERSION}-*" "kubectl=${K8S_VERSION}-*"
apt-mark hold kubelet kubeadm kubectl

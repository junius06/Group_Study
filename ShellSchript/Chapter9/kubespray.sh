#!/bin/bash

master_node=192.168.1.2
client_node=192.168.1.3

# 필수 패키지 설치
echo "필수 패키지 설치 중..."
sudo apt-get update && sudo apt-get install -y software-properties-common
sudo apt-add-repository --yes --update ppa:ansible/ansible
sudo apt-get install -y ansible python3-pip

# Kubespray 클론
echo "Kubespray 저장소 클론 중..."
git clone https://github.com/kubernetes-sigs/kubespray.git
cd kubespray

# 파이썬 종속성 설치
echo "필요한 파이썬 패키지 설치 중..."
pip3 install -r requirements.txt

# 인벤토리 파일 준비
echo "인벤토리 파일 설정 중..."
cp -rfp inventory/sample inventory/mycluster

# SSH 키 생성 (무비밀번호)
echo "SSH 키 생성 중..."
ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa

# 클라이언트 노드에 대한 SSH 키 복사
CLIENT_NODES=("$master_node" "$client_node")
for NODE in "${CLIENT_NODES[@]}"; do
    echo "SSH 키를 $NODE 에 복사 중..."
    ssh-copy-id -i ~/.ssh/id_rsa.pub ubuntu@$NODE
done

# 여기서는 예시로 2개의 노드(노드1, 노드2)에 대한 설정을 진행합니다.
# 실제 환경에 맞추어서 IP 주소와 사용자 이름, ssh 키 파일 경로 등을 수정해야 합니다.
cat <<EOF > inventory/mycluster/inventory.ini
[all]
node1 ansible_host=$master_node ansible_user=ubuntu
node2 ansible_host=$client_node ansible_user=ubuntu

[kube-master]
node1

[kube-node]
node1
node2

[etcd]
node1

[calico-rr]

[k8s-cluster:children]
kube-master
kube-node
calico-rr
EOF

# 클러스터 설치
echo "Kubernetes 클러스터 설치 중..."
ansible-playbook -i inventory/mycluster/inventory.ini --become --become-user=root cluster.yml

echo "설치 완"
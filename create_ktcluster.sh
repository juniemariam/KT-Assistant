#!/bin/bash

# CONFIG
PROJECT_ID="xenon-tracer-464618-p8"
CLUSTER_NAME="ktcluster"
ZONE="us-central1-a"
NODE_POOL_NAME="gpu-pool"
MACHINE_TYPE="n1-standard-4"
GPU_TYPE="nvidia-tesla-t4"
GPU_COUNT="1"
NUM_NODES="1"

# Set project
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable container.googleapis.com compute.googleapis.com

# Create cluster without default pool
gcloud container clusters create $CLUSTER_NAME \
  --zone $ZONE \
  --no-enable-basic-auth \
  --release-channel=REGULAR \
  --enable-ip-alias \
  --scopes=https://www.googleapis.com/auth/cloud-platform \
  --enable-autoupgrade \
  --enable-autorepair \
  --no-create-node-pool

# Create GPU node pool
gcloud container node-pools create $NODE_POOL_NAME \
  --cluster $CLUSTER_NAME \
  --zone $ZONE \
  --accelerator type=$GPU_TYPE,count=$GPU_COUNT \
  --num-nodes $NUM_NODES \
  --machine-type $MACHINE_TYPE \
  --disk-size 100 \
  --scopes=https://www.googleapis.com/auth/cloud-platform \
  --image-type=UBUNTU_CONTAINERD \
  --node-labels accelerator=$GPU_TYPE \
  --enable-autoupgrade \
  --enable-autorepair

# Get credentials for kubectl
gcloud container clusters get-credentials $CLUSTER_NAME \
  --zone $ZONE \
  --project $PROJECT_ID

# Install NVIDIA GPU driver daemonset
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/container-engine-accelerators/stable/nvidia-driver-installer/cos/daemonset-preloaded.yaml

echo "Cluster '$CLUSTER_NAME' and GPU pool are ready!"

#!/bin/bash
set -e
MODEL_DIR=${MODEL_DIR:-models}
MODEL_URL="https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt"
mkdir -p "$MODEL_DIR"
if [ ! -f "$MODEL_DIR/yolov8n.pt" ]; then
    echo "Downloading YOLOv8n model to $MODEL_DIR/yolov8n.pt ..."
    wget -O "$MODEL_DIR/yolov8n.pt" "$MODEL_URL"
    echo "Download complete."
else
    echo "Model already exists at $MODEL_DIR/yolov8n.pt"
fi
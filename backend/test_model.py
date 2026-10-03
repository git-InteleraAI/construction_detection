from ultralytics import YOLO
import torch

MODEL_PATH = "best.pt"

print("=" * 60)
print("LOADING PPE YOLO11s MODEL")
print("=" * 60)

print("PyTorch version :", torch.__version__)
print("Device          :", "CPU")

# Load trained model
model = YOLO(MODEL_PATH)

print("\n✅ Model loaded successfully!")

print("Model type      :", type(model.model).__name__)
print("Number of classes:", len(model.names))

print("\nClass names:")
for class_id, class_name in model.names.items():
    print(f"{class_id}: {class_name}")

print("=" * 60)
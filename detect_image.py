from ultralytics import YOLO
from pathlib import Path

# ============================================================
# PPE YOLO11s - LOCAL IMAGE DETECTION
# ============================================================

MODEL_PATH = "best.pt"
IMAGE_PATH = "construction.png"

print("=" * 60)
print("PPE YOLO11s - IMAGE DETECTION")
print("=" * 60)

# Check model
if not Path(MODEL_PATH).exists():
    raise FileNotFoundError(
        f"Model not found: {MODEL_PATH}"
    )

# Check image
if not Path(IMAGE_PATH).exists():
    raise FileNotFoundError(
        f"Image not found: {IMAGE_PATH}"
    )

print(f"Model : {MODEL_PATH}")
print(f"Image : {IMAGE_PATH}")
print()

# Load trained model
model = YOLO(MODEL_PATH)

print("✅ Model loaded")
print("Running detection on CPU...")
print()

# Run inference
results = model.predict(
    source=IMAGE_PATH,
    device="cpu",
    conf=0.25,
    save=True
)

print()
print("=" * 60)
print("DETECTION COMPLETED")
print("=" * 60)

print("✅ Detection completed successfully.")
print("The annotated image was saved by Ultralytics.")
print("=" * 60)
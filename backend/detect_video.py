from ultralytics import YOLO
from pathlib import Path

# ============================================================
# PPE YOLO11s - LOCAL VIDEO DETECTION
# ============================================================

MODEL_PATH = "best.pt"
VIDEO_PATH = "construction.mp4"

print("=" * 60)
print("PPE YOLO11s - VIDEO DETECTION")
print("=" * 60)

# Check model
if not Path(MODEL_PATH).exists():
    raise FileNotFoundError(
        f"Model not found: {MODEL_PATH}"
    )

# Check video
if not Path(VIDEO_PATH).exists():
    raise FileNotFoundError(
        f"Video not found: {VIDEO_PATH}"
    )

print(f"Model : {MODEL_PATH}")
print(f"Video : {VIDEO_PATH}")
print()

# Load trained model
model = YOLO(MODEL_PATH)

print("✅ Model loaded")
print("Running video detection on CPU...")
print()

# Run detection
results = model.predict(
    source=VIDEO_PATH,
    device="cpu",
    conf=0.25,
    save=True
)

print()
print("=" * 60)
print("VIDEO DETECTION COMPLETED")
print("=" * 60)
print("✅ Detection completed successfully.")
print("The annotated video was saved by Ultralytics.")
print("=" * 60)
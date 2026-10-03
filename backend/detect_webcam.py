from ultralytics import YOLO
import cv2
from pathlib import Path

# ============================================================
# PPE YOLO11s - LIVE WEBCAM DETECTION
# ============================================================

MODEL_PATH = "best.pt"

print("=" * 60)
print("PPE YOLO11s - LIVE WEBCAM DETECTION")
print("=" * 60)

# Check model
if not Path(MODEL_PATH).exists():
    raise FileNotFoundError(
        f"Model not found: {MODEL_PATH}"
    )

# Load trained model
model = YOLO(MODEL_PATH)

print("✅ Model loaded successfully")
print("Starting webcam...")
print()
print("Press 'q' to quit.")
print("=" * 60)

# Open default webcam
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    raise RuntimeError(
        "❌ Could not open webcam."
    )

while True:

    # Read frame
    ret, frame = cap.read()

    if not ret:
        print("❌ Failed to read frame from webcam.")
        break

    # Run YOLO detection
    results = model.predict(
        source=frame,
        device="cpu",
        conf=0.25,
        verbose=False
    )

    # Draw detections
    annotated_frame = results[0].plot()

    # Display live video
    cv2.imshow(
        "PPE YOLO11s - Live Detection",
        annotated_frame
    )

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release webcam
cap.release()
cv2.destroyAllWindows()

print()
print("=" * 60)
print("WEBCAM DETECTION STOPPED")
print("=" * 60)
print("✅ Webcam released successfully.")
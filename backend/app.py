import asyncio

import cv2
import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from ultralytics import YOLO
import uvicorn


# ============================================================
# LOAD YOLO MODEL
# ============================================================

MODEL_PATH = "best.pt"

print("Loading YOLO model...")

model = YOLO(MODEL_PATH)

print("YOLO model loaded successfully.")
print("Classes:", model.names)


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(title="PPE Detection System")


# ============================================================
# YOLO DETECTION
# ============================================================

def detect_frame(frame):
    """
    Run YOLO detection on one frame
    and return the annotated frame.
    """

    results = model.predict(
        source=frame,
        device="cpu",
        conf=0.25,
        verbose=False
    )

    annotated_frame = results[0].plot()

    return annotated_frame


# ============================================================
# WEBSOCKET
# ============================================================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    print("Browser connected.")

    try:

        while True:

            # Receive JPEG image from browser
            data = await websocket.receive_bytes()

            # Convert bytes -> NumPy array
            image_array = np.frombuffer(
                data,
                dtype=np.uint8
            )

            # Convert JPEG -> OpenCV image
            frame = cv2.imdecode(
                image_array,
                cv2.IMREAD_COLOR
            )

            if frame is None:
                print("Invalid image received.")
                continue

            # Run YOLO without blocking FastAPI
            annotated_frame = await asyncio.to_thread(
                detect_frame,
                frame
            )

            # Convert annotated frame -> JPEG
            success, encoded_image = cv2.imencode(
                ".jpg",
                annotated_frame,
                [cv2.IMWRITE_JPEG_QUALITY, 80]
            )

            if not success:
                print("Failed to encode output frame.")
                continue

            # Send detection result back to browser
            await websocket.send_bytes(
                encoded_image.tobytes()
            )

    except WebSocketDisconnect:

        print("Browser disconnected.")

    except Exception as e:

        print("WebSocket error:", e)

        try:
            await websocket.close()
        except Exception:
            pass


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )

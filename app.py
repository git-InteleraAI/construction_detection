import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
from ultralytics import YOLO


# ============================================================
# PPE DETECTION SYSTEM
# ============================================================

MODEL_PATH = "best.pt"
CAMERA_INDEX = 1

model = YOLO(MODEL_PATH)

camera = None
running = False


# ============================================================
# START CAMERA
# ============================================================

def start_camera():
    global camera, running

    if running:
        return

    camera = cv2.VideoCapture(CAMERA_INDEX)

    if not camera.isOpened():
        messagebox.showerror(
            "Camera Error",
            "Could not open the C270 HD webcam."
        )
        return

    running = True

    status_label.config(
        text="Status: C270 HD Camera Connected"
    )

    start_button.config(state="disabled")
    stop_button.config(state="normal")

    update_frame()


# ============================================================
# LIVE FRAME
# ============================================================

def update_frame():
    global camera, running

    if not running:
        return

    ret, frame = camera.read()

    if not ret:
        status_label.config(
            text="Status: Unable to read camera"
        )
        return

    # YOLO detection
    results = model.predict(
        source=frame,
        device="cpu",
        conf=0.25,
        verbose=False
    )

    # Draw detections
    frame = results[0].plot()

    # Convert BGR to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    image = Image.fromarray(frame)

    # Get available display area
    video_width = video_frame.winfo_width()
    video_height = video_frame.winfo_height()

    if video_width > 10 and video_height > 10:

        # Keep video aspect ratio
        image.thumbnail(
            (video_width, video_height),
            Image.Resampling.LANCZOS
        )

    photo = ImageTk.PhotoImage(image)

    video_label.config(image=photo)
    video_label.image = photo

    root.after(10, update_frame)


# ============================================================
# STOP CAMERA
# ============================================================

def stop_camera():
    global camera, running

    running = False

    if camera is not None:
        camera.release()
        camera = None

    video_label.config(image="")
    video_label.image = None

    status_label.config(
        text="Status: Camera Stopped"
    )

    start_button.config(state="normal")
    stop_button.config(state="disabled")


# ============================================================
# EXIT
# ============================================================

def close_app():
    stop_camera()
    root.destroy()


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title("PPE Detection System")

root.geometry("1000x700")
root.minsize(800, 600)

root.configure(bg="#f2f2f2")


# ============================================================
# TITLE
# ============================================================

title_label = tk.Label(
    root,
    text="PPE DETECTION SYSTEM",
    font=("Arial", 24, "bold"),
    bg="#f2f2f2"
)

title_label.pack(
    pady=15
)


# ============================================================
# VIDEO AREA
# ============================================================

video_frame = tk.Frame(
    root,
    bg="black"
)

video_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)


video_label = tk.Label(
    video_frame,
    text="Camera is not started",
    font=("Arial", 16),
    bg="black",
    fg="white"
)

video_label.place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)


# ============================================================
# STATUS
# ============================================================

status_label = tk.Label(
    root,
    text="Status: Camera Stopped",
    font=("Arial", 12),
    bg="#f2f2f2"
)

status_label.pack(
    pady=5
)


# ============================================================
# BUTTON AREA
# ============================================================

button_frame = tk.Frame(
    root,
    bg="#f2f2f2"
)

button_frame.pack(
    pady=15
)


start_button = tk.Button(
    button_frame,
    text="Start Camera",
    command=start_camera,
    width=15,
    height=2,
    font=("Arial", 11, "bold")
)

start_button.grid(
    row=0,
    column=0,
    padx=10
)


stop_button = tk.Button(
    button_frame,
    text="Stop Camera",
    command=stop_camera,
    width=15,
    height=2,
    font=("Arial", 11, "bold"),
    state="disabled"
)

stop_button.grid(
    row=0,
    column=1,
    padx=10
)


exit_button = tk.Button(
    button_frame,
    text="Exit",
    command=close_app,
    width=15,
    height=2,
    font=("Arial", 11, "bold")
)

exit_button.grid(
    row=0,
    column=2,
    padx=10
)


# ============================================================
# CLOSE WINDOW
# ============================================================

root.protocol(
    "WM_DELETE_WINDOW",
    close_app
)


# ============================================================
# START UI
# ============================================================

root.mainloop()
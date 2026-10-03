import { useEffect, useRef, useState } from "react";

function Camera() {
    const videoRef = useRef(null);
    const canvasRef = useRef(null);
    const socketRef = useRef(null);
    const streamRef = useRef(null);
    const outputUrlRef = useRef(null);

    const processingRef = useRef(false);

    const [running, setRunning] = useState(false);
    const [status, setStatus] = useState("Camera stopped");
    const [output, setOutput] = useState(null);

    const sendFrame = () => {
        const socket = socketRef.current;
        const video = videoRef.current;
        const canvas = canvasRef.current;

        if (!socket || !video || !canvas) {
            return;
        }

        if (
            processingRef.current ||
            socket.readyState !== WebSocket.OPEN ||
            video.readyState < 2
        ) {
            return;
        }

        processingRef.current = true;

        canvas.width = 640;
        canvas.height = 480;

        const context = canvas.getContext("2d");

        context.drawImage(
            video,
            0,
            0,
            640,
            480
        );

        canvas.toBlob(
            (blob) => {
                if (
                    blob &&
                    socket.readyState === WebSocket.OPEN
                ) {
                    socket.send(blob);
                } else {
                    processingRef.current = false;
                }
            },
            "image/jpeg",
            0.6
        );
    };

    const startCamera = async () => {
        try {
            setStatus("Requesting camera access...");

            const stream =
                await navigator.mediaDevices.getUserMedia({
                    video: {
                        width: 640,
                        height: 480
                    },
                    audio: false
                });

            streamRef.current = stream;

            if (videoRef.current) {
                videoRef.current.srcObject = stream;
            }

            const protocol =
                window.location.protocol === "https:"
                    ? "wss:"
                    : "ws:";

            const socket = new WebSocket(
                `${protocol}//${window.location.host}/ws`
            );

            socket.binaryType = "blob";

            socket.onopen = () => {
                console.log("WebSocket connected");

                setStatus("Detection running");
                setRunning(true);

                sendFrame();
            };

            socket.onmessage = (event) => {
                processingRef.current = false;

                if (outputUrlRef.current) {
                    URL.revokeObjectURL(
                        outputUrlRef.current
                    );
                }

                const imageUrl =
                    URL.createObjectURL(event.data);

                outputUrlRef.current = imageUrl;

                setOutput(imageUrl);

                sendFrame();
            };

            socket.onerror = (error) => {
                console.error(
                    "WebSocket error:",
                    error
                );

                setStatus("Connection error");

                processingRef.current = false;
            };

            socket.onclose = () => {
                console.log("WebSocket disconnected");

                setStatus("Connection disconnected");
                setRunning(false);

                processingRef.current = false;
            };

            socketRef.current = socket;

        } catch (error) {
            console.error(error);

            setStatus(
                `Camera error: ${error.message}`
            );
        }
    };

    const stopCamera = () => {
        if (socketRef.current) {
            socketRef.current.close();
            socketRef.current = null;
        }

        if (streamRef.current) {
            streamRef.current
                .getTracks()
                .forEach((track) => track.stop());

            streamRef.current = null;
        }

        if (videoRef.current) {
            videoRef.current.srcObject = null;
        }

        if (outputUrlRef.current) {
            URL.revokeObjectURL(
                outputUrlRef.current
            );

            outputUrlRef.current = null;
        }

        processingRef.current = false;

        setOutput(null);
        setRunning(false);
        setStatus("Camera stopped");
    };

    useEffect(() => {
        return () => {
            stopCamera();
        };
    }, []);

    return (
        <section className="detection-section">

            {/* Control Bar */}
            <div className="control-panel">

                <div className="connection-info">
                    <div
                        className={`connection-indicator ${
                            running ? "active" : ""
                        }`}
                    >
                        <span></span>
                    </div>

                    <div>
                        <strong>
                            {running
                                ? "Detection Active"
                                : "Detection Inactive"}
                        </strong>

                        <small>
                            {status}
                        </small>
                    </div>
                </div>

                <div className="controls">

                    <button
                        className="start-button"
                        onClick={startCamera}
                        disabled={running}
                    >
                        <span className="button-icon">
                            ▶
                        </span>

                        Start Camera
                    </button>

                    <button
                        className="stop-button"
                        onClick={stopCamera}
                        disabled={!running}
                    >
                        <span className="button-icon">
                            ■
                        </span>

                        Stop Camera
                    </button>

                </div>
            </div>

            {/* Video Cards */}
            <div className="video-grid">

                {/* Camera */}
                <div className="video-card">

                    <div className="card-header">

                        <div className="card-title">
                            <span className="camera-icon">
                                ●
                            </span>

                            <div>
                                <h3>Live Camera</h3>
                                <p>Camera input</p>
                            </div>
                        </div>

                        <span className="live-badge">
                            LIVE
                        </span>

                    </div>

                    <div className="video-container">

                        {!running && (
                            <div className="video-placeholder">
                                <div className="placeholder-icon">
                                    ◉
                                </div>

                                <h4>Camera is off</h4>

                                <p>
                                    Click "Start Camera"
                                    to begin detection
                                </p>
                            </div>
                        )}

                        <video
                            ref={videoRef}
                            autoPlay
                            playsInline
                            muted
                            width="640"
                            height="480"
                            className={
                                running
                                    ? "video-element"
                                    : "video-element hidden"
                            }
                        />

                        {running && (
                            <div className="video-overlay">
                                <span>
                                    ● LIVE
                                </span>
                            </div>
                        )}

                    </div>

                    <div className="card-footer">
                        <span>640 × 480</span>
                        <span>Camera Feed</span>
                    </div>

                </div>

                {/* Detection */}
                <div className="video-card">

                    <div className="card-header">

                        <div className="card-title">
                            <span className="ai-icon">
                                AI
                            </span>

                            <div>
                                <h3>Detection Output</h3>
                                <p>YOLO inference result</p>
                            </div>
                        </div>

                        {running && (
                            <span className="ai-badge">
                                AI ACTIVE
                            </span>
                        )}

                    </div>

                    <div className="video-container">

                        {!output && (
                            <div className="video-placeholder">
                                <div className="placeholder-icon">
                                    ✦
                                </div>

                                <h4>
                                    Waiting for detection
                                </h4>

                                <p>
                                    Detection output will
                                    appear here
                                </p>
                            </div>
                        )}

                        {output && (
                            <img
                                src={output}
                                alt="YOLO Detection Output"
                                className="video-element"
                            />
                        )}

                        {running && output && (
                            <div className="video-overlay detection">
                                <span>
                                    ● AI DETECTION
                                </span>
                            </div>
                        )}

                    </div>

                    <div className="card-footer">
                        <span>YOLO Detection</span>
                        <span>Real Time</span>
                    </div>

                </div>

            </div>

            <canvas
                ref={canvasRef}
                style={{ display: "none" }}
            />

        </section>
    );
}

export default Camera;

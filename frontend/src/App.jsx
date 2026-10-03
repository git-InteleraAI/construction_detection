import Camera from "./Camera";

function App() {
    return (
        <div className="app">
            <header className="topbar">
                <div className="brand">
                    <div className="brand-icon">
                        AI
                    </div>

                    <div>
                        <h1>PPE Detection</h1>
                        <span>AI-Powered Safety Monitoring</span>
                    </div>
                </div>

                <div className="system-badge">
                    <span className="status-dot"></span>
                    AI SYSTEM ONLINE
                </div>
            </header>

            <main className="main-content">
                <section className="hero">
                    <div>
                        <p className="eyebrow">
                            COMPUTER VISION • REAL TIME
                        </p>

                        <h2>
                            Personal Protective
                            <br />
                            Equipment Detection
                        </h2>

                        <p className="hero-text">
                            Monitor workplace safety using real-time
                            AI-powered object detection.
                        </p>
                    </div>
                </section>

                <Camera />
            </main>

            <footer className="footer">
                <span>PPE Detection System</span>
                <span>YOLO • WebSocket • FastAPI</span>
            </footer>
        </div>
    );
}

export default App;

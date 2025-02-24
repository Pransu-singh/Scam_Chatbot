import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
    const [message, setMessage] = useState("");
    const [response, setResponse] = useState(null);

    const sendMessage = async () => {
        if (message.trim() === "") return;
        const res = await axios.post("http://localhost:8000/check_scam", {
            message,
            user_id: "user123"
        });
        setResponse(res.data);
    };

    return (
        <div className="chat-container">
            <h1>Scam Detection Chatbot</h1>
            <div className="chat-box">
                {response && (
                    <p className={response.scam_detected ? "alert" : "safe"}>
                        {response.alert} (Confidence: {response.confidence.toFixed(2)})
                    </p>
                )}
                <input 
                    type="text" 
                    value={message} 
                    onChange={(e) => setMessage(e.target.value)} 
                    placeholder="Type a message..."
                />
                <button onClick={sendMessage}>Check</button>
            </div>
        </div>
    );
}

export default App;

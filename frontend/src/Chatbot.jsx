import React, { useState } from "react";
import axios from "axios";
import "./Chatbot.css";  // Add custom styles

const backend_url = process.env.REACT_APP_BACKEND_URL
console.log(`Backend URL : ${backend_url}`);

const Chatbot = () => {
  const [userMessage, setUserMessage] = useState("");
  const [chatMessages, setChatMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async (message) => {
    try {
      setLoading(true);
      
      // Add the user's message to the chat history
      setChatMessages([...chatMessages, { sender: "user", message }]);
      
      // Send the message to the Flask backend
      const response = await axios.post(backend_url+"/chat", {
        message,
      });
      setChatMessages([
        ...chatMessages,
        { sender: "user", message },
        { sender: "bot", message: response.data.response },
      ]);
    } catch (error) {
      console.error("Error:", error);
      setChatMessages([
        ...chatMessages,
        { sender: "user", message },
        { sender: "bot", message: "Something is wrong"},
      ]);
    } finally {
      setLoading(false);
      setUserMessage(""); // Clear input field
    }
  };

  const handleInputChange = (e) => {
    setUserMessage(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (userMessage.trim()) {
      sendMessage(userMessage);
    }
  };
  function formatResponse(response) {
    response = response.replace(/^-+\s*/, '');
    response = response.replace(/\*\*/g, "").trim();
    response = response.replace(/^.*\n/, '');
    const points = response.split('\n').filter(line => line.trim() !== "");
    
    return (
        points.map((point, index) => (
          <p key={index}>{point.trim()}</p>
        ))
      );
  }
  return (
    <div className="chatbot-container">
      <div className="chat-window">
        {chatMessages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.sender}`}>
            <div className="message-content">
              <strong>{msg.sender === "user" ? "You" : "Kepler Bot"}:</strong> {formatResponse(msg.message)}
            </div>
          </div>
        ))}
        {loading && (
          <div className="message bot">
            <div className="message-content">Bot is typing...</div>
          </div>
        )}
      </div>
      <form onSubmit={handleSubmit} className="input-form">
        <input
          type="text"
          value={userMessage}
          onChange={handleInputChange}
          placeholder="Type a message..."
          className="input-field"
        />
        <button type="submit" className="send-button">Send</button>
      </form>
    </div>
  );
};

export default Chatbot;

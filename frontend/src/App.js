import React from "react";
import Chatbot from "./Chatbot";
import Refresh from "./Refresh";
import "./App.css"; 

function App() {
  return (
    <div className="App">
      <h1 className="demoproject">AI-driven Energy Savings for RAN </h1>
      <Chatbot />
      <Refresh />
    </div>
  );
}

export default App;

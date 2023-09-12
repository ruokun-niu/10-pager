import lens from "./assets/lens.png";
import { useState } from "react";
import "./App.css";

function App() {
  const [prompt, updatePrompt] = useState(undefined);

  const sendPrompt = async (event) => {
    if (event.key !== "Enter") {
      return;
    }
    console.log('prompt', prompt)
  }

  return (
    <div className="app">
      <div className="app-container">
        <div className="spotlight__wrapper">
          <input
            type="text"
            className="spotlight__input"
            placeholder="Ask me anything..."
            onChange={(e) => updatePrompt(e.target.value)}
            onKeyDown={(e) => sendPrompt(e)}
            style={{
              backgroundImage: `url(${lens})`,
            }}
          />
          <div className="spotlight__answer">
            Dubai is a desert city and has a warm and sunny climate throughout
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
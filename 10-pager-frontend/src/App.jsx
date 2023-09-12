import lens from "./assets/lens.png";
import loadingGif from "./assets/loading.gif";
import { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [prompt, updatePrompt] = useState(undefined);
  const [loading, setLoading] = useState(false);
  const [answer, setAnswer] = useState(undefined);
  

  const sendPrompt = async (event) => {
    if (event.key !== "Enter") {
      return;
    }
    console.log('prompt', prompt)
    try {
      setLoading(true);

      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      };

      // const res = await fetch("/api/pdf/qa", requestOptions); //api/ask for testing?
      const res = await fetch('/api/ask', requestOptions); 

      if (!res.ok) {
        throw new Error("Something went wrong");
      }
      const { message } = await res.json();
      setAnswer(message);

    } catch (err) {
      console.error(err, "err");
    } finally {
      setLoading(false);
    }

  }

  useEffect(() => {
    if (prompt != null && prompt.trim() === "") {
      setAnswer(undefined);
    }
  }, [prompt]);

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
            disabled={loading}
            style={{
              backgroundImage: loading ? `url(${loadingGif})` : `url(${lens})`,
            }}
          />
          <div className="spotlight__answer">{answer && <p>{answer}</p>}</div>
        </div>
      </div>
    </div>
  );
}

export default App;
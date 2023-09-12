import lens from "./assets/lens.png";
import loadingGif from "./assets/loading.gif";
import { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [prompt, updatePrompt] = useState(undefined);
  const [loading, setLoading] = useState(false);
  const [answer, setAnswer] = useState(undefined);

  const [showModal, setShowModal] = useState(false);
  const [pdfUploaded, setPdfUploaded] = useState(false);
  const [pdfFileName, setPdfFileName] = useState("");
  
  const handlePdfUpload = (event) => {
    const file = event.target.files[0];

    if (file && file.type === "application/pdf") {
      //Calling the api to upload the pdf

      try {
        const formData = new FormData();
        formData.append("file", file);
        const requestOptions = {
          method: "POST",
          body: formData,
        };
        const res = fetch("/api/pdf/upload", requestOptions);
        if (!res.ok) {
          throw new Error("Something went wrong");
        }
      } catch (err) {
        console.error(err, "err");
      }
      

      setPdfUploaded(true);
      setPdfFileName(file.name);
      setShowModal(false); // Close the modal after successful upload

      
    } else {
      alert("Please upload a valid PDF file.");
    }
  };

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
          {!pdfUploaded ? (
            <div className="container">
              <input type="file" accept=".pdf" onChange={handlePdfUpload}/>
            </div>
          ) : (
            <>
              <p>Uploaded PDF File: {pdfFileName}</p>
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
            </>
          )}

          
        </div>
          {showModal && (
            <div className="modal">
              <div className="modal-content">
                <h2>Upload PDF</h2>
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handlePdfUpload}
                />
                <button onClick={() => setShowModal(false)}>Close</button>
              </div>
            </div>
          )}
        
      
      </div>
    </div>
  );
}

export default App;
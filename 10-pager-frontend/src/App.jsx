import lens from "./assets/lens.png";
import loadingGif from "./assets/loading.gif";
import React, { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [prompt, updatePrompt] = useState(undefined);
  const [loading, setLoading] = useState(false);
  const [answer, setAnswer] = useState(undefined);

  const [showModal, setShowModal] = useState(false);
  const [pdfUploaded, setPdfUploaded] = useState(false);
  const [pdfFileName, setPdfFileName] = useState("");

  const [apiKey, setApiKey] = useState("");
  const [endpoint, setEndpoint] = useState("");

  const [pageStage, setPageStage] = useState(1);
  
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
      
      setPageStage(2);
      setPdfUploaded(true);
      setPdfFileName(file.name);
      setShowModal(false); // Close the modal after successful uploa
    } else {
      alert("Please upload a valid PDF file.");
    }
  };


  const handleCredentialsSubmit = (event) => {
    try {
      const api_key = apiKey;
      const endpoint = endpoint;

      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ api_key, endpoint }),
      };

      const res = fetch("/api/openai/azure/creds", requestOptions);
      if (!res.ok) {
        throw new Error("Something went wrong");
      }
    } catch (err) {
      console.error(err, "err");
    }
    setPageStage(3);

  };


  const pageStageone= (
    <React.Fragment>
        <div className="container">
          <input type="file" accept=".pdf" onChange={handlePdfUpload}/>
        </div>
    </React.Fragment>
  );

  const pageStagetwo = (
    <React.Fragment>
      <p>Uploaded PDF File: {pdfFileName}</p>
        <input
          type="text"
          placeholder="API Key"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
        /> <div></div>
        <input
          type="text"
          placeholder="Endpoint"
          value={endpoint}
          onChange={(e) => setEndpoint(e.target.value)}
        />
        <button onClick={handleCredentialsSubmit}>Submit Credentials</button>
    </React.Fragment>
  ); 

  const pageStagethree = (
    <React.Fragment>
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
    </React.Fragment>
  );

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

      const res = await fetch("/api/pdf/qa", requestOptions); //api/ask for testing?
      // const res = await fetch('/api/ask', requestOptions); 

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

  let html;

  if (pageStage === 1) {
    html = pageStageone;
  } else if (pageStage === 2) {
    html = pageStagetwo;
  } else if (pageStage === 3) {
    html = pageStagethree;
  }

  return (
    <React.Fragment>
    <div className="app">
      <div className="app-container">
        <div className="spotlight__wrapper">
          {html}
        </div>
      </div>
    </div>
    </React.Fragment>
  )

  // return (
  //   <div className="app">
  //     <div className="app-container">
  //       <div className="spotlight__wrapper">
  //         {!pdfUploaded ? (
  //           <div className="container">
  //             <input type="file" accept=".pdf" onChange={handlePdfUpload}/>
  //           </div>
  //         ) : (
  //           <>
  //             <p>Uploaded PDF File: {pdfFileName}</p>
  //             <input
  //               type="text"
  //               className="spotlight__input"
  //               placeholder="Ask me anything..."
  //               onChange={(e) => updatePrompt(e.target.value)}
  //               onKeyDown={(e) => sendPrompt(e)}
  //               disabled={loading}
  //               style={{
  //                 backgroundImage: loading ? `url(${loadingGif})` : `url(${lens})`,
  //               }}
  //             />
  //             <div className="spotlight__answer">{answer && <p>{answer}</p>}</div>
  //           </>
  //         )}
  //       </div>
  //     </div>
  //   </div>
  // );
}

export default App;
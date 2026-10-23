import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import { StudioProvider } from "./studio/StudioProvider";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <StudioProvider>
      <App />
    </StudioProvider>
  </React.StrictMode>,
);

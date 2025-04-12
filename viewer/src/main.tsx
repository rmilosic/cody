import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import App from "./App.tsx"
import "@/main.css"
import { NuqsAdapter } from "nuqs/adapters/react"
createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <NuqsAdapter>
      <App />
    </NuqsAdapter>
  </StrictMode>
)

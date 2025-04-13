import BillingCodeGenerator from "./components/billing-code-generator"
import { TooltipProvider } from "./components/ui/tooltip"

function App() {
  return (
    <main className="p-8 flex flex-col gap-4">
      <TooltipProvider>
        <BillingCodeGenerator />
      </TooltipProvider>
    </main>
  )
}

export default App

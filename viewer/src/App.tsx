import { useState } from "react"
import { useEffect } from "react"
import BillingCodeGenerator from "./components/billing-code-generator"
import { FlickeringGrid } from "./components/magicui/flickering-grid"
import { TooltipProvider } from "./components/ui/tooltip"

function App() {
  const [width, setWidth] = useState(0)
  const [height, setHeight] = useState(0)

  useEffect(() => {
    setWidth(window.innerWidth)
    setHeight(window.innerHeight)
  }, [])

  return (
    <div>
      <main className="p-8 flex flex-col gap-4 relative min-h-screen items-center justify-center">
        <TooltipProvider>
          <BillingCodeGenerator />
        </TooltipProvider>

        <FlickeringGrid
          className="absolute inset-0 z-0 [mask-image:radial-gradient(450px_circle_at_center,white,transparent)] overflow-hidden"
          squareSize={4}
          gridGap={6}
          color="#60A5FA"
          maxOpacity={0.5}
          flickerChance={0.1}
          height={height}
          width={width}
        />
      </main>
    </div>
  )
}

export default App

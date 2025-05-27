import { useState, useEffect } from "react"
import { Suspense } from "react"
import PojistnaUdalostForm from "@/components/pojistna-udalost-form"
import { Toaster } from "@/components/ui/toaster"

function App() {
  const [width, setWidth] = useState(0)
  const [height, setHeight] = useState(0)

  useEffect(() => {
    setWidth(window.innerWidth)
    setHeight(window.innerHeight)
  }, [])

  return (
    <div>
      <main className="min-h-screen bg-gray-50">
      <div className="container mx-auto py-8 px-4">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Systém pro vyúčtování pojistných událostí</h1>
        <p className="text-gray-600 mb-8">
          Nástroj pro analýzu a přípravu zúčtovatelných položek z lékařských poznámek
        </p>

        <Suspense fallback={<div className="text-center py-10">Načítání aplikace...</div>}>
          <PojistnaUdalostForm />
        </Suspense>
      </div>
      <Toaster />
    </main>
    </div>
  )
}

export default App

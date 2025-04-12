import useSWR from "swr"
import { ofetch } from "ofetch"
import { Button } from "./components/ui/button"
import { useState } from "react"
import { materialLabels, vykonyLabels } from "./data/json"

const fetcher = ofetch.create({
  baseURL: "http://localhost:2024",
})

interface DataTableProps<T extends Record<string, unknown>> {
  data: T[]
  labels: Record<string, string>
}

function DataTable<T extends Record<string, unknown>>({
  data,
  labels,
}: DataTableProps<T>) {
  if (!data || data.length === 0) return null

  return (
    <div className="mt-8 overflow-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            {Object.keys(data[0]).map((key) => (
              <th
                key={key}
                scope="col"
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                {labels[key] || key}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {data.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {Object.entries(row).map(([key, value]) => (
                <td
                  key={key}
                  className="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                >
                  {String(value)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function App() {
  const [idx, setIdx] = useState(0)
  const pacient = useSWR<{
    zpravy_content: string
    dokumentace: {
      CISPAC: string
      DATUM_CAS: string
      CONTENT: string
    }[]
    material: {
      SERIAL: number
      CDOKL: number
      DATUM: string
      TYP: number
      KOD: string
      ZVL: number
      LOKALIZACE: string
      ODDELENI: number
      MNOZSTVI: number
      CENAUZIV: string
      CENA: string
      SERIALCDB: number
      CISPAC: number
    }[]
    vykony: {
      SERIAL: number
      CDOKL: number
      DATUM: string
      KOD: number
      ODBORNOST: number
      DG: string
      LOKALIZACE: string
      ODDELENI: number
      CAS: string
      MNOZSTVI: number
      BODY: string
      CENAMAT: number
      CENAUZIV: number
      CENA: string
      SERIALCDB: number
      CISPAC: number
    }[]
  }>(`/get_patient_data/${idx}`, fetcher)

  return (
    <main className="p-8 grid grid-cols-2">
      <div>
        <div className="flex gap-2 items-center">
          <Button
            size="sm"
            variant="outline"
            onClick={() => setIdx(Math.max(0, idx - 1))}
          >
            Prev
          </Button>
          <span className="text-sm tabular-nums">{idx}</span>
          <Button size="sm" variant="outline" onClick={() => setIdx(idx + 1)}>
            Next
          </Button>
        </div>
        <pre className="text-sm whitespace-pre-wrap">
          {pacient.data?.zpravy_content}
        </pre>
      </div>

      <div className="flex flex-col gap-2">
        <div>
          <h2 className="text-lg font-semibold mt-8">Výkony</h2>
          <DataTable data={pacient.data?.vykony || []} labels={vykonyLabels} />
        </div>

        <div>
          <h2 className="text-lg font-semibold mt-8">Materiál</h2>
          <DataTable
            data={pacient.data?.material || []}
            labels={materialLabels}
          />
        </div>
      </div>
    </main>
  )
}

export default App

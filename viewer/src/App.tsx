import { Button } from "./components/ui/button"
import { Fragment, useState } from "react"

import { Textarea } from "./components/ui/textarea"
import { useStream } from "@langchain/langgraph-sdk/react"
import { Component } from "react"
import BillingCodeGenerator from "./components/billing-code-generator"

interface DataTableProps<T extends Record<string, unknown>> {
  data: T[]
  labels: Record<string, string>
}

function DataTable<T extends Record<string, unknown>>({
  data,
  labels,
}: DataTableProps<T>) {
  if (!data || data.length === 0)
    return (
      <div className="border rounded-lg text-center p-4 text-muted-foreground">
        Žádné výkazy nenalezeny
      </div>
    )

  return (
    <div className="overflow-auto border rounded-lg">
      <table className="min-w-full divide-y">
        <thead>
          <tr>
            {Object.keys(data[0]).map((key) => (
              <th
                key={key}
                scope="col"
                className="px-4 py-3 text-left text-xs font-medium whitespace-nowrap tracking-wider"
              >
                {labels[key] || key}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="">
          {data.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {Object.entries(row).map(([key, value]) => (
                <td key={key} className="px-4 py-4 whitespace-nowrap text-sm">
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

class ErrorBoundary extends Component<
  { children: React.ReactNode; fallback: React.ReactNode },
  { error: Error | null }
> {
  constructor(props: { children: React.ReactNode; fallback: React.ReactNode }) {
    super(props)
    this.state = { error: null }
  }

  componentDidCatch(error: Error) {
    this.setState({ error })
  }

  render() {
    if (this.state.error) {
      return this.props.fallback
    }
    return this.props.children
  }
}

const AssumeRenderVykony = (props: {
  vykony:
    | Array<{
        code: string
        description: string
      }>
    | undefined
}) => {
  if (!props.vykony) return null
  return (
    <div className="grid grid-cols-[auto,1fr] gap-4 border rounded-lg p-4">
      {props.vykony?.map(({ code, description }, idx) => {
        return (
          <Fragment key={code + ":" + idx}>
            <div className="text-muted-foreground">{code}</div>
            <div>{description}</div>
          </Fragment>
        )
      })}
    </div>
  )
}

const GenerateNew = (props: { report: string }) => {
  const [systemPrompt, setSystemPrompt] = useState("")

  const stream = useStream<{
    report: string
    diagnosis?: {
      vykony: Array<{
        code: string
        description: string
      }>
    }
  }>({
    apiUrl: "http://localhost:2024",
    assistantId: "agent",
  })

  return (
    <div className="flex flex-col gap-4">
      <ErrorBoundary
        fallback={
          <pre>{JSON.stringify(stream.values?.diagnosis?.vykony, null, 2)}</pre>
        }
      >
        <AssumeRenderVykony vykony={stream.values?.diagnosis?.vykony} />
      </ErrorBoundary>

      <Textarea
        value={systemPrompt}
        onChange={(e) => setSystemPrompt(e.target.value)}
        placeholder="Vlastní systémový prompt..."
      />

      <Button
        disabled={stream.isLoading}
        onClick={() =>
          stream.submit(
            { report: props.report },
            {
              config: {
                configurable: { system_prompt: systemPrompt || undefined },
              },
            }
          )
        }
      >
        {stream.isLoading ? "Generuji..." : "Vygenerovat"}
      </Button>
    </div>
  )
}

function App() {
  const [idx, setIdx] = useState(0)

  return (
    <main className="p-8 flex flex-col gap-4">
      <BillingCodeGenerator />

      {/* <pre className="text-sm whitespace-pre-wrap border p-4 rounded-lg">
        {pacient.data?.zpravy_content}
      </pre> */}

      {/* <div className="grid grid-cols-2 gap-4">
        <div className="flex flex-col gap-4">
          <div className="flex flex-col gap-4">
            <h2 className="text-lg font-semibold">Výkony</h2>
            <DataTable
              data={pacient.data?.vykony || []}
              labels={vykonyLabels}
            />
          </div>

          <div className="flex flex-col gap-4">
            <h2 className="text-lg font-semibold">Materiály</h2>
            <DataTable
              data={pacient.data?.material || []}
              labels={materialLabels}
            />
          </div>
        </div>

        <div className="flex flex-col gap-4">
          <div className="flex flex-col gap-4">
            <h2 className="text-lg font-semibold">Generovat</h2>
            <GenerateNew
              key={idx}
              report={pacient.data?.zpravy_content || ""}
            />
          </div>
        </div>
      </div> */}
    </main>
  )
}

export default App

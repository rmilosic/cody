import { useEffect, useRef, useState } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import jsConfetti from "js-confetti"
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  MoreVertical,
  Trash2,
  ChevronUp,
  ChevronDown,
  Search,
  Bot,
  User,
  LoaderCircle,
} from "lucide-react"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"
import { Badge } from "@/components/ui/badge"
import useSWR from "swr"
import { fetcher } from "@/fetcher.mjs"
import { useStream } from "@langchain/langgraph-sdk/react"

type BillingCodeItem = {
  code: string
  name: string
  description: string | null
  count: number
  source: "ai" | "user"
}

export default function BillingCodeGenerator() {
  const [isOpen, setIsOpen] = useState(false)
  const [medicalReport, setMedicalReport] = useState("")
  const [selectedCodes, setSelectedCodes] = useState<BillingCodeItem[]>([])

  const [searchQuery, setSearchQuery] = useState("")
  const [randomIdx, setRandomIdx] = useState<number | null>(null)

  useSWR<{
    zpravy_content: string
    material: Record<string, unknown>[]
    vykony: Record<string, unknown>[]
  }>(randomIdx != null ? `/get_patient_data/${randomIdx}` : null, fetcher, {
    keepPreviousData: true,
    onSuccess: (data) => setMedicalReport(data.zpravy_content),
  })

  const billingCodes = useSWR<{
    result: Array<{
      code: number
      name: string
      description: string
      odbornost: string
    }>
  }>("/vykony?query=" + encodeURIComponent(searchQuery), fetcher, {
    keepPreviousData: true,
  })

  const stream = useStream<{
    report: string
    diagnosis?: { vykony: Array<{ code: string; description: string }> }
  }>({
    apiUrl: "http://localhost:2024",
    assistantId: "agent",
    onFinish: (state) => {
      setSelectedCodes((prev) => [
        ...prev,
        ...(state.values.diagnosis?.vykony.map((code) => ({
          code: code.code,
          name: code.description,
          description: code.description,
          count: 1,
          source: "ai" as const,
        })) ?? []),
      ])
    },
  })

  const handleCountChange = (code: string, newCount: number) => {
    setSelectedCodes((prev) =>
      prev.map((item) =>
        item.code === code ? { ...item, count: Math.max(1, newCount) } : item
      )
    )
  }

  const ref = useRef<any | null>(null)
  useEffect(() => {
    if (ref.current == null) ref.current = new jsConfetti()
  }, [])

  const handleGenerateCodes = () => stream.submit({ report: medicalReport })
  const handleSubmit = () => ref.current?.addConfetti()

  return (
    <>
      <div className="flex gap-4 items-center">
        <div className="font-semibold text-3xl flex-grow">Cody</div>
        <div className="flex gap-2 items-center">
          <Button
            size="sm"
            variant="outline"
            onClick={() => setRandomIdx((prev) => (prev ?? -1) + 1)}
          >
            Enter random patient
          </Button>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card className="md:col-span-1">
          <CardHeader>
            <CardTitle>Medical Report</CardTitle>
          </CardHeader>
          <CardContent>
            <Textarea
              placeholder="Enter the patient's medical report here..."
              className="min-h-[300px] font-mono [field-sizing:content]"
              value={medicalReport}
              onChange={(e) => setMedicalReport(e.target.value)}
            />
          </CardContent>
          <CardFooter>
            <Button
              onClick={handleGenerateCodes}
              disabled={!medicalReport.trim() || stream.isLoading}
              className="w-full"
            >
              {stream.isLoading ? (
                <>
                  <LoaderCircle className="mr-1 animate-spin" />
                  <span>Generating...</span>
                </>
              ) : (
                <span>Generate Billing Codes</span>
              )}
            </Button>
          </CardFooter>
        </Card>

        <Card className="md:col-span-1 grid grid-rows-[auto_1fr_auto]">
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>Billing Code Report</CardTitle>
          </CardHeader>
          <CardContent className="flex-grow flex flex-col">
            {/* {error && (
            <Alert variant="destructive" className="mb-4">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {isSubmitted && (
            <Alert className="mb-4 bg-green-50 text-green-800 border-green-200">
              <CheckCircle2 className="h-4 w-4 text-green-600" />
              <AlertDescription>
                Billing report successfully submitted!
              </AlertDescription>
            </Alert>
          )} */}

            <div className="flex-grow flex flex-col gap-4">
              {/* Searchable dropdown for adding codes */}
              <Popover open={isOpen} onOpenChange={setIsOpen}>
                <PopoverTrigger asChild>
                  <Button variant="outline" className="w-full justify-start">
                    <Search className="mr-2 h-4 w-4" />
                    Search and add billing code
                  </Button>
                </PopoverTrigger>
                <PopoverContent
                  className="p-0"
                  align="start"
                  side="bottom"
                  sideOffset={5}
                  style={{ width: "30vw", minWidth: "256px" }}
                >
                  <Command>
                    <CommandInput
                      placeholder="Search billing codes..."
                      value={searchQuery}
                      onInput={(e) => setSearchQuery(e.currentTarget.value)}
                    />
                    <CommandList>
                      <CommandEmpty>No billing code found.</CommandEmpty>
                      <CommandGroup heading="Available Billing Codes">
                        {billingCodes.data?.result
                          .slice(0, 10)
                          ?.map((codeItem) => (
                            <CommandItem
                              key={codeItem.code}
                              value={`${codeItem.code} ${codeItem.description}`}
                              onSelect={() => {
                                setSelectedCodes((prev) => [
                                  ...prev,
                                  {
                                    code: codeItem.code.toString(),
                                    name: codeItem.name,
                                    description: codeItem.description,
                                    count: 1,
                                    source: "user",
                                  },
                                ])

                                setSearchQuery("")
                              }}
                            >
                              <div className="flex flex-col gap-2">
                                <div className="font-medium text-sm">
                                  {codeItem.name}
                                </div>
                                <span className="text-xs text-muted-foreground">
                                  {codeItem.description}
                                </span>
                                <span className="font-medium text-xs">
                                  Kód: {codeItem.code}
                                </span>
                              </div>
                            </CommandItem>
                          ))}
                      </CommandGroup>
                    </CommandList>
                  </Command>
                </PopoverContent>
              </Popover>

              {selectedCodes.length > 0 ? (
                <div className="border rounded-md p-4 space-y-2">
                  <div className="grid grid-cols-[auto_1fr] gap-4 pb-2 border-b mb-2">
                    <span className="font-medium">Billing Codes</span>
                    <span className="sr-only">Actions</span>
                  </div>

                  {selectedCodes.map((codeItem, idx) => (
                    <div
                      key={codeItem.code}
                      className={`grid grid-cols-[1fr_auto_auto] gap-4 items-center pb-2 pt-2.5 border rounded-md p-3 ${
                        codeItem.source === "ai"
                          ? "bg-blue-50/30"
                          : "bg-green-50/30"
                      }`}
                    >
                      <div className="min-w-0">
                        <div className="flex items-center flex-wrap">
                          <label
                            htmlFor={`code-${codeItem.code}`}
                            className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 cursor-pointer align-baseline"
                          >
                            <span className="mr-2">
                              {codeItem.source === "ai" ? (
                                <Bot className="h-3 w-3 text-blue-600 inline-flex" />
                              ) : (
                                <User className="h-3 w-3 text-green-600 inline-flex" />
                              )}
                            </span>
                            <span>{codeItem.name}</span>
                          </label>
                        </div>
                        <p className="text-sm text-muted-foreground truncate mt-1">
                          {codeItem.description}
                        </p>
                      </div>
                      <div className="text-sm text-center">
                        {codeItem.count}
                      </div>
                      <div className="flex items-center">
                        <Button
                          variant="ghost"
                          size="icon"
                          className="h-8 w-8 text-red-500 hover:text-red-700 hover:bg-red-50"
                          onClick={() => {
                            setSelectedCodes((prev) => {
                              const newCodes = [...prev]
                              newCodes.splice(idx, 1)
                              return newCodes
                            })
                          }}
                          title="Remove code"
                        >
                          <Trash2 className="h-4 w-4" />
                          <span className="sr-only">Remove code</span>
                        </Button>
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button
                              variant="ghost"
                              size="icon"
                              className="h-8 w-8"
                            >
                              <MoreVertical className="h-4 w-4" />
                              <span className="sr-only">Adjust quantity</span>
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuItem
                              onClick={() =>
                                handleCountChange(
                                  codeItem.code,
                                  codeItem.count + 1
                                )
                              }
                            >
                              <ChevronUp className="mr-2 h-4 w-4" />
                              <span>Increase quantity</span>
                            </DropdownMenuItem>
                            <DropdownMenuItem
                              onClick={() =>
                                handleCountChange(
                                  codeItem.code,
                                  codeItem.count - 1
                                )
                              }
                              disabled={codeItem.count <= 1}
                            >
                              <ChevronDown className="mr-2 h-4 w-4" />
                              <span>Decrease quantity</span>
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 flex items-center justify-center text-muted-foreground border rounded-md flex-grow">
                  <p>
                    No codes in report yet. Generate codes from the medical
                    report or add them manually.
                  </p>
                </div>
              )}

              {selectedCodes.length > 0 && (
                <div className="flex justify-between items-center">
                  <p className="text-sm text-muted-foreground">
                    {selectedCodes.length} of {selectedCodes.length} codes
                    selected for billing
                  </p>

                  <div className="flex flex-wrap gap-2 mb-2">
                    <Badge
                      variant="outline"
                      className="bg-blue-50 text-blue-700 border-blue-200 flex items-center gap-1"
                    >
                      <Bot className="h-3 w-3" />
                      <span className="text-xs">AI suggested</span>
                    </Badge>
                    <Badge
                      variant="outline"
                      className="bg-green-50 text-green-700 border-green-200 flex items-center gap-1"
                    >
                      <User className="h-3 w-3" />
                      <span className="text-xs">Manually added</span>
                    </Badge>
                  </div>
                </div>
              )}
            </div>
          </CardContent>
          <CardFooter>
            <Button
              onClick={handleSubmit}
              disabled={selectedCodes.length === 0}
              className="w-full"
            >
              Submit Billing Report
            </Button>
          </CardFooter>
        </Card>
      </div>
    </>
  )
}

"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Loader2 } from "lucide-react"
import VysledkyAnalyzy from "./vysledky-analyzy"
// import SouhrFinalizovanychPolozek from "./souhrn-finalizovanych-polozek"
import { useToast } from "../hooks/use-toast"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { fetcher } from "@/fetcher.mjs"
import { useStream } from "@langchain/langgraph-sdk/react"

import useSWR from "swr"


// Typy pro položky
export type PolozkaVykon = {
  name: string
  code: string
  description: string
  verbatim_name: string
  prijato: boolean
  count: number // Přidáno množství pro výkony
}

export type VykonyResults = {
  results_deduped: { [code: string]: PolozkaVykon }
}

export type MaterialResults = Array<PolozkaMaterial>

export type Material= {
  name: string
  code: string
  count: number
  // jednotka: string
  verbatim_name: string
  prijato: boolean
}
export type PolozkaMaterial = {
  results: Array<Material>
}

export type MedicalText = {
  text: string,
  diag_primary: string,
  diag_others: Array<string> | null
}

export default function PojistnaUdalostForm() {
  const [lekarskePoznamky, setLekarskePoznamky] = useState("")
  const [threadId, setThreadId] = useState<string | null>(null)
  const [hlavniDiagnoza, setHlavniDiagnoza] = useState("")
  const [vedlejsiDiagnozy, setVedlejsiDiagnozy] = useState("")
  const [odbornost, setOdbornost] = useState("913")
  const [analyzuji, setAnalyzuji] = useState(false)
  const [analyzovano, setAnalyzovano] = useState(false)
  const [vykony, setVykony] = useState<PolozkaVykon[]>([])
  const [materialy, setMaterialy] = useState<PolozkaMaterial[]>([])
  const [aktivniTab, setAktivniTab] = useState("vstup")
  const { toast } = useToast()


  const getTextandDiag = useSWR<{
    results: {
      text: string,
      diag_primary: string,
      diag_others: string
    }
  }>(`/generate`, fetcher, {
    keepPreviousData: true,
    onSuccess: (data) => {
      setLekarskePoznamky(data.results.text)
      setHlavniDiagnoza(data.results.diag_primary)
      setVedlejsiDiagnozy(data.results.diag_others?.replace("; ", ",") || "")
    },
  })

  const stream = useStream<{
    materialy: MaterialResults
    vykony: VykonyResults
    // code: string
    // odbornost: string
    // hlavniDiagnoza: string
    // vedlejsiDiagnozy: string
    // diagnosis?: {
    //   vykony: Array<{
    //     code: string
    //     name: string
    //     description: string | null
    //     explanation: string
    //   }>
    // }
  }>({
    apiUrl: "http://localhost:2024",
    threadId,
    onThreadId: setThreadId,
    assistantId: "agent",
    onFinish: (state) => {
      setVykony((prev: any) => [
        ...prev,
        ...(
          Object.values(state.values.vykony.results_deduped)
            .map((code: PolozkaVykon) => ({
              code: code.code,
              name: code.name,
              verbatim_name: code.verbatim_name,
              description: code.description || null,
              count: 1,
              source: "ai" as const,
            }))
            .sort((a, b) => Number(a.code) - Number(b.code)) ?? []
        ),
      ])

      // if dict has any items 
      const materials = state.values.materialy
      if (!materials || materials.length === 0) {
        setAnalyzuji(false)
        setAnalyzovano(true)
        toast({
          title: "Analýza dokončena",
          description: "Text byl úspěšně analyzován, ale nebyly nalezeny žádné položky.",
        })
        return
      }
      setMaterialy((prev: any) => [
        ...prev,
        ...(
          materials.flatMap(material => material.results.map(item => ({
            code: (item as any).code,
            name: (item as any).name,
            count: 1,
            verbatim_name: (item as any).verbatim_name,
            prijato: true,
            source: "ai" as const,
          })))
        ),
      ])



      setAnalyzuji(false)
      toast({
        title: "Analýza dokončena",
        description: "Text byl úspěšně analyzován.",
      })
    },
  })

  const analyzujText = async () => {
    if (!odbornost.trim()) {
      toast({
        title: "Chybí odbornost",
        description: "Prosím, zadejte 3-písmenný kód odbornosti organizace.",
        variant: "destructive",
      })
      return
    }

    if (odbornost.length !== 3) {
      toast({
        title: "Neplatná odbornost",
        description: "Odbornost musí být přesně 3 písmena.",
        variant: "destructive",
      })
      return
    }

    if (!lekarskePoznamky.trim()) {
      toast({
        title: "Chybí text poznámek",
        description: "Prosím, vložte lékařské poznámky pro analýzu.",
        variant: "destructive",
      })
      return
    }

    if (!hlavniDiagnoza.trim()) {
      toast({
        title: "Chybí hlavní diagnóza",
        description: "Prosím, zadejte hlavní diagnózu MKN-10.",
        variant: "destructive",
      })
      return
    }
    setAnalyzuji(true)


    // setSelectedCodes((prev) => prev.filter(({ source }) => source !== "ai"))
    setThreadId(null)
    stream.submit({ text: lekarskePoznamky, odbornost: odbornost })
    // await new Promise((resolve) => setTimeout(resolve, 3000))

    // Simulované výsledky analýzy
    // const simulovaneVykony: PolozkaVykon[] = [
    //   {
    //     id: "v1",
    //     name: "Vyšetření pacienta praktickým lékařem",
    //     code: "01021",
    //     zdrojovyText: "Pacient přišel na kontrolu k praktickému lékaři",
    //     prijato: false,
    //     count: 1,
    //   },
    //   {
    //     id: "v2",
    //     name: "Odběr krve ze žíly u dospělého",
    //     code: "09119",
    //     zdrojovyText: "Byl proveden odběr krve pro biochemické vyšetření",
    //     prijato: false,
    //     count: 1,
    //   },
    //   {
    //     id: "v3",
    //     name: "EKG vyšetření",
    //     code: "09127",
    //     zdrojovyText: "Provedeno EKG vyšetření s normálním nálezem",
    //     prijato: false,
    //     count: 1,
    //   },
    // ]

    // const simulovaneMaterialy: PolozkaMaterial[] = [
    //   {
    //     id: "m1",
    //     name: "Injekční stříkačka",
    //     code: "M0001",
    //     count: 1,
    //     jednotka: "ks",
    //     zdrojovyText: "Použita injekční stříkačka pro odběr krve",
    //     prijato: false,
    //   },
    //   {
    //     id: "m2",
    //     name: "Obvazový materiál",
    //     code: "M0023",
    //     count: 2,
    //     jednotka: "ks",
    //     zdrojovyText: "Aplikován obvazový materiál na ránu",
    //     prijato: false,
    //   },
    // ]

    // setVykony(simulovaneVykony)
    // setMaterialy(simulovaneMaterialy)
    // setAnalyzuji(false)
    // setAnalyzovano(true)
    // setAktivniTab("vysledky")


  }

  const resetujFormular = () => {
    setLekarskePoznamky("")
    setHlavniDiagnoza("")
    setVedlejsiDiagnozy("")
    setOdbornost("")
    setVykony([])
    setMaterialy([])
    setAnalyzovano(false)
    setAktivniTab("vstup")
  }

  const prijmiPolozku = (typ: "vykon" | "material", id: string) => {
    if (typ === "vykon") {
      setVykony(vykony.map((v) => (v.code === id ? { ...v, prijato: true } : v)))
    } else {
      setMaterialy(materialy.map((m) => (m.code === id ? { ...m, prijato: true } : m)))
    }
  }

  const odmitnoutPolozku = (typ: "vykon" | "material", id: string) => {
    if (typ === "vykon") {
      setVykony(vykony.map((v) => (v.code === id ? { ...v, prijato: false } : v)))
    } else {
      setMaterialy(materialy.map((m) => (m.code === id ? { ...m, prijato: false } : m)))
    }
  }

  const upravPolozku = (typ: "vykon" | "material", id: string, data: Partial<PolozkaVykon | PolozkaMaterial>) => {
    if (typ === "vykon") {
      setVykony(vykony.map((v) => (v.code === id ? { ...v, ...data } : v)))
    } else {
      setMaterialy(materialy.map((m) => (m.code === id ? { ...m, ...data } : m)))
    }
  }

  const pridejNovouPolozku = (
    typ: "vykon" | "material",
    polozka: Omit<PolozkaVykon | PolozkaMaterial, "id" | "prijato">,
  ) => {
    const id = `${typ}-${Date.now()}`

    if (typ === "vykon") {
      const novaPolozka = {
        ...(polozka as Omit<PolozkaVykon, "id" | "prijato">),
        id,
        prijato: true,
        count: (polozka as any).mnozstvi || 1, // Zajistíme, že množství bude vždy definováno
      }
      setVykony([...vykony, novaPolozka])
    } else {
      const novaPolozka = {
        ...(polozka as Omit<PolozkaMaterial, "id" | "prijato">),
        id,
        prijato: true,
      }
      setMaterialy([...materialy, novaPolozka])
    }
  }

  const zvyrazniZdrojovyText = (text: string) => {
    if (!text || !lekarskePoznamky) return lekarskePoznamky

    let zvyraznenyText = lekarskePoznamky

    // Pokud zdrojový text existuje v lékařských poznámkách, obalíme ho span tagem pro zvýraznění
    if (lekarskePoznamky.includes(text)) {
      zvyraznenyText = lekarskePoznamky.replace(
        new RegExp(text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "g"),
        `<mark class="bg-yellow-100 px-0.5 rounded">${text}</mark>`,
      )
    }

    return zvyraznenyText
  }

  return (
    <Card className="bg-white shadow-md">
      <CardContent className="p-6">
        <Tabs value={aktivniTab} onValueChange={setAktivniTab}>
          <TabsList className="mb-6">
            <TabsTrigger value="vstup">Vstupní data</TabsTrigger>
            {/* <TabsTrigger value="vysledky" disabled={!analyzovano}>
              Výsledky analýzy
            </TabsTrigger>
            <TabsTrigger value="souhrn" disabled={!analyzovano}>
              Souhrn položek
            </TabsTrigger> */}
          </TabsList>

          <TabsContent value="vstup">
            <div className="space-y-4">
              <div>
                <h2 className="text-xl font-semibold mb-2">Lékařské poznámky</h2>
                <p className="text-gray-600 mb-4">
                  Vložte nebo napište lékařské poznámky pro analýzu zúčtovatelných položek
                </p>
                <Textarea
                  placeholder="Vložte text lékařských poznámek zde..."
                  className="min-h-[200px]"
                  value={lekarskePoznamky}
                  onChange={(e) => setLekarskePoznamky(e.target.value)}
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="odbornost">Odbornost organizace *</Label>
                  <Input
                    id="odbornost"
                    placeholder="např. PRA"
                    value={odbornost}
                    onChange={(e) => setOdbornost(e.target.value.toUpperCase())}
                    maxLength={3}
                    className="mt-1"
                  />
                  <p className="text-xs text-gray-500 mt-1">3-písmenný kód odbornosti</p>
                </div>

                <div>
                  <Label htmlFor="hlavni-diagnoza">Hlavní diagnóza MKN-10 *</Label>
                  <Input
                    id="hlavni-diagnoza"
                    placeholder="např. J06.9"
                    value={hlavniDiagnoza}
                    onChange={(e) => setHlavniDiagnoza(e.target.value)}
                    className="mt-1"
                  />
                  <p className="text-xs text-gray-500 mt-1">Zadejte kód hlavní diagnózy podle MKN-10</p>
                </div>

                <div>
                  <Label htmlFor="vedlejsi-diagnozy">Vedlejší diagnózy MKN-10</Label>
                  <Input
                    id="vedlejsi-diagnozy"
                    placeholder="např. Z87.891, I10"
                    value={vedlejsiDiagnozy}
                    onChange={(e) => setVedlejsiDiagnozy(e.target.value)}
                    className="mt-1"
                  />
                  <p className="text-xs text-gray-500 mt-1">Oddělte více diagnóz čárkou</p>
                </div>
              </div>

              <div className="flex justify-end space-x-2">
                {analyzovano && (
                  <Button variant="outline" onClick={resetujFormular}>
                    Nová analýza
                  </Button>
                )}
                <Button onClick={analyzujText} disabled={analyzuji}>
                  {analyzuji ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Analyzuji...
                    </>
                  ) : (
                    "Analyzovat text"
                  )}
                </Button>
              </div>
            </div>

            <VysledkyAnalyzy
              vykony={vykony}
              materialy={materialy}
              prijmiPolozku={prijmiPolozku}
              odmitnoutPolozku={odmitnoutPolozku}
              upravPolozku={upravPolozku}
              pridejNovouPolozku={pridejNovouPolozku}
            />
          </TabsContent>

          {/* <TabsContent value="vysledky">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="space-y-4">
                <h2 className="text-xl font-semibold">Vstupní data</h2>
                <Card className="bg-gray-50">
                  <CardContent className="p-4">
                    <div
                      className="whitespace-pre-wrap text-sm p-4 bg-white border rounded-md overflow-auto max-h-[500px]"
                      dangerouslySetInnerHTML={{
                        __html:
                          zvyrazniZdrojovyText(
                            [...vykony, ...materialy]
                              .filter((item) => item.zdrojovyText)
                              .map((item) => item.zdrojovyText)
                              .join("|"),
                          ) || "Žádná vstupní data",
                      }}
                    />
                  </CardContent>
                </Card>
              </div>
              <div>
                <VysledkyAnalyzy
                  vykony={vykony}
                  materialy={materialy}
                  odbornost={odbornost}
                  hlavniDiagnoza={hlavniDiagnoza}
                  vedlejsiDiagnozy={vedlejsiDiagnozy}
                  prijmiPolozku={prijmiPolozku}
                  odmitnoutPolozku={odmitnoutPolozku}
                  upravPolozku={upravPolozku}
                  pridejNovouPolozku={pridejNovouPolozku}
                />
              </div>
            </div>
          </TabsContent>

          <TabsContent value="souhrn">
            <SouhrFinalizovanychPolozek
              vykony={vykony.filter((v) => v.prijato)}
              materialy={materialy.filter((m) => m.prijato)}
              odbornost={odbornost}
              hlavniDiagnoza={hlavniDiagnoza}
              vedlejsiDiagnozy={vedlejsiDiagnozy}
            />
          </TabsContent> */}
        </Tabs>
      </CardContent>
    </Card>
  )
}

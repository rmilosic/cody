"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
// Importujeme další ikony
import { Check, X, Edit, Plus, Minus } from "lucide-react"
import type { PolozkaVykon, PolozkaMaterial } from "./pojistna-udalost-form"

interface VysledkyAnalyzyProps {
  vykony: PolozkaVykon[]
  materialy: PolozkaMaterial[]
  prijmiPolozku: (typ: "vykon" | "material", id: string) => void
  odmitnoutPolozku: (typ: "vykon" | "material", id: string) => void
  upravPolozku: (typ: "vykon" | "material", id: string, data: Partial<PolozkaVykon | PolozkaMaterial>) => void
  pridejNovouPolozku: (
    typ: "vykon" | "material",
    polozka: Omit<PolozkaVykon | PolozkaMaterial, "id" | "prijato">,
  ) => void
}

export default function VysledkyAnalyzy({
  vykony,
  materialy,
  prijmiPolozku,
  odmitnoutPolozku,
  upravPolozku,
  pridejNovouPolozku,
}: VysledkyAnalyzyProps) {
  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-xl font-semibold">Výsledky analýzy</h2>
        <p className="text-gray-600">Systém identifikoval následující zúčtovatelné položky z lékařských poznámek.</p>
      </div>

      

      {/* Sekce výkonů */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-medium">Výkony ({vykony.length})</h3>
          <span className="text-sm text-gray-500">
            Přijato: {vykony.filter((v) => v.prijato).length} z {vykony.length}
          </span>
        </div>

        {vykony.length > 0 ? (
          <div className="space-y-3">
            {vykony.map((vykon) => (
              <PolozkaVykonuKarta
                key={vykon.id}
                vykon={vykon}
                prijmiPolozku={() => prijmiPolozku("vykon", vykon.id)}
                odmitnoutPolozku={() => odmitnoutPolozku("vykon", vykon.id)}
                upravPolozku={(data) => upravPolozku("vykon", vykon.id, data)}
              />
            ))}
            <PridatNovyVykonDialog pridejVykon={(vykon) => pridejNovouPolozku("vykon", vykon)} />
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500 bg-gray-50 rounded-lg border-2 border-dashed">
            Nebyly nalezeny žádné výkony
          </div>
        )}
      </div>

      {/* Sekce materiálů */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-medium">Materiály ({materialy.length})</h3>
          <span className="text-sm text-gray-500">
            Přijato: {materialy.filter((m) => m.prijato).length} z {materialy.length}
          </span>
        </div>

        {materialy.length > 0 ? (
          <div className="space-y-3">
            {materialy.map((material) => (
              <PolozkaMaterialuKarta
                key={material.id}
                material={material}
                prijmiPolozku={() => prijmiPolozku("material", material.id)}
                odmitnoutPolozku={() => odmitnoutPolozku("material", material.id)}
                upravPolozku={(data) => upravPolozku("material", material.id, data)}
              />
            ))}
            <PridatNovyMaterialDialog pridejMaterial={(material) => pridejNovouPolozku("material", material)} />
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500 bg-gray-50 rounded-lg border-2 border-dashed">
            Nebyly nalezeny žádné materiály
          </div>
        )}
      </div>
    </div>
  )
}

interface PolozkaVykonuKartaProps {
  vykon: PolozkaVykon
  prijmiPolozku: () => void
  odmitnoutPolozku: () => void
  upravPolozku: (data: Partial<PolozkaVykon>) => void
}

// Upravíme komponentu PolozkaVykonuKarta
function PolozkaVykonuKarta({ vykon, prijmiPolozku, odmitnoutPolozku, upravPolozku }: PolozkaVykonuKartaProps) {
  const [isEditing, setIsEditing] = useState(false)
  const [editedNazev, setEditedNazev] = useState(vykon.nazev)
  const [editedKod, setEditedKod] = useState(vykon.kod)
  const [editedMnozstvi, setEditedMnozstvi] = useState(vykon.mnozstvi.toString())

  const ulozitZmeny = () => {
    upravPolozku({
      nazev: editedNazev,
      kod: editedKod,
      mnozstvi: Number.parseInt(editedMnozstvi) || 1,
    })
    setIsEditing(false)
  }

  const zvysitMnozstvi = () => {
    upravPolozku({
      mnozstvi: vykon.mnozstvi + 1,
    })
  }

  const snizitMnozstvi = () => {
    if (vykon.mnozstvi > 1) {
      upravPolozku({
        mnozstvi: vykon.mnozstvi - 1,
      })
    }
  }

  return (
    <Card className={`border-l-4 ${vykon.prijato ? "border-l-green-500" : "border-l-gray-300"}`}>
      <CardContent className="p-4">
        <div className="flex justify-between items-start">
          <div className="flex-1">
            {isEditing ? (
              <div className="space-y-3">
                <div>
                  <Label htmlFor={`nazev-${vykon.id}`}>Název výkonu</Label>
                  <Input
                    id={`nazev-${vykon.id}`}
                    value={editedNazev}
                    onChange={(e) => setEditedNazev(e.target.value)}
                  />
                </div>
                <div>
                  <Label htmlFor={`kod-${vykon.id}`}>Kód výkonu</Label>
                  <Input id={`kod-${vykon.id}`} value={editedKod} onChange={(e) => setEditedKod(e.target.value)} />
                </div>
                <div>
                  <Label htmlFor={`mnozstvi-${vykon.id}`}>Množství</Label>
                  <Input
                    id={`mnozstvi-${vykon.id}`}
                    type="number"
                    min="1"
                    value={editedMnozstvi}
                    onChange={(e) => setEditedMnozstvi(e.target.value)}
                  />
                </div>
                <div className="flex space-x-2">
                  <Button size="sm" onClick={ulozitZmeny}>
                    Uložit
                  </Button>
                  <Button size="sm" variant="outline" onClick={() => setIsEditing(false)}>
                    Zrušit
                  </Button>
                </div>
              </div>
            ) : (
              <>
                <div className="flex items-center space-x-2">
                  <h3 className="font-medium">{vykon.nazev}</h3>
                  <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">Kód: {vykon.kod}</span>
                  <div className="flex items-center space-x-1 bg-gray-100 rounded px-1">
                    <Button
                      size="sm"
                      variant="ghost"
                      onClick={snizitMnozstvi}
                      disabled={vykon.mnozstvi <= 1}
                      className="h-6 w-6 p-0"
                    >
                      <Minus className="h-3 w-3" />
                      <span className="sr-only">Snížit množství</span>
                    </Button>
                    <span className="text-xs font-medium">{vykon.mnozstvi}</span>
                    <Button size="sm" variant="ghost" onClick={zvysitMnozstvi} className="h-6 w-6 p-0">
                      <Plus className="h-3 w-3" />
                      <span className="sr-only">Zvýšit množství</span>
                    </Button>
                  </div>
                </div>
                <p className="text-sm text-gray-600 mt-1">
                  <span className="font-medium">Zdroj:</span>{" "}
                  <span className="bg-yellow-100 px-1 py-0.5 rounded">{vykon.zdrojovyText}</span>
                </p>
              </>
            )}
          </div>

          {!isEditing && (
            <div className="flex space-x-1">
              <Button size="sm" variant="ghost" onClick={() => setIsEditing(true)} className="h-8 w-8 p-0">
                <Edit className="h-4 w-4" />
                <span className="sr-only">Upravit</span>
              </Button>

              {vykon.prijato ? (
                <Button
                  size="sm"
                  variant="ghost"
                  onClick={odmitnoutPolozku}
                  className="h-8 w-8 p-0 text-red-500 hover:text-red-700"
                >
                  <X className="h-4 w-4" />
                  <span className="sr-only">Odmítnout</span>
                </Button>
              ) : (
                <Button
                  size="sm"
                  variant="ghost"
                  onClick={prijmiPolozku}
                  className="h-8 w-8 p-0 text-green-500 hover:text-green-700"
                >
                  <Check className="h-4 w-4" />
                  <span className="sr-only">Přijmout</span>
                </Button>
              )}
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}

interface PolozkaMaterialuKartaProps {
  material: PolozkaMaterial
  prijmiPolozku: () => void
  odmitnoutPolozku: () => void
  upravPolozku: (data: Partial<PolozkaMaterial>) => void
}

// Upravíme komponentu PolozkaMaterialuKarta
function PolozkaMaterialuKarta({
  material,
  prijmiPolozku,
  odmitnoutPolozku,
  upravPolozku,
}: PolozkaMaterialuKartaProps) {
  const [isEditing, setIsEditing] = useState(false)
  const [editedNazev, setEditedNazev] = useState(material.nazev)
  const [editedKod, setEditedKod] = useState(material.kod)
  const [editedMnozstvi, setEditedMnozstvi] = useState(material.mnozstvi.toString())
  const [editedJednotka, setEditedJednotka] = useState(material.jednotka)

  const ulozitZmeny = () => {
    upravPolozku({
      nazev: editedNazev,
      kod: editedKod,
      mnozstvi: Number.parseInt(editedMnozstvi) || 1,
      jednotka: editedJednotka,
    })
    setIsEditing(false)
  }

  const zvysitMnozstvi = () => {
    upravPolozku({
      mnozstvi: material.mnozstvi + 1,
    })
  }

  const snizitMnozstvi = () => {
    if (material.mnozstvi > 1) {
      upravPolozku({
        mnozstvi: material.mnozstvi - 1,
      })
    }
  }

  return (
    <Card className={`border-l-4 ${material.prijato ? "border-l-green-500" : "border-l-gray-300"}`}>
      <CardContent className="p-4">
        <div className="flex justify-between items-start">
          <div className="flex-1">
            {isEditing ? (
              <div className="space-y-3">
                <div>
                  <Label htmlFor={`nazev-${material.id}`}>Název materiálu</Label>
                  <Input
                    id={`nazev-${material.id}`}
                    value={editedNazev}
                    onChange={(e) => setEditedNazev(e.target.value)}
                  />
                </div>
                <div>
                  <Label htmlFor={`kod-${material.id}`}>Kód materiálu</Label>
                  <Input id={`kod-${material.id}`} value={editedKod} onChange={(e) => setEditedKod(e.target.value)} />
                </div>
                <div className="flex space-x-2">
                  <div className="w-1/2">
                    <Label htmlFor={`mnozstvi-${material.id}`}>Množství</Label>
                    <Input
                      id={`mnozstvi-${material.id}`}
                      type="number"
                      min="1"
                      value={editedMnozstvi}
                      onChange={(e) => setEditedMnozstvi(e.target.value)}
                    />
                  </div>
                  <div className="w-1/2">
                    <Label htmlFor={`jednotka-${material.id}`}>Jednotka</Label>
                    <Input
                      id={`jednotka-${material.id}`}
                      value={editedJednotka}
                      onChange={(e) => setEditedJednotka(e.target.value)}
                    />
                  </div>
                </div>
                <div className="flex space-x-2">
                  <Button size="sm" onClick={ulozitZmeny}>
                    Uložit
                  </Button>
                  <Button size="sm" variant="outline" onClick={() => setIsEditing(false)}>
                    Zrušit
                  </Button>
                </div>
              </div>
            ) : (
              <>
                <div className="flex items-center space-x-2">
                  <h3 className="font-medium">{material.nazev}</h3>
                  <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">Kód: {material.kod}</span>
                  <div className="flex items-center space-x-1 bg-gray-100 rounded px-1">
                    <Button
                      size="sm"
                      variant="ghost"
                      onClick={snizitMnozstvi}
                      disabled={material.mnozstvi <= 1}
                      className="h-6 w-6 p-0"
                    >
                      <Minus className="h-3 w-3" />
                      <span className="sr-only">Snížit množství</span>
                    </Button>
                    <span className="text-xs font-medium">
                      {material.mnozstvi} {material.jednotka}
                    </span>
                    <Button size="sm" variant="ghost" onClick={zvysitMnozstvi} className="h-6 w-6 p-0">
                      <Plus className="h-3 w-3" />
                      <span className="sr-only">Zvýšit množství</span>
                    </Button>
                  </div>
                </div>
                <p className="text-sm text-gray-600 mt-1">
                  <span className="font-medium">Zdroj:</span>{" "}
                  <span className="bg-yellow-100 px-1 py-0.5 rounded">{material.zdrojovyText}</span>
                </p>
              </>
            )}
          </div>

          {!isEditing && (
            <div className="flex space-x-1">
              <Button size="sm" variant="ghost" onClick={() => setIsEditing(true)} className="h-8 w-8 p-0">
                <Edit className="h-4 w-4" />
                <span className="sr-only">Upravit</span>
              </Button>

              {material.prijato ? (
                <Button
                  size="sm"
                  variant="ghost"
                  onClick={odmitnoutPolozku}
                  className="h-8 w-8 p-0 text-red-500 hover:text-red-700"
                >
                  <X className="h-4 w-4" />
                  <span className="sr-only">Odmítnout</span>
                </Button>
              ) : (
                <Button
                  size="sm"
                  variant="ghost"
                  onClick={prijmiPolozku}
                  className="h-8 w-8 p-0 text-green-500 hover:text-green-700"
                >
                  <Check className="h-4 w-4" />
                  <span className="sr-only">Přijmout</span>
                </Button>
              )}
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}

// Upravíme dialog pro přidání nového výkonu
function PridatNovyVykonDialog({
  pridejVykon,
}: { pridejVykon: (vykon: Omit<PolozkaVykon, "id" | "prijato">) => void }) {
  const [open, setOpen] = useState(false)
  const [nazev, setNazev] = useState("")
  const [kod, setKod] = useState("")
  const [mnozstvi, setMnozstvi] = useState("1") // Přidáno množství
  const [zdrojovyText, setZdrojovyText] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    pridejVykon({
      nazev,
      kod,
      zdrojovyText,
      mnozstvi: Number.parseInt(mnozstvi) || 1, // Přidáno množství
    })
    setOpen(false)
    resetForm()
  }

  const resetForm = () => {
    setNazev("")
    setKod("")
    setMnozstvi("1") // Resetujeme množství
    setZdrojovyText("")
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" className="w-full">
          <Plus className="h-4 w-4 mr-2" />
          Přidat nový výkon
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Přidat nový výkon</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Label htmlFor="nazev">Název výkonu</Label>
            <Input id="nazev" value={nazev} onChange={(e) => setNazev(e.target.value)} required />
          </div>
          <div>
            <Label htmlFor="kod">Kód výkonu</Label>
            <Input id="kod" value={kod} onChange={(e) => setKod(e.target.value)} required />
          </div>
          <div>
            <Label htmlFor="mnozstvi">Množství</Label>
            <Input
              id="mnozstvi"
              type="number"
              min="1"
              value={mnozstvi}
              onChange={(e) => setMnozstvi(e.target.value)}
              required
            />
          </div>
          <div>
            <Label htmlFor="zdrojovyText">Zdrojový text (volitelné)</Label>
            <Textarea
              id="zdrojovyText"
              value={zdrojovyText}
              onChange={(e) => setZdrojovyText(e.target.value)}
              placeholder="Část textu, která souvisí s tímto výkonem"
            />
          </div>
          <div className="flex justify-end space-x-2">
            <Button type="button" variant="outline" onClick={() => setOpen(false)}>
              Zrušit
            </Button>
            <Button type="submit">Přidat výkon</Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  )
}

function PridatNovyMaterialDialog({
  pridejMaterial,
}: { pridejMaterial: (material: Omit<PolozkaMaterial, "id" | "prijato">) => void }) {
  const [open, setOpen] = useState(false)
  const [nazev, setNazev] = useState("")
  const [kod, setKod] = useState("")
  const [mnozstvi, setMnozstvi] = useState("1")
  const [jednotka, setJednotka] = useState("ks")
  const [zdrojovyText, setZdrojovyText] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    pridejMaterial({
      nazev,
      kod,
      mnozstvi: Number.parseInt(mnozstvi) || 1,
      jednotka,
      zdrojovyText,
    })
    setOpen(false)
    resetForm()
  }

  const resetForm = () => {
    setNazev("")
    setKod("")
    setMnozstvi("1")
    setJednotka("ks")
    setZdrojovyText("")
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" className="w-full">
          <Plus className="h-4 w-4 mr-2" />
          Přidat nový materiál
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Přidat nový materiál</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Label htmlFor="nazev">Název materiálu</Label>
            <Input id="nazev" value={nazev} onChange={(e) => setNazev(e.target.value)} required />
          </div>
          <div>
            <Label htmlFor="kod">Kód materiálu</Label>
            <Input id="kod" value={kod} onChange={(e) => setKod(e.target.value)} required />
          </div>
          <div className="flex space-x-2">
            <div className="w-1/2">
              <Label htmlFor="mnozstvi">Množství</Label>
              <Input
                id="mnozstvi"
                type="number"
                min="1"
                value={mnozstvi}
                onChange={(e) => setMnozstvi(e.target.value)}
                required
              />
            </div>
            <div className="w-1/2">
              <Label htmlFor="jednotka">Jednotka</Label>
              <Input id="jednotka" value={jednotka} onChange={(e) => setJednotka(e.target.value)} required />
            </div>
          </div>
          <div>
            <Label htmlFor="zdrojovyText">Zdrojový text (volitelné)</Label>
            <Textarea
              id="zdrojovyText"
              value={zdrojovyText}
              onChange={(e) => setZdrojovyText(e.target.value)}
              placeholder="Část textu, která souvisí s tímto materiálem"
            />
          </div>
          <div className="flex justify-end space-x-2">
            <Button type="button" variant="outline" onClick={() => setOpen(false)}>
              Zrušit
            </Button>
            <Button type="submit">Přidat materiál</Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  )
}

import { Textarea } from "@/components/ui/textarea"

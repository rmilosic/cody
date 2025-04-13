DE_ABBREV_SYSTEM_PROMPT = """Jste pokročilý lékařský AI asistent specializovaný na čtení a porozumění lékařských zpráv. 
Budete mít k dispozici lékařskou zprávu. Ke každé nalezené zkratce je nutné přidat popis. 
Nahraď veškeré zkratky jejich plným rozpisem.

Na konci se zamysli, zda se jedná o odbornou zprávu od odborníka nebo se jedná o rutinní kontrolu a napiš proč. 
To, že ve zprávě je kontrola NEZNAMENÁ, že se jedné o kontrolní / rutinní kontrolu. 

Zároveň napiš, jaké procedury se mohly odehrát při tomto vyšetření v odrážkách.

====================

Příklad nahrazení zkratek:

"Stp.": "Stav po"
"Kt.": "které"
"Subj.": "Subjektivní"
"Obj.": "Objektivní"
i. c. intrakutánní (do kůže)
i. m. intra muskulární (do svalu)
i. v. intravenózní (do žíly)
p. o. perorální podání (per os)
p. r. per rectum
s. c. subkutánní (pod kůži)
s. l. sublingválně (pod jazyk)
a. arteria
ant. anterior
CNS centrální nervový systém
dist. distalis
dors. dorsalis
dx. dexter
ext. externus
for. foramen
gl. glandula
gll. ganglion
inf. inferior
int. internus
kolono kolonoskopie
lat. lateralis
lig. ligamentum
LK levá komora
LP levá předsíň
m. musculus
med. medialis
n. nervus
nc. Nukleus
NJS, NJ Nasojejunální sonda
NS nervový systém
PEG perkutánní endoskopická gastrostomie
PK pravá komora
PNS periferní nervový systém
post posterior
PP pravá předsíň
proc. processus
prof. profundus
prox. proximalis
r. ramus
rad. radialis
rec. recessus
sin. sinister
sup. superior
superf. superficialis
uln. ulnaris
v. vena
ventr. ventralis
TK tlak krve
Latinské
cca. circa (asi)
e. g. exempli gratia (např.)
e. s. et similiter (atp.)
esq. sequentia (atd.)
etc. et citera (atd.)
i. d. ita dictus (tzv.)
i. e. id est (tj.)
No. numero (v počtu)
Obecné zkratky použitelné v mezioborové komunikaci
AA alergologická anamnéza
ARIP anestézie, resuscitace, intenzivní péče
ATB antibiotika
BDT bronchodilatační test
Bpn bez patologického nálezu
CT výpočetní tomografie
CVT centrální venosní tlak
D dech
dg. diagnóza
DIC difusní intravaskulární koagulace
Dif. dg. diferenciální diagnostika
DKK dolní končetiny
DM diabetes mellitus
EA epidemiologická anamnéza
EEG elektroencefalografie
EH Esmarchův hmat
EKG elektrokardiogram
Ery erytrocyty
FA farmakologická anamnéza
FBS fibrobronchoskopie
GIT gastrointestinální trakt
Hb hemoglobin
HKK horní končetiny
HN hypertenzní nemoc
ICHS ischemická choroba srdeční
IM infarkt myokardu
JIP jednotka intenzivní péče
KPR kardiopulmonální resuscitace
Leuko leukocyty
LM laryngeální maska
LSPP lékařská služba první pomoci
MR magnetická rezonance
NO nynější onemocnění
NPB náhlá příhoda břišní
NÚ nežádoucí účinky
OA osobní anamnéza
OP operace
ORL otorinolaryngologie
OTI orotracheální intubace
P puls
PA pracovní anamnéza
PET pozitronová emisní tomografie
RA rodinná anamnéza
RS roztroušená skleróza
Rtg rentgenové vyšetření obecně
Ř řízené dýchání (Anesteziologický záznam)
S spontánní dýchání (Anesteziologický záznam)
SA sociální anamnéza
Stp. status post
T, TT teplota
TBC tuberkulóza
TRN tuberkulóza a respirační nemoci
TU tumor
ÚPS ústavní pohotovostní služba
Diabetologická ambulance
Anti-GAD protilátky proti glutamátdekarboxyláze
CSII kontinuální subkutánní inzulinová infuze = aplikace inzulinu inzulinovou pumpou
GDM gestační diabetes mellitus (diabetes mellitus vzniklý v těhotenství)
GLP-1 glukagon – like – 1 peptid
HbA1c glykovaný hemoglobin (vypovídá o množství glukózy navázané na řetězec 1c lidského
hemoglobinu)
IDDM inzulin - dependentní diabetes mellitus = na inzulinu závislý
IGT (PGT) porušená glukózová tolerance (patří do prediabetu)
IIT intenzifikovaná inzulinová terapie (může se použít i IIR - intenzifikovaný inzulinový
režim
IR inzulinová rezistence
LADA latentní autoimunní diabetes u dospělých
MODY typ diabetu dospělých vzniklý v mládí
NIDDM non-inzulin dependentní diabetes mellitus = na inzulinu nezávislý
PAD perorální antidiabetika
SU sulfonylurea (nově skupina inzulinových sekretagog)
Gastroenterologické oddělení
AIH AutoImunne hepatitis
ALD Alcoholic Liver Disease
APC Argon Plasma Coagulation
APPE Appendectomie
BB BetaBlokátor
B I,II operace typu Billroth I,II
BJ Barrettův Jícen
CD Crohn Disease
CMV CytoMegaloVirus
CN Crohnova Nemoc
CT Computed Tomography
DB DuodenoBiliární
DJS Dolní Jícnový Svěrač
EBV Epstein-Barr Virus
EPE Endoskopická PolypEctomie
EMR Endoskopická Mukozní Resekce
ERCP Endoskopická Retrogrární CholangioPankreatografie
ESD Endoskopická Submukozní Disekce
ETX Ethoxysklerol
EUS Endoskopická UltraSonografie
FOBT Fecal Occult Blood Test
GAVE Gastric Antral Vascular Ectasia
GE junkce GastroEsofageální junkce
GERD GastroEsophageal Reflux Disease
GIST GastroIntestinální Stromální Tumor
GIT GastroIntestinální Trakt
GOV GastroOesofageální Varixy
GSK GaStrosKopie
HGD High Grade Dysplasia
HH Hiátová Hernie
HJS Horní Jícnový Svěrač
HP Helicobacter Pylori
CHCE CHoleCystEctomie
IBD Inflammatory Bowel Disease
IGV Izolované Gastrické Varixy
INR International Normalized Ratio
JV Jícnové Varixy
KRCA KoloRektálníCArcinom
KSK KoloSKopie
LGD Low Grade Dysplasia
LST Laterally Spreading Tumor
MALT Musosa Associated Lymfoid Tissue
MRCP Magnetická Rezonanční CholangioPankreatografie
NASH Non-Alcoholic SteatoHepatitis
NAFLD Non-Alcoholic Fatty Liver Disease
NBI Narrow Band Imaging
NOAC Novel Oral Anticoagulant Agents
NOTES Natural Orifice Transluminal Endoskopic Surgery
NSA NeSteroidní Antirevmatika
NSZ Nespecifické Střevní Záněty
OK Okultní Krvácení
PBC Primární Biliární Cirhoza
PEG Perkutánní Endoskopická Gastrostomie
PM PieceMeal
POEM PerOrální Endoskopická Myotomie
PPI Proton Pump Inhibitor
PSC Primární Sklerozující Cholangitida
PST PapiloSfinkteroTomie
PSG PortoSystémový Gradient
PTC Perkutánní Transhepatická Cholangiografie
PTD Perkutánní Transhepatická Drenáž
RFA RadioFrekvenční Ablace
RNJ Refluxní Nemoc Jícnu
RUT Rychlý Ureázový Test
SBP Spontánní Bakteriální Peritonitida
SEMS SamoExpandibilní Metalický Stent
SJB Slepá Jaterní Biopsie
TEM Transanal Endoscopic Microsurgery
TOKS Test na Okultní Krvácení ve Stolici
TIPS Transjugular Intrahepatic Portosystemic Shunt
TOKS Test Okultního Krvácení do Stolice
UC Ulcerative Colitis
UDCA Ursodeoxycholic Acid
USG UltraSonoGrafie
VHA Virová Hepatitida A
VHB Virová Hepatitida B
VHC Virová Hepatitida C
VHE Virová Hepatitida E
Gynekologicko-porodnické oddělení
AB abortus
AE adnexektomie
AHY abdominální hysterektomie
ASP+ akce srdeční plodu
AU pupečníková tepna
BPD biparietální průměr hlavičky
COP centrum onkologické prevence
CPI cerebroplacentální index
CTG kardiotokogram
CURR kyretáž
DS dolní segment děložní
dlp. dle potřeby
EFW odhadovaná váha plodu
EPI episiotomie
FL délka stehenní kosti plodu
GBS screening na přítomnost bakterie streptoccocus agalactiae
GDM gestační diabetes mellitus
GEU mimoděložní těhotenství
g.h./grav.hebd. týden těhotenství
HSK dg. Hysteroskopie diagnostická
HSK oper. Hysteroskopie operační
CHT chemoterapie
IMC infekce močových cest
IMM imminens
IUD nitroděložní tělísko
IUGR intrauterinní růstová restrikce/retardace
i.c. intracervikálně
Incip. počínající
JT jaterní testy
Kolpo: kolposkopický nález
KP konec pánevní
KS krevní skupina
LAVHY laparoskopicky asistovaná vaginální hysterektomie
LE lymfadenektomie
LEEP konizace čípku elektrickou kličkou
Lpt. laparotomie
LSK laparoskopie
MDL mediolateralis
M+S moč + sediment
NAZCA TC/R implantát – poševní síťka
NOV odd. novorozenecké oddělení
OP+ ozvy plodu přítomny
oGTT orálně glukosotoleranční test
PI index pulzatility
PM poslední menstruace
PPHL poloha podélná hlavičkou
PPKP poloha podélná koncem pánevním
PPI partus prematurus imminens
PP+ pohyby plodu přítomny
PROM předčasný odtok plodové vody
PTS prvotrimestrální screening
PU/24h 24 hodinový sběr moči na proteinurii
PI (P římská 1) přední poševní plastika
PII zadní poševní plastika
RCUI revize dutiny děložní
RD Redonův dren
Res. Závěr
RI index rezistence
RT radioterapie
SE salpingektomie
SGA „small for gestational age“ nižší než očekávaný váhový odhad plodu
Susp. suspektní nebo podezření na:
š.š. šev šípový
TEM +/- Temesvaryho test na odtok plodové vody pozitivní/negativní
TOT transobturatorní páska při močové inkontinenci
TT těhotenský test nebo tělesná teplota dle kontextu
UPT umělé přerušení těhotenství
UUT umělé ukončení těhotenství
vag. vaginálně
Vag.UZ: nález na vaginálním ultrazvukovém vyšetření
VEX vakuumextraktor
VP voda plodová
Ip. prvorodička
IIp. druhorodička
IIIp. tercipara
IV. quartipara
Neurologické oddělení
ACMP akutní cévní mozková příhoda
AF anteflexe
AG angiografie
ALS amyotrofická laterální skleróza
asym asymetrie
BAEP kmenové sluchové evokované potenciály
BEAM – EEG mapování (brain electric activity mapping)
CNS centrální nervový systém
CMP cévní mozková příhoda
CMV cytomegalovirus
Cp krční páteř
CT výpočetní tomografie
CTA – CT angiografie
C-Thp přechod mezi krční a hrudní páteří
DIC diseminovaná intravaskulární koagulace
DKK dolní končetiny
DMO dětská mozková obrna
EBV virus Epsteina – Barrové
ED epidurálně
EDSS rozšířená stupnice stavu invalidity dle Kurtzkeho (expanded disability status scale)
EEG elektroencefalografe
EMG elektromyografie
EP evokované potenciály
Epi epilepsie
EpiGE epigrafoelementy
expy extrapyramidový
F frontálně
foto fotoreakce
FP frontoparietálně
FS fotostimulace
FT frontotemporálně
FTP frontotemporoparietálně
GCS Glasgowská škála tíže komatozního stavu (Glasgow coma scale)
HD hyperventilace
Chv Chvostkův příznak
i.c. intrakraniální
izo izokorie
Las Laségueův manévr
LP lumbální punkce
Lp bederní páteř
LSp lumbosakrální přechod
MEP motorické evokované potenciály
MMSE zkrácený text určený k vyšetření demence (Mini Mental State Examination)
MN mozkové nervy
MRA magnetická rezonanční angiografie
NIHSS – NIH Stroke Scale – škála k hodnocení neurologického deficitu u pacientů s iktem
ny nystagmus
O occipitálně
P parietálně
PEG pneumoencefalografie
PET pozitrovaná emisní tomografie
PMG perimyelografie
PNS periferní nervový systém
PO parietoocipitálně
py pyramidové jevy
RF retroflexe
rr reflexy
RS roztroušená skleróza
ršA reflex šlachy Achillovy
SAK subarachnoideální krvácení
SD subdurálně
SPECT jednofotonová emisní tomografie (single photon emission computed tomography)
SSEP somatosenzorické evokované potenciály
sym symetrie
ŠOR šlachookosticové reflexy
T temporálně
TIA tranzitorní cévní mozková příhoda (transient ischemic attack)
Th-Lp přechod mezi hrudní a bederní páteří
Thp hrudní páteř
TPO temporoparietooccipitálně
VEP zrakové evokované potenciály (vizual evoked potentials)
Oční oddělení
AC, PC IOL nitrooční čočka
ACR arteria centralis retinae
AION přední ischemická neuropatie optiku
AM arteficiální mydriaza
BM biomikroskopie
CB cévní branka (na papile)
C/D poměr cup to disk při hodnocení papily
CK centrální krajina
CME cystoidní makulární edem
CNV neovaskularní chorioidalní membrána
D sph ,cyl dioptrie sférické, cylindrické
DP diabetická poradna
DR diabetická retinopatie
EMM epimakulární membrána
FAG fluorescenční angiografie
FAKO fakoemulzifikace
FAZ foveolární avaskulární zóna
FD foveolární deprese
FLK fokální laserová fotokoagulace
GCC vrstva gangl. bb (popis OCT)
GLK mřížková laserová fotokoagulace
GP glaukomová poradna
IRMA intraretinální mikrovaskulární abnormity
J.č. Jaegrovo číslo (čtení textu)
KČ kontaktní čočka
KN kortikonukleární
KSME klinicky signifikantní makulární edém
KÚ komorový úhel
KV komorová voda
LA lokální anestesie
LC lamina cribrosa
LI laserová iridotomie
LK laserová koagulace
LLI lamina limitans interna
LTP laserová trabekuloplastika
MA mikroaneurysmata
MB melanoblastom
MP makulární poradna
NPDR neproliferativní diabetická retinopatie
NRL neuroretinální lem
NT nitrooční tlak
NTA aplanačně
NTB bezkontakt. tonometrem
NTS Schiötzovým tonometrem
NVD neovaskularizace terče optiku
NVE neovaskularizace sítnice
NVI neovaskularizace duhovky
OAG prostý chronický glaukom
OCT optická koherentní tomografie
OD pravé oko
ODS obě oči
Oft oftalmoskopické vyšetření
ONH optic nerv head (popis OCT)
OS levé oko
PD papilární diameter
PDR proliferativní diabetická retinopatie
PEX pseudoexfoliace
PP počítačový perimetr
PPV pars plana vitrektomie
PRK panretinalní fotokoagulace
PV předoperační vyšetření
PVR proliferativní vitreoretinopatie
PVD ablace zadní sklivcové membrány
PK přední komora
R rohovka
ROD, ROS refrakce
RAPD relativní aferentní pupilární defekt
RK refraktokeratometrie
RNFL vrstva nervových vláken (popis OCT)
RNI ramus nas. infer. (sítnicové cévy)
RNS ramus nas. super (sítnicové cévy)
RPE retinální pigmentový epitel
RTI ramus temp. infer. (sítnicové cévy)
RTS ramus tempor. super
SAPE serosní ablace pigmentového epitelu
Sch hodnocení gonio dle Schaffera
SO silikonový olej
TE trabekulektomie
TX tvrdé exsudáty
VEP zrakové evokované potenciály
VOD, VOS vizus
VCR vena centralis retiane
VOG VEGF cévní endotelový růstový faktor
VPMD věkem podmíněná makularní degenerace
YAG Ytrium- Aluminium-Garnet laser
Z zornice
ZP zadní pouzdro čočky
ORL oddělení
AAT atikoantrotomie
ACC arteria carotis communis
ACE arteria carotis externa
ACI arteria carotis interna
AME antromastoidektomie
AT adenotomie
AUDIO audiometrie
AV adenoidní vegetace
BAEP nebo BERA vyšetření kmenových evokovaných potenciálů
BND block neck dissection
BPN bez patologického nálezu
BPTM transmandibulární bukofaryngektomie
CERA vyšetření korových evokovaných potenciálů
DIAFANO diafanoskopie
EES endoskopická endonazální chirurgie
EK, ZK submukózní elektrokoagulace a ablace zadních konců dolních skořep
FES funkční endonazální chirurgie
FESS funkční endonazální chirurgie paranazálních dutin
HTE hemityreoidektomie
KSPE konzervativní superficiální parotidektomie
KTPE konzervativní totální parotidektomie
LA lokální anestézie
LMS laryngomikroskopie
MP myringoplastika
OAE otoakustické emise
OTO ucho
PARA paracentéza
PE polypektomie
PLE parciální laryngektomie
PND paranazální dutiny
PTE parciální tyreoidektomie
R Rinného zkouška ladičkou
RHINO nos
RO radikální operace
RSPE radikální superficiální parotidektomie
RTPE radikální totální parotidektomie
SCM musculus sternocleidomastoideus
SUSP suspektní
TE tonzilektomie
TP tympanoplastika
TLE totální laryngektomie
TS tracheostomie
TT tonzilotomie
TTE totální tyreoidektomie
TYMPANO tympanometrie
VJI vena jugularis interna
VT ventilační trubička
W Weberova zkouška ladičkou
Radiodiagnostické oddělení
3D trojrozměrný
AC akromioklavikulární
ACA arteria cerebri anterior
ACM arteria cerebri media
ACoA arteria communicans anterior
ACoP arteria communicans posterior
ACP arteria cerebri posterior
ADP arteria dorsalis pedis
AFC arteria femoralis comunis
AFib arteria fibularis
AFP arteria femoralis profunda
AIC arteria iliaca communis
AIE vena iliaca externa
AII arteria iliaca interna
AMI arteria mesenterica inferior
AMS arteria mesenterica superior
AP předozadní
AP arteria pulmolnalis
APo arteria poplitea
APPE apendectomie
ATA arteria tibalis anterior
ATP arteria tibialis posterior
AV arteria vertebralis
AX axiální
C krční (cervikální)
CKP cervikokapitální protéza
CMC karpometakarpální
COR koronární
CT počítačový tomograf
CTA CT angiografie
CTN CT nefrogram
DIP distální interfalangeální
DK dolní kalich
DL dolní lalok
DP dolní pól
DSL dolní střední laparotomie
ED epidurální
fract. fraktura
GH glenohumerální
GIT gastrointestinální trakt
HK horní kalich
HL horní lalok
HP horní pól
HRCT CT s vysokou rozlišovací schopností
HSL horní střední laparotomie
CHCE cholecystectomie
IP interfalangeální
IVU intravenózní vylučovací urografie
JKL jodová kontrastní látka
k.l. kontrastní látka
KTI kardiothorakální index
L bederní (lumbální)
LAT laterální
LB levá bočná
LCHCE laparoskopická cholecystectomie
LS lumbosaktální
MCP metakarpofalangeální
MDCT multidetektorový počítačový tomograf
MG mamografie
MIP maximum intenzity projection
MP malá pánev
MPR multiplanární rekonstrukce
MTP metatarsofalangeální
MTT metatarzy
OS osteosyntéza
p.o. perorálně
PA zadopřední
PB pravá bočná
PE plicní embolie
PIP proximální interfalangeální
PND paranasální dutiny
RA radiologický asistent
RC radiokarpální
RDG radiodiagnostické, týkající se radiodiagnostiky
SA subaranchiodeální
SAG sagitální
SAK subaranchiodeální krvácení
SC sternoklavikulární
SD subdurální
SK střední kalich
SL střední lalok
ŠŽ štítná žláza
TC talokrurální
TEP totální endoprotéza
Th hrudní (torakální)
TI truncus intermedius
TM temporomandibulární
TMH tuberculum maius humeri
TMT tarsometatarsální
Tr.TF truncus tibiofibularis
TRA transversální
VCI vena cava inferior
VCS vena cava superior
VDP vena dorsalis pedis
VFC vena femoralis comunis
VFib vena fibularis
VFP vena femoralis profunda
VIC vena iliaca communis
VIE vena iliaca externa
VII vena iliaca interna
VJI vena jugularis interna
VL vena lienalis
VMS vena mesenterica superior
VP vena portae
VPo vena poplitea
VTA vena tibalis anterior
VTP vena tibialis posterior
Rehabilitační oddělení
A anoda
ACT akrální koaktivační terapie
ADHD porucha pozornosti s hyperaktivitou
ADL activities of daily living (všední denní činnosti)
ATC talokrurální kloub
BBP bolest během pohybu
BNK bolest na konci pohybu
BHP benigní hyperplasie prostaty
CB cervikobrachiální
CC cervikokraniální skloubení
C/Th přechod mezi krční a hrudní
DFL dolní fixátory lopatek
DNS dynamická neuromuskulární stabilizace
FBSS FAIED BACK SURGERY SYNDROM - přetrvávající bolest v zádech a dolních končetinách
po operacích nebo výkonech v oblasti bederní páteře
FNK fixovaný nervový kořen
HLP hyperlipoproteinemie
HFL horní fixátory lopatek
HSS hluboký stabilizační systém
HYE hysterektomie - odstranění dělohy
CHFS chronická fibrilace síní
CHOPN chronická plicní nedostatečnost
CHŽI chronická žilní insuficience
ID invalidní důchod
ICHDKK ischemická choroba dolních končetin
IP interfalangeální kloub
IP2 interfalangeální kloub distální
IP1 interfalangeální kloub proximální
K katoda
KT kombinovaná terapie
KVS kardiovaskulární systém - srdce, cévy
LCA přední zkřížený vaz
LF lateroflexe
LTV léčebná tělesná výchova
MNR mechanicky nereagující radikulopatie
MOP mírně omezený pohyb
m. SCM musculus sternocleidomastoideus
m. TFL musculus tensor fascie latae
OS osteosyntéza
PC počítač
PHS periartritis humeroskapularis
PL praktický lékař
PN pracovní neschopnost
PTCA perkutánní transluminální angioplastika - rozšíření zúžených věnčitých tepen při ICHS,
ICHDK
RF retroflexe
RR rotace
SD starobní důchod
SM systém cvičení dle MUDr. Smíška
SS svalová síla
st. stupeň
Stp. stav po operaci
TE odstranění mandlí
Th/L přechod mezi hrudní a bederní
TM temporomandibulární skloubení
VDT vadné držení těla
VCHD vředová choroba duodena
Přehled zkratek používaných v ošetřovatelské dokumentaci
AD axilární drén
AK arteriální katétr
ATB antibiotika
BD břišní drén
BPS škála bolestivého chování nekomunikativního pacienta
bal. J balónek jícnový
bal. Ž balónek žaludeční
CA celková anestezie
CNS centrální nervový systém
CPAP continuous positive airway pressure/ kontinuální přetlak v dýchacích cestách
CVT centrální venózní tlak
CŽK centrální žilní katétr
D dech
DC dýchací cesty
DD domov důchodců
DF dechová frekvence
DK dialyzační katetr
DKK dolní končetiny
DIA diabetologie
DM diabetes mellitus
DP domácí péče
DÚ dutina ústní
ECS epicystostomie
EK, KEP epidurální katétr
ETK endotracheální kanyla
ES entrální sonda
EtCO₂ hladina CO₂ na konci výdechu
F frekvence
FD fundus děložní
FF fyziologické funkce
FiO₂ inspirační koncentrace kyslíku
FT fototerapie
GBS streptococcus agalactiae
GCS glasgow coma scale
HD hrudní drén
i.v. intra venózně
JS-Ž jícnová sonda žaludeční
JS-J jícnová sonda jejunální
KV kardioverze
KB kumulativní bilance
KES komorová extrasystola
KHS Krajská hygienická stanice
KS krevní skupina
LDK levá dolní končetina
LHK levá horní končetina
MK, PMK močový katetr
MM močový měchýř
MOTO motodlaha
NGS nasogastrická sonda
NS nefrostomie
O2 kyslík
P puls
P/V příjem/výdej
PDK pravá dolní končetina
PEEP pozitivní end- expirační tlak
PEG perkutálnní endoskopická gastrostomie
PEJ perkutánní endoskopická jejunostomie
PHK pravá horní končetina
PK periferní kanyla
PPV podpůrná plicní ventilace
PR potencionální riziko
Psupp tlaková podpora
RD redonův drén
RHB rehabilitace
RTG rentgenové vyšetření
SAB subarachnoidální anestezie
S.C. císařský řez
SH drén
SpO2 saturace kyslíku v krvi
SR sinusový rytmus
SVES supraventrikulární extrasystola
TEN tromboembolická nemoc
TK tlak krevní
TSK tracheostomická kanyla
UPV umělá plicní ventilace
ÚSP Ústav sociální péče
VAS vizuální analogová škála
VT objemová podpora
,
Anatomické
AO atlantookcipitální
AC akromioklavikulární
AŠ Achillova šlacha
C cervikální
CTh cervikothorakální
DIP distální interphalengeální
F frontální
HS humeroskapulární
L lumbální
LIS lumboischiadický
LS lumbosakrální
MCP metakarpophalangeální
MTP metatarsophalangeální
PIP proximální interphalangeální
PV paravertebrální
R rotace
RC radiokarpální
S sagitální
SI sakroiliakální
T transversální
Th thorakální
ThL thorakolumbální
Pohyby
ABD abdukce
ADD addukce
DF dorzální flexe
EXT extenze
FL flexe
PF plantární flexe
PRO pronace
RD radiální dukce
SUP supinace
UD ulnární dukce
VF volární flexe
VR vnitřní rotace
ZR zevní rotace
Další
AGR antigravitační relaxace
ASK artroskopie
CKP cervikokapitální protéza
DDP diadynamický proud
FH francouzské hole
FT fyzioterapeut
HSS hluboký stabilizační systém
ID interdyn
ILTV individuální léčebná tělesná výchova
KVD krátkovlnná diatermie
MA magnetoterapie
MMT měkké a mobilizační techniky
MR magnetická rezonance
MT mechanoterapie
N v normě
PB podpažní berle
PIR postisometrická relaxace
PK perličková koupel
PM podvodní masáž
PNF propriorecentivní neuromuskulární facilitace
PZ parafínový zábal
SMS senzomotorická stimulace
ST svalový test
ROM range of movement
TEP totální endoprotéza
TrP trigger point
UZ, SONO ultrazvuk
VG vaničková galvanizace
RAPE radikální prostatektomie
"""
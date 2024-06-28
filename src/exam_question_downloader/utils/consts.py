import re
from pathlib import Path

APP_NAME = "exam_question_downloader"

ROOT_DIR = Path(__file__).absolute().parent.parent.parent.parent
ASSETS_DIR = ROOT_DIR.joinpath("assets")
OUTPUT_PATH = ROOT_DIR.joinpath("output")
CONFIG_F = ROOT_DIR.joinpath("config.json")

SOURCE_URLS = [
    "https://www.upv.es/entidades/SRH/pas/676960normalc.html",   # Acceso libre
    "https://www.upv.es/entidades/SRH/pas/679590normalc.html",   # Promoción interna (algunas coinciden)
    "https://www.upv.es/entidades/SRH/pas/681577normalc.html",   # Personal temporal
]



RGX_EJERCICIO = re.compile(r".*[Ee]jercicio.*")
RGX_CODIGOS = re.compile(r".*\d{4}/\w+/\w+/\w+/\d+.*")
RGX_EXAMEN = re.compile(r".*[Ee]xamen.*")

RGX0 = (re.compile(r".*[Cc]onstituci[óo]n.*"), "Constitución Española")
RGX1 = (re.compile(r".*3\/2007.*"), "Ley 3/2007")
RGX2 = (re.compile(r".*1\/2004.*"), "Ley 1/2004")
RGX3 = (re.compile(r".*[Ee]statut.*[Aa]utonom[íi]a.*"), "Estatut Autonomia")
RGX4 = (re.compile(r".*((4\/2021)|([Ff]unci[óo]n [Pp][uú]blica [Vv]alenciana)).*"), "Ley FPV")
RGX5 = (re.compile(r".*[Pp]revenci[óo]n de [Rr]iesgos.*"), "Prevención de riesgos")
RGX6 = (re.compile(r".*((LOSU)|([Ss]istema [Uu]niversitario)).*"), "LOSU")
RGX7 = (re.compile(r".*[Pp]resupuesto.*((UPV)|([Uu]niversi.*[Pp]olit.*[Vv]al.*)).*"), "Presupuesto UPV")
RGX8 = (re.compile(r".*1\/2022.*"), "Ley 1/2022")
RGX9 = (re.compile(r".*[Pp]ol[íi]tica.*[Ss]eguridad.*[Ii]nformaci[óo]n.*"), "Política Infosec")
RGX10 = (re.compile(r".*[Pp]ol[íi]tica.*[Aa]mbiental.*"), "Política ambiental")
RGX11 = (re.compile(r".*[Cc]onsejo.*[Ss]ocial.*"), "Estatutos UPV")
RGX12 = (re.compile(r".*[Rr]ector.*"), "Estatutos UPV")
RGX13 = (re.compile(r".*[Cc]onsejo.*[Dd]e.*[Gg]obierno.*"), "Estatutos UPV")
RGX14 = (re.compile(r".*[Ii]nstituto.*[Uu]niversitario.*[Ii]nvestigaci[óo]m.*"), "Estatutos UPV")
RGX15 = (re.compile(r".*(([Cc]orte?s.*[Vv]alencian[ae]s)|([Cc]orte?s)).*"), "Corts Valencianes")
RGX16 = (re.compile(r".*(([Ll]ey.*[Oo]rg[áa]nica.*[Uu]niversidades)|(LOU)).*"), "LOSU")
RGX17 = (re.compile(r".*[Cc]reative\s*[Cc]ommons.*"), "Creative Commons")
RGX18 = (re.compile(r".*[Ff]uncionari.*"), "Ley FPV")
RGX19 = (re.compile(r".*TIC.*"), "TIC")
RGX20 = (re.compile(r".*(([Ee]squema.*[Nn]acional.*[Ss]eguridad)|(ENS)).*"), "ENS")
RGX20 = (re.compile(r".*157801.*"), "157801")
RGX21 = (re.compile(r".*PKI.*"), "PKI")
RGX22 = (re.compile(r".*((3\/2018)|([Pp]rotecci[oó]n.*[Dd]atos.*[Pp]ersonales)).*"), "Protección Datos Personales")
RGX23 = (re.compile(r".*[Aa]ctividad.*[Dd]e.*[Tt]ratamiento.*"), "Protección Datos Personales")
RGX24 = (re.compile(r".*((39\/2015)|([Pp]rocedimiento.*[Aa]dministrativo.*[Cc]om[úu]n)).*"), "LPAC")
RGX25 = (re.compile(r".*((40\/2015)|([Rr][ée]gimen.*[Jj]ur[íi]dico.*[Ss]ector.*[Pp][úu]blico)).*"), "Régimen Jurídico Sector Público")
RGX26 = (re.compile(r".*[Vv]iolencia.*[Dd]e.*[Gg][ée]nero.*"), "Viogen")
RGX27 = (re.compile(r".*[Ee]statutos.*"), "Estatutos UPV")
#  Preguntas MULTIMEDIA
RGX30 = (re.compile(r".*Sakai.*"), "Sakai")
RGX31 = (re.compile(r".*Poliformat.*"), "Poliformat")
RGX32 = (re.compile(r".*MOOC.*"), "MOOC")
RGX33 = (re.compile(r".*Learning Management System.*"), "LMS")
RGX34 = (re.compile(r".*(([Oo]pen [Ee][Dd][Xx])|([Oo]pened[Xx])).*"), "Open edX")
RGX35 = (re.compile(r".*libres de derechos.*"), "Creative Commons")
RGX36 = (re.compile(r".*Riunet.*"), "Riunet") # Nota Riunet debe estar antes de opencast
RGX37 = (re.compile(r".*((Polimedia)|(media\.upv\.es)|(Opencast)).*"), "Polimedia y Opencast") 
RGX38 = (re.compile(r".*((H\.264)|(H\.265)|(YCbCr)|(MP3)|(audio digital)).*"), "Sistemas de audio y vídeo") 
RGX39 = (re.compile(r".*((xAPI)|(Experience API)).*"), "LMS")
RGX40 = (re.compile(r".*((LTI)|(learning analytics)).*"), "LMS")
# Inteligencia artificial y realidad virtual
RGX41 = (re.compile(r".*((inteligencia artificial)|(realidad virtual)).*"), "IA y realidad virtual") 
# HTML, CSS y Javascript
RGX42 = (re.compile(r".*((HTML)|(CSS)|([Jj]ava[Ss]cript)).*"), "HTML, CSS o Javascript") 
# Preguntas REDES
RGX50 = (re.compile(r".*IPv4.*"), "Redes - IPv4") 
RGX51 = (re.compile(r".*IPv6.*"), "Redes - IPv6") 
RGX52 = (re.compile(r".*VPN.*"), "Redes - VPN") 
RGX53 = (re.compile(r".*((TCP\/IP)|( TCP )|( IP )).*"), "Redes")
RGX54 = (re.compile(r".*((DNS)|(ICMP)).*"), "Redes")
# Preguntas SISTEMAS
RGX60 = (re.compile(r".*((UNIX)|([Uu]nix)|([Ll]inux)).*"), "Sistemas - Linux") 
RGX61 = (re.compile(r".*((Windows 10)|(Windows 11)|(TPM)|([Bb]it[Ll]ocker)).*"), "Sistemas - Windows 10 y Windows 11") 
RGX62 = (re.compile(r".*(([Cc]ontenedor)|([Dd]ocker)|(Kubernetes)|(Open[Ss]tack)|(Open[Nn]ebula)|(Proxmox)).*"), "Sistemas - Contenedores")




DIR_PATTERNS = [RGX_CODIGOS, RGX_EJERCICIO]
PDF_PATTERNS = [RGX_EXAMEN, RGX_EJERCICIO]
SUBJECTS_PATTERNS = [RGX0, RGX1, RGX2, RGX3, RGX4, RGX5, RGX6, RGX7, RGX8, RGX9, RGX10, RGX11, RGX12, RGX13, RGX14, RGX15, RGX16, RGX17, RGX18, RGX19,
    RGX20, RGX21, RGX22, RGX23, RGX24, RGX25, RGX26, RGX27, RGX30, RGX31, RGX32, RGX33, RGX34, RGX35, RGX36, RGX37, RGX38, RGX39, RGX40, RGX41, RGX42,
    RGX50, RGX51, RGX52, RGX53, RGX54,
    RGX60, RGX61, RGX62]
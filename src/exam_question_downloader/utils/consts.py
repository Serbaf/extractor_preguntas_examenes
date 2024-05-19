import re
from pathlib import Path

APP_NAME = "exam_question_downloader"
MAINTAINER_EMAIL = "spuche@upv.es"
UPV_EDX_URL = "https://www.edx.org/es/search?q=UPValenciaX&tab=course"

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

RGX0 = re.compile(r".*[Cc]onstituci[óo]n.*")
RGX1 = re.compile(r".*3\/2007.*")
RGX2 = re.compile(r".*1\/2004.*")
RGX3 = re.compile(r".*[Ee]statut.*")
RGX4 = re.compile(r".*((4\/2021)|([Ff]unci[óo]n [Pp][uú]blica [Vv]alenciana)).*")
RGX5 = re.compile(r".*[Pp]revenci[óo]n de [Rr]iesgos.*")
RGX6 = re.compile(r".*((LOSU)|([Ss]istema [Uu]niversitario)).*")
RGX7 = re.compile(r".*[Pp]resupuesto.*((UPV)|([Uu]niversi.*[Pp]olit.*[Vv]al.*)).*")
RGX8 = re.compile(r".*1\/2022.*")
RGX9 = re.compile(r".*[Pp]ol[íi]tica.*[Ss]eguridad.*[Ii]nformaci[óo]n.*")
RGX10 = re.compile(r".*[Pp]ol[íi]tica.*[Aa]mbiental.*")
RGX11 = re.compile(r".*[Cc]onsejo.*[Ss]ocial.*")
RGX12 = re.compile(r".*[Rr]ector.*")
RGX13 = re.compile(r".*[Cc]onsejo.*[Dd]e.*[Gg]obierno.*")
RGX14 = re.compile(r".*[Ii]nstituto.*[Uu]niversitario.*[Ii]nvestigaci[óo]m.*")
RGX15 = re.compile(r".*(([Cc]orte?s.*[Vv]alencian[ae]s)|([Cc]orte?s)).*")
RGX16 = re.compile(r".*(([Ll]ey.*[Oo]rg[áa]nica.*[Uu]niversidades)|(LOU)).*")
RGX17 = re.compile(r".*[Cc]reative\s*[Cc]ommons.*")
RGX18 = re.compile(r".*[Ff]uncionari.*")
RGX19 = re.compile(r".*TIC.*")
RGX20 = re.compile(r".*(([Ee]squema.*[Nn]acional.*[Ss]eguridad)|(ENS)).*")
RGX20 = re.compile(r".*157801.*")
RGX21 = re.compile(r".*PKI.*")
RGX22 = re.compile(r".*((3\/2018)|([Pp]rotecci[oó]n.*[Dd]atos.*[Pp]ersonales)).*")
RGX23 = re.compile(r".*[Aa]ctividad.*[Dd]e.*[Tt]ratamiento.*")
RGX24 = re.compile(r".*((39\/2015)|([Pp]rocedimiento.*[Aa]dministrativo.*[Cc]om[úu]n)).*")
RGX25 = re.compile(r".*((40\/2015)|([Rr][ée]gimen.*[Jj]ur[íi]dico.*[Ss]ector.*[Pp][úu]blico)).*")
RGX26 = re.compile(r".*[Vv]iolencia.*[Dd]e.*[Gg][ée]nero.*")

DIR_PATTERNS = [RGX_CODIGOS, RGX_EJERCICIO]
PDF_PATTERNS = [RGX_EXAMEN, RGX_EJERCICIO]
SUBJECTS_PATTERNS = [RGX0, RGX1, RGX2, RGX3, RGX4, RGX5, RGX6, RGX7, RGX8, RGX9, RGX10, RGX11, RGX12, RGX13, RGX14, RGX15, RGX16, RGX17, RGX18, RGX19,
    RGX20, RGX21, RGX22, RGX23, RGX24, RGX25, RGX26]
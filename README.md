# exam-question-downloader


Requires Python 3.10 o superior

## Instalación en WSL - KALI LINUX

El primer paso es instalar las librerías con 

    pip3 install -r requirements.lock

En el caso de Kali Linux en WSL también necesita instalar  firefox

    sudo apt install firefox-esr

## Descripción de los notebooks

`Run.ipynb`  Realiza scraping de la web, descarga PDF, guarda en carpeta output, clasifica y guarda en CSV

`FromPDFToText.ipnyb`  Lee PDF, reconoce preguntas y las guarda en formato pickle.

`FromTextToCSV.ipnyb`  Lee los picke generado por el anterior, clasifica las preguntas y las guarda en CSV.

`ClassifyFromText.ipnyb`  Muestra las preguntas que no han sido clasificadas de los pickle (Útil para probar las expresiones regulares).

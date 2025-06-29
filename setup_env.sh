#!/bin/bash

ENV_NAME="env"

# Prüfen, ob das Environment existiert
if [ -d "$ENV_NAME" ]; then
    echo "Virtuelles Environment '$ENV_NAME' existiert bereits."
else
    echo "Virtuelles Environment '$ENV_NAME' wird erstellt..."
    python3 -m venv "$ENV_NAME"
    if [ $? -ne 0 ]; then
        echo "FEHLER: Konnte das virtuelle Environment nicht erstellen."
        exit 1
    fi
fi

# Aktivieren: Erst Windows (Scripts), dann Linux/Mac (bin)
if [ -f "$ENV_NAME/Scripts/activate" ]; then
    source "$ENV_NAME/Scripts/activate"
elif [ -f "$ENV_NAME/bin/activate" ]; then
    source "$ENV_NAME/bin/activate"
else
    echo "FEHLER: Konnte das Environment nicht aktivieren!"
    exit 1
fi

# Pakete installieren
if [ ! -f "requirements.txt" ]; then
    echo "WARNUNG: Keine requirements.txt gefunden! (Pakete werden nicht installiert)"
else
    echo "Installiere Pakete aus requirements.txt..."
    pip install --upgrade pip
    pip install -r requirements.txt
fi

echo ""
echo "FERTIG! Das Environment ist jetzt aktiv."
echo "Python-Version im Environment:"
python --version
echo ""
echo "Um später das Environment wieder zu aktivieren, nutze (je nach System):"
echo "source $ENV_NAME/bin/activate"
echo "oder"
echo "-> source $ENV_NAME/Scripts/activate"

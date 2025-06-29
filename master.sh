#!/bin/bash
# Erstellt ein logfile und alle weiteren Ausgaben werden in dieses umgeleitet
echo
exec > logfile_bash.log # 2>&1
echo "Logfile erstellt: $(date)" # Konsolen-Ausgabe


output_folder="output"
mkdir -p "$output_folder"  # Basisordner erstellen
echo "Basisordner '$output_folder' erstellt." # Konsolen-Ausgabe

ordnerliste=(run{1..3})



# Check ob die Folder run1-run3 bereits existieren und ob diese erstellt oder überschribene werden sollen je nach User-Eingabe
for ordner in "${ordnerliste[@]}"; do
  pfad="$output_folder/$ordner"
  if [ -d "$pfad" ]; then
    echo -e "\n\e[33mWarnung:\e[0m Der Ordner '$ordner' existiert bereits."
    read -p "Möchten Sie den Ordner überschreiben? [y/n] " antwort < /dev/tty > /dev/tty
    if [[ "$antwort" =~ ^[yY]$ ]]; then
        echo "Ordner '$pfad' wird überschrieben..."
        rm -rf "$pfad"
        mkdir -p "$pfad"
    else
        echo "Ordner bleibt erhalten."
    fi

  else
    echo -e "\nOrdner '$ordner' existiert nicht. Erstelle..."
    mkdir -p "$pfad"
  fi
done


# Verschiebt die Files in die entsprechenden Ordner und entfernt gleichzeitig die unerwüschten Inhalte
echo "Verschiebe Files" # Konsolen-Ausgabe
for i in {1..3}; do
    # Entfernt aus der Datei die Zeilen 2-17 heraus, da diese Inhalte nicht relevant sind
    sed -i '2,17d' dataset/*run$i.xvg

    # Verschiebt die Files in die Entsprechenden Ordner
    mv dataset/*run$i.xvg $output_folder/run$i/

    echo "Prozess für Ordner 'run$i' abgeschlossen" # Konsolen-Ausgabe
done

# Das Bash-logfile in den outputfolder verschieben
mv logfile_bash.log output/

# Rufe das Pythonskript auf für die Weitere Datenverarbeitung
python seminar.py "$output_folder"














#!/bin/bash

output_folder="output"
# # Erstellen eines Output folders
# mkdir $output_folder


#### Prüfe ob die Run1-3 Folder im outputfolder existieren und falls nicht, erstelle diese

# # Liste der gewünschten Ordner
# ordnerliste=("$output_folder" run{1..3})

# # Schleife durch alle Ordnernamen
# for ordner in "${ordnerliste[@]}"; do
#   if [ -d "$ordner" ]; then
#     echo "Ordner '$ordner' existiert bereits."
    
#   else
#     echo "Ordner '$ordner' existiert nicht. Erstelle..."
#     mkdir -p "$output_folder/$ordner"
#   fi
# done



ordnerliste=(run{1..3})

mkdir -p "$output_folder"  # Basisordner erstellen


# Check ob die Folder bereits existieren und ob diese erstellt oder überschribene werden sollen je nach User-Eingabe
for ordner in "${ordnerliste[@]}"; do
  pfad="$output_folder/$ordner"
  if [ -d "$pfad" ]; then
    # echo "Ordner '$pfad' existiert bereits."
    echo -e "\n\e[33mWarnung:\e[0m Der Ordner '$ordner' existiert bereits."
    read -p "Möchten Sie den Ordner überschreiben? [y/n] " antwort
    if [[ "$antwort" =~ ^[yY]$ ]]; then
        echo "Ordner wird überschrieben..."
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
echo "Verschiebe Files, dauert ein wenig" # Konsolen-Ausgabe
for i in {1..3}; do
    # Entfernt aus der Datei die Zeilen 2-17 heraus, da diese Inhalte nicht relevant sind
    sed -i '2,17d' dataset/*run$i.xvg

    # Verschiebt die Files in die Entsprechenden Ordner
    mv dataset/*run$i.xvg $output_folder/run$i/

    echo "Prozess für Ordner 'run$i' abgeschlossen" # Konsolen-Ausgabe
done















# Aufbau des Skriptes:
  - Bash:
    - Aufgabe 01
    - Aufgabe 02
    - Aufgabe 03
  - Python:
    - Aufgabe 04
    - Aufgabe 05
    - Aufgabe 06
    - Aufgabe 07
    - Aufgabe 08
    - Aufgabe 09
    - Aufgabe 10 


# How to run the code:
  1. Master-Skript "master.sh" im terminal runnen
  2. Als erstes das Terminal/Bash-Console öffnen
  3. Eingabe ins Terminal "bash master.sh output" [output ist the folder, where the results are stored] and press Enter to run the script
  4. Alle Rohdaten befinden sich in einem Ordner

  0. Setup des Codes:
    1. Öffne die Bash-Shell
    2. Navigiere in den Aktuellen Ordner, wo die Daten zur Auswertung liegen
    3. Führe dann 'setup_env.sh' über den Befehl 'bash setup_env.sh' aus [Erstellt ein virtuelles Environment und installiert alle notwendigen Packages, damit es keine Komplikationen gibt]
    4. Aktiviere das virtuelle Environment über den Befehl 'source Seminar_Bash_Python/Scripts/activate'

  1. Start des Programmes:
    1. Navigiert in diesen Ordner [./Seminar] [Für VS-Code: VS-Code öffnen und Ordner öffnen, Für Terminal: per "cd path_to_folder" in den Ordner navigieren]
    2. Auszuwertende Datenset als Ordner "dataset" in den geöffneten Ordner einfügen [./Seminar/dataset]
    3. Skript aufrufen über Terminal/ bash console -> "bash master.sh output" [output ist the folder, where the results are stored] and press Enter to run the script
    4. Bei erstmaliger Ausführung erfolgen keine weiteren User-Eingaben. Bei mehrfachausführung oder berits bestehenden Auswertungsdatensätzen werden Sie aufgefordert zu entscheiden, wie die Ordner weiter behandelt werden sollen. Dazu werden Sie durch ein kurzes User-Menü geführt.
    5. Die anschließende Datenauswertung erfolgt vollautomatisch, keine weitere Usereingaben sind notwendig.
    6. Die Datenauswetung ist abgeschlossen, wenn die Console schreibt "Skript vollständig ausgeführt"

  2. Datenstruktur nach der Datenauswertung
    1. Es wird ein outputfolder generiert, in welchem alle verarbeiteten/erstellten Daten enthalten sind.
    2. Der ursprüngliche Ordner "dataset" beinhaltet nach Ausführung des Skriptes keinerlei Inhalte mehr, sodass dieser gelöscht wurde. Die Rohdaten werden in die jeweiligen "run"-Ordner verschoben
    3. Der Output Folder beinhaltet für jeden "run" einen separaten Ordner. Zudem ist dort eine log-Datei, sowie der summary_report enthalten. Dort wird die Zusammenfassung aller ausgewerteten Runs Zusammengefasst.
    4. Jeder "run"-Ordner enthält einen Unterordner "basedata", dort werden die Rohdaten des jeweiligen "runs" gespeichert.
    5. Ebenfalls im output-Folder enthalten, sind die zusammengefügten Datenstrukturen aus den jeweiligen "forces" und "distances" - Files
    6. Ebenfalls sind dort die Superimposed frequency diagrams enthalten [.svg, damit eine Skaliertfähige Qualität]
    7. Ebenfalls ist dort ein Summary-File enthalten, welchesfvon jedem Frame den Mittelwert und die Standardabweichung enthält
    8. 







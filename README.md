  ### How to connect to the repository:
    1. In den gewünschten Speicherort mit 'cd /pfad/zu/deinem/verzeichnis' navigieren
    2. git clone https://github.com/timknit/Bash_und_Python.git
  ### How to push
    1. git pull 
    2. git add .
    3. git commit -m "Meine Message"
    4. git push origin main




# Structure of the script:
  ## Bash:
    - Aufgabe 01
    - Aufgabe 02
    - Aufgabe 03
  ## Python:
    - Aufgabe 04
    - Aufgabe 05
    - Aufgabe 06
    - Aufgabe 07
    - Aufgabe 08
    - Aufgabe 09
    - Aufgabe 10 


# How to run the code:
### Setup of the code:
     1. Öffne die Bash-Shell
     2. Navigiere in den Auswerte Ordner [der geschickt wurde]
     3. Führe dann 'setup_env.sh' über den Befehl 'bash setup_env.sh' aus [Erstellt ein virtuelles Environment und installiert alle notwendigen Packages, damit es keine Komplikationen gibt]

### Start of the program:
     1. Navigiere in diesen Ordner [./Seminar] [Für VS-Code: VS-Code öffnen und Ordner öffnen, Für Terminal: per "cd path_to_folder" in den Ordner navigieren]
     2. Auszuwertende Daten in den Ordner "dataset" einfügen [./Seminar/dataset]
     3. Skript aufrufen über Terminal/ bash console -> "bash master.sh" [output is the folder, where the results are stored] and press Enter to run the script
     4. Bei erstmaliger Ausführung erfolgen keine weiteren User-Eingaben. Bei mehrfachausführung oder bereits bestehenden Auswertungsdatensätzen werden Sie aufgefordert zu entscheiden, wie die Ordner weiter behandelt werden sollen. Dazu werden Sie durch ein kurzes User-Menü geführt.
     5. Die anschließende Datenauswertung erfolgt vollautomatisch, keine weitere Usereingaben sind notwendig.
     6. Die Datenauswetung ist abgeschlossen, wenn die Console schreibt "Skript vollständig ausgeführt".
     7. Die Ergebnisse für jeden 'Run' sind dann im Ordner 'output' zu finden.


### Data structure after data evaluation:
     1. Es wird ein outputfolder generiert, in welchem alle verarbeiteten/erstellten Daten enthalten sind.
     2. Der ursprüngliche Ordner "dataset" beinhaltet nach Ausführung des Skriptes keinerlei Inhalte mehr, sodass dieser leer verbleibt und für eine neue Auswetung mit Daten befüllt werden kann. Die Rohdaten einer Auswertung werden in die jeweiligen "run"-Ordner in den Folder 'basedata' verschoben.
     3. Der Output Folder beinhaltet für jeden "run" einen separaten Ordner. Zudem ist dort jeweils eine log-Datei für das 'master.sh' Skript, sowie für das 'semianr.py' Skript zu finden. Ebenfalls ist dort auch der 'summary_report' enthalten. Dort wird die Zusammenfassung aller ausgewerteten Run's Zusammengefasst.
     4. Jeder "run"-Ordner enthält einen Unterordner "basedata", dort werden die Rohdaten des jeweiligen "runs" gespeichert.
     5. Ebenfalls im output-Folder enthalten, sind die zusammengefügten Datenstrukturen aus den jeweiligen "force" und "distance" - Files.
     6. Ebenfalls sind dort die Superimposed frequency diagrams enthalten [.svg, da Skaliertfähige Qualität]
     7. Ebenfalls ist dort ein Summary-File enthalten, welchesfvon jedem Frame den Mittelwert und die Standardabweichung enthält
     8. Das .csv File mit dem Namen 'x_max_runX.csv' enthält die berechneten Maxima der Kurven aus den Superimposed Histograms jeweils für die 'forces' und 'distances'





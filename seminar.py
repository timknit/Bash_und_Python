# === Auto-Install ===
import sys
import subprocess
# import logging

def install_requirements() -> None:
    '''
    Funktion zum installieren der nötigen Packages zur Datenverarbeitung.
    Diese Funktion prüft, ob die benötigten Pakete installiert sind und installiert sie bei Bedarf.
    Installation erfolgt über pip
    '''
    logging.info(f"Function: install_requirements -> Requirements werden installiert ...")
    # required_modules = [
    # 'pandas',
    # 'matplotlib',
    # 'numpy',
    # 'seaborn'
    # 'logging',     # Standardmodul, wird nicht installiert
    # 'getpass',     # Standardmodul, wird nicht installiert
    # 'datetime',    # Standardmodul, wird nicht installiert
    # 'shutil',      # Standardmodul, wird nicht installiert
    # 'string',      # Standardmodul, wird nicht installiert
    # 'os',          # Standardmodul, wird nicht installiert
    # 'sys'          # Standardmodul, wird nicht installiert
    # ]

    # Nur Pakete installieren, die nicht im Standardumfang von Python enthalten sind
    installable_modules = ['pandas', 'matplotlib', 'numpy', 'seaborn']

    # for module in installable_modules:
    #     try:
    #         __import__(module)
    #         print(f"{module} ist bereits installiert.")
    #         logging.info(f"Modul: '{module}'")
    #     except ImportError:
    #         logging.info(f"Modul: '{module}' nicht installiert")
    #         logging.info(f"Modul: '{module}' wird installiert")
    #         print(f"{module} wird installiert...")
    #         subprocess.check_call([sys.executable, "-m", "pip", "install", module])
    #         logging.info(f"Modul: '{module}' wurde installiert")


    for module in installable_modules:
        try: # Versucht es Abzurufen/Importieren
            __import__(module)
            print(f"{module} ist bereits installiert.")
            logging.info(f"Modul: '{module}' ist bereits installiert")
        except ImportError:# Fall nicht Abzurufbart/Importierbar -> Neuinstallation
            try: # Versucht Neuinstallation
                logging.info(f"Modul: '{module}' nicht installiert")
                logging.info(f"Modul: '{module}' wird installiert")
                print(f"{module} wird installiert...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", module])
                logging.info(f"Modul: '{module}' wurde installiert")
            except Exception as e: # Fängt Fehler, falls einer auftritt
                logging.error(f"Fehler bei Installation von '{module}': {e}")
                print(f"Fehler bei Installation von {module}: {e}")

    logging.info("Alle Module wurden überprüft.\n")



# === Imports der vorher Installierten Bibliotheken ===
import os
import pandas as pd 
import sys
import string
import shutil
import matplotlib.pyplot as plt
import datetime
import getpass
import numpy as np
import logging
import seaborn as sns




def setup_logger(log_path: str) -> None:
    '''
    Funktion zum Einrichten des Loggers, der die Ausgaben in eine log-Datei schreibt.
    Das File mit dem Filename wird erstellt
    Das Logfile solle jedes Mal neu erstellt werden, wenn das Skript ausgeführt wird, daher 'w'
    :inputs -> log_path: Verzeichnis, in dem das logfile gespeichert werden solle
    '''

    logging.basicConfig(
        filename=log_path,
        filemode='w',  # 'a' für anhängen, 'w' für überschreiben
        level=logging.INFO,  # oder DEBUG, ERROR, etc.
        format='%(asctime)s - %(levelname)s - %(message)s' # Zeitstempel - Info/Debug/Error,... - Nachricht
    )



def sorted_filelist(dirname: str) -> list:
    '''
    Funktion zum Sortieren der Liste der Namen der .xvg Dateien.
    Diese Funktion liest alle Dateien im angegebenen Verzeichnis ein, filtert die .xvg Dateien heraus und sortiert sie basierend auf der Nummer im Dateinamen.

    :inputs -> dirname: Verzeichnis, in dem die .xvg Dateien liegen
    :return -> Sortierte Liste der .xvg Dateinamen
    '''
    logging.info(f"Function: sorted_filelist -> Liste der Ordnerinhalte sortieren")
    xvg_file_names = [] # Erstellt leer Liste zur Speicherung
    files = os.listdir(dirname) # Liest alle Filenames aus dem Ordner ein
    for file in files: # Iteriert durch jeden dieser Filenames
        if file.endswith(".xvg") and "combined" not in file: # combined muss nur rein, dass wenn man das Skrpt zwei mal runt, dass die Sammeldateien nicht mit ausgelesen werden 
            xvg_file_names.append(file) # fügt den Namen der aktuellen Datei an die Speicherliste an
            logging.info(f"File: '{file}' wurde hinzugefügt")
        else:
            logging.warning(f"File: '{file}' ist kein '.xvg' File")

    xvg_file_names_sort = sorted(xvg_file_names, key=lambda x: int(x.split('_')[1][5:])) # sortiert die Liste mit den Namen aller .xvg-Dateien anhand der Nummer im Dateinamen, 
    # lamda fuction erlaubt es eine bestimmte Operation auf eine gesamte Liste durchzuführen, es nimmt das Element 'x' und splittet es druch den '_' und nimmt dann das zweite Element [framexxx] und scheidet dann das frame durch [5:] ab
    logging.info(f"File Liste wurde sortiert\n")

    return xvg_file_names_sort



def gen_colnames(n_frames: int) -> list:
    '''
    Funktion zum Generieren von Spaltennamen für die Dataframes.
    Damit die Frames die Namen FrameA bis FrameZ und dann anschließend FrameAA bis FraemZZ haben können
    :inputs -> n_frames: Anzahl der Spaltennamen/Frames [ohne Time (ps)]
    :return -> names: Erzeugte Spaltennamen
    '''

    logging.info(f"Function: gen_colnames -> Spaltennamen werden generiert ...")
    alphabet = string.ascii_uppercase # Erzeugt eine Liste ['A', 'B', 'C', 'D', ..., 'Y', 'Z']
    names = [] # Leere Liste zur Speicherung der Namen
    
    i = 0
    while len(names) < n_frames: # Für jeden Splatennamen
        name = ""
        num = i
        while True:
            name = alphabet[num % 26] + name # Berechnet dann über Modulo, um das über 25 ist und nimmt dann das nächste Element also bspw 26 -> 1, also A und A
            num = num // 26 - 1
            if num < 0:
                break
        names.append(f"frame{name}")
        i += 1
    logging.info(f"Spaltennamen wurden generiert\n")
    
    return names



def df_combined(dir_path: str, sorted_list: list) -> tuple[pd.DataFrame, pd.DataFrame]:
    '''
    Funktion zum Zusammenführen der Dataframes aus den .xvg Dateien.
    Splatennamen werden auf Anforderungen der Aufgabenstellung angepasst
    :inputs -> dir_path: Verzeichnis in welchem die Files liegen, sorted_list: Sortierte Liste der Namen der .xvg-Files in dem Ordner
    :return -> names: Zwei sortierte Dataframes jeweils für Force und Distance
    '''
    logging.info(f"Function: df_combined -> Dataframes werden zusammengeführt ...")
    df_all_forces = None # Müssen als None definiert werden, damit das Später beim Mergen keine Porbleme gibt, 
    df_all_distances = None # denn es solle der erste Dataframe als 'Muster' übernommen werden so muss ich keinen Leeren Dataframe mit vorgschriebenen Col_names erstellen

    for filename in sorted_list:
        logging.info(f"File: {filename} wird verarbeitet")
        file_path = os.path.join(dir_path, filename)
        # print(filename) # debuggig
        df = pd.read_csv(file_path, sep='\t', comment='#', header=None, names=["Time (ps)", "Value"]) # comment übersprint lines mit '#' am Anfang
        
        col_name = os.path.basename(filename).replace('.xvg', '') # schneidet die Dateiendung ab
        df = df.rename(columns={"Value": col_name}) # bennent im aktuellen Dataframe die Spalte um, damit das gleich beim Mergen keine Porbleme macht, wenn die die gleichen Spaltennamen ahebn
        # print(col_name) # debuggig

        if "pullf" in filename: # Check, ob bereits ein Dataframe für Force erstellt wurde, oder ob der aktuelle als Template dienen solle
            if df_all_forces is None:
                df_all_forces = df
            else:
                df_all_forces = pd.merge(df_all_forces, df, on="Time (ps)")

        elif "pullx" in filename: # Check, ob bereits ein Dataframe für Distance erstellt wurde, oder ob der aktuelle als Template dienen solle
            if df_all_distances is None:
                df_all_distances = df
            else:
                df_all_distances = pd.merge(df_all_distances, df, on="Time (ps)")

        else:
            print("Kein geeigneter Datentyp identifiziert")
            logging.warning(f"Kein geeigneter Datentyp identifiziert")


    # Vorbereitungen für die Bennenung der neuen Spaltennamen hier nur für einen der Beiden Dataframes berechnet, da die Dateien immer komplementär vorliegen, also eine Force datei zu einer Distance Datei
    anzahl_cols = len(df_all_forces.columns) - 1  # -1 weil Time (ps) nicht umebannt werden solle
    new_colnames = ["# Time (ps)"] + gen_colnames(anzahl_cols) # '#' vor Time (ps) da Aufgabe das so Verlangt

    # Neue Splatennamen umbenennen in den jeweiligen Dataframes
    df_all_forces.columns = new_colnames
    df_all_distances.columns = new_colnames
    logging.warning(f"Dataframes wurden erstellt\n")

    return df_all_forces, df_all_distances



def move_basedata_files(dirname: str, dir_path: str) -> None:
    '''
    Funktion zum Verschieben der Rohdaten-Dateien in den "basedata" Ordner.
    :inputs -> dirname: Name des aktuellen Verzeichnisses, dir_path: Pfad zum aktuellen Verzeichnis
    '''
    logging.info(f"Function: move_basedata_files -> Rohdaten-Files werden verschoben ...")
    # Zielordner erstellen, falls noch nicht vorhanden
    basedata_folder = os.path.join(dir_path, "basedata")
    os.makedirs(basedata_folder, exist_ok=True)
    logging.info(f"Folder 'basedata' wurde erstellt")

    # Alle Dateien im Ordner durchgehen
    for filename in os.listdir(dir_path):
        # vollständiger Pfad der Datei
        full_path = os.path.join(dir_path, filename)
        
        # Nur Dateien bewegen (keine Unterordner)
        if os.path.isfile(full_path):
            if filename in [f"forces_combined_{dirname}.xvg", f"distances_combined_{dirname}.xvg"]:
                logging.warning(f"File: {filename} ist ein 'combined' file")
                continue
            else:
                # Datei in basedata verschieben
                shutil.move(full_path, basedata_folder)
                logging.info(f"File: {filename} wurde verschoben")
    logging.info("Alle Files wurden verschoben.\n")



def create_mean_stbw_files(dir_path: str) -> None:
    '''
    Funktion zum Erstellen der Durchschnitts- und Standardabweichungsdateien.
    :inputs -> dir_path: Pfad zum aktuellen Verzeichnis
    '''
    logging.info(f"Function: create_mean_stbw_files -> Durchschnittsdaten und Standardabweichungen werden berechnet ...")
    run_name = os.path.basename(dir_path)
    file_names = os.listdir(dir_path)

    for file_name in file_names:
        if file_name.endswith(".xvg"):
            file_path = os.path.join(dir_path, file_name)
            curr_df = pd.read_csv(file_path, sep='\t')

            mean_val = curr_df.drop(columns="# Time (ps)").mean() # berechnet den Mittelwert für jede Spalte außer der Zeitspalte
            std_val = curr_df.drop(columns="# Time (ps)").std() # berechnet die Standardabweichung für jede Spalte außer der Zeitspalte
            logging.info(f"Durchschnitt für File: '{file_name}' berechnet")
            logging.info(f"Standardabweichung für File: '{file_name}' berechnet")

            # Forces
            if "forces" in file_name: # erstellt Dataframe mit den Mittelwerten und Standardabweichungen für die Kräfte
                df_force_mean_std = pd.DataFrame({
                    "Frame": mean_val.index,
                    "Force (kJ/mol/nm)": mean_val.values,
                    "STD_F": std_val.values
                }) 

            # Distances
            if "distances" in file_name: # erstellt Dataframe mit den Mittelwerten und Standardabweichungen für die Distanzen
                df_distance_mean_std = pd.DataFrame({
                    "Frame": mean_val.index,
                    "Distance (nm)": mean_val.values,
                    "STD_D": std_val.values
                })

    # Merge alle Daten zusammen
    df_merged = pd.merge(df_distance_mean_std, df_force_mean_std, on="Frame") # Zusammenfügen der Dataframes anhand des Frames / Namen des Frames
    logging.info(f"Durchschnitts- und Standardabweichungsdaten gemerged")

    output_path = os.path.join(dir_path, f"summary_file_{run_name}.xvg") # Speichernamen und -pfad für die Zusammenfassungsdatei
    df_merged.to_csv(output_path, sep='\t', index=False) # Speichert den merged-dataframe als .xvg ab 
    logging.info(f"Durchschnitts- und Standardabweichungsdaten im summary_file_{run_name}.xvg gespeichert.\n")



def plot_distance_force(dir_path: str) -> None:
    '''
    Funktion zum Erstellen des Force-Distance-Plots.
    :inputs -> dir_path: Pfad zum aktuellen Verzeichnis
    '''
    logging.info(f"Function: plot_distance_force -> Force-Distance-Plot erstellen ...")
    run_name = os.path.basename(dir_path)
    file_path = os.path.join(dir_path, f"summary_file_{run_name}.xvg")

    # Lade die Zusammenfassungsdatei
    df_summary = pd.read_csv(file_path, sep='\t')
    logging.info(f"Daten aus File: 'summary_file_{run_name}.xvg' eingelesen")

    # Plot
    plt.errorbar(# Fehlerbalken jeweils mit der berechneten Standardabweichung
        df_summary["Distance (nm)"], df_summary["Force (kJ/mol/nm)"],
        xerr=df_summary["STD_D"], yerr=df_summary["STD_F"],
        fmt='o', ecolor='gray', capsize=3, markersize=4, label='Datenpunkte'
    ) 

    plt.title(f"Distance-Force: {run_name}")
    plt.xlabel("Distance (nm)")
    plt.ylabel("Force (kJ/mol/nm)")
    plt.grid(True)
    plt.legend()
    # plt.legend(handles=[errorbar.lines[0], error_patch])
    plt.tight_layout()

    # Speichern
    output_path = os.path.join(dir_path, f"distance_force_plot_{run_name}.png")
    plt.savefig(output_path)
    logging.info(f"Force-Distance-Plot gespeichert: {output_path}.\n")
    # plt.show()
    plt.close()

    # print(f"Plot gespeichert: {output_path}")



def calc_max_hist(df_values: list, file_name: str) -> float:
    '''
    Funktion zum Berechnen des Maximums aus den Histogrammdaten.
    :inputs ->  df_values: Liste der Werte aus dem DataFrame, file_name: Name der Datei, aus der die Daten stammen
    :return -> x_max: Wert, bei dem das Maximum liegt
    '''
    logging.info(f"Function: calc_max_hist -> Maximum der einzelnen Graphen ermitteln ...")
    
    plt.figure(figsize=(16, 10))
    line = sns.kdeplot(df_values) # , color='blue', linewidth=2, legend=None)

    # Zugriff auf x- und y-Daten der gezeichneten Kurve (Angepasste KDE-Kurve)
    x_data = line.get_lines()[0].get_xdata()
    y_data = line.get_lines()[0].get_ydata()

    # Maximum finden
    max_idx = np.argmax(y_data)
    x_max = x_data[max_idx]
    y_max = y_data[max_idx]

    # print(f"Maximum bei x = {x_max:.6f}, y = {y_max:.6f}")

    logging.info(f"Maximum aus: {file_name} ermittelt")
    # plt.show()
    plt.close()

    return x_max # Wert wo das y-Maximum liegt aus P_max = (x_max, y_max)



def plot_histogram(dir_path: str) -> None:
    '''
    Funktion zum Erstellen von Histogrammen für die Kräfte und Distanzen.
    :inputs -> dir_path: Pfad zum aktuellen Verzeichnis
    '''
    logging.info(f"Function: plot_histogram -> Histogramm-Superimposed frequency Diagram plotten ...")
    run_name = os.path.basename(dir_path) # ermittelt welche runfolder gerade bearbeitete wird
    basedata_path = os.path.join(dir_path, "basedata")
    files = sorted_filelist(basedata_path) # eigene Function aufrufen, sortiert die Files
    # files = os.listdir(basedata_path)
    force_data = []
    distance_data = []

    force_x_max = [] 
    distance_x_max = [] 


    counter = 0
    # Iteriert durch die beiden combined Files aus den vorherigen Schritten
    for file_name in files:
        logging.info(f"Daten aus File: '{file_name}' verarbeitet")
        # counter = counter + 1
        # if counter == 10:
        #     break
        if file_name.endswith(".xvg") and "run" in file_name:
            file_path = os.path.join(basedata_path, file_name)
            df = pd.read_csv(file_path, sep='\t', comment='#', header=None, names=["Time (ps)", "Value"]) # comment übersprint lines mit '#' am Anfang
            df = df.drop(columns=["Time (ps)"])  # Zeitspalte entfernen da nicht benötigt

            # Transformation der Daten in ein 1D Array/ Liste
            df_values = df.values.flatten()

            if "pullf" in file_name:
                force_data.append(df_values)
                logging.info(f"Daten wurden 'force_data' zugeordnet und hinzugefügt")
                force_x_max.append(calc_max_hist(df_values, file_name))

            elif "pullx" in file_name:
                distance_data.append(df_values)
                logging.info(f"Daten wurden 'distance_data' zugeordnet und hinzugefügt")
                distance_x_max.append(calc_max_hist(df_values, file_name))


    # Histogramm plotten Force
    plt.figure(figsize=(16, 10))
    labels = [f'Dataset {i+1}' for i in range(len(force_data))]
    # plt.hist(force_data, bins=50, density=True, label=labels)  # density=True → relative Häufigkeit
    # sns.histplot(force_data, stat='density', kde=True, bins=50, edgecolor='black')
    sns.kdeplot(force_data, color='blue', linewidth=2, legend=None)
    plt.title("Superimposed-Histogramm der Kräfte")
    plt.xlabel("Force (kJ/mol/nm)")
    plt.ylabel("Relative Häufigkeit")
    plt.grid(True)
    # plt.legend() 
    # plt.tight_layout()
    # plt.show()
    # Speichern
    output_path = os.path.join(dir_path, f"Histogramm_force_{run_name}.svg")
    plt.savefig(output_path)
    plt.close()
    logging.info(f"Histogramm-Superimposed frequency Diagram für 'Force' wurde geplottet und gespeichert: '{output_path}'")


    # Histogramm plotten Distance
    plt.figure(figsize=(16, 10))
    labels = [f'Dataset {i+1}' for i in range(len(distance_data))]
    # plt.hist(distance_data, bins=30, density=True, label=labels)  # density=True → relative Häufigkeit
    # sns.histplot(force_data)
    sns.kdeplot(distance_data, color='blue', linewidth=2, legend=None)
    plt.title("Superimposed-Histogramm der Distanzen")
    plt.xlabel("Distance (nm)")
    plt.ylabel("Relative Häufigkeit")
    plt.grid(True)
    # plt.legend()
    # plt.tight_layout()
    # plt.show()
    # Speichern
    output_path = os.path.join(dir_path, f"Histogramm_distance_{run_name}.svg")
    plt.savefig(output_path)
    plt.close()
    logging.info(f"Histogramm-Superimposed frequency Diagram für 'Distance' wurde geplottet und gespeichert: '{output_path}'")

    print(f"Histogramme gespeichert: {output_path}\n")



    # x_max speichern für force und distance die zuvor berechnet wurden
    df_x_max = pd.DataFrame({
    'force_x_max': force_x_max,
    'distance_x_max': distance_x_max
    })

    output_path = os.path.join(dir_path, f"x_max_{run_name}.csv")
    df_x_max.to_csv(output_path, sep='\t', index=False)
    logging.info(f"Werte für 'x_max' wurden zusammengefügt und gespeichert: '{output_path}'")



def create_report(output_folder: str) -> None:
    '''
    Funktion zum Erstellen des Abschlussreports.
    :inputs -> output_folder: Pfad zum Ordner, in dem die Auswertungen liegen
    '''
    logging.info(f"Function: create_report -> Report-File wird erstellt ...")
    output_path = os.path.join("output", "summary_report.txt")
    report_lines = []

    username = getpass.getuser()

    # Header
    report_lines.append("# REPORT")
    report_lines.append(f"# Created on {datetime.date.today()} by {username}")
    report_lines.append("#")
    report_lines.append("# Run\tForce variation(kJ/mol/nm)\tDistance variation(nm)")
    logging.info(f"Header wurde eingefügt")

    for item_name in os.listdir(output_folder): # Geht jeden Run ordner durch
        if "run" in item_name:
            logging.info(f"Report-Data für Folder: '{item_name}' werden verarbeitet")
            dir_path = os.path.join(output_folder, item_name)
            run_name = os.path.basename(dir_path) # Hier könnte man auch einfach das Item selst benutzen

            # Pfade zu den bereits erstellten Zusammenfassungsdatei
            # summary_file = os.path.join(dir_path, f"summary_file_{run_name}.xvg") # Kann als alternative zu KDE und max points verwendet werden, wenn Data normally distributed
            summary_file = os.path.join(dir_path, f"x_max_{run_name}.csv")

            if not os.path.exists(summary_file):
                # print(f"summary_file{run_name} existiert nicht.")
                # logging.warning(f"File: summary_file{run_name} existiert nicht oder konnte nicht gefunden werden")
                print(f"x_max_{run_name} existiert nicht.")
                logging.warning(f"File: x_max_{run_name} existiert nicht oder konnte nicht gefunden werden")
                continue

            df_summary = pd.read_csv(summary_file, sep="\t") # Einlesen des Files


            # Extrahiere die Spalten als Listen
            # forces = df_summary["Force (kJ/mol/nm)"].tolist()
            # distances = df_summary["Distance (nm)"].tolist()
            forces = df_summary["force_x_max"].tolist()
            distances = df_summary["distance_x_max"].tolist()
            

            # Sortiere die Listen aufsteigend
            forces_sorted = sorted(forces)
            distances_sorted = sorted(distances)
            

            # Differenzen berechnen
            force_variation = []
            distance_variation = []
            
            for i in range(1, len(distances_sorted)):
                force_variation.append(forces_sorted[i] - forces_sorted[i-1])
                distance_variation.append(distances_sorted[i] - distances_sorted[i-1])
                

            # Mittelwerte berechnen
            avg_force_variation = np.mean(force_variation)
            avg_distance_variation = np.mean(distance_variation)
            

            # Mittelwert der Standardabweichungen für Force und Distance berechnen
            # std_f = df_summary["STD_F"].mean()
            # std_d = df_summary["STD_D"].mean()

            report_lines.append(f"{run_name.replace("run","Run_")}\t{avg_force_variation:.4f}\t{avg_distance_variation:.4f}")

    # Report schreiben
    with open(output_path, "w") as f:
        f.write("\n".join(report_lines))
    
    logging.info(f"Report-File geschrieben")
    logging.info(f"Report-File gespeichert\n")



# !!! Aktuelle Änderungen:
# Anpassung der Kommenatr in den Functions
# ggf noch den leeren ordner Dataset automatisiert löschen -> os.rmdir("Dataset") or shutil.rmtree("Dataset") 


#!!!!!!!!!!!!!!!!!!!!!!!
#!!! Executive Part !!!#
#!!!!!!!!!!!!!!!!!!!!!!! 

if __name__ == "__main__":


    log_file = os.path.join("output", "logfile_python.log")
    setup_logger(log_file)
    logging.info(f"Logfile wurde erstellt: {log_file}")

    logging.info(f"Python-Interpreter: {sys.executable}")

    output_folder = sys.argv[1]
    logging.info(f"Daten aus Bash-Skript ausgelesen und übergeben\n")

    logging.info("Python-Skript gestartet\n")
    # install_requirements() # Ersetzt durch das Setupfile 'settup_env.sh'

    for dirname in os.listdir(output_folder): # Iteriert durch jeden Inhalt in dem Ordner/Verzeichnis "output" also 'run1' 'run2' und 'run3'
        logging.info(f"Verzeichnis '{dirname}' geöffnet")
        dir_path = os.path.join(output_folder, dirname) # Fügt die Namen der Inhalte mit dem Ursprungspfad zu einem gemeinsamen Pfad zusammen 
        if "run" in dirname:

            if "basedata" in os.listdir(dir_path): # Notwendig um beim erneuten Runnen des Files keine Fehler zu erzeugen
                logging.warning(f"Verzeichnis '{dirname}' enthält bereits eine Auswertung")
                continue

            xvg_file_names_sort = sorted_filelist(dir_path) # Ruft eigene funnktion auf, welche dann für den aktuellen Folder alle darin befindlichen .xvg-Dateien als sortierte Liste zurückgibt
            df_all_forces, df_all_distances = df_combined(dir_path, xvg_file_names_sort) # Teilt alle sortierten .xvg-Files in Force und Distance auf bennt die Überschriften um und gibt die Dataframes dann aus
            

            # Erstellte Dateien outputen -> kann auch nich in combined-Dataframes integriert werden
            output_path = os.path.join(dir_path, f"forces_combined_{dirname}.xvg")
            df_all_forces.to_csv(output_path, sep='\t', index=False)

            output_path = os.path.join(dir_path, f"distances_combined_{dirname}.xvg")
            df_all_distances.to_csv(output_path, sep='\t', index=False)


            # Ordner aufräumen
            move_basedata_files(dirname, dir_path) # Ruft eigene function auf

            # Erstellen des Files mit den jeweiligen Durchschnittswerten und zugehöriger STBW
            create_mean_stbw_files(dir_path) # Ruft eigene function auf

            # Erstellt die Plots mit Force über Distance
            plot_distance_force(dir_path) # Ruft eigene function auf

            # Erstellt die Histogramme mit den Häufigkeiten auf der y-Achse und den möglichen Werten auf der x-Achse
            plot_histogram(dir_path) # Ruft eigene function auf

        else:
            continue


    # Erstellt den Abschlussreport 
    create_report(output_folder) # Ruft eigene function auf

    logging.info(f"Skript vollständig ausgeführt")








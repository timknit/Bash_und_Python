def plot_histogram2(dir_path: str) -> None:
    '''
    Funktion zum Erstellen von Histogrammen für die Kräfte und Distanzen.
    :param dir_path: Pfad zum aktuellen Verzeichnis
    '''
    run_name = os.path.basename(dir_path)
    files = os.listdir(dir_path)

    # Iteriert durch die beiden combined Files aus den vorherigen Schritten
    for file_name in files:
        if file_name.endswith(".xvg") and "combined" in file_name:
            if "forces" in file_name:
                prefix = "force"
                title = "Histogramm der Kräfte"
                xlabel = "Force (kJ/mol/nm)"

            elif "distances" in file_name:
                prefix = "distance"
                title = "Histogramm der Distanzen"
                xlabel = "Distance (nm)"

            # Daten aus der Datei laden
            file_path = os.path.join(dir_path, file_name)
            df = pd.read_csv(file_path, sep="\t")  
            df = df.drop(columns=["Time (ps)"])  # Zeitspalte entfernen da nicht benötigt

            # Transformation der Daten in ein 1D Array/ Liste
            all_values = df.values.flatten()

            # Histogramm plotten
            plt.figure(figsize=(8, 5))
            plt.hist(all_values, bins=30, density=True, edgecolor='black')  # density=True → relative Häufigkeit
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel("Relative Häufigkeit")
            plt.grid(True)
            plt.tight_layout()
            # plt.show()

            # Speichern
            output_path = os.path.join(dir_path, f"Histogramm_{prefix}_{run_name}.png")
            plt.savefig(output_path)
            # plt.show()
            plt.close()

            print(f"Plot gespeichert: {output_path}")



import os
import logging




def setup_logger(log_path: str) -> None:
    # os.makedirs(os.path.dirname(log_path), exist_ok=True)
    logging.basicConfig(
        filename=log_path,
        filemode='w',  # 'a' für anhängen, 'w' für überschreiben
        level=logging.INFO,  # oder DEBUG, ERROR, etc.
        format='%(asctime)s - %(levelname)s - %(message)s'
    )




log_file = os.path.join("output", "logfile.log")
setup_logger(log_file)
print(f"Logfile wurde erstellt: {log_file}")

logging.info("Programm gestartet")



logging.info("Programm gestartet2")


for i in range(0,10):
    logging.info(f"Programm gestartet Stage: {i}")
# install_requirements()
from pathlib import Path
import shutil
from datetime import datetime


BANCO = Path("database/monitor.db")

PASTA_BACKUP = Path("backup")


def criar_backup():

    if not BANCO.exists():

        print("Banco não encontrado. Backup ignorado.")
        return


    PASTA_BACKUP.mkdir(exist_ok=True)


    data = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )


    destino = PASTA_BACKUP / f"monitor_{data}.db"


    shutil.copy2(
        BANCO,
        destino
    )


    print(
        f"Backup criado: {destino}"
    )



if __name__ == "__main__":

    criar_backup()
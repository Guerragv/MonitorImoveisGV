from pathlib import Path
import shutil
from datetime import datetime

# Diretório raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

BANCO = BASE_DIR / "database" / "monitor.db"
PASTA_BACKUP = BASE_DIR / "backup"


def criar_backup():

    if not BANCO.exists():
        print(f"Banco não encontrado: {BANCO}")
        return

    PASTA_BACKUP.mkdir(exist_ok=True)

    data = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    destino = PASTA_BACKUP / f"monitor_{data}.db"

    shutil.copy2(BANCO, destino)

    print(f"Backup criado: {destino}")


if __name__ == "__main__":
    criar_backup()
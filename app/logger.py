import logging
from pathlib import Path
from datetime import datetime


def configurar_logger():

    pasta_logs = Path("logs")

    pasta_logs.mkdir(
        exist_ok=True
    )


    arquivo = (
        pasta_logs /
        f"monitor_{datetime.now().strftime('%Y-%m-%d')}.log"
    )


    logging.basicConfig(

        filename=arquivo,

        level=logging.INFO,

        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(message)s"
        ),

        encoding="utf-8"

    )


    return logging.getLogger(
        "MonitorImoveisGV"
    )
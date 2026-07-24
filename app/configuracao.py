import yaml
from pathlib import Path


def carregar_config():

    caminho = Path("config/config.yaml")

    with open(
        caminho,
        "r",
        encoding="utf-8"
    ) as arquivo:

        return yaml.safe_load(arquivo)
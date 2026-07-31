@echo off

cd /d G:\Documentos\Projetos\Projetos\MonitorImoveisGV

call .venv\Scripts\activate

python main.py >> logs\agendamento.log 2>&1

exit
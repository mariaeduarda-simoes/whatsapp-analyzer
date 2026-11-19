@echo off
cd /d "%~dp0"

echo === 1/4 Criando ambiente virtual (so na primeira vez) ===
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate.bat

echo === 2/4 Instalando bibliotecas ===
pip install -r requirements.txt

echo === 3/4 Rodando testes ===
python -m pytest

echo === 4/4 Ligando a API ===
echo Abrindo http://127.0.0.1:8000/docs no navegador...
start "" cmd /c "timeout /t 5 >nul & start http://127.0.0.1:8000/docs"
uvicorn app.main:app --reload
pause

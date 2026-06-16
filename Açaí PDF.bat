@echo off 
:: 1. Forçar o Windows a aceitar os acentos em portugues (Padrão UTF-8)
chcp 65001 >nul

:: 2. Entra na pasta onde está o prjeto
cd "C:\Users\PADRE LEANDRO 05\Documents\André\Açaí PDF"

:: 3. Roda o Streamlit m segundo plano
python -m streamlit run app.py --server.address 0.0.0.0

pause
# EcoTech Solutions — BJ

## Ejecutar con SQLite 
En PowerShell, desde la carpeta raíz del proyecto:

powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
Copy-Item .env.example .env
python -m compileall src
python -m unittest discover -s tests -v
python src\main.py
```

4.  el archivo `.env` del proyecto y configúrarlo con tus datos reales

   DB_ENGINE=mysql
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=ecotech
   DB_USER=ecotech_app
   DB_PASSWORD=TU_CLAVE_REAL

5. Inicia el programa:
   python src\main.py
Para volver a SQLite, cambia `DB_ENGINE=sqlite` y configura `DB_NAME=ecotech.db`.


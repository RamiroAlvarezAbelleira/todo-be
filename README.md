
<!-- Para correr el entorno virtual -->
source env/bin/activate

<!-- Para cortarlo -->
deactivate

<!-- Para correr el servidor -->
uvicorn app.main:app --reload

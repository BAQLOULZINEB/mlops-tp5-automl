# TP05 - Deployer un modele AutoML

Fiche explicative : `EXPLICATION_TP5.html` | Rapport : `rapport_tp5.md`

```powershell
.venv\Scripts\Activate.ps1
python donnees.py
# terminal 1 : serveur MLflow (port 5000)
mlflow server --host 127.0.0.1 --port 5000 --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlartifacts
# terminal 2
python src/automl_deploy.py
python src/modele_manuel.py
python src/promouvoir.py fraude-automl
python src/promouvoir.py fraude-manuel
# terminal 3 et 4 : $env:MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"
mlflow models serve -m "models:/fraude-automl@production" -p 8100 --env-manager local
mlflow models serve -m "models:/fraude-manuel@production" -p 8101 --env-manager local
# terminal 2
python src/client.py 8100
python src/client.py 8101
```

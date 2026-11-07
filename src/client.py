"""TP5 - src/client.py

ROLE      : Joue le role d'une application cliente : appelle l'API, puis mesure 200 appels (mediane et p95).
ENTREE    : numero de port du service (8100 AutoML, 8101 manuel)
SORTIE    : affichage : reponse + latence mediane et p95 en ms
A RETENIR : Le p95 (95 % des appels plus rapides) montre la stabilite ressentie par les utilisateurs.
"""

import sys
import time
import statistics
import requests

port = sys.argv[1] if len(sys.argv) > 1 else '8100'
URL = f'http://127.0.0.1:{port}/invocations'   # le service local de MLflow
CORPS = {'dataframe_records': [{'montant': 8500.0, 'anciennete': 3,
                                'freq_24h': 9, 'nuit': 1}]}

r = requests.post(URL, json=CORPS, timeout=10)
print('reponse :', r.status_code, r.json())

for _ in range(10):                             # echauffement, non mesure
    requests.post(URL, json=CORPS, timeout=10)
lat = []
for _ in range(200):                            # 200 appels mesures
    t = time.perf_counter()
    requests.post(URL, json=CORPS, timeout=10)
    lat.append((time.perf_counter() - t) * 1000)

print(f'port {port} | mediane : {statistics.median(lat):.1f} ms'
      f' | p95 : {statistics.quantiles(lat, n=20)[18]:.1f} ms')

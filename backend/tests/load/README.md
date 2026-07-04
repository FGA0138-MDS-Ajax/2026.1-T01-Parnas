# Teste de carga (Locust)

Teste de carga do endpoint de simulacao de credito (`POST .../simulations/calculate`),
correspondente ao caso TS-27 do roteiro.

## Como rodar

```bash
pip install locust

# 1. semear o banco (usuario + empresa de teste)
export DATABASE_URL="sqlite:///$(pwd)/loadtest.db"
PYTHONPATH="$(pwd)" python tests/load/seed_loadtest.py

# 2. subir o backend (threaded, sem debug)
PYTHONPATH="$(pwd)" python -c "from app import create_app; create_app().run(port=5001, threaded=True)"

# 3. rodar a carga (50 usuarios, 2 min, headless)
locust -f tests/load/locustfile.py --host http://127.0.0.1:5001 \
       --users 50 --spawn-rate 5 --run-time 2m --headless
```

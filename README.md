## Start Svelte Frontend

```sh
npm run dev -- --port 5173 
```

## Start Python Backend

```sh
cd backend 
.venv/bin/python -m uvicorn main:app --reload --port 8000
```

´´´sh
python3 -m pip install pyperf
´´´

./.venv/bin/python run_benchmark.py --output bench_$(date +%Y%m%d_%H%M%S).json

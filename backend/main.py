from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import src.transform as transform
import src.normalise as norm
import data.problems as data

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/api/schemes')
def get_schemes():
    problems = data.get_problems()
    result = [transform.serialise_problem_data(problem_data) for problem_data in problems]
    
    return result


@app.post('/api/normalise')
def normalise(payload: dict):
    problem_data = transform.deserialise_problem_data(payload)
    problem_data = norm.normalise(problem_data)
    result = transform.serialise_problem_data(problem_data)

    return result


@app.post('/api/solve')
def solve(payload: dict):
    ...
   
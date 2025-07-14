from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import src.normalise as norm
import data.problems as data
import model.problem_data as pbd
import model.points as pts
from model.solver import Solver
from src.solver.solve import solve


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
    result = [pbd.serialise_problem_data(problem_data) for problem_data in problems]
    
    return result


@app.post('/api/normalise')
def normalise(payload: dict):
    problem_data = pbd.deserialise_problem_data(payload)
    problem_data = norm.normalise(problem_data)
    result = pbd.serialise_problem_data(problem_data)

    return result


@app.post('/api/solve')
def solve_(payload: dict):
    problem_data = pbd.deserialise_problem_data(payload['problem'])
    solver_type = Solver(payload['solver'])
    result = solve(problem_data, solver_type)

    if not result['result']:
        result['points'] = []
    else:
        result['points'] = pts.serialise_points(result['points'])
    return result

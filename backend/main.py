from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


import src.normalise as norm
import data.problems as data
import data.flat as flat
import data.comp as comp
from model.problem_data import ProblemData

app = FastAPI()


origins = [
    # "http://localhost:5173",
    "*",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/schemes")
def get_schemes():
    problems = data.get_problems()
    problems.append(flat.get_problem(50, 0.1))
    # problems.append(comp.get_problem(50, 0.1, 3))
    result = [problem_data.serialise() for problem_data in problems]

    return result


@app.post("/api/normalise")
def normalise(payload: dict):
    problem_data = ProblemData.deserialise(payload)

    # problem_data = norm.normalise(problem_data)
    result = problem_data.serialise()

    return result

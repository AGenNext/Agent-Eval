import json
import typer
from rich import print
from .runner import load_spec, run_eval

app = typer.Typer()

@app.command()
def run(spec_path: str):
    spec = load_spec(spec_path)
    predict = lambda x: x  # echo baseline
    result = run_eval(spec, predict)
    print(json.dumps(result.model_dump(), indent=2))

if __name__ == '__main__':
    app()

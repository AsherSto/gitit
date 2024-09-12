import typer
import subprocess
from PyInquirer import prompt, print_json, Separator
from rich import print as rprint
import utils

app = typer.Typer()

@app.command()
def hello():
    typer.echo(f"Hello world")

@app.command()
def gitit(repo_url: str):
    def sanitise_url(repo_url):
        if repo_url.endswith(".git"):
            return repo_url
        else:
            return repo_url + ".git"
    sanitised_url = sanitise_url(repo_url)
    utils.spin_up_vscode(sanitised_url)

if __name__ == "__main__":
    app()
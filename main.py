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
def gitit(repo_url: str, branch: str = typer.Option("main", help="The branch to clone"), docker: bool = typer.Option(False, help="Use Docker for setup")):
    def sanitise_url(repo_url):
        if repo_url.endswith(".git"):
            return repo_url
        else:
            return repo_url + ".git"
    sanitised_url = sanitise_url(repo_url)
    rprint(f"Sanitised URL: {sanitised_url}")
    rprint(f"Branch: {branch}")
    rprint(f"Docker: {docker}")
    utils.spin_up_vscode(sanitised_url, branch, docker)

if __name__ == "__main__":
    app()
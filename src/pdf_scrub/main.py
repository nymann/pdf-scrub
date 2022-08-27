from pathlib import Path

import typer

from pdf_scrub.pdf import PDF

app = typer.Typer()


@app.command()
def scrub(files: list[Path]) -> None:
    for pdf_file in files:
        pdf = PDF(pdf_file=pdf_file)
        for potential in pdf.scrub():
            typer.echo(potential)


if __name__ == "__main__":
    app()

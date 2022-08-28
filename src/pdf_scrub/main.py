from pathlib import Path

import typer

from pdf_scrub.pdf import PDF

app = typer.Typer()
CompressOption = typer.Option(default=True, help="Compress the final pdf to reduce file size greatly")


def save(index: int, potential: bytes, name: str) -> None:
    out = Path.cwd().joinpath(f"{index}-{name}")
    with open(file=out, mode="w+b") as output_file:
        output_file.write(potential)


@app.command()
def scrub(
    files: list[Path],
    compress: bool = CompressOption,
) -> None:
    for pdf_file in files:
        typer.echo(f"Scrubbing {pdf_file.name}")
        pdf = PDF(pdf_file=pdf_file)
        for index, potential in enumerate(pdf.scrub(compress=compress)):
            save(index=index, potential=potential, name=pdf_file.name)


if __name__ == "__main__":
    app()

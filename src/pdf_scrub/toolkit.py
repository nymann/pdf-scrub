from pathlib import Path
import subprocess  # noqa: S404
from typing import Iterable

from block_pruner import BlockPruner
from pdf_information import PDFInfo


def _pdftk(stdin: bytes, command: str) -> bytes:
    return subprocess.check_output(  # noqa: S603
        ["/usr/bin/pdftk", "-", "output", "-", command],
        input=stdin,
    )


def uncompress_pdf(pdf_file_buffer: bytes) -> bytes:
    return _pdftk(stdin=pdf_file_buffer, command="uncompress")


def decrypt_pdf(pdf_file: Path) -> bytes:
    return subprocess.check_output(["/usr/bin/qpdf", "--decrypt", pdf_file, "-"])  # noqa: S603


def compress_pdf(pdf_bytes: bytes) -> bytes:
    return _pdftk(stdin=pdf_bytes, command="compress")


def remove_metadata(pdf_bytes: bytes) -> bytes:
    return BlockPruner(
        start=r"<\?xpacket\ begin",
        end=r"<\?xpacket\ end",
        needle="DocumentID",
    ).prune_bytes(input_data=pdf_bytes)


def remove_watermark(pdf_bytes: bytes, needle: str) -> bytes:
    return BlockPruner(
        start=r"[0-9]+\ [0-9]+\ obj",
        end="endobj",
        needle=needle,
    ).prune_bytes(input_data=pdf_bytes)


def find_possible_watermark_needles(pdf_bytes: bytes, pdf_info: PDFInfo) -> Iterable[str]:
    if pdf_info.pages is None:
        raise ValueError("Cannot find watermark if pages is none")
    possibilities: dict[str, int] = {}
    for raw_line in pdf_bytes.splitlines(keepends=False):
        line = utf8_or_space(raw_line)
        if "/Length" not in line:
            continue
        try:
            possibilities[line] += 1
        except KeyError:
            possibilities[line] = 1
    yield from (needle for needle, count in possibilities.items() if count == pdf_info.pages)


def utf8_or_space(line: bytes) -> str:
    try:
        return line.decode()
    except UnicodeDecodeError:
        return ""

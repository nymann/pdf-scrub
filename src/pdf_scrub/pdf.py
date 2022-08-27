from pathlib import Path
import subprocess
from typing import Iterable

from block_pruner import BlockPruner
from pdf_information import PDFInfo


class PDF:
    def __init__(self, pdf_file: Path) -> None:
        self.pdf_file = pdf_file
        self.scrubbed = pdf_file
        self.info = PDFInfo.from_cmd(pdf_file=pdf_file)

    def scrub(self) -> Iterable[Path]:
        if self.info.encrypted:
            self.scrubbed = self._decrypt()
        self.scrubbed = self._uncompress()
        self.scrubbed = self._remove_metadata()
        for index, possibility in enumerate(self._find_possible_watermarks()):
            needle: str = possibility.strip("\n")
            potential = self._remove_potential_watermark(needle=needle, attempt=index)
            yield self._compress(potential=potential)

    def _remove_metadata(self) -> Path:
        block_pruner = BlockPruner(start=r"[0-9]+\ [0-9]+\ obj", end="endobj", needle=r"DocumentID")
        remove_metadata = block_pruner.prune_file(self.scrubbed)
        out = self.scrubbed.parent.joinpath(f"{self.scrubbed.name}.no_metadata")
        with open(out, "w+b") as output_file:
            output_file.write(remove_metadata)
        return out

    def _remove_potential_watermark(self, needle: str, attempt: int) -> Path:
        block_pruner = BlockPruner(start=r"[0-9]+\ [0-9]+\ obj", end="endobj", needle=needle)
        out = self.scrubbed.parent.joinpath(f"{self.scrubbed.name}.{attempt}")

        potential = block_pruner.prune_file(self.scrubbed)
        with open(out, "w+b") as output_file:
            output_file.write(potential)
        return out

    def _decrypt(self) -> Path:
        out = Path(f"/tmp/{self.scrubbed.name}.decrypted")
        subprocess.check_call(
            [
                "qpdf",
                "--decrypt",
                self.scrubbed,
                out,
            ],
        )
        return out

    def _compress(self, potential: Path) -> Path:
        out = Path(f"/tmp/{potential.name}.compressed")
        subprocess.check_call(
            [
                "pdftk",
                potential,
                "output",
                out,
                "compress",
            ],
        )
        return out

    def _uncompress(self) -> Path:
        out = Path(f"/tmp/{self.scrubbed.name}.uncompressed")
        subprocess.check_call(
            [
                "pdftk",
                self.scrubbed,
                "output",
                out,
                "uncompress",
            ],
        )
        return out

    def _find_possible_watermarks(self) -> Iterable[str]:
        if self.info.pages is None:
            raise ValueError("Cannot find watermark if pages is none")
        possibilities: dict[str, int] = {}
        with open(file=self.scrubbed, mode="rb") as decrypted_file:
            for raw_line in decrypted_file:
                line = utf8_or_space(raw_line)
                if "/Length" not in line:
                    continue
                try:
                    possibilities[line] += 1
                except KeyError:
                    possibilities[line] = 1
        for key, val in possibilities.items():
            if val == self.info.pages:
                yield key


def utf8_or_space(line: bytes) -> str:
    try:
        return line.decode()
    except UnicodeDecodeError:
        return ""

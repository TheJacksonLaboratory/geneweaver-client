"""Convert data files."""
from enum import Enum
from pathlib import Path
from typing import List

import typer
from geneweaver.client.utils.cli.prompt.pydantic import prompt_for_missing_fields
from geneweaver.core.parse import xlsx
from geneweaver.core.parse.utils import get_file_type
from geneweaver.core.render.batch import format_batch_file
from geneweaver.core.schema.batch import BatchUploadGeneset
from geneweaver.core.schema.gene import GeneValue
from pydantic import ValidationError
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing_extensions import Annotated


class CovertFileType(str, Enum):
    """Enum for file types."""

    CSV = "csv"
    BATCH = "gw"


def convert(
    file_path: Path,
    value_header: Annotated[str, typer.Option(prompt=True)],
    to: CovertFileType = CovertFileType.BATCH,
    id_header: str = "symbol",
) -> None:
    """Convert files from one format to another."""
    file_type = get_file_type(file_path)
    out_file = file_path.with_suffix(f".{to.value}")
    print(f"Converting {file_path} to {out_file}")

    genesets = []

    if file_type == "xlsx":
        genesets = _convert_excel(file_path, id_header, value_header)

    with open(out_file, "w") as f:
        f.write(format_batch_file(genesets))

        print(f"Converted {file_path} to {out_file}")


def _convert_excel(
    file_path: Path, id_header: str, value_header: str
) -> List[BatchUploadGeneset]:
    """Convert an Excel file to a batch file."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Loading document...", total=None)
        data = _parse_excel(file_path)

    file_name = file_path.name.split(".")[0]
    genesets = []

    for sheet_name, _header, sheet_metadata, sheet_data in data:
        print("Working on sheet:", sheet_name)
        gs_name = f"{file_name} - {sheet_name}"
        gs_abbreviation = gs_name.replace(" ", "").replace("-", "_").capitalize()
        gs_description = gs_name + " " + ", ".join(sheet_metadata)
        geneset = _build_geneset(
            name=gs_name, abbreviation=gs_abbreviation, description=gs_description
        )
        geneset.values = _parse_gene_list(  # noqa: PD011
            sheet_data, id_header, value_header
        )
        genesets.append(geneset)

    return genesets


def _parse_excel(file_path: Path) -> List[tuple]:
    """Parse an Excel file.

    :param file_path: The file path to the Excel file.
    :returns: A list of tuples containing the sheet name, headers, metadata, and data.
    """
    sheet_names = xlsx.get_sheet_names(file_path)

    headers, headers_idx = [], []
    for s in sheet_names:
        h, h_idx = xlsx.get_headers(file_path, sheet_name=s)
        headers.append(h)
        headers_idx.append(h_idx)

    sheet_metadata = [
        xlsx.read_metadata(file_path, header_idx, sheet_name=sheet)
        for sheet, header_idx in zip(sheet_names, headers_idx)  # noqa: B905
    ]

    data = [
        xlsx.read_to_dict(file_path, header_idx, sheet_name=sheet)
        for sheet, header_idx in zip(sheet_names, headers_idx)  # noqa: B905
    ]

    return zip(sheet_names, headers, sheet_metadata, data)  # noqa: B905


def _parse_gene_list(
    data: List[dict], id_header: str, value_header: str
) -> List[GeneValue]:
    """Parse a list of genes from a data file.

    :param data: A list of dictionaries representing the data from a data file.
    :param id_header: The name of the column containing the gene IDs.
    :param value_header: The name of the column containing the gene values.
    :returns: A list of GeneValue instances.
    """
    gene_list = []

    for row in data:
        try:
            j = GeneValue(symbol=row[id_header], value=row[value_header])
            gene_list.append(j)
        except ValidationError:
            continue

    return gene_list


def _build_geneset(**kwargs: str) -> BatchUploadGeneset:
    """Build a geneset from kwargs and by prompting for missing fields.

    :param kwargs: Keyword arguments to pass to the BatchUploadGeneset constructor.
    :returns: A BatchUploadGeneset instance.
    """
    geneset_args = prompt_for_missing_fields(
        BatchUploadGeneset, kwargs, exclude={"values"}
    )

    batch_upload = BatchUploadGeneset(values=[], **geneset_args)

    return batch_upload

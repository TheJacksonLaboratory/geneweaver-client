"""A module for parsing batch files."""

import csv
from pathlib import Path
from typing import Dict, List, Optional

from geneweaver.core.parse import batch
from geneweaver.core.schema.batch import BatchUploadGeneset


def to_csv(
    batch_file: Path,
    output_directory: Optional[Path] = None,
    prefix: Optional[str] = None,
    geneset_ids: Optional[List[str]] = None,
    read_file: bool = True,
) -> Optional[List[Path]]:
    """Convert a batch file to a CSV file.

    :param batch_file: The path to the batch file.
    :param output_directory: The directory to write the CSV file to. If not provided,
    :param prefix: A prefix to add to the CSV file name.
    :param geneset_ids: A list of geneset IDs to use for the CSV file names.
    the CSV file will be written to the current working directory.
    """
    if read_file:
        with open(batch_file, "r") as f:
            contents = f.read()
    else:
        contents = batch_file

    genesets = batch.process_lines(contents)

    csv_files = [
        write_geneset_to_csv(geneset, None, output_directory, prefix, gs_id)
        for geneset, gs_id in zip(genesets, geneset_ids)  # noqa: B905
    ]

    return csv_files


def to_csv_indexed(
    batch_file: Path, index_file: Path, output_directory: Optional[Path] = None
) -> List[Path]:
    """Convert a batch file to a CSV file, using the index file to name the CSV files.

    :param batch_file: The path to the batch file.
    :param index_file: The path to the index file.
    :param output_directory: The directory to write the CSV file to. If not provided,
    the CSV file will be written to the current working directory.
    :return: A list of the paths to the created CSV files.
    """
    index_data = read_index_file(index_file)

    with open(batch_file, "r") as f:
        contents = f.read()

    genesets = batch.process_lines(contents)

    filenames = []

    for geneset in genesets:
        try:
            index = index_data["GW Name"].index(geneset.name)
            disease = index_data["disease name"][index].lower().replace(" ", "_")
            gs_id = index_data["GW gene set id"][index]
            uberon_id = index_data["UBERON id"][index]
            filename = write_geneset_to_csv(
                geneset, uberon_id, output_directory, disease, gs_id
            )
            filenames.append(filename)
        except ValueError:
            print(f"Could not find geneset {geneset.name} in index file")
            continue

    return filenames


def read_index_file(index_file: Path) -> Dict[str, List[str]]:
    """Read the index file and return a dictionary of lists.

    :param index_file: The path to the index file.
    :return: A dictionary of lists.
    """
    with open(index_file, "r", errors="replace") as tsvfile:
        header = next(tsvfile).strip().split("\t")
        data_dict = {col: [] for col in header}

    # Read the TSV file and populate the lists in the dictionary
    with open(index_file, "r", errors="replace") as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter="\t")

        for row in reader:
            for col in header:
                data_dict[col].append(row[col])

    return data_dict


def _index_of_geneset(name: str, index_data: Dict[str, List[str]]) -> int:
    return index_data["name"].index(name)


def write_geneset_to_csv(
    geneset: BatchUploadGeneset,
    uberon_id: Optional[str] = None,
    output_directory: Optional[Path] = None,
    prefix: Optional[str] = None,
    gs_id: Optional[str] = None,
    hash_header: bool = False,
) -> Path:
    """Write a geneset to a CSV file.

    :param geneset: The geneset to write to a CSV file.
    :param uberon_id: The UBERON ID of the geneset.
    :param output_directory: The directory to write the CSV file to. If not provided,
    the CSV file will be written to the current working directory.
    :param prefix: A prefix to add to the CSV file name.
    :param gs_id: The ID of the geneset.
    :param hash_header: Whether to prefix the header with a hash.
    :return: The name of the CSV file.
    """
    if not gs_id:
        filename = geneset.abbreviation.replace(" ", "_").lower() + ".csv"
    else:
        filename = gs_id + ".csv"

    if prefix:
        filename = prefix + "_" + filename

    filename = Path(filename)

    header_prefix = "#" if hash_header else ""

    output_path = output_directory / filename if output_directory else filename
    header = [
        (f"{header_prefix}{key}", value)
        for key, value in geneset.dict(exclude={"values"}).items()
    ]
    header.append((f"{header_prefix}uberon_id", uberon_id))
    geneset_values = [
        (value.symbol, value.value) for value in geneset.values  # noqa: PD011
    ]

    # Write headers to a CSV file
    with open(output_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(header)
        writer.writerow(("gene_id", "value"))
        writer.writerows(geneset_values)

    return filename

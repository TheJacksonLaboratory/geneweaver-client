"""CLI for manipulating and parsing batch data files."""

from pathlib import Path
from typing import List, Optional

import requests
import typer
from geneweaver.client.parser import batch
from geneweaver.core.parse.exceptions import InvalidBatchValueLineError
from pydantic import ValidationError

cli = typer.Typer()


@cli.command()
def to_csv(
    batch_file: Path,
    output_directory: Optional[Path] = None,
    prefix: Optional[str] = None,
    geneset_ids: Optional[List[str]] = None,
) -> None:
    """Export a batch file as a csv file.

    :param batch_file: The batch file to create the csv file from.
    :param output_directory: The output directory to write the csv file to.
                             (default: current working directory)
    :param prefix: A prefix to apply to the csv filename.
    :param geneset_ids: The geneset ids that match those in the batch file (in order).
    :return: The path to the csv file.
    """
    output_files = batch.to_csv(batch_file, output_directory, prefix, geneset_ids)

    for file in output_files:
        print(f"Created {file}")


@cli.command()
def to_csv_indexed(
    batch_file: Path, index_file: Path, output_directory: Optional[Path] = None
) -> list:
    """Export a batch file as a csv file, using the index file to name the csv files.

    (This is experimental)

    :param batch_file: The batch file to create the csv file from.
    :param index_file: The index file to use to name the csv files.
    :param output_directory: Where to write the csv files to.
                             (default: current working directory)
    :return: A list of the paths to the created csv files.
    """
    output_files = batch.to_csv_indexed(batch_file, index_file, output_directory)

    for file in output_files:
        print(f"Created {file}")

    return output_files


@cli.command()
def download_genesets(
    index_file: Path,
    session: str,
    output_directory: Optional[Path] = None,
    hash_header: bool = False,
) -> None:
    """Download genesets from the Geneweaver API.

    (experimental)
    :param index_file: The index file to use to name the csv files.
    :param session: The session cookie to use to authenticate with the Geneweaver API.
    :param output_directory: Where to write the csv files to.
    :param hash_header: Whether to hash the header of the csv files.
    :return: None
    """
    # URL of the Flask app
    base_url = "https://geneweaver.org"

    index_data = batch.read_index_file(index_file)
    genesets = {}
    output_files = []
    skipped = []
    with requests.Session() as s:
        s.cookies.set("session", session)

        for index, gsid in enumerate(index_data["GW gene set id"]):
            if gsid != "NA":
                disease = index_data["disease name"][index].lower().replace(" ", "_")
                response = s.get(f"{base_url}/exportBatch/{gsid[2:]}")
                if response.ok:
                    print(f"Found {gsid}")
                    genesets[gsid] = response.text
                    try:
                        geneset = batch.batch.process_lines(genesets[gsid])[0]
                    except (ValidationError, InvalidBatchValueLineError) as e:
                        print(f"Failed parsing {gsid}")
                        skipped.append(gsid)
                        print(e)
                    output_files.append(
                        batch.write_geneset_to_csv(
                            geneset,
                            index_data["UBERON id"][index],
                            output_directory,
                            disease,
                            gsid,
                            hash_header=hash_header,
                        )
                    )
                else:
                    print(f"Skipping {gsid}")
                    skipped.append(gsid)

    # TODO: Cocaine related sets not in the index file
    # with requests.Session() as s:
    #
    #     for gs in range(407450, 407481):
    #         if response.ok:
    #             output_files.append(batch.write_geneset_to_csv(
    #                 geneset, None, output_directory, 'cocaine', f'GS{gs}')

    for output_file in output_files:
        print(f"Created {output_file}")

    for skip in skipped:
        print(f"Skipped {skip}")

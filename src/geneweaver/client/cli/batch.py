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
    print(geneset_ids)

    output_files = batch.to_csv(batch_file, output_directory, prefix, geneset_ids)

    for file in output_files:
        print(f"Created {file}")


@cli.command()
def to_csv_indexed(
    batch_file: Path, index_file: Path, output_directory: Optional[Path] = None
) -> None:
    output_files = batch.to_csv_indexed(batch_file, index_file, output_directory)

    for file in output_files:
        print(f"Created {file}")


@cli.command()
def download_genesets(
    index_file: Path,
    session: str,
    output_directory: Optional[Path] = None,
    hash_header: bool = False,
) -> None:
    # URL of the Flask app
    BASE_URL = "https://geneweaver.org"

    index_data = batch.read_index_file(index_file)
    genesets = {}
    output_files = []
    skipped = []
    with requests.Session() as s:
        s.cookies.set("session", session)

        for index, gsid in enumerate(index_data["GW gene set id"]):
            if gsid != "NA":
                disease = index_data["disease name"][index].lower().replace(" ", "_")
                response = s.get(f"{BASE_URL}/exportBatch/{gsid[2:]}")
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

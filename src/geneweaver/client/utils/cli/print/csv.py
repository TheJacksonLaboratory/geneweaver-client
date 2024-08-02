"""A module to format data as a csv file."""

import csv
import io
from typing import Any, Dict, List


def format_csv(data: List[Dict[str, Any]], with_header: bool = False) -> str:
    """Format a list of dictionaries as a csv file.

    :param data: A list of dictionaries to format as a csv file.
    :param with_header: Whether to include the header in the csv file.

    :return: A string formatted as a csv file.
    """
    if len(data) == 0:
        return ""

    csv_data = io.StringIO()
    writer = csv.DictWriter(csv_data, fieldnames=data[0].keys())
    if with_header:
        writer.writeheader()
    writer.writerows(data)

    return csv_data.getvalue()

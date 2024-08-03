"""Utilities for AON interaction."""


def map_symbols(starting: dict, mappings: list) -> dict:
    """Map gene symbols using a list of mappings."""
    # TODO: Improve the signature of this function.
    mapped_values = {}
    for mapping in mappings:
        source = mapping["from_gene"]
        target = mapping["to_gene"]
        value = starting.get(source, 0)

        if target not in mapped_values or abs(value) > abs(mapped_values[target]):
            mapped_values[target] = value

    return mapped_values

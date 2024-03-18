"""Dataset definition for NCI60's: DNA__Combined_aCGH_gene_summary.xls."""

import pandas as pd
from geneweaver.client.datasets.base import BaseDataset


class DNACombinedaCGHGeneSummary(BaseDataset):
    """Dataset definition for NCI60's: DNA__Combined_aCGH_gene_summary.xls."""

    URL = (
        "https://discover.nci.nih.gov/cellminer/download/processeddataset/"
        "nci60_DNA__Combined_aCGH_gene_summary.zip"
    )
    DS_FOLDER = "nci60_DNA__Combined_aCGH_gene_summary"
    UNZIPPED_LOC = "output/DNA__Combined_aCGH_gene_summary.xls"
    LINKOUT = "https://discover.nci.nih.gov/cellminer/loadDownload.do"

    def __init__(self, base_folder: str = "data") -> None:
        """Initialize the DNACombinedaCGHGeneSummary dataset."""
        super().__init__(base_folder)
        self.download_zip_file()
        self.dataset_skip_rows = 10
        self._pandas_read_f = pd.read_excel

    @property
    def entrez_ids(self) -> pd.DataFrame:
        """Return the dataset's entrez ids."""
        return self.as_pandas().iloc[:, 1]

    @property
    def gene_names(self) -> pd.DataFrame:
        """Return the dataset's gene names."""
        return self.as_pandas().iloc[:, 0]

    @property
    def intensity(self) -> pd.DataFrame:
        """Return the dataset's intensity values."""
        intensity = self.as_pandas().iloc[:, 6:]
        intensity = intensity.replace("-", 0)
        return intensity

    @property
    def intensity_type(self) -> str:
        """Return the dataset's intensity type."""
        return (
            "Average log2 intensity values of the ratio of the cell line "
            "DNA with respect to normal DNA."
        )

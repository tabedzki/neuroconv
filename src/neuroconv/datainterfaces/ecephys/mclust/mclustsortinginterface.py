from typing import Optional

from neuroconv.utils import FolderPathType
from ..basesortingextractorinterface import BaseSortingExtractorInterface


class MClustSortingInterface(BaseSortingExtractorInterface):
    """Data interface class for converting MClust data. Uses
    :py:class:`~spikeinterface.extractors.MClustSortingExtractor`."""

    def __init__(
        self,
        folder_path: FolderPathType,
        sampling_frequency: float,
        sampling_frequency_raw: Optional[float] = None,
        verbose: bool = True,
    ):
        """
        Initialize an MClustSortingInterface.

        Parameters
        ----------
        folder_path : str or Path
        sampling_frequency : float
        sampling_frequency_raw : float, optional
        verbose : bool, default: True
        """
        super().__init__(
            folder_path=folder_path,
            sampling_frequency=sampling_frequency,
            sampling_frequency_raw=sampling_frequency_raw,
            verbose=verbose,
        )

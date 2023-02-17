"""Authors: Szonja Weigl, Cody Baker."""
from typing import Optional

from ..baserecordingextractorinterface import BaseRecordingExtractorInterface
from ....utils import FolderPathType, get_schema_from_method_signature


class OpenEphysLegacyRecordingInterface(BaseRecordingExtractorInterface):
    """Primary data interface for converting legacy Open Ephys data (.continuous files).
    Uses :py:class:`~spikeinterface.extractors.OpenEphysLegacyRecordingExtractor`."""

    ExtractorName = "OpenEphysLegacyRecordingExtractor"

    @classmethod
    def get_source_schema(cls):
        """Compile input schema for the RecordingExtractor."""
        source_schema = get_schema_from_method_signature(
            class_method=cls.__init__,
            exclude=["stream_name", "block_index", "all_annotations"],
        )
        source_schema["properties"]["folder_path"][
            "description"
        ] = "Path to directory containing OpenEphys legacy files."
        return source_schema

    def __init__(
        self,
        folder_path: FolderPathType,
        stream_name: Optional[str] = "Signals CH",
        block_index: Optional[int] = None,
        all_annotations: Optional[bool] = True,
        verbose: bool = True,
    ):
        """
        Initialize reading of OpenEphys legacy recording (.continuous files).
        See :py:class:`~spikeinterface.extractors.OpenEphysLegacyRecordingExtractor` for options.

        Parameters
        ----------
        folder_path : FolderPathType
            Path to OpenEphys directory.
        stream_name : str, default: "Signals CH"
            The name of the recording stream.
            When the recording stream is not specified the channel stream is chosen if available.
            When channel stream is not available the name of the stream must be specified.
        block_index : int, default: None
        all_annotations : bool, default: True
        stub_test : bool, default: False
        verbose : bool, default: True
        """

        super().__init__(
            folder_path=folder_path,
            stream_name=stream_name,
            block_index=block_index,
            all_annotations=all_annotations,
            verbose=verbose,
        )

    def get_metadata(self):
        """Auto-fill as much of the metadata as possible. Must comply with metadata schema."""
        import pyopenephys

        metadata = super().get_metadata()

        folder_path = self.source_data["folder_path"]
        fileobj = pyopenephys.File(foldername=folder_path)
        session_start_time = fileobj.experiments[0].datetime

        metadata["NWBFile"].update(session_start_time=session_start_time)
        return metadata

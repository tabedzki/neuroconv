from pathlib import Path
from typing import Optional

from pynwb import NWBFile

from .... import BaseDataInterface
from ....tools import get_package
from ....utils import DeepDict, FolderPathType


class MiniscopeBehaviorInterface(BaseDataInterface):
    """Data Interface for Miniscope behavior data."""

    def __init__(self, folder_path: FolderPathType):
        """
        Initialize reading recordings from the Miniscope behavioral camera.

        Parameters
        ----------
        folder_path : FolderPathType
            The path that points to the main Miniscope folder.
            The movie files are expected to be in sub folders within the main folder.
        """
        natsort = get_package(package_name="natsort", installation_instructions="pip install natsort")
        self._ndx_miniscope = get_package(
            package_name="ndx_miniscope", installation_instructions="pip install ndx-miniscope"
        )

        super().__init__(folder_path=folder_path)

        folder_path = Path(self.source_data["folder_path"])
        self._behav_avi_file_paths = natsort.natsorted(list(folder_path.glob("*/BehavCam*/*.avi")))
        assert (
            self._behav_avi_file_paths
        ), f"The behavior movies (.avi files) are missing from '{self.source_data['folder_path']}'."
        # note we might have to change this if we have other examples
        configuration_file_name = "metaData.json"
        miniscope_config_files = natsort.natsorted(list(folder_path.glob(f"*/BehavCam*/{configuration_file_name}")))
        assert (
            miniscope_config_files
        ), f"The configuration files ({configuration_file_name} files) are missing from '{self.folder_path}'."

        behavcam_subfolders = list(folder_path.glob(f"*/BehavCam*/"))
        self._miniscope_config = self._ndx_miniscope.utils.read_miniscope_config(
            folder_path=str(behavcam_subfolders[0])
        )

        self._recording_start_times = self._ndx_miniscope.utils.get_recording_start_times(folder_path=str(folder_path))
        self._starting_frames = self._ndx_miniscope.utils.get_starting_frames(folder_path=str(folder_path))
        assert len(self._starting_frames) == len(self._behav_avi_file_paths)
        self._timestamps = self._ndx_miniscope.utils.get_timestamps(
            folder_path=str(folder_path), file_pattern="BehavCam*/timeStamps.csv"
        )

    def get_metadata(self) -> DeepDict:
        metadata = super().get_metadata()
        metadata["NWBFile"].update(session_start_time=self._recording_start_times[0])

        metadata["Behavior"]["Device"] = [self._miniscope_config]
        # Add link to Device for ImageSeries
        metadata["Behavior"]["ImageSeries"] = [
            dict(
                name="BehavCamImageSeries",
                device=self._miniscope_config["name"],
                dimension=[self._miniscope_config["ROI"]["width"], self._miniscope_config["ROI"]["height"]],
                unit="px",
            )
        ]

        return metadata

    def add_to_nwbfile(
        self,
        nwbfile: NWBFile,
        metadata: Optional[dict] = None,
    ):
        self._ndx_miniscope.utils.add_miniscope_image_series(
            nwbfile=nwbfile,
            metadata=metadata,
            external_files=[str(file_path) for file_path in self._behav_avi_file_paths],
            starting_frames=self._starting_frames,
            timestamps=self._timestamps,
        )

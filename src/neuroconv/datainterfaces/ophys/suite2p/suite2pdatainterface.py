from copy import deepcopy
from typing import Optional

from ..basesegmentationextractorinterface import BaseSegmentationExtractorInterface
from ....utils import DeepDict, FolderPathType


def _update_metadata_with_new_imaging_plane_name(metadata: dict, imaging_plane_name: str) -> DeepDict:
    """Private utility function to update the metadata with a new imaging plane name."""
    metadata_copy = deepcopy(metadata)

    imaging_plane_metadata = metadata_copy["Ophys"]["ImagingPlane"][0]
    plane_name_suffix = imaging_plane_name.replace("ImagingPlane", "")
    imaging_plane_metadata.update(name=imaging_plane_name)
    plane_segmentation_metadata = metadata_copy["Ophys"]["ImageSegmentation"]["plane_segmentations"][0]
    default_plane_segmentation_name = plane_segmentation_metadata["name"]
    default_plane_suffix = default_plane_segmentation_name.replace("PlaneSegmentation", "")
    plane_segmentation_name = "PlaneSegmentation" + plane_name_suffix
    plane_segmentation_metadata.update(
        name=plane_segmentation_name,
        imaging_plane=imaging_plane_name,
    )

    fluorescence_metadata_per_plane = metadata_copy["Ophys"]["Fluorescence"].pop(default_plane_segmentation_name)
    # override the default name of the plane segmentation
    metadata_copy["Ophys"]["Fluorescence"][plane_segmentation_name] = fluorescence_metadata_per_plane
    trace_names = [property_name for property_name in fluorescence_metadata_per_plane.keys() if property_name != "name"]
    for trace_name in trace_names:
        default_raw_traces_name = fluorescence_metadata_per_plane[trace_name]["name"].replace(default_plane_suffix, "")
        fluorescence_metadata_per_plane[trace_name].update(name=default_raw_traces_name + plane_name_suffix)

    segmentation_images_metadata = metadata_copy["Ophys"]["SegmentationImages"].pop(default_plane_segmentation_name)
    metadata_copy["Ophys"]["SegmentationImages"][plane_segmentation_name] = segmentation_images_metadata
    metadata_copy["Ophys"]["SegmentationImages"][plane_segmentation_name]["correlation"].update(
        name=f"CorrelationImage{plane_name_suffix}",
    )
    metadata_copy["Ophys"]["SegmentationImages"][plane_segmentation_name].update(
        dict(mean=dict(name=f"MeanImage{plane_name_suffix}"))
    )

    return metadata_copy


class Suite2pSegmentationInterface(BaseSegmentationExtractorInterface):
    """Data interface for Suite2pSegmentationExtractor."""

    @classmethod
    def get_available_planes(cls, folder_path: FolderPathType) -> dict:
        from roiextractors import Suite2pSegmentationExtractor

        return Suite2pSegmentationExtractor.get_available_planes(folder_path=folder_path)

    @classmethod
    def get_available_channels(cls, folder_path: FolderPathType) -> dict:
        from roiextractors import Suite2pSegmentationExtractor

        return Suite2pSegmentationExtractor.get_available_channels(folder_path=folder_path)

    def __init__(
        self,
        folder_path: FolderPathType,
        channel_name: Optional[str] = None,
        plane_name: Optional[str] = None,
        verbose: bool = True,
        combined: Optional[bool] = False,  # TODO: to be removed
        plane_no: Optional[int] = None,  # TODO: to be removed
    ):
        """

        Parameters
        ----------
        folder_path : FolderPathType
        channel_name: str, optional
            The name of the channel to load, to determine what channels are available use Suite2pSegmentationInterface.get_available_channels(folder_path).
        plane_name: str, optional
            The name of the plane to load, to determine what planes are available use Suite2pSegmentationInterface.get_available_planes(folder_path).

        """

        super().__init__(folder_path=folder_path, channel_name=channel_name, plane_name=plane_name)
        self.channel_name = self.segmentation_extractor.channel_name
        self.plane_name = self.segmentation_extractor.plane_name
        self.verbose = verbose

    def get_metadata(self) -> DeepDict:
        metadata = super().get_metadata()

        available_planes = self.get_available_planes(folder_path=self.source_data["folder_path"])
        available_channels = self.get_available_channels(folder_path=self.source_data["folder_path"])
        if len(available_planes) == 1 and len(available_channels) == 1:
            return metadata

        plane_name_suffix = f"{self.channel_name.capitalize()}{self.plane_name.capitalize()}"
        imaging_plane_metadata = metadata["Ophys"]["ImagingPlane"][0]
        imaging_plane_name = imaging_plane_metadata["name"] + plane_name_suffix
        metadata = _update_metadata_with_new_imaging_plane_name(
            metadata=metadata, imaging_plane_name=imaging_plane_name
        )

        return metadata

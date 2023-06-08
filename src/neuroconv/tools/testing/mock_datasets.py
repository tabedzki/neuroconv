"""
Convenience functions for generating fake datasets for testing NeuroConv and the NWB GUIDE.

Utilizes various files that must be downloaded from the corresponding GIN repositories.
"""
import os
from pathlib import Path
from shutil import copytree

from pydantic import DirectoryPath


def generate_mock_ecephys_dataset(
    ephy_testing_data_folder_path: DirectoryPath, mock_dataset_folder_path: DirectoryPath
):
    """
    A helper function that generates a subfolder at the target location containing a mock dataset with ecephys formats.

    Parameters
    ----------
    ephy_testing_data_folder_path : DirectoryPath
        Local path of the GIN repository 'ephy_testing_data' on the local system.
    mock_dataset_folder_path : DirectoryPath
        Target destination at which to generate the fake dataset.
    """
    ephy_base_path = Path(ephy_testing_data_folder_path)
    mock_dataset_folder_path = Path(mock_dataset_folder_path) / "mock_ecephys_dataset"

    if mock_dataset_folder_path.exists():
        num_copies = len(
            [item for item in mock_dataset_folder_path.parent.glob("*") if "mock_ecephys_dataset" in item.name]
        )
        mock_dataset_folder_path = mock_dataset_folder_path.parent / f"mock_ecephys_dataset ({num_copies})"

    subjects = ["mouse1", "mouse2"]

    sessions = ["070623", "060623"]

    base_id = "Noise4Sam"

    for subject in subjects:
        for session in sessions:
            full_id = f"{subject}_{session}"
            session_output_directory = mock_dataset_folder_path / subject / full_id
            spikeglx_base_directory = ephy_base_path / "spikeglx" / f"{base_id}_g0"
            phy_base_directory = ephy_base_path / "phy" / "phy_example_0"

            # phy_base_directory.symlink_to(session_output_directory / f'{full_id}_phy', True)

            spikeglx_output_dir = session_output_directory / f"{full_id}_g0"
            phy_output_dir = session_output_directory / f"{full_id}_phy"

            copytree(spikeglx_base_directory, spikeglx_output_dir)

            # Rename directories
            for root, dirs, files in os.walk(spikeglx_output_dir):
                for dir in dirs:
                    if base_id in dir:
                        os.rename(os.path.join(root, dir), os.path.join(root, dir.replace(base_id, full_id)))

            # Rename files
            for root, dirs, files in os.walk(spikeglx_output_dir):
                for file in files:
                    if base_id in file:
                        os.rename(os.path.join(root, file), os.path.join(root, file.replace(base_id, full_id)))

            phy_output_dir.symlink_to(phy_base_directory, True)

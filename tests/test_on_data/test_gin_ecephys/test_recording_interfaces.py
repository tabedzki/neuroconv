from neuroconv.tools.testing.data_interface import AbstractRecordingInterfaceTest

from neuroconv.datainterfaces import AxonaRecordingInterface

try:
    from ..setup_paths import ECEPHY_DATA_PATH as DATA_PATH
    from ..setup_paths import OUTPUT_PATH
except ImportError:
    from setup_paths import ECEPHY_DATA_PATH as DATA_PATH
    from setup_paths import OUTPUT_PATH


class TestAxonRecordingInterface(AbstractRecordingInterfaceTest):
    data_interface_cls = AxonaRecordingInterface
    kwargs_cases = {
        "1": dict(file_path=str(DATA_PATH / "axona" / "axona_raw.bin")),
    }
    save_directory = OUTPUT_PATH

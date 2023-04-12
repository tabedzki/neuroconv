import shutil
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

import numpy as np
from dateutil.tz import gettz
from hdmf.testing import TestCase
from pynwb import NWBHDF5IO

from neuroconv import NWBConverter
from neuroconv.datainterfaces import VideoInterface

try:
    import cv2

    skip_test = False
except ImportError:
    skip_test = True


@unittest.skipIf(skip_test, "cv2 not installed")
class TestVideoInterface(TestCase):
    def setUp(self) -> None:
        self.test_dir = Path(tempfile.mkdtemp())
        self.video_files = self.create_videos()
        self.nwb_converter = self.create_video_converter()
        self.metadata = self.nwb_converter.get_metadata()
        self.metadata["NWBFile"].update(session_start_time=datetime.now(tz=gettz(name="US/Pacific")))
        self.nwbfile_path = self.test_dir / "video_test.nwb"
        self.starting_times = [0.0, 50.0]

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir)
        del self.nwb_converter

    def create_videos(self):
        video_file1 = str(self.test_dir / "test1.avi")
        video_file2 = str(self.test_dir / "test2.avi")
        number_of_frames = 30
        number_of_rows = 640
        number_of_columns = 480
        frameSize = (number_of_columns, number_of_rows)  # This is give in x,y images coordinates (x is columns)
        fps = 25
        # Standard code for specifying image formats
        fourcc_specification = ("M", "J", "P", "G")
        # Utility to transform the four code specification to OpenCV specification
        fourcc = cv2.VideoWriter_fourcc(*fourcc_specification)

        writer1 = cv2.VideoWriter(
            filename=video_file1,
            fourcc=fourcc,
            fps=fps,
            frameSize=frameSize,
        )
        writer2 = cv2.VideoWriter(
            filename=video_file2,
            fourcc=fourcc,
            fps=fps,
            frameSize=frameSize,
        )

        for frame in range(number_of_frames):
            writer1.write(np.random.randint(0, 255, (number_of_rows, number_of_columns, 3)).astype("uint8"))
            writer2.write(np.random.randint(0, 255, (number_of_rows, number_of_columns, 3)).astype("uint8"))

        writer1.release()
        writer2.release()

        return [video_file1, video_file2]

    def create_video_converter(self):
        class VideoTestNWBConverter(NWBConverter):
            data_interface_classes = dict(Video=VideoInterface)

        source_data = dict(Video=dict(file_paths=self.video_files))
        return VideoTestNWBConverter(source_data=source_data)


@unittest.skipIf(skip_test, "cv2 not installed")
class TestExternalVideoInterface(TestVideoInterface):
    def test_video_internal_mode_multiple_file_paths_error(self):
        conversion_opts = dict(Video=dict(external_mode=False))
        with self.assertRaisesWith(
            exc_type=ValueError,
            exc_msg="No timing information is specified and there are 2 total video files! "
            "Please specify the temporal alignment of each video.",
        ):
            self.nwb_converter.run_conversion(
                nwbfile_path=self.nwbfile_path,
                overwrite=True,
                conversion_options=conversion_opts,
                metadata=self.metadata,
            )

    def test_video_external_mode(self):
        timestamps = [np.array([2.2, 2.4, 2.6]), np.array([3.2, 3.4, 3.6])]
        interface = self.nwb_converter.data_interface_objects["Video"]
        interface.align_timestamps(aligned_timestamps=timestamps)
        interface.align_starting_times(starting_times=self.starting_times)

        conversion_options = dict(Video=dict(external_mode=True))
        self.nwb_converter.run_conversion(
            nwbfile_path=self.nwbfile_path,
            overwrite=True,
            conversion_options=conversion_options,
            metadata=self.metadata,
        )
        with NWBHDF5IO(path=self.nwbfile_path, mode="r") as io:
            nwbfile = io.read()
            module = nwbfile.acquisition
            metadata = self.nwb_converter.get_metadata()
            for index, video_metadata in enumerate(metadata["Behavior"]["Videos"]):
                video_interface_name = video_metadata["name"]
                print(module)
                assert module.external_file[0] == str(self.video_files[index])

    def test_video_duplicate_names_with_external_mode(self):
        conversion_options = dict(Video=dict(external_mode=True, starting_frames=[0, 4]))
        metadata = self.metadata
        video_interface_name = metadata["Behavior"]["Videos"][0]["name"]
        metadata["Behavior"]["Videos"][1]["name"] = video_interface_name
        self.nwb_converter.run_conversion(
            nwbfile_path=self.nwbfile_path,
            overwrite=True,
            conversion_options=conversion_options,
            metadata=metadata,
        )
        with NWBHDF5IO(path=self.nwbfile_path, mode="r") as io:
            nwbfile = io.read()
            mod = nwbfile.acquisition
            assert len(mod) == 1
            assert video_interface_name in mod
            assert len(mod[video_interface_name].external_file) == 2

    def test_video_irregular_timestamps(self):
        timestamps = [np.array([1, 2, 4]), np.array([5, 6, 7])]
        interface = self.nwb_converter.data_interface_objects["Video"]
        interface.align_timestamps(aligned_timestamps=timestamps)
        interface.align_starting_times(starting_times=self.starting_times)

        conversion_options = dict(Video=dict(external_mode=True))
        self.nwb_converter.run_conversion(
            nwbfile_path=self.nwbfile_path,
            overwrite=True,
            conversion_options=conversion_options,
            metadata=self.metadata,
        )

        with NWBHDF5IO(path=self.nwbfile_path, mode="r") as io:
            nwbfile = io.read()
            acquisition_module = nwbfile.acquisition
            metadata = self.nwb_converter.get_metadata()
            for video_metadata in metadata["Behavior"]["Videos"]:
                video_interface_name = video_metadata["name"]
                np.testing.assert_array_equal(timestamps, acquisition_module[video_interface_name].timestamps[:])

    def test_video_regular_timestamps(self):
        timestamps = [np.array([2.2, 2.4, 2.6]), np.array([3.2, 3.4, 3.6])]
        interface = self.nwb_converter.data_interface_objects["Video"]
        interface.align_timestamps(aligned_timestamps=timestamps)
        interface.align_starting_times(starting_times=self.starting_times)

        conversion_opts = dict(Video=dict(external_mode=True))
        expected_warn_msg = (
            "The fps=25 from video data is unequal to the difference in "
            "regular timestamps. Using fps=5 from timestamps instead."
        )
        with self.assertWarnsWith(warn_type=UserWarning, exc_msg=expected_warn_msg):
            self.nwb_converter.run_conversion(
                nwbfile_path=self.nwbfile_path,
                overwrite=True,
                conversion_options=conversion_opts,
                metadata=self.metadata,
            )

        with NWBHDF5IO(path=self.nwbfile_path, mode="r") as io:
            nwbfile = io.read()
            acquisition_module = nwbfile.acquisition
            metadata = self.nwb_converter.get_metadata()
            for video_metadata in metadata["Behavior"]["Videos"]:
                video_interface_name = video_metadata["name"]
                expected_rate = round(1 / (timestamps[1] - timestamps[0]), 2)
                assert acquisition_module[video_interface_name].rate == expected_rate
                assert acquisition_module[video_interface_name].timestamps is None

    def test_starting_frames_type_error(self):
        conversion_opts = dict(Video=dict(external_mode=True))
        metadata = self.metadata
        video_interface_name = metadata["Behavior"]["Videos"][0]["name"]
        metadata["Behavior"]["Videos"][1]["name"] = video_interface_name

        with self.assertRaisesWith(
            exc_type=TypeError,
            exc_msg="Multiple paths were specified for ImageSeries index 0, but no starting_frames were specified!",
        ):
            self.nwb_converter.run_conversion(
                nwbfile_path=self.nwbfile_path,
                overwrite=True,
                conversion_options=conversion_opts,
                metadata=metadata,
            )

    def test_starting_frames_value_error(self):
        conversion_opts = dict(Video=dict(external_mode=True, starting_frames=[[0]]))
        metadata = self.metadata
        video_interface_name = metadata["Behavior"]["Videos"][0]["name"]
        metadata["Behavior"]["Videos"][1]["name"] = video_interface_name

        with self.assertRaisesWith(
            exc_type=ValueError,
            exc_msg="Multiple paths (2) were specified for ImageSeries index 0, but the length of starting_frames (1) did not match the number of paths!",
        ):
            self.nwb_converter.run_conversion(
                nwbfile_path=self.nwbfile_path,
                overwrite=True,
                conversion_options=conversion_opts,
                metadata=metadata,
            )


@unittest.skipIf(skip_test, "cv2 not installed")
class TestInternalVideoInterface(TestVideoInterface):
    def create_video_converter(self):
        class VideoTestNWBConverter(NWBConverter):
            data_interface_classes = dict(Video=VideoInterface)

        source_data = dict(Video=dict(file_paths=[self.video_files[0]]))
        return VideoTestNWBConverter(source_data=source_data)

    def test_save_video_to_custom_module(self):
        module_name = "TestModule"
        module_description = "This is a test module."
        conversion_opts = dict(
            Video=dict(
                external_mode=False,
                module_name=module_name,
                module_description=module_description,
            )
        )
        self.nwb_converter.run_conversion(
            nwbfile_path=self.nwbfile_path,
            overwrite=True,
            conversion_options=conversion_opts,
            metadata=self.metadata,
        )
        with NWBHDF5IO(path=self.nwbfile_path, mode="r") as io:
            nwbfile = io.read()
            assert module_name in nwbfile.processing
            assert module_description == nwbfile.processing[module_name].description

    def test_video_chunking(self):
        conversion_options = dict(Video=dict(external_mode=False, stub_test=True, chunk_data=False))
        self.nwb_converter.run_conversion(
            nwbfile_path=self.nwbfile_path,
            overwrite=True,
            conversion_options=conversion_options,
            metadata=self.metadata,
        )

        with NWBHDF5IO(path=self.nwbfile_path, mode="r") as io:
            nwbfile = io.read()
            mod = nwbfile.acquisition
            metadata = self.nwb_converter.get_metadata()
            for video_metadata in metadata["Behavior"]["Videos"]:
                video_interface_name = video_metadata["name"]
                assert mod[video_interface_name].data.chunks is not None  # TODO retrieve storage_layout of hdf5 dataset

    def test_video_stub(self):
        timestamps = [np.array([1, 2, 4, 5, 6, 7, 8, 9, 10, 11])]
        interface = self.nwb_converter.data_interface_objects["Video"]
        interface.align_timestamps(aligned_timestamps=timestamps)
        interface.align_starting_times(starting_times=[self.starting_times[0]])

        conversion_options = dict(Video=dict(external_mode=False, stub_test=True))
        self.nwb_converter.run_conversion(
            nwbfile_path=self.nwbfile_path,
            overwrite=True,
            conversion_options=conversion_options,
            metadata=self.metadata,
        )
        with NWBHDF5IO(path=self.nwbfile_path, mode="r") as io:
            nwbfile = io.read()
            mod = nwbfile.acquisition
            metadata = self.nwb_converter.get_metadata()
            for video_index in range(len(metadata["Behavior"]["Videos"])):
                video_interface_name = metadata["Behavior"]["Videos"][video_index]["name"]
                assert mod[video_interface_name].data.shape[0] == 10
                assert mod[video_interface_name].timestamps.shape[0] == 10

import os
from pathlib import Path
from typing import Optional


def generate_path_expander_demo_ibl(folder_path: Optional[str] = None) -> None:
    """
    Partially replicate the file structure of IBL data with dummy files for
    experimentation with `LocalPathExpander`. Specifically, it recreates the
    directory tree for the video files of the Steinmetz Lab's data.

    Parameters
    ----------
    folder_path : str, optional
        Path to folder where the files are to be generated.
        If None, the current working directory will be used.
    """
    if folder_path is None:
        folder_path = os.getcwd()  # use current directory if no folder provided
    folder_path = Path(folder_path)

    video_file_paths = [
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0017"
        / "2022-03-22"
        / "001"
        / "raw_video_data"
        / "_iblrig_bodyCamera.raw.2f88d70a-2172-4635-8ee9-88d9c5193aae.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0017"
        / "2022-03-22"
        / "001"
        / "raw_video_data"
        / "_iblrig_leftCamera.raw.6252a2f0-c10f-4e49-b085-75749ba29c35.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0017"
        / "2022-03-22"
        / "001"
        / "raw_video_data"
        / "_iblrig_rightCamera.raw.4472ab1c-cad8-4eca-8023-b10a4d9005fb.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0019"
        / "2022-04-29"
        / "001"
        / "raw_video_data"
        / "_iblrig_bodyCamera.raw.44f8c3db-45fa-4c47-aed5-fade079b6d3d.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0019"
        / "2022-04-29"
        / "001"
        / "raw_video_data"
        / "_iblrig_leftCamera.raw.9041b63e-02e2-480e-aaa7-4f6b776a647f.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0019"
        / "2022-04-29"
        / "001"
        / "raw_video_data"
        / "_iblrig_rightCamera.raw.a2d1f683-48fe-4212-b7fd-27ec21421c59.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0019"
        / "2022-05-03"
        / "001"
        / "raw_video_data"
        / "_iblrig_bodyCamera.raw.4dcfd4a8-8034-4832-aa93-cee3ddb97a41.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0019"
        / "2022-05-03"
        / "001"
        / "raw_video_data"
        / "_iblrig_leftCamera.raw.05576d90-6fb7-4aba-99ae-7ba63cc50a9a.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0019"
        / "2022-05-03"
        / "001"
        / "raw_video_data"
        / "_iblrig_rightCamera.raw.284fc2c3-a73e-4b86-aeac-efe8359368d9.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0020"
        / "2022-05-08"
        / "001"
        / "raw_video_data"
        / "_iblrig_bodyCamera.raw.cb0a07b5-995f-4143-9590-905af7c4a3f6.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0020"
        / "2022-05-08"
        / "001"
        / "raw_video_data"
        / "_iblrig_leftCamera.raw.1bbb8002-3f34-4d46-8bbd-f46862869f2c.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0020"
        / "2022-05-08"
        / "001"
        / "raw_video_data"
        / "_iblrig_rightCamera.raw.5ad559b2-d5ad-4768-b1f6-cb3db8ebc7e5.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0020"
        / "2022-05-09"
        / "001"
        / "raw_video_data"
        / "_iblrig_bodyCamera.raw.aba7e662-e45b-409b-893d-4ca827bee29a.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0020"
        / "2022-05-09"
        / "001"
        / "raw_video_data"
        / "_iblrig_leftCamera.raw.6fd084e3-93cd-439a-a655-132f1e74138d.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0020"
        / "2022-05-09"
        / "001"
        / "raw_video_data"
        / "_iblrig_rightCamera.raw.22479d80-252b-4d97-8d6e-c9bb61af3fed.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0020"
        / "2022-05-10"
        / "001"
        / "raw_video_data"
        / "_iblrig_bodyCamera.raw.d93f87ae-eec7-435e-9bc7-753d84f1dc98.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0020"
        / "2022-05-10"
        / "001"
        / "raw_video_data"
        / "_iblrig_leftCamera.raw.17c69b88-6aa1-4699-9837-f93b1083275d.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0020"
        / "2022-05-10"
        / "001"
        / "raw_video_data"
        / "_iblrig_rightCamera.raw.eb8c31f0-9181-421a-91c2-59dd1f027bd9.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0020"
        / "2022-05-11"
        / "001"
        / "raw_video_data"
        / "_iblrig_bodyCamera.raw.c282d15f-ad59-4ac7-b4c1-b68d47da91b4.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0020"
        / "2022-05-11"
        / "001"
        / "raw_video_data"
        / "_iblrig_leftCamera.raw.d5e4ed1b-c8a4-402c-a64d-803f734a8569.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0020"
        / "2022-05-11"
        / "001"
        / "raw_video_data"
        / "_iblrig_rightCamera.raw.d52f6dca-1f39-401b-8882-e0dd80df3847.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0021"
        / "2022-06-28"
        / "001"
        / "raw_video_data"
        / "_iblrig_bodyCamera.raw.1788de4f-fd08-4c10-b357-1e2a9b928045.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0021"
        / "2022-06-28"
        / "001"
        / "raw_video_data"
        / "_iblrig_leftCamera.raw.3060c6cb-4d3a-47b9-83c8-080aa55248ef.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0021"
        / "2022-06-28"
        / "001"
        / "raw_video_data"
        / "_iblrig_rightCamera.raw.f40094eb-3187-4468-ba6f-5fc4b6225dfa.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0021"
        / "2022-06-30"
        / "002"
        / "raw_video_data"
        / "_iblrig_bodyCamera.raw.984df1d2-9fb2-4396-bb03-39f32ad97781.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0021"
        / "2022-06-30"
        / "002"
        / "raw_video_data"
        / "_iblrig_leftCamera.raw.4734f477-4d4c-447c-a21b-7ae184f8f010.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0021"
        / "2022-06-30"
        / "002"
        / "raw_video_data"
        / "_iblrig_rightCamera.raw.ddc65491-e553-4ac4-b0bd-d693315f244f.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0021"
        / "2022-07-08"
        / "001"
        / "raw_video_data"
        / "_iblrig_bodyCamera.raw.d55292a6-efe0-49e7-90fe-82598f7417b4.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0021"
        / "2022-07-08"
        / "001"
        / "raw_video_data"
        / "_iblrig_leftCamera.raw.6fc48a3f-77e7-4a6b-ae71-32c79012a7b6.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0021"
        / "2022-07-08"
        / "001"
        / "raw_video_data"
        / "_iblrig_rightCamera.raw.9ff0a260-40c3-4c33-9fd2-5f5a0d712eb0.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0027"
        / "2022-08-19"
        / "001"
        / "raw_video_data"
        / "_iblrig_bodyCamera.raw.bb6ecc2b-5090-4306-a65c-5360f999d832.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0027"
        / "2022-08-19"
        / "001"
        / "raw_video_data"
        / "_iblrig_leftCamera.raw.e5fd349b-71e5-47b9-b0e1-12fad48d4f29.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0027"
        / "2022-08-19"
        / "001"
        / "raw_video_data"
        / "_iblrig_rightCamera.raw.a774dc77-d6f2-4104-8a37-3eb1adc49a85.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0027"
        / "2022-08-22"
        / "001"
        / "raw_video_data"
        / "_iblrig_bodyCamera.raw.f8c3543c-fbb4-446d-b939-df82bc9bee7b.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0027"
        / "2022-08-22"
        / "001"
        / "raw_video_data"
        / "_iblrig_leftCamera.raw.ede51706-c9bd-48f5-ad6b-cacbccd770f5.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0027"
        / "2022-08-22"
        / "001"
        / "raw_video_data"
        / "_iblrig_rightCamera.raw.34cd1cd6-1762-44d2-af6f-9b4be4372093.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0027"
        / "2022-08-23"
        / "001"
        / "raw_video_data"
        / "_iblrig_bodyCamera.raw.e09efb66-223a-402a-ae39-3f92dfd06db7.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0027"
        / "2022-08-23"
        / "001"
        / "raw_video_data"
        / "_iblrig_leftCamera.raw.2c64c58e-45a2-4476-825d-da2b919c5204.mp4",
        folder_path
        / "steinmetzlab"
        / "Subjects"
        / "NR_0027"
        / "2022-08-23"
        / "001"
        / "raw_video_data"
        / "_iblrig_rightCamera.raw.5c187fad-1e86-4b48-975c-e47ebf2c401a.mp4",
    ]

    for video_file_path in video_file_paths:
        video_file_path.parent.mkdir(parents=True, exist_ok=True)  # make directory if needed
        video_file_path.touch()  # make dummy file

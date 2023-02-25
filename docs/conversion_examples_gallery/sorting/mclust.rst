MClust data conversion
----------------------

Install NeuroConv with the additional dependencies necessary for reading MClust data.

.. code-block:: bash

    pip install neuroconv[mclust]

Convert MClust data to NWB using
:py:class:`~neuroconv.datainterfaces.ecephys.mclust.mclustsortinginterface.MClustSortingInterface`.

.. code-block:: python

    >>> from datetime import datetime
    >>> from dateutil import tz
    >>> from pathlib import Path
    >>>
    >>> from neuroconv.datainterfaces import MClustSortingInterface
    >>>
    >>> folder_path = f"{ECEPHY_DATA_PATH}/mclust/data-here"
    >>> # Change the folder_path to the location of the data in your system
    >>> interface = MClustSortingInterface(folder_path=folder_path, verbose=False)
    >>>
    >>> metadata = interface.get_metadata()
    >>> session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=tz.gettz("US/Pacific"))
    >>> metadata["NWBFile"].update(session_start_time=session_start_time)
    >>> nwbfile_path = f"{path_to_save_nwbfile}"  # This should be something like: "./saved_file.nwb"
    >>> interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)

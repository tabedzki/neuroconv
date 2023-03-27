# Example

```
$RCLONE_COMMANDS = "rclone copy Testing:feldman_lab_catalystneuro_data_share/Example_Output/test_spikes.mat . --drive-shared-with-me -v --log-file=./rclone_speed_$RANDOM_NAME.txt --config=./rclone.conf \
  && rclone copy ./rclone_speed_$RANDOM_NAME.txt Testing:Testing_RClone/ -v --config=./rclone.conf"
```
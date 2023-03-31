# Example

```
$RCLONE_COMMANDS = "rclone copy Testing:feldman_lab_catalystneuro_data_share/Example_Output/test_spikes.mat . --drive-shared-with-me -v --log-file=./rclone_speed_$RANDOM_NAME.txt --config=./rclone.conf \
  && rclone copy ./rclone_speed_$RANDOM_NAME.txt Testing:Testing_RClone/ -v --config=./rclone.conf"
```


# Example with `rclone_auto_config`

```
docker run --rm -it --volume /home/ec2-user/test_transfer_6/:/mnt/data/ --env RCLONE_COMMAND --env-file env.list rclone_auto_config
```

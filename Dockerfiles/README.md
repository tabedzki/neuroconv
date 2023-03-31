# Example

```
$RCLONE_COMMANDS = "rclone copy Testing:feldman_lab_catalystneuro_data_share/Example_Output/test_spikes.mat . --drive-shared-with-me -v --log-file=./rclone_speed_$RANDOM_NAME.txt --config=./rclone.conf \
  && rclone copy ./rclone_speed_$RANDOM_NAME.txt Testing:Testing_RClone/ -v --config=./rclone.conf"
```


# Example with `rclone_auto_config`

```
docker run --rm -it --volume /home/ec2-user/test_transfer_6/:/mnt/data/ --env RCLONE_COMMAND --env-file env.list rclone_auto_config
```

with `env.list` as

```
DRIVE_NAME=<Your drive name>
TOKEN=<your token>
REFRESH_TOKEN=<your refresh token>
EXPIRY=<your expiry>
```

and

```
export RCLONE_COMMAND="sync Cody:/ephy_testing_data_2/spikeglx/Noise4Sam_g0 /mnt/data/Noise4Sam_g0 --config /mnt/data/rclone.conf"
```

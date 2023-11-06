# bilder

Very simple photo album viewer made with flask

## Remember

Example on how to mount aws s3 as a systemd service

```
# /etc/systemd/system/mounts3.service
[Unit]
Description=Mount photo album from s3
After=multi-user.target

[Service]
ExecStart=mount-s3 --allow-other --read-only nikwik-photos /mnt/s3/nikwik-photos/
ExecStop=umount /mnt/s3/nikwik-photos
RemainAfterExit=yes

[Install]
WantedBy=default.target
```

```
sudo systemctl enable mounts3.service --now
```

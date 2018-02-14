# caltechdata_map

Map interface for CaltechDATA 

Requires Python 3 (Recommended via Anaconda https://www.anaconda.com/download)
with reqests and pyproj libraries and caltechdata_api https://github.com/caltechlibrary/caltechdata_api.

## Setup 

Type `python makemap.py` to generate the map.  caltechdata_map.html will be
generated - view it on a web browser.

## Configuration

To run automatically on a Ubuntu server and power an S3-hosted site.

Install aws cli utility `pip install awscli --upgrade --user`
Configure aws cli following the instructions at https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html
Edit crontab by typing `crontab -e` and typing:
`PATH=/home/ubuntu/anaconda3/bin:/home/ubuntu/bin:/home/ubuntu/.local/bin:/home/ubuntu/anaconda3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin`
`*/5 * * * * /home/ubuntu/caltechdata_map/run.sh > /home/ubuntu/cron.log 2>&1`
You can adjust the path to match your system.


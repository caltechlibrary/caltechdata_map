# Map interface for CaltechDATA 

[![DOI](https://data.caltech.edu/badge/115029918.svg)](https://data.caltech.edu/badge/latestdoi/115029918)

Shows a map of theses data files from the Geological and Planetary Science division that
have geolocation information in CaltechDATA.

Most files are maps and drawings from the supplemental materials pockets of
theses.

Requires Python 3 (Recommended via Anaconda https://www.anaconda.com/download)

Install python dependencies listed in `requirements.txt` using pip

## Usage

Type `python makemap.py` to generate the map. 

A file caltechdata_map.html will be
generated, which you can view on a web browser.

## Configuration

To run automatically on a Ubuntu server and power an S3-hosted site:

Install aws cli utility `pip install awscli --upgrade --user`

Configure aws cli following the instructions at https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html

Edit crontab by typing `crontab -e` and typing:
`PATH=/home/ubuntu/anaconda3/bin:/home/ubuntu/bin:/home/ubuntu/.local/bin:/home/ubuntu/anaconda3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin`
`*/5 * * * * /home/ubuntu/caltechdata_map/run.sh > /home/ubuntu/cron.log 2>&1`

You can adjust the path to match your system.


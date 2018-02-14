#!/bin/bash
# Run make_map.

echo "____________________________" >> out.log
echo $(date -u) >> out.log
python make_map.py >> out.log
aws s3 cp caltechdata_map.html s3://maps.library.caltech.edu --acl public-read

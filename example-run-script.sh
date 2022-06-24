#!/bin/bash
{
. /home/user/pco-env-vars.sh
. /home/user/dw-env-vars.sh
day=`date +%a`
hour=`date +%H`
[[ $day == "Sun" && ( $hour == "09" || $hour == "10" )]] && /opt/pco-checkouts/bin/python /opt/pco-checkouts/checkins-dwspectrum.py 123456,654321 1234ABCD-0987-4321-1234-123ABC678456
[[ $day == "Sun" && ( $hour == "17" || $hour == "18" )]] && /opt/pco-checkouts/bin/python /opt/pco-checkouts/checkins-dwspectrum.py 123456,654321 1234ABCD-0987-4321-1234-123ABC678456
[[ $day == "Wed" && ( $hour == "18" || $hour == "19" )]] && /opt/pco-checkouts/bin/python /opt/pco-checkouts/checkins-dwspectrum.py 123456,654321 1234ABCD-0987-4321-1234-123ABC678456
} >> /tmp/run_checkins-dwspectrum.log 2>>/tmp/run_checkins-dwspectrum.log


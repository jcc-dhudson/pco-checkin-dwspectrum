# PCO-Checkin-DWSpectrum
This script collects check-ins from Planning Center Online for specified locations and adds corresponding events in the DW Spectrum VMS application. This allows users in DW to see names and other details on screen while watching the specified camera.

## Installation
* Generate PCO application tokens for yourself at https://api.planningcenteronline.com/access_tokens
* Save those tokens as PCO_APP_ID and PCO_SECRET environment variables. I use a bash script that I source from ~/pco-env-vars.sh
* Create a user in DW Spectrum and save a full base URL as DW_URL environment variable. The value of this variable should have the `http://[username]:[password]@[ip/dns]:[port]/` format. For example, `http://api:password@127.0.0.1:7001/`
* Install the https://github.com/jcc-dhudson/libpcocheckin library `pip install "git+https://github.com/jcc-dhudson/libpcocheckin.git"`

## Usage
* Call the script and pass locations and DW Spectrum camera UUID as arguments, example: `python checkin-dwspectrum.py 123456,654321 1234ABCD-0987-4321-1234-123ABC678456`
* Or if running from cron, use a script such as the example script named example-run-script.sh

## Links
* Planning Center Online: https://www.planningcenteronline.com/
* DW Spectrum VMS: https://dwspectrum.com/
* Planning Center Online API Documentation: https://api.planningcenteronline.com/
* Ticket to request webhooks for Check-Ins: https://github.com/planningcenter/developers/issues/998
* libpcocheckin project: https://github.com/jcc-dhudson/libpcocheckin 
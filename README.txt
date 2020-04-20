#
# ---------------------------------------------------------------------------------------------
# mhg-gis
#
# Description
#
#   Application to produce a status graphic for Covid Impact tracking
#
# Requirements:
#
#   Windows 10			
#   Python 3.x          https://www.python.org/downloads/
#   pip                 Python package installer (included in Python 3.x)
#   GooglePyAPIs        pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
#   QGIS 3.10           https://qgis.org/en/site/forusers/download.html
#
#                       Python and QGIS required installs are available in 'kits' folder, or
#                       can be pulled from provided links.
#
# Notes:
#
#   mhgCovidEnv.bat      environment variables pointing to folders for this application and QGIS need to
#                           be defined by editing this file after installing requirements.
#
#   mhgCovidReport       Application generates two warnings and one error, which are expected:
#                           libpng warning: iCCP: known incorrect sRGB profile
#                           libpng warning: iCCP: known incorrect sRGB profile
#                           ERROR 6: The JPEG driver does not support update access to existing datasets.
#  
#  Usage:
# 
#       mhgCovidStatus.bat [-h] [--start START] [--end END] [--ndays [NDAYS]] [--nodetail] [--nosummary] [--debug]
# 
#       optional arguments:
#           -h, --help       show this help message and exit
#           --start START    Beginning date of range to select data by
#           --end END        End date of range to select data by
#           --ndays [NDAYS]  Number of days from begin date to select data by
#           --nodetail       Disables capture of detail to daily CSV files
#           --nosummary      Disables generation of summary info CSV file
#           --info           Whether to barf progress info
#           --debug          Whether to barf debug info
#       	--zombies        Whether to enable zombie tracking
# 
#       Note:
#           dates may be entered mm/dd, mm/dd/yyyy or yyyy.mm.dd
#           nDays may be positive or negative.
# 
#       Examples:
#           mhgCovidStatus.bat                                  # Run for today
#           mhgCovidStatus.bat --start 2020.04.03               # Run for specific date
#           mhgCovidStatus.bat --start 04/03 --end 04/06        # Run for a date range
#           mhgCovidStatus.bat --start 04/03 --ndays 7          # Run for week following (and including) start date given
#           mhgCovidStatus.bat --start 04/03/2020 --ndays -7    # Run for week prior to (and including) start date given
#           mhgCovidStatus.bat --ndays -7                       # Run for the past week
#
#
# Date			Version		Author			Description
# 2020.04.20    02.00       SquintMHG       Rewrite as an app from a pair of scripts
# 2020.03.23    01.00       SquintMHG       Initial version
# ---------------------------------------------------------------------------------------------

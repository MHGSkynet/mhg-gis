#
# ---------------------------------------------------------------------------------------------
# mhg-gis
#
# Description
#
#   Set of tools to produce a status graphic for Covid Impact tracking
#
#     o mhgCovidStatus  runs covidFetch and covidReport
#
#     o mhgCovidFetch   pulls data from a Google spreadsheet for a given date,
#                           stores to local CSV, compiles statistics by county and writes
#                           stats to local CSV and merges stats into KML for presentation.
#                       creates (2) kml files. One in data folder as input to covidReport, 
#                           and an identical one in the output folder with current date added
#                           to file name.
#
#     o mhgCovidReport  take generated KML and construct a QGIS project and save. Render as a
#                           graphic and save to JPG and PDF formats.
#
#     o mhgCovidEnv     sets package environment variables
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
# Date			Version		Author			Description
# 2020.03.23    01.00       SquintMHG       Initial version
# ---------------------------------------------------------------------------------------------


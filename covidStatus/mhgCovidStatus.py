#
#------------------------------------       .     ----------------------------------------------------
# mhgCovidStatus.py                      ,'/ \`.                           ,,,,,,,,,,,,,,,,
#                                       |\/___\/|                    <"> -{ I am a virus,  }
# Description                           \'\   /`/                    _T_  { please copy me }
#                                        `.\ /,'    <">              /Y\   ````````````````                           
#    Covid Status Reporting                 |       _T_                         <">       <">      
#    Tool                                   |       /Y\      <">                _T_       _T_        
#                                          |=|               _T_         <">    /Y\       /Y\          
#                                     /\  ,|=|.  /\          /Y\    <">  _T_        <">         
#                                 ,'`.  \/ |=| \/  ,'`.             _T_  /Y\     <"> T_              
#                               ,'    `.|\ `-' /|,'    `.           /Y\          _T_ Y\             
#                             ,'   .-._ \ `---' / _,-.   `.                      /Y\               
#                                ,'    `-`-._,-'-'    `.             <">
#                               '                       `            _T_
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
# Usage:
#
#    mhgCovidStatus.py [-h] [--start START] [--end END] [--ndays [NDAYS]] [--nodetail] [--nosummary]
#                         [--noproject] [--nopdf] [--noimage] [--info] [--debug] [--zombies]
#
#     === MHG Covid Status Report ===
#
#     optional arguments:
#       -h, --help       show this help message and exit
#       --start START    Beginning date of range to select data by
#       --end END        End date of range to select data by
#       --ndays [NDAYS]  Number of days from begin date to select data by
#       --nodetail       Disables capture of detail to daily CSV files
#       --nosummary      Disables generation of summary info CSV file
#       --noproject      Disables saving of GIS Project
#       --nopdf          Disables saving of PDF file
#       --noimage        Disables saving of JPG image
#       --info           Whether to barf progress info
#       --debug          Whether to barf debug info
#       --zombies        Whether to enable zombies
#
#     Note:
#             dates may be entered mm/dd, mm/dd/yyyy or yyyy.mm.dd
#             nDays may be positive or negative.
#
#     Examples:
#             mhgCovidStatus.py                                  # Run for today
#             mhgCovidStatus.py --start 2020.04.03               # Run for specific date
#             mhgCovidStatus.py --start 04/03 --end 04/06        # Run for a date range
#             mhgCovidStatus.py --start 04/03 --ndays 7          # Run for week following start date given
#             mhgCovidStatus.py --start 04/03/2020 --ndays -7    # Run for week prior to and including start date given
#             mhgCovidStatus.py --ndays -7                       # Run for the past week# Description
#     
#     Sample Spreadsheet:
#             https://docs.google.com/spreadsheets/d/1ckdKCNIB-5-KSUlV2ehW3KPARVlu_CC2npjsAHrml7Q/edit?usp=sharing
#
# Copyright
#
#   Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#                       non profit conservative organizations and individuals to use in support
#                       of American freedom and the constitution. All other rights are reserved,
#                       and any other use prohibited.
#
# Date          Version     Author          Description
# 2020.04.20    02.00       SquintMHG       Rewrite from script to oo app
# 2020.04.04    01.01       SquintMHG       Fix filter date compare problem
# 2020.03.27    01.00       SquintMHG       Initial version
# ---------------------------------------------------------------------------------------------

# Python Imports
import os
import sys
import gc

# MHGLIB imports
from mhgAppSettings		import AppSettings
from mhgCovidDataReader	import CovidDataReader
from mhgDetailWriter	import DetailWriter
from mhgSummaryWriter   import SummaryWriter
from mhgKmlWriter		import KmlWriter
from mhgGisWriter		import GisWriter
from mhgException		import CommandArgError
from mhgException		import EnvironmentError
from mhgException		import RenderError
from mhgException		import UserError
from mhgException		import AppError
from mhgUtility			import *


#
# Exit handler
#
def appExit(err=None):

	statusText = ''
	statusCode = AppError.ERR_NONE

	#if not err is None:
	#	print(err.formattedText())
	#	statusCode = err.errorNumber()
	#	statusText = " Status={}".format(statusCode)

	print ("####\n#### {} complete.  Status={}\n####".format(AppSettings.PROGNM,statusCode))

	sys.exit(statusCode)

"""
##########################################
		MAIN
##########################################
"""
def main():

	# Get Application settings (environment info and command args). Retain a reference to command arg options for convenience
	try:
		_appOptions = AppSettings.glob().options()
	except (CommandArgError, EnvironmentError) as err:
		appExit(err)

	# App Start
	print ("####\n#### {} starting.\n####".format(AppSettings.PROGNM))

	# Get Corona data from spreadsheet
	dataReader = CovidDataReader()
	fetchOk = dataReader.FetchCoronaData()
	if not fetchOk: 
		appExit(UserError('No records retrieved from sheet.',AppError.ERR_FETCHFAIL))
		
	# Generate Output CSVs and KML from County stats
	try:
		# Write Detail
		if _appOptions.captureDetail(): DetailWriter().WriteStatusRows(dataReader.covidSheet().statusRowsFiltered())
		
		# Write Summary
		if _appOptions.generateSummary(): SummaryWriter().WriteStateCountyStats(dataReader.stateData())

		# Write KML
		KmlWriter().WriteStateCountyStats(dataReader.stateData())

	except EnvironmentError as err:
		appExit(err)
	
	# Close spreadsheet
	dataReader.Close()																# Close dataReader to cause Google resources to clean up
	dataReader = None																

	# Remojinate generated KML into QGIS Project, then barf to PDF and JPG
	try:
		
		gisWriter = GisWriter()														# Fire up GIS Writer
		gisWriter.GenerateProject()													# Create a GIS project base on generated KML
		if _appOptions.generateProject(): 	gisWriter.SaveProject()					# Save project, if needed.
		if _appOptions.generatePdf(): 		gisWriter.GeneratePdf()					# Write to PDF, if needed.
		if _appOptions.generateImage(): 	gisWriter.GenerateImage()				# Write to JPG image, if needed.
		gisWriter.Cleanup()															# Shut down GIS Writer
		gisWriter = None

	except (RenderError,EnvironmentError) as err:
		appExit(err)

	#gc.set_debug(gc.DEBUG_STATS or gc.DEBUG_COLLECTABLE or gc.DEBUG_UNCOLLECTABLE)
	
	# App Exit
	appExit()

if __name__ == '__main__':
	main()
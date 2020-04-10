#
# ---------------------------------------------------------------------------------------------
# mhgCovidStatus.py
#
# Description
#
#	Get data from spreadsheet and render as chart. 	
#
#	Sample Spreadsheet:
#   	https://docs.google.com/spreadsheets/d/1ckdKCNIB-5-KSUlV2ehW3KPARVlu_CC2npjsAHrml7Q/edit?usp=sharing
#
# Copyright
#
#	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#						non profit conservative organizations and individuals to use in support
#						of American freedom and the constitution. All other rights are reserved,
#						and any other use prohibited.
#
# Date			Version		Author			Description
# 2020.04.07	02.00		SquintMHG		Rewrite from script to oo app
# 2020.04.04	01.01		SquintMHG		Fix filter date compare problem
# 2020.03.27	01.00		SquintMHG		Initial version
# ---------------------------------------------------------------------------------------------

from __future__ import print_function
import copy
import os
import os.path
import re
import sys
from pathlib import Path
from datetime import datetime
from datetime import timedelta

from mhgDateParse import DateParser
from mhgDateParse import DateParseResult

import mhgAppSettings
import mhgCovidDataReader
import mhgDetailWriter
import mhgException
import mhgUtility

#
# Exit handler
#
def appExit(err=None):

	statusText = ''
	statusCode = AppError.ERR_NONE

	if not err is None:
		print(err.formattedText())
		statusCode = err.errorNumber()
		statusText = " Status={}".format(statusCode)

	print ("####\n#### {} complete.{}\n####".format(AppSettings.PROGNM,statusText))

	sys.exit(statusCode)

"""
##########################################
		MAIN
##########################################
"""
def main():

	# App Start
	print ("####\n#### {} starting.\n####".format(PROGNM))

	# Get Application settings (environment info and command args). Retain a reference to command arg options for convenience
	try:
		_appOptions = AppSettings.glob().options()
	except (CommandArgError, EnvironmentError) as err:
		appExit(err)

	# Get Corona data from spreadsheet
	dataReader = CovidDataReader()
	fetchOk = dataReader.FetchCoronaData():
	if not fetchOk: 
		appExit(UserError('No records retrieved from sheet.',ERR_FETCHFAIL))
		
	# Generate Output
	try:
		# Write Detail
		if _appOptions.captureDetail(): DetailWriter.WriteStatusRows(dataReader.covidSheet().statusRowsFiltered())
		
		# Write Summary
		if _appOptions.generateSummary(): SummaryWriter.WriteCountyStats(dataReader.countyStats())

		mergeKmlData()
	except EnvironmentError as err:
		appExit(err)

	# App Exit
	appExit()


if __name__ == '__main__':
	main()
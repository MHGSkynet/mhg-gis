#
# ---------------------------------------------------------------------------------------------
# mhgCovidDataFetch.py
#
# Description
#
# 	Pull MHG Covid data for a given day from Google spreadsheet, save detail and
#   statistics to CSV. Merge data into KML and save for daily report generation.
#
#	Sample Spreadsheet:
#   	https://docs.google.com/spreadsheets/d/1ckdKCNIB-5-KSUlV2ehW3KPARVlu_CC2npjsAHrml7Q/edit?usp=sharing
#
# Input Resources
#   MHGCovidDetail.kml	Michigan KML file with 
#
# Copyright
#
#	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#						non profit conservative organizations and individuals to use in support
#						of American freedom and the constitution. All other rights are reserved,
#						and any other use prohibited.
#
# Date			Version		Author			Description
# 2020.04.07	01.03		SquintMHG		Convert to command line args, class modules
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

from mhgFetchCommandArgs import mhgFetchCommandArgs
from mhgFetchEnvironment import getPackageRoot
from mhgDateParse import dateParser
from mhgDateParse import dateParseResult

import mhgUtility

COVID_SPREADSHEET_ID	= '1ckdKCNIB-5-KSUlV2ehW3KPARVlu_CC2npjsAHrml7Q'				# Google Document ID to fetch
COVID_DATA_RANGE		= 'DailyData!A1:H'												# Spreadsheet range to fetch

#
# Fetch Corona Data
#
def fetchCoronaData(service,countyStats):

	_appOptions = mhgAppSettings.options()

	fetchStatus = False

	barfd("DEBUG: fetchCoronaData.enter")
	if _appOptions.isDateRange(): 		barfd("Fetching Data for {} to {} ...".format(_appOptions.startDate(),_appOptions.endDate()))
	if not _appOptions.isDateRange(): 	barfd("Fetching Data for {}...".format(_appOptions.startDate()))

	# Call the Sheets API
	sheet = service.spreadsheets()
	result = sheet.values().get(spreadsheetId=COVID_SPREADSHEET_ID,range=COVID_DATA_RANGE).execute()
	values = result.get('values', [])
	gshtRowCt = 0
	gshtMatchRowCt = 0

	countyDailyCounts	= {}

	if not values:
		print('ERROR: No spreadsheet data found.')
	else:																					# Walk spreadsheet data filtered by date and build stats by county
		barfd("DEBUG: fetchCoronaData.process sheet values")
		barfd("DEBUG: args.startDate={}, args.endDate={}".format(_appOptions.startDate(),_appOptions.endDate()))
		#countyStats	= CountyStats()
		for gshtRow in values:
			gshtRowCt += 1
			if gshtRowCt == 1: continue														# Skip header gshtRow
			infoDate = rowElem(GSHT_DATE,gshtRow)
			barfd("DEBUG: fetchCoronaData.date={},site={},county={}".format(infoDate,rowElem(GSHT_SITE,gshtRow),rowElem(GSHT_COUNTY,gshtRow)))
			infoYmd = dateParser().parseDate(infoDate).dateYMD()
			if not infoYmd in countyDailyCounts: countyDailyCounts[infoYmd] = 0
			countyDailyCounts[infoYmd] += 1

			# Filer by date
			if infoYmd >= _appOptions.startDate() and  infoYmd <= _appOptions.endDate():

				gshtMatchRowCt += 1
				county	 = rowElem(GSHT_COUNTY,gshtRow)
				# Add to statics
				if county != "":
					if not county in countyStats: countyStats[county] = copy.deepcopy(COUNTY_STATS_DEFAULT)

					if county=='Kent': barfd("DEBUG: FetchAddStats1:(util:{},svc:{},cons:{},max:{})".format(impactWeight(rowElem(GSHT_UTILITIES,gshtRow)),	\
																										 impactWeight(rowElem(GSHT_SERVICES,gshtRow)),	\
																										 impactWeight(rowElem(GSHT_CONSUMABLES,gshtRow)),	\
																										 countyStats[county][STAT_MAX_IMPACT]))
					countyStats[county][STAT_STATUS_REPORTS]			+= 1
					countyStats[county][STAT_UTILITIES_WEIGHT]		+= impactWeight(rowElem(GSHT_UTILITIES,gshtRow))
					countyStats[county][STAT_SERVICES_WEIGHT]		+= impactWeight(rowElem(GSHT_SERVICES,gshtRow))
					countyStats[county][STAT_CONSUMABLES_WEIGHT]		+= impactWeight(rowElem(GSHT_CONSUMABLES,gshtRow))
					countyStats[county][STAT_MAX_IMPACT]				=  max(countyStats[county][STAT_MAX_IMPACT], 			\
																			impactWeight(rowElem(GSHT_UTILITIES,gshtRow)),	\
																			impactWeight(rowElem(GSHT_SERVICES,gshtRow)),	\
																			impactWeight(rowElem(GSHT_CONSUMABLES,gshtRow)))

					if county=='Kent': barfd("DEBUG: FetchAddStats2:(util:{},svc:{},cons:{},max:{})".format(impactWeight(rowElem(GSHT_UTILITIES,gshtRow)),	\
																										 impactWeight(rowElem(GSHT_SERVICES,gshtRow)),	\
																										 impactWeight(rowElem(GSHT_CONSUMABLES,gshtRow)),	\
																										 countyStats[county][STAT_MAX_IMPACT]))

					countyStats[county][STAT_2M_CHECKINS]			+= nullz(rowElem(GSHT_2M_CHECKINS,gshtRow))
					countyStats[county][STAT_2M_PARTICIPATE] 		+= nullz(rowElem(GSHT_2M_PARTICIPATE,gshtRow))
					countyStats[county][STAT_HF_CHECKINS]			+= nullz(rowElem(GSHT_HF_CHECKINS,gshtRow))
					countyStats[county][STAT_HF_PARTICIPATE] 		+= nullz(rowElem(GSHT_HF_PARTICIPATE,gshtRow))

					if infoYmd not in countyStats[county][STAT_DAILY_COUNTS]: countyStats[county][STAT_DAILY_COUNTS][infoYmd] = 0
					countyStats[county][STAT_DAILY_COUNTS][infoYmd] += 1

				# Write to Detail CSV
				if _appOptions.captureDetail():
					detailCsvWriteRow(infoYmd,gshtRow)

		barfd("DEBUG: fetchCoronaData.forLoopDone.matchCt={}".format(gshtMatchRowCt))

		if gshtMatchRowCt == 0:
			if _appOptions.isDateRange():
				print("WARNING: No spreadsheet data matches filter date range of {} to {}".format(_appOptions.startDate(),_appOptions.endDate()) )
			else:
				print("WARNING: No spreadsheet data matches filter date of {}".format(_appOptions.startDate()) )
		else:
			if _appOptions.captureDetail():	detailCsvClose()
			fetchStatus = True

	barf("Fetch complete. {} records retrieved.".format(gshtMatchRowCt))
	
	barfd("DEBUG: countyStats:{}".format(countyStats['Kent']))
	
	barfd("DEBUG: fetchCoronaData.exit rowCt={},matchCt={}".format(gshtRowCt,gshtMatchRowCt))
	return fetchStatus

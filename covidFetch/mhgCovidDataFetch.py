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

import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from mhgFetchCommandArgs import mhgFetchCommandArgs
from mhgFetchEnvironment import getPackageRoot
from mhgDateParse import dateParser
from mhgDateParse import dateParseResult

"""
##########################################
		INITIALIZATION
##########################################
"""

PROGNM				= 'mhgCovidDataFetch'
ERR_NONE			= 0
ERR_BADENV			= 1
ERR_BADFILTER		= 2
ERR_FETCHFAIL		= 3

"""
##########################################
		DRIVING DATA
##########################################
"""

# Command Arguments
_appOptions				= {}															# Command Options

# System date
FORMAT_YMD				= "%Y.%m.%d"													# date format yyyy.mm.dd
currTimestamp			= datetime.now() 												# current date and time (timestamp)
currDateYmd				= currTimestamp.strftime(FORMAT_YMD)							# current date YYYY.MM.DD (text)
currDateTS				= datetime.strptime(currDateYmd,FORMAT_YMD)						# current date (timestamp)

# covidReport data
ENV_REPORT_DATE			= "MHGGIS_FILTER_DATE"											# Environment variable to set to pass report date to mhgCovidReport. TODO: FIX KLUDGE

# Goo Security
SCOPES 					= ['https://www.googleapis.com/auth/spreadsheets.readonly']		# If modifying scope(s), delete the file token.pickle.
COVID_SPREADSHEET_ID	= '1ckdKCNIB-5-KSUlV2ehW3KPARVlu_CC2npjsAHrml7Q'				# Google Document ID to fetch
COVID_DATA_RANGE		= 'DailyData!A1:H'												# Spreadsheet range to fetch

# Folders
PACKAGE_ROOT			= getPackageRoot()												# MHGGIS Package root folder for mgh-gis suite
APP_FOLDER				= PACKAGE_ROOT + 'covidFetch/'									# Application folder
DATA_FOLDER				= PACKAGE_ROOT + 'data/'										# Folder for data accumulation
KML_FOLDER				= PACKAGE_ROOT + 'kml/'											# Folder for kml
OUTPUT_FOLDER			= PACKAGE_ROOT + 'output/'										# Folder for output 

# Security File Specs
gooPickleSpec		  	= APP_FOLDER + 'token.pickle'									# Google API pickle file
gooCredentialsSpec		= APP_FOLDER + 'credentials.json'								# Google API credentials file

# Input Resource File Specs
statusTemplateSpec		= KML_FOLDER + "mhgCovidStatusMichigan.kml"						# Template KML of Michigan counties and MHG Covid data schema

# Output File Specs
TEMPLATE_DATE_TOKEN		= "YMD"
detailCsvTemplate		= DATA_FOLDER + "mhgCovidStatus-Detail-YMD.csv"					# Detail CSV file specification (output)
summaryCsvTemplate		= DATA_FOLDER + "mhgCovidStatus-Summary-YMD.csv"				# Summary CSV file specification (output)
statusKmlCurrentSpec	= DATA_FOLDER + "mhgCovidStatus.kml"							# Status KML file (for input to covidReport)
statusKmlDailyTemplate	= OUTPUT_FOLDER + "mhgCovidStatus-YMD.kml"						# Status KML file daily generated file

# Data Output 																			# TODO: replace with command args
XMIT_START_DATE			= 'StartDate'
XMIT_END_DATE			= 'EndDate'
reportInfoXmitSpec		= DATA_FOLDER + "mhgCovidReportXmit.ini"						# File to transmit report date to mhgCovidReport app.

# CSV Generation
CSV_FIELD_SEP			= ','															# CSV field separator
CSV_FIELD_QUOTE			= '"'															# CSV field quote bounds character


"""
##########################################
		FILE METADATA
##########################################
"""

# Impact Codes
IMPACT_CODE_AVAILABLE	= 'A'
IMPACT_CODE_MODERATE	= 'M'
IMPACT_CODE_SEVERE		= 'S'
IMPACT_CODE_UNKNOWN		= 'U'
#IMPACT_CODE_ZOMBIES	= 'Z'

# Data Types
DTYPE_NUMERIC			= 'numeric'
DTYPE_TEXT				= 'text'
DTYPE_DATE				= 'date'

# ColInfo hash
COL_ID					= 'colId'
COL_DTYPE				= 'dType'
COL_HEADER				= 'header'
COL_SOURCE				= 'srcId'

# Google Covid Data (input) metadata 
GSHT_DATE			= 0
GSHT_SITE			= 1
GSHT_COUNTY			= 2
GSHT_UTILITIES		= 3
GSHT_SERVICES		= 4
GSHT_CONSUMABLES	= 5
GSHT_2M_CHECKINS	= 6
GSHT_2M_PARTICIPATE	= 7
GSHT_HF_CHECKINS	= 8
GSHT_HF_PARTICIPATE	= 9
GSHT_COMMENTS		= 10
GSHT_METADATA		= [ { COL_ID: GSHT_DATE,			COL_DTYPE: DTYPE_DATE,		COL_HEADER: 'IntelDate'			},
						{ COL_ID: GSHT_SITE,			COL_DTYPE: DTYPE_TEXT,		COL_HEADER: 'Site' 				},
						{ COL_ID: GSHT_COUNTY,			COL_DTYPE: DTYPE_TEXT,		COL_HEADER: 'County'			},
						{ COL_ID: GSHT_UTILITIES,		COL_DTYPE: DTYPE_TEXT,		COL_HEADER: 'UtilityImpact'		},
						{ COL_ID: GSHT_SERVICES,		COL_DTYPE: DTYPE_TEXT,		COL_HEADER:	'ServicesImpact'	},
						{ COL_ID: GSHT_CONSUMABLES,		COL_DTYPE: DTYPE_TEXT,		COL_HEADER:	'ConsumablesImpact'	},
						{ COL_ID: GSHT_2M_CHECKINS,		COL_DTYPE: DTYPE_NUMERIC,	COL_HEADER:	'2M Checkins'		},
						{ COL_ID: GSHT_2M_PARTICIPATE,	COL_DTYPE: DTYPE_NUMERIC,	COL_HEADER:	'2M Participate'	},
						{ COL_ID: GSHT_HF_CHECKINS,		COL_DTYPE: DTYPE_NUMERIC,	COL_HEADER:	'HF Checkins'		},
						{ COL_ID: GSHT_HF_PARTICIPATE,	COL_DTYPE: DTYPE_NUMERIC,	COL_HEADER:	'HF Participate'	},
						{ COL_ID: GSHT_COMMENTS,		COL_DTYPE: DTYPE_TEXT,		COL_HEADER:	'Comments'			} ]

# Detail CSV (output) metadata
DCSV_DATE			= 0
DCSV_SITE			= 1
DCSV_COUNTY			= 2
DCSV_UTILITIES		= 3
DCSV_SERVICES		= 4
DCSV_CONSUMABLES	= 5
DCSV_2M_CHECKINS	= 6
DCSV_2M_PARTICIPATE	= 7
DCSV_HF_CHECKINS	= 8
DCSV_HF_PARTICIPATE	= 9
DCSV_COMMENTS		= 10
DCSV_METADATA		= [ { COL_ID: DCSV_DATE,			COL_DTYPE: DTYPE_DATE,		COL_HEADER: 'IntelDate',			COL_SOURCE: GSHT_DATE			},
						{ COL_ID: DCSV_SITE,			COL_DTYPE: DTYPE_TEXT,		COL_HEADER: 'Site',					COL_SOURCE: GSHT_SITE			},
						{ COL_ID: DCSV_COUNTY,			COL_DTYPE: DTYPE_TEXT,		COL_HEADER: 'County',				COL_SOURCE: GSHT_COUNTY			},
						{ COL_ID: DCSV_UTILITIES,		COL_DTYPE: DTYPE_TEXT,		COL_HEADER: 'UtilityImpact',		COL_SOURCE:	GSHT_UTILITIES		},
						{ COL_ID: DCSV_SERVICES,		COL_DTYPE: DTYPE_TEXT,		COL_HEADER:	'ServicesImpact',		COL_SOURCE: GSHT_SERVICES		},
						{ COL_ID: DCSV_CONSUMABLES,		COL_DTYPE: DTYPE_TEXT,		COL_HEADER:	'ConsumablesImpact',	COL_SOURCE: GSHT_CONSUMABLES	},
						{ COL_ID: DCSV_2M_CHECKINS,		COL_DTYPE: DTYPE_NUMERIC,	COL_HEADER:	'2MCheckins',			COL_SOURCE: GSHT_2M_CHECKINS	},
						{ COL_ID: DCSV_2M_PARTICIPATE,	COL_DTYPE: DTYPE_NUMERIC,	COL_HEADER:	'2MParticipate',		COL_SOURCE: GSHT_2M_PARTICIPATE	},
						{ COL_ID: DCSV_HF_CHECKINS,		COL_DTYPE: DTYPE_NUMERIC,	COL_HEADER:	'HFCheckins',			COL_SOURCE: GSHT_HF_CHECKINS	},
						{ COL_ID: DCSV_HF_PARTICIPATE,	COL_DTYPE: DTYPE_NUMERIC,	COL_HEADER:	'HFParticipate',		COL_SOURCE: GSHT_HF_PARTICIPATE	},
						{ COL_ID: DCSV_COMMENTS,		COL_DTYPE: DTYPE_TEXT,		COL_HEADER:	'Comments',				COL_SOURCE: GSHT_COMMENTS		} ]

# Summary CSV (output) metadata
SCSV_START_DATE			= 0
SCSV_END_DATE			= 1
SCSV_COUNTY				= 2
SCSV_NDAYS				= 3
SCSV_OBSERVATIONS		= 4
SCSV_UTILITIES_WEIGHT	= 5
SCSV_SERVICES_WEIGHT	= 6
SCSV_CONSUMABLES_WEIGHT	= 7
SCSV_UTILITIES_IMPACT	= 8
SCSV_SERVICES_IMPACT	= 9
SCSV_CONSUMABLES_IMPACT	= 10
SCSV_MAX_IMPACT			= 11
SCSV_2M_CHECKINS		= 12
SCSV_2M_PARTICIPATE		= 13
SCSV_HF_CHECKINS		= 14
SCSV_HF_PARTICIPATE		= 15
SCSV_METADATA		= [ { COL_ID: SCSV_START_DATE,			COL_DTYPE: DTYPE_DATE,		COL_HEADER: 'IntelStartDate'	},
						{ COL_ID: SCSV_END_DATE,			COL_DTYPE: DTYPE_DATE,		COL_HEADER: 'IntelEndDate'		},
						{ COL_ID: SCSV_COUNTY,				COL_DTYPE: DTYPE_TEXT,		COL_HEADER: 'County'			},
						{ COL_ID: SCSV_NDAYS,				COL_DTYPE: DTYPE_NUMERIC,	COL_HEADER: 'ObserveDays'		},
						{ COL_ID: SCSV_OBSERVATIONS,		COL_DTYPE: DTYPE_NUMERIC,	COL_HEADER: 'ObserveCount'		},
						{ COL_ID: SCSV_UTILITIES_WEIGHT,	COL_DTYPE: DTYPE_NUMERIC,	COL_HEADER: 'UtilityWeight'		},
						{ COL_ID: SCSV_SERVICES_WEIGHT,		COL_DTYPE: DTYPE_NUMERIC,	COL_HEADER:	'ServicesWeight'	},
						{ COL_ID: SCSV_CONSUMABLES_WEIGHT,	COL_DTYPE: DTYPE_NUMERIC,	COL_HEADER:	'ConsumablesWeight'	},
						{ COL_ID: SCSV_UTILITIES_IMPACT,	COL_DTYPE: DTYPE_TEXT,		COL_HEADER: 'UtilityImpact'		},
						{ COL_ID: SCSV_SERVICES_IMPACT,		COL_DTYPE: DTYPE_TEXT,		COL_HEADER:	'ServicesImpact'	},
						{ COL_ID: SCSV_CONSUMABLES_IMPACT,	COL_DTYPE: DTYPE_TEXT,		COL_HEADER:	'ConsumablesImpact'	},
						{ COL_ID: SCSV_MAX_IMPACT,			COL_DTYPE: DTYPE_TEXT,		COL_HEADER:	'MaxImpact'			},
						{ COL_ID: SCSV_2M_CHECKINS,			COL_DTYPE: DTYPE_NUMERIC,	COL_HEADER:	'2MCheckins'		},
						{ COL_ID: SCSV_2M_PARTICIPATE,		COL_DTYPE: DTYPE_NUMERIC,	COL_HEADER:	'2MParticipate'		},
						{ COL_ID: SCSV_HF_CHECKINS,			COL_DTYPE: DTYPE_NUMERIC,	COL_HEADER:	'HFCheckins'		},
						{ COL_ID: SCSV_HF_PARTICIPATE,		COL_DTYPE: DTYPE_NUMERIC,	COL_HEADER:	'HFParticipate'		}  ]

"""
##########################################
		WORKING DATA
##########################################
"""

# Statistics by County
STAT_STATUS_START_DATE			= 'IntelStartDate'									# End date of observations
STAT_STATUS_END_DATE			= 'IntelEndDate'									# End date of observations
STAT_STATUS_NDAYS				= 'IntelNDays'										# Number of days observed 
STAT_STATUS_REPORTS				= 'StatusReports'									# Number of observations
STAT_UTILITIES_WEIGHT			= 'UtilitiesWeight'									# Total utility impact weight
STAT_SERVICES_WEIGHT			= 'ServicesWeight'									# Total services impact weight
STAT_CONSUMABLES_WEIGHT			= 'ConsumablesWeight'								# Total consumables impact weight
STAT_2M_CHECKINS				= '2M Checkins'										# Total 2M check-ins by net control
STAT_2M_PARTICIPATE				= '2M Participate'									# Total 2M nets participated in
STAT_HF_CHECKINS				= 'HF Checkins'										# Total HF check-ins by net control
STAT_HF_PARTICIPATE				= 'HF Participate'									# Total HF nets participated in

STAT_OVERALL_IMPACT_SCORE		= 'OverallImpactScore'								# Overall Impact Score
STAT_MAX_SCORE					= 'MaxScore'										# Maximum Score
STAT_MAX_IMPACT					= 'MaxImpact'										# Maximum Impact
STAT_UTILITIES_IMPACT_SCORE		= 'UtilitiesImpactScore'							# Utilities Impact Score
STAT_SERVICES_IMPACT_SCORE		= 'ServicesImpactScore'								# Services Impact Score
STAT_CONSUMABLES_IMPACT_SCORE	= 'ConsumablesImpactScore'							# Consumables Impact Score

STAT_OVERALL_IMPACT_CODE		= 'OverallImpactCode'								# Overall Impact Code (A,M,S)
STAT_MAX_SCORE_CODE				= 'MaxScoreCode'									# Max Score Code (A,M,S)
STAT_MAX_IMPACT_CODE			= 'MaxImpactCode'									# Max Impact Code (A,M,S)
STAT_UTILITIES_IMPACT_CODE		= 'UtilitiesImpactCode'								# Utilities Impact Code (A,M,S)
STAT_SERVICES_IMPACT_CODE		= 'ServicesImpactCode'								# Services Impact Code (A,M,S)
STAT_CONSUMABLES_IMPACT_CODE	= 'ConsumablesImpactCode'							# Consumables Impact Code (A,M,S)

STAT_DAILY_COUNTS				= 'DailyCounts'										# Counts of observations by date for county

COUNTY_DEFAULT					= 'DEFAULT'											# Default county values
COUNTY_STATS_DEFAULT			= { STAT_STATUS_START_DATE:			None,
									STAT_STATUS_END_DATE:			None,
									STAT_STATUS_NDAYS:				0,
									STAT_STATUS_REPORTS:			0,
									STAT_UTILITIES_WEIGHT:			0,
									STAT_SERVICES_WEIGHT:			0,
									STAT_CONSUMABLES_WEIGHT:		0,
									STAT_2M_CHECKINS:				0,
									STAT_2M_PARTICIPATE:			0,
									STAT_HF_CHECKINS:				0,
									STAT_HF_PARTICIPATE:			0,
									STAT_OVERALL_IMPACT_SCORE:		0,
									STAT_MAX_SCORE:					0,
									STAT_MAX_IMPACT:				0,
									STAT_UTILITIES_IMPACT_SCORE:	0,
									STAT_SERVICES_IMPACT_SCORE:		0,
									STAT_CONSUMABLES_IMPACT_SCORE:	0,
									STAT_OVERALL_IMPACT_CODE:		IMPACT_CODE_UNKNOWN,
									STAT_MAX_SCORE_CODE:			IMPACT_CODE_UNKNOWN,
									STAT_MAX_IMPACT_CODE:			IMPACT_CODE_UNKNOWN,
									STAT_UTILITIES_IMPACT_CODE:		IMPACT_CODE_UNKNOWN,
									STAT_SERVICES_IMPACT_CODE:		IMPACT_CODE_UNKNOWN,
									STAT_CONSUMABLES_IMPACT_CODE:	IMPACT_CODE_UNKNOWN,
									STAT_DAILY_COUNTS:				{} }

covidStats						= {COUNTY_DEFAULT: copy.deepcopy(COUNTY_STATS_DEFAULT)}	# Statistics hash, by county
covidDailyCounts				= {}													# Counts of observation by date

# KML Constants
KDATA_SCHEMA					= '#OGRGeoJSON'
KDATA_STATUS_DATE				= 'STATUS_DATE'
KDATA_STATUS_NDAYS				= 'STATUS_NDAYS'
KDATA_STATUS_OVERALL			= 'STATUS_OVERALL'
KDATA_STATUS_MAX				= 'STATUS_MAX'
KDATA_STATUS_UTILITIES			= 'STATUS_UTILITIES'
KDATA_STATUS_SERVICES			= 'STATUS_SERVICES'
KDATA_STATUS_CONSUMBALES		= 'STATUS_CONSUMABLES'
KDATA_2M_CHECKINS				= 'CHECKINS_2M'
KDATA_2M_PARTICIPATE			= 'PARTICIPATE_2M'
KDATA_HF_CHECKINS				= 'CHECKINS_HF'
KDATA_HF_PARTICIPATE			= 'PARTICIPATE_HF'

KSTYLE_IMPACT_UNKNOWN			= '#impactUnknown'
KSTYLE_IMPACT_NONE				= '#impactNormal'
KSTYLE_IMPACT_MODERATE			= '#impactModerate'
KSTYLE_IMPACT_SEVERE			= '#impactSevere'
KSTYLE_IMPACT_ZOMBIES			= '#impactZombies'


impactCodeStyleMap				= { IMPACT_CODE_AVAILABLE: 	KSTYLE_IMPACT_NONE,
									IMPACT_CODE_MODERATE:	KSTYLE_IMPACT_MODERATE,
									IMPACT_CODE_SEVERE:		KSTYLE_IMPACT_SEVERE,
									IMPACT_CODE_UNKNOWN:	KSTYLE_IMPACT_UNKNOWN }
#									IMPACT_CODE_ZOMBIES:	KSTYLE_IMPACT_ZOMBIES }

# Kml Data
kmlLines	= []

# Map of STAT_ items to KML Schema Data Items
statsSchemaDataMap			= { KDATA_STATUS_DATE: 			STAT_STATUS_END_DATE,
								KDATA_STATUS_NDAYS: 		STAT_STATUS_NDAYS,
								KDATA_STATUS_OVERALL: 		STAT_OVERALL_IMPACT_CODE,
								KDATA_STATUS_MAX: 			STAT_MAX_IMPACT_CODE,
								KDATA_STATUS_UTILITIES:		STAT_UTILITIES_IMPACT_CODE,
								KDATA_STATUS_SERVICES:		STAT_SERVICES_IMPACT_CODE,
								KDATA_STATUS_CONSUMBALES:	STAT_CONSUMABLES_IMPACT_CODE,
								KDATA_2M_CHECKINS:			STAT_2M_CHECKINS,
								KDATA_2M_PARTICIPATE:		STAT_2M_PARTICIPATE,
								KDATA_HF_CHECKINS:			STAT_HF_CHECKINS,
								KDATA_HF_PARTICIPATE:		STAT_HF_PARTICIPATE }

# File handles		
fhDetailCSV				= None
detailCSVDateYmd		= None
fhSummaryCSV			= None
fhStatusTemplate		= None
fhStatusKml				= None

"""
##########################################
		SECURITY
##########################################
"""

#
# Goo Login
#
def login():
	"""
	Handle Credentials
	"""
	creds = None

	# Get pickle (session token) figured out.
	# The file token.pickle stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists(gooPickleSpec):
		with open(gooPickleSpec, 'rb') as token:
			creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(gooCredentialsSpec, SCOPES)
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open(gooPickleSpec, 'wb') as token:
			pickle.dump(creds, token)

	# Connect to Google Sheets service
	service = build('sheets', 'v4', credentials=creds)
	return service

"""
##########################################
		FUNCTIONS
##########################################
"""

#
# Regurgitation
#
def barfd(text):
	if _appOptions.debug():	print(text)

def barf(text):
	print (text)


#
# CSV/Data Functions
#
def csvText(dataValue,dataType,addSeparator=True):										# Format data as CSV text
	outText = ''
	if dataType == DTYPE_NUMERIC:	outText = str(coalesce(dataValue,0))
	if dataType == DTYPE_TEXT:		outText = CSV_FIELD_QUOTE + dataValue + CSV_FIELD_QUOTE
	if dataType == DTYPE_DATE:		outText = dateParser().parseDate(dataValue).dateYMD()
	if addSeparator:				outText += CSV_FIELD_SEP
	return outText
	
def rowElem(elemNo,rowData = []):														# Row Element - get a cell value from a spreadsheet gshtRow.
	elemValue = ''
	if elemNo < len(rowData):	elemValue = rowData[elemNo]
	return elemValue

#
# Scoring stuff
#
def impactWeight(impactSeverity):														# Determine Impact Weight - numeric weight of a severity code (A,M,S)
	weight = 0
	if impactSeverity.strip() == IMPACT_CODE_AVAILABLE:	weight = 1
	if impactSeverity.strip() == IMPACT_CODE_MODERATE:	weight = 2
	if impactSeverity.strip() == IMPACT_CODE_SEVERE:	weight = 3
#	if impactSeverity.strip() == IMPACT_CODE_ZOMBIES:	weight = 12
	return weight

def impactScore(totalWeight,observeCount):												# Calculate Impact Score
	score = 0.0
	if observeCount > 0: score = round(totalWeight / observeCount,2)
	return score
	
def impactCodeFromScore(score):															# Derive Impact Code (A,M,S) from Impact Score
	impactCode = 'U'
	score = round(score)
	if score == 1: impactCode = IMPACT_CODE_AVAILABLE
	if score == 2: impactCode = IMPACT_CODE_MODERATE
	if score == 3: impactCode = IMPACT_CODE_SEVERE
#	if score >= 4: impactCode = IMPACT_CODE_ZOMBIES
	return impactCode
	
def nullz(someValue):																	# Coalesce null and empty string -> zero
	retVal = 0
	if not someValue is None and someValue.strip() != "": retVal = int(someValue)
	return retVal
	
def coalesce(someValue,ifNullValue):																	# Coalesce null and empty string -> zero
	retVal = someValue
	if someValue is None or someValue == "": retVal = ifNullValue
	return retVal

#
# Stats
# 
def statsGenerateCalculatedData():
	global covidStats
	global covidDailyCounts
	for countyName in covidStats.keys():

		countyStats	= covidStats[countyName]

		countyStats[STAT_STATUS_START_DATE]			= _appOptions.startDate()
		countyStats[STAT_STATUS_END_DATE]			= _appOptions.endDate()
		countyStats[STAT_STATUS_NDAYS]				= len(countyStats[STAT_DAILY_COUNTS].keys())	# Number of days having observations

		totalWeight = countyStats[STAT_UTILITIES_WEIGHT] + countyStats[STAT_SERVICES_WEIGHT] + countyStats[STAT_CONSUMABLES_WEIGHT]
		totalObservations = countyStats[STAT_STATUS_REPORTS] * 3
		countyStats[STAT_OVERALL_IMPACT_SCORE]		= impactScore(totalWeight,totalObservations)

		countyStats[STAT_UTILITIES_IMPACT_SCORE]	= impactScore(countyStats[STAT_UTILITIES_WEIGHT],countyStats[STAT_STATUS_REPORTS])
		countyStats[STAT_SERVICES_IMPACT_SCORE]		= impactScore(countyStats[STAT_SERVICES_WEIGHT],countyStats[STAT_STATUS_REPORTS])
		countyStats[STAT_CONSUMABLES_IMPACT_SCORE]	= impactScore(countyStats[STAT_CONSUMABLES_WEIGHT],countyStats[STAT_STATUS_REPORTS])

		countyStats[STAT_MAX_SCORE]					= max(countyStats[STAT_UTILITIES_IMPACT_SCORE],
														  countyStats[STAT_SERVICES_IMPACT_SCORE],
														  countyStats[STAT_CONSUMABLES_IMPACT_SCORE])

		countyStats[STAT_OVERALL_IMPACT_CODE]		= impactCodeFromScore(countyStats[STAT_OVERALL_IMPACT_SCORE])
		countyStats[STAT_MAX_SCORE_CODE]			= impactCodeFromScore(countyStats[STAT_MAX_SCORE])
		countyStats[STAT_MAX_IMPACT_CODE]			= impactCodeFromScore(countyStats[STAT_MAX_IMPACT])
		countyStats[STAT_UTILITIES_IMPACT_CODE]		= impactCodeFromScore(countyStats[STAT_UTILITIES_IMPACT_SCORE])
		countyStats[STAT_SERVICES_IMPACT_CODE]		= impactCodeFromScore(countyStats[STAT_SERVICES_IMPACT_SCORE])
		countyStats[STAT_CONSUMABLES_IMPACT_CODE]	= impactCodeFromScore(countyStats[STAT_CONSUMABLES_IMPACT_SCORE])

	return


"""
##########################################
		OUTPUT PROCESSING
##########################################
"""

#
# Detail CSV (output)
#
def detailCsvCleanup():
	barfd("DEBUG: detailCsvCleanup()")
	detailStartTS = _appOptions.startDateTS()
	detailDateTS = detailStartTS
	deltaOneDay = timedelta(days=1)
	
	for dayNo in range(_appOptions.nDays()):
		barfd("DEBUG: detailCsvCleanup(cleanLoopNo={})".format(dayNo))
		detailDateYmd = detailDateTS.strftime(FORMAT_YMD)
		detailCsvSpec = detailCsvTemplate.replace(TEMPLATE_DATE_TOKEN,detailDateYmd)
		barfd("DEBUG: detailCsvCleanup({},date={},file={})".format(dayNo,detailDateYmd,detailCsvSpec))
		if os.path.isfile(detailCsvSpec):
			barfd("DEBUG: detailCsvCleanup(deleteFile={})".format(detailCsvSpec))
			os.remove(detailCsvSpec)
		detailDateTS = detailDateTS + deltaOneDay

	return True

def detailCsvClose():																	# Close Detail CSV
	global fhDetailCSV
	global detailCSVDateYmd
	barfd("DEBUG: detailCSVClose(date={})".format(detailCSVDateYmd))
	fhDetailCSV.close()
	fhDetailCSV = None
	detailCSVDateYmd = None
	return True

def detailCsvOpen(dateYmd):																# Open Detail CSV for output
	global fhDetailCSV
	global detailCSVDateYmd

	if not fhDetailCSV is None and dateYmd != detailCSVDateYmd:
		detailCsvClose()

	if fhDetailCSV is None:
		detailCsvSpec = detailCsvTemplate.replace(TEMPLATE_DATE_TOKEN,dateYmd)
		isNew = not os.path.isfile(detailCsvSpec)
		barfd("DEBUG: detailCSVOpen(isNew={},file={})".format(isNew,detailCsvSpec))
		fhDetailCSV = open(detailCsvSpec, 'a')
		if fhDetailCSV is None:
			print("ERROR: Can't open output detailCsv ({})".format(detailCsvSpec))
			sys.exit(1)
		if isNew: detailCsvWriteHeader(dateYmd)

	detailCSVDateYmd = dateYmd
	return True

def detailCsvWriteHeader(dateYmd):														# Write Detail CSV header
	barfd("DEBUG: detailCSVWriteHeader")
	csvLine = ''
	for colMeta in DCSV_METADATA:
		csvLine += csvText(colMeta[COL_HEADER], DTYPE_TEXT, True)
	
	detailCsvWrite(dateYmd,csvLine)

def detailCsvWriteRow(dateYmd,gshtRow):													# Write Google Sheet row to Detail CSV
	csvLine = ''
	for colMeta in DCSV_METADATA:
		csvLine += csvText(rowElem(colMeta[COL_SOURCE],gshtRow), colMeta[COL_DTYPE], True)	# TODO: type conversion problem possibilities? be careful mapping fields

	detailCsvWrite(dateYmd,csvLine)

def detailCsvWrite(dateYmd,text):														# Write text to Detail CSV
	detailCsvOpen(dateYmd)
	barfd("DEBUG: detailCsvWrite({})".format(text))
	fhDetailCSV.write(text + '\n')

#
# Summary CSV (output)
#
def summaryCsvOpen():																	# Open Summary CSV for output
	global fhSummaryCSV
	if fhSummaryCSV is None:
		summaryCsvSpec = summaryCsvTemplate.replace(TEMPLATE_DATE_TOKEN,_appOptions.endDate())
		barfd("DEBUG: summaryCSVOpen(file={})".format(summaryCsvSpec))
		fhSummaryCSV = open(summaryCsvSpec, 'w')
		summaryCsvWriteHeader()

def summaryCsvClose():																	# Close Summary CSV
	global fhSummaryCSV
	barfd("DEBUG: summaryCSVClose")
	fhSummaryCSV.close()
	fhSummaryCSV = None

def summaryCsvWriteHeader():															# Write Summary CSV header
	csvLine = ''
	for colMeta in SCSV_METADATA:
		csvLine += csvText(colMeta[COL_HEADER], DTYPE_TEXT, True)
	
	summaryCsvWrite(csvLine)

def summaryCsvWrite(text):																# Write text to Summary CSV
	summaryCsvOpen()
	fhSummaryCSV.write(text + '\n')

def summaryCsvGenerate():																# Write a summary row to Summary CSV
	generateStatus = True
	barf("Summary data generating ...")
	for countyName in covidStats.keys():
		countyStats	= covidStats[countyName]
		csvLine 	= ''
		for colMeta in SCSV_METADATA:
			if colMeta[COL_ID] == SCSV_START_DATE:			csvLine += csvText(_appOptions.startDate(), colMeta[COL_DTYPE])
			if colMeta[COL_ID] == SCSV_END_DATE:			csvLine += csvText(_appOptions.endDate(), colMeta[COL_DTYPE])
			if colMeta[COL_ID] == SCSV_NDAYS:				csvLine += csvText(_appOptions.nDays(), colMeta[COL_DTYPE])
			if colMeta[COL_ID] == SCSV_COUNTY:				csvLine += csvText(countyName, colMeta[COL_DTYPE])
			if colMeta[COL_ID] == SCSV_OBSERVATIONS:		csvLine += csvText(countyStats[STAT_STATUS_REPORTS], colMeta[COL_DTYPE])
			if colMeta[COL_ID] == SCSV_UTILITIES_WEIGHT:	csvLine += csvText(countyStats[STAT_UTILITIES_WEIGHT], colMeta[COL_DTYPE])
			if colMeta[COL_ID] == SCSV_SERVICES_WEIGHT:		csvLine += csvText(countyStats[STAT_SERVICES_WEIGHT], colMeta[COL_DTYPE])
			if colMeta[COL_ID] == SCSV_CONSUMABLES_WEIGHT:	csvLine += csvText(countyStats[STAT_CONSUMABLES_WEIGHT], colMeta[COL_DTYPE])
			if colMeta[COL_ID] == SCSV_UTILITIES_IMPACT:	csvLine += csvText(countyStats[STAT_UTILITIES_IMPACT_CODE], colMeta[COL_DTYPE])
			if colMeta[COL_ID] == SCSV_SERVICES_IMPACT:		csvLine += csvText(countyStats[STAT_SERVICES_IMPACT_CODE], colMeta[COL_DTYPE])
			if colMeta[COL_ID] == SCSV_CONSUMABLES_IMPACT:	csvLine += csvText(countyStats[STAT_CONSUMABLES_IMPACT_CODE], colMeta[COL_DTYPE])
			if colMeta[COL_ID] == SCSV_MAX_IMPACT:			csvLine += csvText(countyStats[STAT_MAX_IMPACT_CODE], colMeta[COL_DTYPE])
			if colMeta[COL_ID] == SCSV_2M_CHECKINS:			csvLine += csvText(countyStats[STAT_2M_CHECKINS], colMeta[COL_DTYPE])
			if colMeta[COL_ID] == SCSV_2M_PARTICIPATE:		csvLine += csvText(countyStats[STAT_2M_PARTICIPATE], colMeta[COL_DTYPE])
			if colMeta[COL_ID] == SCSV_HF_CHECKINS:			csvLine += csvText(countyStats[STAT_HF_CHECKINS], colMeta[COL_DTYPE])
			if colMeta[COL_ID] == SCSV_HF_PARTICIPATE:		csvLine += csvText(countyStats[STAT_HF_PARTICIPATE], colMeta[COL_DTYPE])

		summaryCsvWrite(csvLine)

	summaryCsvClose()
	
	barf("Summary data complete. Stats recorded for {} counties.".format(len(covidStats)))
	return generateStatus

#
# Status Kml (output)
#
def statusKmlOpen(kmlSpec):																# Open Status KML for output
	global fhStatusKml
	if fhStatusKml is None:
		summmaryCsvSpec = summaryCsvTemplate.replace(TEMPLATE_DATE_TOKEN,_appOptions.endDate())
		barfd("DEBUG: statusKmlOpen({})".format(kmlSpec))
		fhStatusKml = open(kmlSpec, 'w')

def statusKmlClose():																	# Close Status KML
	global fhStatusKml
	barfd("DEBUG: statusKmlClose")
	fhStatusKml.close()
	fhStatusKml = None

def statusKmlWrite(text):																# Write text to Status KML
	fhStatusKml.write(text + '\n')

def statusKmlCreate(kmlLines,kmlSpec):													# Dump kml lines list to Status KML
	barfd("DEBUG: statusKmlCreate.Enter({})".format(kmlSpec))
	statusKmlOpen(kmlSpec)

	for kmlLine in kmlLines:
		statusKmlWrite(kmlLine)

	statusKmlClose()

#
# Write covidReportData
#
def ReportParamsXmit():
	barfd("DEBUG: ReportParamsXmit({})".format(reportInfoXmitSpec))
	fhXmit = open(reportInfoXmitSpec, 'w')
	fhXmit.write("{}={}\n".format(XMIT_START_DATE,_appOptions.startDate()))
	fhXmit.write("{}={}\n".format(XMIT_END_DATE,_appOptions.endDate()))
	fhXmit.close()


"""
##########################################
		INPUT PROCESSING
##########################################
"""

#
# Fetch Corona Data
#
def fetchCoronaData(service):
	global covidStats
	global covidDailyCounts

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

	covidDailyCounts	= {}

	if not values:
		print('ERROR: No spreadsheet data found.')
	else:																					# Walk spreadsheet data filtered by date and build stats by county
		barfd("DEBUG: fetchCoronaData.process sheet values")
		barfd("DEBUG: args.startDate={}, args.endDate={}".format(_appOptions.startDate(),_appOptions.endDate()))
		covidStats	= {COUNTY_DEFAULT: COUNTY_STATS_DEFAULT}																
		for gshtRow in values:
			gshtRowCt += 1
			if gshtRowCt == 1: continue														# Skip header gshtRow
			infoDate = rowElem(GSHT_DATE,gshtRow)
			barfd("DEBUG: fetchCoronaData.date={},site={},county={}".format(infoDate,rowElem(GSHT_SITE,gshtRow),rowElem(GSHT_COUNTY,gshtRow)))
			infoYmd = dateParser().parseDate(infoDate).dateYMD()
			if not infoYmd in covidDailyCounts: covidDailyCounts[infoYmd] = 0
			covidDailyCounts[infoYmd] += 1

			# Filer by date
			if infoYmd >= _appOptions.startDate() and  infoYmd <= _appOptions.endDate():

				gshtMatchRowCt += 1
				county	 = rowElem(GSHT_COUNTY,gshtRow)
				# Add to statics
				if county != "":
					if not county in covidStats: covidStats[county] = copy.deepcopy(COUNTY_STATS_DEFAULT)

					if county=='Kent': barfd("DEBUG: FetchAddStats1:(util:{},svc:{},cons:{},max:{})".format(impactWeight(rowElem(GSHT_UTILITIES,gshtRow)),	\
																										 impactWeight(rowElem(GSHT_SERVICES,gshtRow)),	\
																										 impactWeight(rowElem(GSHT_CONSUMABLES,gshtRow)),	\
																										 covidStats[county][STAT_MAX_IMPACT]))
					covidStats[county][STAT_STATUS_REPORTS]			+= 1
					covidStats[county][STAT_UTILITIES_WEIGHT]		+= impactWeight(rowElem(GSHT_UTILITIES,gshtRow))
					covidStats[county][STAT_SERVICES_WEIGHT]		+= impactWeight(rowElem(GSHT_SERVICES,gshtRow))
					covidStats[county][STAT_CONSUMABLES_WEIGHT]		+= impactWeight(rowElem(GSHT_CONSUMABLES,gshtRow))
					covidStats[county][STAT_MAX_IMPACT]				=  max(covidStats[county][STAT_MAX_IMPACT], 			\
																			impactWeight(rowElem(GSHT_UTILITIES,gshtRow)),	\
																			impactWeight(rowElem(GSHT_SERVICES,gshtRow)),	\
																			impactWeight(rowElem(GSHT_CONSUMABLES,gshtRow)))

					if county=='Kent': barfd("DEBUG: FetchAddStats2:(util:{},svc:{},cons:{},max:{})".format(impactWeight(rowElem(GSHT_UTILITIES,gshtRow)),	\
																										 impactWeight(rowElem(GSHT_SERVICES,gshtRow)),	\
																										 impactWeight(rowElem(GSHT_CONSUMABLES,gshtRow)),	\
																										 covidStats[county][STAT_MAX_IMPACT]))

					covidStats[county][STAT_2M_CHECKINS]			+= nullz(rowElem(GSHT_2M_CHECKINS,gshtRow))
					covidStats[county][STAT_2M_PARTICIPATE] 		+= nullz(rowElem(GSHT_2M_PARTICIPATE,gshtRow))
					covidStats[county][STAT_HF_CHECKINS]			+= nullz(rowElem(GSHT_HF_CHECKINS,gshtRow))
					covidStats[county][STAT_HF_PARTICIPATE] 		+= nullz(rowElem(GSHT_HF_PARTICIPATE,gshtRow))

					if infoYmd not in covidStats[county][STAT_DAILY_COUNTS]: covidStats[county][STAT_DAILY_COUNTS][infoYmd] = 0
					covidStats[county][STAT_DAILY_COUNTS][infoYmd] += 1

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
	
	barfd("DEBUG: covidStats:{}".format(covidStats['Kent']))
	
	barfd("DEBUG: fetchCoronaData.exit rowCt={},matchCt={}".format(gshtRowCt,gshtMatchRowCt))
	return fetchStatus

"""
##########################################
		KML DATA MERGE
##########################################
"""

def mergeKmlData():
	mergeKmlSuccess = True

	# Walk KML looking for placemarks, and set data values as appropriate from stats hash
	# Typical county placemark...
	#	<Placemark>
	#		<name>Alcona</name>
	#		<styleUrl>#countyDefault</styleUrl>												#TODO: update style based on STATUS_OVERALL
	#		<ExtendedData>
	#			<SchemaData schemaUrl="#MHGCoronaData">
	#				<SimpleData name="STATUS_OVERALL">U</SimpleData>
	#				<SimpleData name="STATUS_MAX">U</SimpleData>
	#				<SimpleData name="STATUS_UTILITIES">U</SimpleData>
	#				<SimpleData name="STATUS_SERVICES">U</SimpleData>
	#				<SimpleData name="STATUS_CONSUMABLES">U</SimpleData>
	#			</SchemaData>
	#		</ExtendedData>

	barfd("DEBUG: mergeKmlData.enter")
	barf("KML Generating...")
	with open(statusTemplateSpec) as fhStatusTemplate:

		kmlLines = fhStatusTemplate.readlines()
		barfd("DEBUG: mergeKmlData.readlines({} read)".format(len(kmlLines)))
		
		errorText 				= ''
		countyName				= None
		
		placemarkPattern 		= re.compile('^[\t ]*<Placemark>[\t ]*$')
		placemarkEndPattern		= re.compile('^[\t ]*</Placemark>[\t ]*$')
		countyNamePattern 		= re.compile('^[\t ]*<name>([A-Za-z]+)</name>[\t ]*$')
		stylePattern	 		= re.compile('(^[\t ]*<styleUrl>)([^<]+)(</styleUrl>[\t ]*)$')
		schemaDataStartPattern 	= re.compile('^[\t ]*<SchemaData schemaUrl="' + KDATA_SCHEMA + '">[\t ]*$')
		schemaDataItemPattern	= re.compile('^[\t ]*<SimpleData name="([A-Za-z_]+)">([^<]*)</SimpleData>[\t ]*$')
		schemaDataUpdatePattern	= re.compile('^([\t ]*<SimpleData name="[A-Za-z_]+">)([^<]*)(</SimpleData>[\t ]*)$')
		schemaDataEndPattern 	= re.compile('^[\t ]*</SchemaData>[\t ]*$')

		statsKey = None
		lookFor  = 'placemark'
		for kmlLineIndex in range(0,len(kmlLines)-1):
			kmlLines[kmlLineIndex] = kmlLines[kmlLineIndex].replace(chr(10),'')
			kmlLines[kmlLineIndex] = kmlLines[kmlLineIndex].replace(chr(13),'')
			kmlLine = kmlLines[kmlLineIndex]
			lookForLast = lookFor
			if lookFor == 'placemark' and placemarkPattern.match(kmlLine):  lookFor = 'county'
			if lookFor == 'county' and countyNamePattern.match(kmlLine):
				countyName = countyNamePattern.match(kmlLine).group(1)
				statsKey   = countyName
				barfd("DEBUG: mergeKmlData.evalCounty({})".format(countyName))
				lookFor = 'style'
				#if not countyName in covidStats: lookFor = 'placemark'
				if not countyName in covidStats: statsKey = COUNTY_DEFAULT				# If we don't have stats, use default values
				
			if lookFor == 'style' and stylePattern.match(kmlLine):
				styleMatch = stylePattern.match(kmlLine)
				newStyle = impactCodeStyleMap[covidStats[statsKey][STAT_OVERALL_IMPACT_CODE]]
				kmlLines[kmlLineIndex] = styleMatch.group(1) + newStyle + styleMatch.group(3)
				lookFor = 'schemaStart'

			if lookFor == 'schemaStart' and schemaDataStartPattern.match(kmlLine): lookFor = 'schemaData'
			if lookFor == 'schemaData'  and schemaDataItemPattern.match(kmlLine):
				if countyName == 'Kent': barfd("DEBUG: Evaluating DataItem kmlLine={}".format(kmlLine))
				schemaDataItemMatch = schemaDataItemPattern.match(kmlLine)
				schemaItemName	= schemaDataItemMatch.group(1)
				schemaItemValue	= schemaDataItemMatch.group(2)
				if schemaItemName in statsSchemaDataMap:
					statName = statsSchemaDataMap[schemaItemName]
					if countyName == 'Kent': barfd("DEBUG: Updating kmlLine={}".format(kmlLine))
					schemaDataUpdateMatch = schemaDataUpdatePattern.match(kmlLine)
					kmlLines[kmlLineIndex] = schemaDataUpdateMatch.group(1) + str(covidStats[statsKey][statName]) + schemaDataUpdateMatch.group(3)
					if countyName == 'Kent': barfd("DEBUG: Updated kmlLine={}".format(kmlLines[kmlLineIndex]))

			if (lookFor == 'schemaData' or lookFor == lookForLast) and schemaDataEndPattern.match(kmlLine): lookFor = 'placemark'

		statusKmlDailySpec = statusKmlDailyTemplate.replace(TEMPLATE_DATE_TOKEN,_appOptions.endDate())
		statusKmlCreate(kmlLines,statusKmlDailySpec)
		statusKmlCreate(kmlLines,statusKmlCurrentSpec)

	barf("KML Generation complete. File={}".format(statusKmlDailySpec))
	barfd("DEBUG: mergeKmlData.exit")
	return mergeKmlData

#
# Command Arguments
#
def getCommandArguments():
	global _appOptions

	success = False
	
	_appOptions = mhgFetchCommandArgs()
	success = _appOptions.getArguments()

	return success

#
# Exit handler
#
def appExit(statusCode,errorText=''):
	statusText = ''
	if errorText != '': print(errorText)
	if statusCode != ERR_NONE: statusText = " Status={}".format(statusCode)
	print ("####\n#### {} complete.{}\n####".format(PROGNM,statusText))
	sys.exit(statusCode)
	

"""
##########################################
		MAIN
##########################################
"""
def main():

	print ("####\n#### {} starting.\n####".format(PROGNM))

	if not getCommandArguments():
		barf("FATALITY trying to parse arguments")
		sys.exit(1)

	if _appOptions.captureDetail(): detailCsvCleanup()

	service = login()
	if service:	
		fetchOk = fetchCoronaData(service)
		if not fetchOk: 
			appExit(ERR_FETCHFAIL)
		else:
			statsGenerateCalculatedData()
			if _appOptions.generateSummary(): summaryCsvGenerate()
			mergeKmlData()

	
	ReportParamsXmit()
	
	appExit(ERR_NONE)


if __name__ == '__main__':
	main()
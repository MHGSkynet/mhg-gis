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
#   MHGCovidDetail		Michigan KML file with 
#
# Copyright
#
#	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#						non profit conservative organizations and individuals to use in support
#						of American freedom and the constitution. All other rights are reserved,
#						and any other use prohibited.
#
# Date			Version		Author			Description
# 2020.04.04	01.01		SquintMHG		Fix filter date compare problem
# 2020.03.27	01.00		SquintMHG		Initial version
# ---------------------------------------------------------------------------------------------

from __future__ import print_function
import argparse
import os
import os.path
import re
import sys
from pathlib import Path
from datetime import datetime

import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

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

#
# Exit handler
#
def appExit(statusCode,errorText=''):
	statusText = ''
	if errorText != '': print(errorText)
	if statusCode != ERR_NONE: statusText = " Status={}".format(statusCode)
	print ("####\n#### {} complete.{}\n####".format(PROGNM,statusText))
	sys.exit(statusCode)

#
# Package Info
#
def getPackageRoot():																	# Get package root folder
	packageRoot = os.environ.get(ENV_PACKAGE_FOLDER)									# See if root folder is defined
	errorText 	= ''
	errorText2 	= ''
	if packageRoot is None:
		packageRoot = "./"
		errorText2 = "ERROR: {} environment var is not defined and current folder is not package root folder.".format(ENV_PACKAGE_FOLDER)
	else:
		packageRoot = packageRoot.replace("\\","/")
		packagePath = Path(packageRoot)
		if not packagePath.is_dir():
			errorText = "ERROR: {} environment var is not a valid folder".format(ENV_PACKAGE_FOLDER)
		else:
			errorText2 = "ERROR: {} environment var does not point to package root".format(ENV_PACKAGE_FOLDER)
	
	if packageRoot[-1:] != '/':		packageRoot = packageRoot + '/'

	if errorText == '':
		for packageFolder in ROOT_KEY_FOLDERS:
			keyFolderSpec = packageRoot + packageFolder
			keyFolderPath = Path(keyFolderSpec)
#			print("DEBUG: testing install folder keyFolderSpec={}".format(keyFolderSpec))
			if not keyFolderPath.is_dir():
				errorText = "ERROR: Folder {} not found in package root. Invalid installation.".format(packageFolder)
				break

	if errorText != '':
		print(errorText)
		appExit(ERR_BADENV,errorText2)

	return packageRoot

def testDatePattern(regex,parseString,strptimeFormat,strptimeString=''):				# Test a date string for pattern match, and parse to timestamp on match
	if strptimeString == '': strptimeString = parseString
	dateTS = None																		
	pattern = re.compile(regex)
	if pattern.match(parseString):
		dateTS = datetime.strptime(strptimeString, strptimeFormat)
		
	return dateTS

def getParam(paramName):
	paramVal = ''
	if paramName == ENV_FILTER_DATE:
		filterTS = datetime.now()
		filterDate = os.environ.get(ENV_FILTER_DATE)
		if not filterDate is None:
			dateTS	= testDatePattern('^[0-9]{4}[.][0-9]+[.][0-9]+$', filterDate, '%Y.%m.%d')		#	yyyy.mm.dd
			if dateTS is None:
				appExit(ERR_BADFILTER,"ERROR: Parameter {} value ({}) is not yyyy.mm.dd format".format(ENV_FILTER_DATE,filterDate))
			else:
				filterTS = datetime.strptime(filterDate,"%Y.%m.%d")
		paramVal = filterTS
		
	return paramVal
	
OPT_CAPTURE_DETAIL		= 'CaptureDetail'												# Whether to capture detail to daily CSV files.
OPT_GENERATE_SUMAMRY	= 'GenerateSummary'												# Whether to generate daily summary info CSV file.
OPT_FILTER_START_DATE	= 'FilterStartDate'												# Beginning date of range to select data by
OPT_FILTER_END_DATE		= 'FilterEndDate'												# End date of range to select data by
OPT_FILTER_DAYS			= 'FilterDays'													# Number of days from begin date to select data by

defaultOptions = {	OPT_CAPTURE_DETAIL 		: True,
					OPT_GENERATE_SUMMARY	: True,
					OPT_DEBUG				: False,
					OPT_FILTER_START_DATE	: currentDateYmd,
					OPT_FILTER_END_DATE		: currentDateYmd,
					OPT_FILTER_DAYS			: 1
				}

options = {defaultOptions}

def getCommandArguments():

	i
	
	
	
	
	
	

"""
##########################################
		DRIVING DATA
##########################################
"""

# Driving Data
CAPTURE_DETAIL			= True															# Whether to capture detail to daily CSV files.
GENERATE_SUMMARY		= True															# Whether to generate daily summary info CSV file.
DEBUG_ON				= False															# Debug enable
ENV_FILTER_DATE			= 'MHGGIS_FILTER_DATE'											# Date to filter by environment variable 

# Environment 
ENV_PACKAGE_FOLDER		= 'MHGGIS_ROOT'													# MHGGIS Package root folder environment var

# System date
currTimestamp			= datetime.now() 												# current date and time (timestamp)
currDateYmd				= currTimestamp.strftime("%Y.%m.%d")							# current date YYYY.MM.DD (text)
currDateTS				= datetime.strptime(currDateYmd,"%Y.%m.%d")						# current date (timestamp)

# Goo Security
SCOPES 					= ['https://www.googleapis.com/auth/spreadsheets.readonly']		# If modifying scope(s), delete the file token.pickle.
COVID_SPREADSHEET_ID	= '1ckdKCNIB-5-KSUlV2ehW3KPARVlu_CC2npjsAHrml7Q'				# Google Document ID to fetch
COVID_DATA_RANGE		= 'DailyData!A1:H'												# Spreadsheet range to fetch

# Covid Selection Criteria
covidDateFilterTS		= getParam(ENV_FILTER_DATE)										# Date to filter Covid spreadsheet by (timestamp)
covidDateFilterYmd		= covidDateFilterTS.strftime("%Y.%m.%d")						# Date to filter Covid spreadsheet by (yyy.mm.dd)

# Folders
ROOT_KEY_FOLDERS		= [ 'covidFetch', 'data', 'kml', 'output' ] 					# MHGGIS Package folders for verification of install
PACKAGE_ROOT			= getPackageRoot()												# MHGGIS Package root folder for mgh-gis suite
APP_FOLDER				= PACKAGE_ROOT + 'covidFetch/'									# Application folder
DATA_FOLDER				= PACKAGE_ROOT + 'data/'										# Folder for data accumulation
KML_FOLDER				= PACKAGE_ROOT + 'kml/'											# Folder for kml
OUTPUT_FOLDER			= PACKAGE_ROOT + 'output/'										# Folder for output 

# Security File Specs
gooPickleSpec		  	= APP_FOLDER + 'token.pickle'									# Google API pickle file
gooCredentialsSpec		= APP_FOLDER + 'credentials.json'								# Google API credentials file

# Input Resource File Specs
statusTemplateSpec		= KML_FOLDER + "mhgCovidStatusMichigan.kml"								# Template KML of Michigan counties and MHG Covid data schema

# Output File Specs
detailCsvSpec			= DATA_FOLDER + "mhgCovidStatus-Detail-" + covidDateFilterYmd + ".csv"	# Detail CSV file specification (output)
summaryCsvSpec			= DATA_FOLDER + "mhgCovidStatus-Summary-" + covidDateFilterYmd + ".csv"	# Summary CSV file specification (output)
statusKmlCurrentSpec	= DATA_FOLDER + "mhgCovidStatus.kml"									# Status KML file (for input to covidReport)
statusKmlYmdSpec		= OUTPUT_FOLDER + "mhgCovidStatus-" + covidDateFilterYmd + ".kml"		# Status KML file daily generated file

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
IMPACT_CODE_ZOMBIES		= 'Z'

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
GSHT_COMMENTS		= 7
GSHT_METADATA		= [ { COL_ID: GSHT_DATE,		COL_DTYPE: DTYPE_DATE,		COL_HEADER: 'ObservationDate'	},
						{ COL_ID: GSHT_SITE,		COL_DTYPE: DTYPE_TEXT,		COL_HEADER: 'Site' 				},
						{ COL_ID: GSHT_COUNTY,		COL_DTYPE: DTYPE_TEXT,		COL_HEADER: 'County'			},
						{ COL_ID: GSHT_UTILITIES,	COL_DTYPE: DTYPE_TEXT,		COL_HEADER: 'UtilityImpact'		},
						{ COL_ID: GSHT_SERVICES,	COL_DTYPE: DTYPE_TEXT,		COL_HEADER:	'ServicesImpact'	},
						{ COL_ID: GSHT_CONSUMABLES,	COL_DTYPE: DTYPE_TEXT,		COL_HEADER:	'ConsumablesImpact'	},
						{ COL_ID: GSHT_2M_CHECKINS,	COL_DTYPE: DTYPE_NUMERIC,	COL_HEADER:	'2MCheckins'		},
						{ COL_ID: GSHT_COMMENTS,	COL_DTYPE: DTYPE_TEXT,		COL_HEADER:	'Comments'			} ]

# Detail CSV (output) metadata
DCSV_DATE			= 0
DCSV_SITE			= 1
DCSV_COUNTY			= 2
DCSV_UTILITIES		= 3
DCSV_SERVICES		= 4
DCSV_CONSUMABLES	= 5
DCSV_2M_CHECKINS	= 6
DCSV_COMMENTS		= 7
DCSV_METADATA		= [ { COL_ID: DCSV_DATE,		COL_DTYPE: DTYPE_DATE,		COL_HEADER: 'ObservationDate',		COL_SOURCE: GSHT_DATE			},
						{ COL_ID: DCSV_SITE,		COL_DTYPE: DTYPE_TEXT,		COL_HEADER: 'Site',					COL_SOURCE: GSHT_SITE			},
						{ COL_ID: DCSV_COUNTY,		COL_DTYPE: DTYPE_TEXT,		COL_HEADER: 'County',				COL_SOURCE: GSHT_COUNTY			},
						{ COL_ID: DCSV_UTILITIES,	COL_DTYPE: DTYPE_TEXT,		COL_HEADER: 'UtilityImpact',		COL_SOURCE:	GSHT_UTILITIES		},
						{ COL_ID: DCSV_SERVICES,	COL_DTYPE: DTYPE_TEXT,		COL_HEADER:	'ServicesImpact',		COL_SOURCE: GSHT_SERVICES		},
						{ COL_ID: DCSV_CONSUMABLES,	COL_DTYPE: DTYPE_TEXT,		COL_HEADER:	'ConsumablesImpact',	COL_SOURCE: GSHT_CONSUMABLES	},
						{ COL_ID: DCSV_2M_CHECKINS,	COL_DTYPE: DTYPE_NUMERIC,	COL_HEADER:	'2MCheckins',			COL_SOURCE: GSHT_2M_CHECKINS	},
						{ COL_ID: DCSV_COMMENTS,	COL_DTYPE: DTYPE_TEXT,		COL_HEADER:	'Comments',				COL_SOURCE: GSHT_COMMENTS		} ]

# Summary CSV (output) metadata
SCSV_DATE				= 0
SCSV_SITE				= 1
SCSV_COUNTY				= 2
SCSV_OBSERVATIONS		= 3
SCSV_UTILITIES_WEIGHT	= 4
SCSV_SERVICES_WEIGHT	= 5
SCSV_CONSUMABLES_WEIGHT	= 6
SCSV_UTILITIES_IMPACT	= 7
SCSV_SERVICES_IMPACT	= 8
SCSV_CONSUMABLES_IMPACT	= 9
SCSV_2M_REPORTS			= 10
SCSV_2M_CHECKINS		= 11
SCSV_METADATA		= [ { COL_ID: SCSV_DATE,				COL_DTYPE: DTYPE_DATE,		COL_HEADER: 'ObservationDate'	},
						{ COL_ID: SCSV_COUNTY,				COL_DTYPE: DTYPE_TEXT,		COL_HEADER: 'County'			},
						{ COL_ID: SCSV_OBSERVATIONS,		COL_DTYPE: DTYPE_NUMERIC,	COL_HEADER: 'ObservationCount'	},
						{ COL_ID: SCSV_UTILITIES_WEIGHT,	COL_DTYPE: DTYPE_NUMERIC,	COL_HEADER: 'UtilityWeight'		},
						{ COL_ID: SCSV_SERVICES_WEIGHT,		COL_DTYPE: DTYPE_NUMERIC,	COL_HEADER:	'ServicesWeight'	},
						{ COL_ID: SCSV_CONSUMABLES_WEIGHT,	COL_DTYPE: DTYPE_NUMERIC,	COL_HEADER:	'ConsumablesWeight'	},
						{ COL_ID: SCSV_UTILITIES_IMPACT,	COL_DTYPE: DTYPE_TEXT,		COL_HEADER: 'UtilityImpact'		},
						{ COL_ID: SCSV_SERVICES_IMPACT,		COL_DTYPE: DTYPE_TEXT,		COL_HEADER:	'ServicesImpact'	},
						{ COL_ID: SCSV_CONSUMABLES_IMPACT,	COL_DTYPE: DTYPE_TEXT,		COL_HEADER:	'ConsumablesImpact'	},
						{ COL_ID: SCSV_2M_REPORTS,			COL_DTYPE: DTYPE_NUMERIC,	COL_HEADER:	'2MReports'			},
						{ COL_ID: SCSV_2M_CHECKINS,			COL_DTYPE: DTYPE_NUMERIC,	COL_HEADER:	'2MCheckins'		} ]

"""
##########################################
		WORKING DATA
##########################################
"""

# Statistics by County
STAT_STATUS_DATE				= 'StatusDate'										# Date of observations
STAT_STATUS_REPORTS				= 'StatusReports'									# Number of observations
STAT_UTILITIES_WEIGHT			= 'UtilitiesWeight'									# Total utility impact weight
STAT_SERVICES_WEIGHT			= 'ServicesWeight'									# Total services impact weight
STAT_CONSUMABLES_WEIGHT			= 'ConsumablesWeight'								# Total consumables impact weight
STAT_2M_PARTICIPATION			= '2M Participate'									# Total 2M nets participated in
STAT_2M_CHECKINS				= '2M Checkins'										# Total 2M check-ins by net control

STAT_OVERALL_IMPACT_SCORE		= 'OverallImpactScore'								# Overall Impact Score
STAT_MAX_IMPACT_SCORE			= 'MaxImpactScore'									# Maximum Impact Score
STAT_UTILITIES_IMPACT_SCORE		= 'UtilitiesImpactScore'							# Utilities Impact Score
STAT_SERVICES_IMPACT_SCORE		= 'ServicesImpactScore'								# Services Impact Score
STAT_CONSUMABLES_IMPACT_SCORE	= 'ConsumablesImpactScore'							# Consumables Impact Score

STAT_OVERALL_IMPACT_CODE		= 'OverallImpactCode'								# Overall Impact Code (A,M,S)
STAT_MAX_IMPACT_CODE			= 'MaxImpactCode'									# Max Impact Code (A,M,S)
STAT_UTILITIES_IMPACT_CODE		= 'UtilitiesImpactCode'								# Utilities Impact Code (A,M,S)
STAT_SERVICES_IMPACT_CODE		= 'ServicesImpactCode'								# Services Impact Code (A,M,S)
STAT_CONSUMABLES_IMPACT_CODE	= 'ConsumablesImpactCode'							# Consumables Impact Code (A,M,S)

COUNTY_DEFAULT					= 'DEFAULT'											# Default county values
defaultStats					= { STAT_STATUS_DATE:		covidDateFilterYmd,
									STAT_STATUS_REPORTS:			0,
									STAT_UTILITIES_WEIGHT:			0,
									STAT_SERVICES_WEIGHT:			0,
									STAT_CONSUMABLES_WEIGHT:		0,
									STAT_2M_PARTICIPATION:			0,
									STAT_2M_CHECKINS:				0,
									STAT_OVERALL_IMPACT_SCORE:		0,
									STAT_SERVICES_IMPACT_SCORE:		0,
									STAT_CONSUMABLES_IMPACT_SCORE:	0,
									STAT_OVERALL_IMPACT_CODE:		IMPACT_CODE_UNKNOWN,
									STAT_SERVICES_IMPACT_CODE:		IMPACT_CODE_UNKNOWN,
									STAT_CONSUMABLES_IMPACT_CODE:	IMPACT_CODE_UNKNOWN }

covidStats						= {COUNTY_DEFAULT: defaultStats}					# Statistics hash, by county

# KML Constants
KDATA_SCHEMA					= '#OGRGeoJSON'
KDATA_STATUS_DATE				= 'STATUS_DATE'
KDATA_STATUS_OVERALL			= 'STATUS_OVERALL'
KDATA_STATUS_MAX				= 'STATUS_MAX'
KDATA_STATUS_UTILITIES			= 'STATUS_UTILITIES'
KDATA_STATUS_SERVICES			= 'STATUS_SERVICES'
KDATA_STATUS_CONSUMBALES		= 'STATUS_CONSUMABLES'
KDATA_2M_CHECKINS				= 'CHECKINS_2M'
KDATA_2M_PARTICIPATION			= 'PARTICIPATE_2M'

KSTYLE_IMPACT_UNKNOWN			= '#impactUnknown'
KSTYLE_IMPACT_NONE				= '#impactNormal'
KSTYLE_IMPACT_MODERATE			= '#impactModerate'
KSTYLE_IMPACT_SEVERE			= '#impactSevere'
KSTYLE_IMPACT_ZOMBIES			= '#impactZombies'


impactCodeStyleMap				= { IMPACT_CODE_AVAILABLE: 	KSTYLE_IMPACT_NONE,
									IMPACT_CODE_MODERATE:	KSTYLE_IMPACT_MODERATE,
									IMPACT_CODE_SEVERE:		KSTYLE_IMPACT_SEVERE,
									IMPACT_CODE_UNKNOWN:	KSTYLE_IMPACT_UNKNOWN,
									IMPACT_CODE_ZOMBIES:	KSTYLE_IMPACT_ZOMBIES }
# Kml Data
kmlLines	= []

# Map of STAT_ items to KML Schema Data Items
statsSchemaDataMap			= { KDATA_STATUS_DATE: 			STAT_STATUS_DATE,
								KDATA_STATUS_OVERALL: 		STAT_OVERALL_IMPACT_CODE,
								KDATA_STATUS_MAX: 			STAT_MAX_IMPACT_CODE,
								KDATA_STATUS_UTILITIES:		STAT_UTILITIES_IMPACT_CODE,
								KDATA_STATUS_SERVICES:		STAT_SERVICES_IMPACT_CODE,
								KDATA_STATUS_CONSUMBALES:	STAT_CONSUMABLES_IMPACT_CODE,
								KDATA_2M_CHECKINS:			STAT_2M_CHECKINS,
								KDATA_2M_PARTICIPATION:		STAT_2M_PARTICIPATION }

# File handles		
fhDetailCSV				= None
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
	if DEBUG_ON:	print(text)

def barf(text):
	print (text)

#
# Date Routines
#
def parseDate(dateString):																# Parse a date string into a timestamp
	dateTS = None
	
	dateTS	= testDatePattern('^[0-9]+/[0-9]+$', dateString, '%Y/%m/%d', '2020/' + dateString)								#	mm/dd format
	if dateTS is None: dateTS	= testDatePattern('^[0-9]{4}[-][0-9]+[-][0-9]+$', dateString, '%Y-%m-%d', dateString)		#	yyyy-mm-dd
	if dateTS is None: dateTS	= testDatePattern('^[0-9]{4}[/][0-9]+[/][0-9]+$', dateString, '%Y/%m/%d', dateString)		#	yyyy/mm/dd
	if dateTS is None: dateTS	= testDatePattern('^[0-9]{4}[.][0-9]+[.][0-9]+$', dateString, '%Y.%m.%d', dateString)		#	yyyy.mm.dd

	return dateTS

#
# CSV/Data Functions
#
def csvText(dataValue,dataType,addSeparator=True):										# Format data as CSV text
	outText = ''
	if dataType == DTYPE_NUMERIC:	outText = str(dataValue)
	if dataType == DTYPE_TEXT:		outText = CSV_FIELD_QUOTE + dataValue + CSV_FIELD_QUOTE
	if dataType == DTYPE_DATE:		
		dateTS = parseDate(dataValue)
		outText = dateTS.strftime('%Y-%m-%d')

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
	if impactSeverity.strip() == IMPACT_CODE_ZOMBIES:	weight = 12
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
	if score >= 4: impactCode = IMPACT_CODE_ZOMBIES
	return impactCode
	
def nullz(someValue):																	# Coalesce null and empty string -> zero
	retVal = 0
	if not someValue is None and someValue.strip() != "": retVal = int(someValue)
	return retVal
	
#
# Stats
# 
def statsGenerateCalculatedData():
	global covidStats
	for countyName in covidStats.keys():

		countyStats	= covidStats[countyName]

		countyStats[STAT_STATUS_DATE]				= covidDateFilterYmd

		totalWeight = countyStats[STAT_UTILITIES_WEIGHT] + countyStats[STAT_SERVICES_WEIGHT] + countyStats[STAT_CONSUMABLES_WEIGHT]
		totalObservations = countyStats[STAT_STATUS_REPORTS] * 3
		countyStats[STAT_OVERALL_IMPACT_SCORE]		= impactScore(totalWeight,totalObservations)

		countyStats[STAT_UTILITIES_IMPACT_SCORE]	= impactScore(countyStats[STAT_UTILITIES_WEIGHT],countyStats[STAT_STATUS_REPORTS])
		countyStats[STAT_SERVICES_IMPACT_SCORE]		= impactScore(countyStats[STAT_SERVICES_WEIGHT],countyStats[STAT_STATUS_REPORTS])
		countyStats[STAT_CONSUMABLES_IMPACT_SCORE]	= impactScore(countyStats[STAT_CONSUMABLES_WEIGHT],countyStats[STAT_STATUS_REPORTS])

		countyStats[STAT_MAX_IMPACT_SCORE]			= max(countyStats[STAT_UTILITIES_IMPACT_SCORE],
														  countyStats[STAT_SERVICES_IMPACT_SCORE],
														  countyStats[STAT_CONSUMABLES_IMPACT_SCORE])

		countyStats[STAT_OVERALL_IMPACT_CODE]		= impactCodeFromScore(countyStats[STAT_OVERALL_IMPACT_SCORE])
		countyStats[STAT_MAX_IMPACT_CODE]			= impactCodeFromScore(countyStats[STAT_MAX_IMPACT_SCORE])
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
def detailCsvClose():																	# Close Detail CSV
	global fhDetailCSV
	barfd("DEBUG: detailCSVClose")
	fhDetailCSV.close()
	fhDetailCSV = None

def detailCsvOpen():																	# Open Detail CSV for output
	global fhDetailCSV
	if fhDetailCSV is None:
		barfd("DEBUG: detailCSVOpen")
		fhDetailCSV = open(detailCsvSpec, 'w')
		if fhDetailCSV is None:
			print("ERROR: Can't open output detailCsv ({})".format(detailCsvSpec))
			sys.exit(1)
		detailCsvWriteHeader()

def detailCsvWriteHeader():																# Write Detail CSV header
	barfd("DEBUG: detailCSVWriteHeader")
	csvLine = ''
	for colMeta in DCSV_METADATA:
		csvLine += csvText(colMeta[COL_HEADER], DTYPE_TEXT, True)
	
	detailCsvWrite(csvLine)

def detailCsvWriteRow(gshtRow):															# Write Google Sheet row to Detail CSV
	csvLine = ''
	for colMeta in DCSV_METADATA:
		csvLine += csvText(rowElem(colMeta[COL_SOURCE],gshtRow), colMeta[COL_DTYPE], True)	# TODO: type conversion problem possibilities? be careful mapping fields

	detailCsvWrite(csvLine)

def detailCsvWrite(text):																# Write text to Detail CSV
	detailCsvOpen()
	barfd("DEBUG: detailCsvWrite({})".format(text))
	fhDetailCSV.write(text + '\n')

#
# Summary CSV (output)
#
def summaryCsvOpen():																	# Open Summary CSV for output
	global fhSummaryCSV
	if fhSummaryCSV is None:
		barfd("DEBUG: summaryCSVOpen")
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
			if colMeta[COL_ID] == SCSV_DATE:				csvLine += csvText(covidDateFilterYmd, colMeta[COL_DTYPE])
			if colMeta[COL_ID] == SCSV_COUNTY:				csvLine += csvText(countyName, colMeta[COL_DTYPE])
			if colMeta[COL_ID] == SCSV_OBSERVATIONS:		csvLine += csvText(countyStats[STAT_STATUS_REPORTS], colMeta[COL_DTYPE])
			if colMeta[COL_ID] == SCSV_UTILITIES_WEIGHT:	csvLine += csvText(countyStats[STAT_UTILITIES_WEIGHT], colMeta[COL_DTYPE])
			if colMeta[COL_ID] == SCSV_SERVICES_WEIGHT:		csvLine += csvText(countyStats[STAT_SERVICES_WEIGHT], colMeta[COL_DTYPE])
			if colMeta[COL_ID] == SCSV_CONSUMABLES_WEIGHT:	csvLine += csvText(countyStats[STAT_CONSUMABLES_WEIGHT], colMeta[COL_DTYPE])
			if colMeta[COL_ID] == SCSV_UTILITIES_IMPACT:	csvLine += csvText(countyStats[STAT_UTILITIES_IMPACT_CODE], colMeta[COL_DTYPE])
			if colMeta[COL_ID] == SCSV_SERVICES_IMPACT:		csvLine += csvText(countyStats[STAT_SERVICES_IMPACT_CODE], colMeta[COL_DTYPE])
			if colMeta[COL_ID] == SCSV_CONSUMABLES_IMPACT:	csvLine += csvText(countyStats[STAT_CONSUMABLES_IMPACT_CODE], colMeta[COL_DTYPE])
			if colMeta[COL_ID] == SCSV_2M_CHECKINS:			csvLine += csvText(countyStats[STAT_2M_CHECKINS], colMeta[COL_DTYPE])
			if colMeta[COL_ID] == SCSV_2M_REPORTS:			csvLine += csvText(countyStats[STAT_2M_PARTICIPATION], colMeta[COL_DTYPE])

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
# Debug
#
def barfd(text):
	if DEBUG_ON:	print(text)


"""
##########################################
		INPUT PROCESSING
##########################################
"""

#
# Fetch Corona Data
#
def fetchCoronaData(service):
	fetchStatus = False
	global covidStats

	barfd("DEBUG: fetchCoronaData.enter")
	barf("Fetching Data for {}...".format(covidDateFilterYmd))
	# Call the Sheets API
	sheet = service.spreadsheets()
	result = sheet.values().get(spreadsheetId=COVID_SPREADSHEET_ID,range=COVID_DATA_RANGE).execute()
	values = result.get('values', [])
	gshtRowCt = 0
	gshtMatchRowCt = 0

	if not values:
		print('ERROR: No spreadsheet data found.')
	else:																					# Walk spreadsheet data filtered by date and build stats by county
		barfd("DEBUG: fetchCoronaData.process sheet values")
		barfd("DEBUG: fetchCoronaData.covidDateFilterTS=" + covidDateFilterTS.strftime("%Y.%m.%d"))
		covidStats	= {COUNTY_DEFAULT: defaultStats}																
		for gshtRow in values:
			gshtRowCt += 1
			if gshtRowCt == 1: continue														# Skip header gshtRow
			infoDate = rowElem(GSHT_DATE,gshtRow)
			barfd("DEBUG: fetchCoronaData.date={},site={},county={}".format(infoDate,rowElem(GSHT_SITE,gshtRow),rowElem(GSHT_COUNTY,gshtRow)))
			infoTS = parseDate(infoDate)

			# Filer by date
			if infoTS.strftime("%Y.%m.%d") == covidDateFilterTS.strftime("%Y.%m.%d"):

				gshtMatchRowCt += 1
				county	 = rowElem(GSHT_COUNTY,gshtRow)
				# Add to statics
				if county != "":
					if not county in covidStats:
						covidStats[county] = {}
						covidStats[county][STAT_STATUS_REPORTS]		= 0
						covidStats[county][STAT_UTILITIES_WEIGHT]	= 0
						covidStats[county][STAT_SERVICES_WEIGHT]	= 0
						covidStats[county][STAT_CONSUMABLES_WEIGHT]	= 0
						covidStats[county][STAT_2M_PARTICIPATION]			= 0
						covidStats[county][STAT_2M_CHECKINS]		= 0

					covidStats[county][STAT_STATUS_REPORTS]			+= 1
					covidStats[county][STAT_UTILITIES_WEIGHT]		+= impactWeight(rowElem(GSHT_UTILITIES,gshtRow))
					covidStats[county][STAT_SERVICES_WEIGHT]		+= impactWeight(rowElem(GSHT_SERVICES,gshtRow))
					covidStats[county][STAT_CONSUMABLES_WEIGHT]		+= impactWeight(rowElem(GSHT_CONSUMABLES,gshtRow))
					if rowElem(GSHT_CONSUMABLES,gshtRow) != '':
						covidStats[county][STAT_2M_PARTICIPATION] 		+= 1
						covidStats[county][STAT_2M_CHECKINS]		+= nullz(rowElem(GSHT_2M_CHECKINS,gshtRow))

				# Write to Detail CSV
				if CAPTURE_DETAIL:
					detailCsvWriteRow(gshtRow)

		barfd("DEBUG: fetchCoronaData.forLoopDone.matchCt={}".format(gshtMatchRowCt))

		if gshtMatchRowCt == 0:
			print("WARNING: No spreadsheet data matches filter date of "  + covidDateFilterTS.strftime("%Y.%m.%d") )
		else:
			if CAPTURE_DETAIL:	detailCsvClose()
			fetchStatus = True

	barf("Fetch complete. {} records retrieved.".format(gshtMatchRowCt))
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
				barfd("DEBUG: Evaluating DataItem kmlLine={}".format(kmlLine))
				schemaDataItemMatch = schemaDataItemPattern.match(kmlLine)
				schemaItemName	= schemaDataItemMatch.group(1)
				schemaItemValue	= schemaDataItemMatch.group(2)
				if schemaItemName in statsSchemaDataMap:
					statName = statsSchemaDataMap[schemaItemName]
					barfd("DEBUG: Updating kmlLine={}".format(kmlLine))
					schemaDataUpdateMatch = schemaDataUpdatePattern.match(kmlLine)
					kmlLines[kmlLineIndex] = schemaDataUpdateMatch.group(1) + str(covidStats[statsKey][statName]) + schemaDataUpdateMatch.group(3)

			if (lookFor == 'schemaData' or lookFor == lookForLast) and schemaDataEndPattern.match(kmlLine): lookFor = 'placemark'

		statusKmlCreate(kmlLines,statusKmlYmdSpec)
		statusKmlCreate(kmlLines,statusKmlCurrentSpec)

	barf("KML Generation complete. File={}".format(statusKmlYmdSpec))
	barfd("DEBUG: mergeKmlData.exit")
	return mergeKmlData

"""
##########################################
		MAIN
##########################################
"""
def main():

	print ("####\n#### {} starting.\n####".format(PROGNM))

	service = login()
	if service:	
		fetchOk = fetchCoronaData(service)
		if not fetchOk: 
			appExit(ERR_FETCHFAIL)
		else:
			statsGenerateCalculatedData()
			if GENERATE_SUMMARY: summaryCsvGenerate()
			mergeKmlData()

	appExit(ERR_NONE)


if __name__ == '__main__':
	main()
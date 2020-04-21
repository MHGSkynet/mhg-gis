#
#                                        ,~-. 
# ---------------------------------     (  ' )-.   ---    ,~'`-.   -----------------------------
# mhgGoogleSheet.py                  ,~' `  ' ) )       _(   _) )                               
#                                   ( ( .--.===.--.    (  `    ' )                              
# Description                        `.%%.;::|888.#`.   `-'`~~=~'                               
#                                    /%%/::::|8888\##\                      /^v^\                  
#    Google Spreadsheet Class       |%%/:::::|88888\##|               /^v^\                /^v^\
#                                   |%%|:::::|88888|##|      .,-.
#                                   \%%|:::::|88888|##/     ( { _ }_            /^v^\              
#                                    \%\:::::|88888/#/     ( {`'   )
#                                     \%\::::|8888/#/     {  ,  -'` }                   /^v^\
#                                 ,~-. `%\:::|888/#'     (  {     '} )
#                                (  ) )_ `\__|__/'        `~-~=--~=~~       
#                               ( ` ')  ) [VVVVV]            ` ` ` ` `   
#                              (_(_.~~~'   \|_|/               ` ` ` ` `  
#                                          [XXX]               ` ` ` ` `    
# Copyright                                `"""'                 ` `  ` ` `
#
#   Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#                       non profit conservative organizations and individuals to use in support
#                       of American freedom and the constitution. All other rights are reserved,
#                       and any other use prohibited.
#
# TODO
#	TODO: Tool for generic spreadsheet. Class currently models a specific sheet.
#   TODO: Add dynamic filters. Currently, only a date filter is applied
#
# Date          Version     Author          Description
# 2020.04.20    02.00       SquintMHG       New module
# ---------------------------------------------------------------------------------------------

# Python includes
import copy
import os
import os.path
from pathlib 			import Path

# MHGLIB includes
from mhgAppSettings		import AppSettings
from mhgDataField   	import DataField
from mhgDateParser   	import DateParser
from mhgException	  	import EnvironmentError
from mhgGoogleGoo   	import GoogleGoo
from mhgUtility			import *

#
# Google Spreadsheet
#
class GoogleSheet():

	#
	# Properties (private)
	#
	_sheetService					= None										# Sheet Service on a shingle
	_gshtRows						= None										# List of sheet data rows
	_gshtStatusRows					= None										# List of sheet data rows converted to RowData objects.
	_gshtStatusRowsFiltered			= None										# List of sheet data rows converted to RowData objects and matching date range
	_spreadsheet_id					= None										# Google spreadsheet identifier string
	_spreadsheet_range				= None										# Range to pull
	_rowCt							= 0											# Count of rows read from sheet
	_rowGoodCt						= 0											# Count of valid rows read from sheet
	_rowMatchCt						= 0											# Count of valid rows read from sheet matching filter
	
	#
	# Constructor
	#
	def __init__(self):
		self._spreadsheet_id		= AppSettings.glob().covidSheetID()
		self._spreadsheet_range		= AppSettings.glob().covidSheetDataRange()
		self._InitData()

	#
	# Methods (private)
	#
	def _InitData(self):
		self._sheetService				= None									# Initialize Google sheet service object
		self._gshtRows					= []									# Initialize list of raw sheet rows
		self._gshtStatusRows			= []									# Initialize list of sheet Status Rows
		self._gshtStatusRowsFiltered	= []									# Initialize list of sheet Status Rows filtered by date
		self._rowCt						= 0										# Count of rows read from sheet
		self._rowGoodCt					= 0										# Count of valid rows read from sheet
		self._rowMatchCt				= 0										# Count of valid rows read from sheet matching filter

	def _Login(self):
		self._sheetService = GoogleGoo().Login()
		if self._sheetService is None:
			raise EnvironmentError("Google Sheets login failed.",AppError.ERR_LOGINFAIL)
		return self._sheetService

	#
	# Methods (public)
	#
	def GetData(self):
		success = True
		barfd("GoogleSheet.GetData.enter()")
		
		appOptions = AppSettings.glob().options()									# Get convenience reference to app command options
	
		self._InitData()															# Initialize data
		self._Login()																# Log in to Google sheets service
		sheet = self._sheetService.spreadsheets()									# Get reference to the source spreadsheet
		result = sheet.values().get( 												# Query the sheet for the cell range having
								spreadsheetId=self._spreadsheet_id,					#    the data we want, and retrieve result...
								range=self._spreadsheet_range).execute()			#
		self._gshtRows = result.get('values', [])									#    ... convert result to a list of rows of data
		if not self._gshtRows:														# Puke if no data returned
			raise EnvironmentError("ERROR: No spreadsheet data found at all.")		#

		for sheetRow in self._gshtRows:												# Generate list of StatusRows and filtered StatusRows
			self._rowCt += 1														# Increment row counter
			if self._rowCt <= 5: barfd("row({}): {}".format(self._rowCt,sheetRow))
			statusRow = StatusRow(sheetRow)											# Convert sheet raw data to a StatusRow
			#if self._rowCt <= 2: statusRow.DumpFields()
			validateMessage = ""													# Validate data in the row,
			if not statusRow.isValidRow(self._rowCt):								#     report bad data if info reporting is enabled
				barfi(statusRow.validateMessage())									#     and ignore row
			else:																	#
				self._rowGoodCt += 1												# Increment good row counter
				self._gshtStatusRows.append(StatusRow(sheetRow))					# Add valid rows to StausRows list
				if statusRow.isFilterMatchRow():									# If row matches filter,
					self._gshtStatusRowsFiltered.append(StatusRow(sheetRow))		#   add to StatusRowsFiltered list
					self._rowMatchCt += 1											#     and increment match row counter

		barfd("GoogleSheet.GetData.exit(rowsCt={},goodCt={},matchCt={})".format(	self._rowCt, self._rowGoodCt, self._rowMatchCt ))
		
		return success
		
	def Close(self):
		barfd("GoogleSheet.Close.enter()")
		self._gshtRows					= None										# Clean up Google objects to close HTTPS connection
		self._gshtStatusRows			= None										# 
		self._gshtStatusRowsFiltered	= None										# 
		self._sheetService				= None										# 
		barfd("GoogleSheet.Close.exit()")
		return True

	#
	# Properties (public)
	#
	def rawRows(self):															# Sheet rows, as returned from google service
		return self._gshtRows

	def statusRows(self):														# Sheet rows as list of Status Row objects
		return self._gshtStatusRows

	def statusRowsFiltered(self):												# Sheet rows filtered by date, as list of Status Row objects
		return self._gshtStatusRowsFiltered
		
	def rowCt(self):
		return copy.deepcopy(self._rowCt)
		
	def rowGoodCt(self):
		return copy.deepcopy(self._rowGoodCt)
		
	def rowMatchCt(self):
		return copy.deepcopy(self._rowMatchCt)
		
#
# Status Row
#	A row from the spreadsheet with data typing and validation functionality
#
class StatusRow():

	# ColInfo hash
	_COL_DTYPE				= 'dType'
	_COL_HEADER				= 'header'

	# Google Covid Data (input) metadata 
	_GSHT_DATE				= 0
	_GSHT_SITE				= 1
	_GSHT_COUNTY			= 2
	_GSHT_UTILITIES			= 3
	_GSHT_SERVICES			= 4
	_GSHT_CONSUMABLES		= 5
	_GSHT_2M_CHECKINS		= 6
	_GSHT_2M_PARTICIPATE	= 7
	_GSHT_HF_CHECKINS		= 8
	_GSHT_HF_PARTICIPATE	= 9
	_GSHT_COMMENTS			= 10
	_GSHT_METADATA			= { \
			_GSHT_DATE:				{ _COL_DTYPE: DataField.DTYPE_DATE,		_COL_HEADER: 'IntelDate'			},
			_GSHT_SITE:				{ _COL_DTYPE: DataField.DTYPE_TEXT,		_COL_HEADER: 'Site' 				},
			_GSHT_COUNTY:			{ _COL_DTYPE: DataField.DTYPE_TEXT,		_COL_HEADER: 'County'				},
			_GSHT_UTILITIES:		{ _COL_DTYPE: DataField.DTYPE_TEXT,		_COL_HEADER: 'UtilityImpact'		},
			_GSHT_SERVICES:			{ _COL_DTYPE: DataField.DTYPE_TEXT,		_COL_HEADER: 'ServicesImpact'		},
			_GSHT_CONSUMABLES:		{ _COL_DTYPE: DataField.DTYPE_TEXT,		_COL_HEADER: 'ConsumablesImpact'	},
			_GSHT_2M_CHECKINS:		{ _COL_DTYPE: DataField.DTYPE_NUMERIC,	_COL_HEADER: '2M Checkins'			},
			_GSHT_2M_PARTICIPATE:	{ _COL_DTYPE: DataField.DTYPE_NUMERIC,	_COL_HEADER: '2M Participate'		},
			_GSHT_HF_CHECKINS:		{ _COL_DTYPE: DataField.DTYPE_NUMERIC,	_COL_HEADER: 'HF Checkins'			},
			_GSHT_HF_PARTICIPATE:	{ _COL_DTYPE: DataField.DTYPE_NUMERIC,	_COL_HEADER: 'HF Participate'		},
			_GSHT_COMMENTS:			{ _COL_DTYPE: DataField.DTYPE_TEXT,		_COL_HEADER: 'Comments'				}   }

	# Properties (private)
	_rowData				= None
	_fieldData				= []
	_validateMessage		= ""

	#
	# Constructor
	#
	def __init__(self,sheetRow):
		self._rowData = sheetRow
		self._SetFieldData()

	#
	# Methods (private)
	#
	def _SetFieldData(self):
		self._fieldData = []
		self._fieldData.append(self.intelDate())
		self._fieldData.append(self.site())
		self._fieldData.append(self.county())
		self._fieldData.append(self.utilities())
		self._fieldData.append(self.services())
		self._fieldData.append(self.consumables())
		self._fieldData.append(self.checkins2M())
		self._fieldData.append(self.participate2M())
		self._fieldData.append(self.checkinsHF())
		self._fieldData.append(self.participateHF())

	def _StatusField(self,columnId):
		fieldValue = ''
		if columnId < len(self._rowData):	fieldValue = self._rowData[columnId]
		if self._GSHT_METADATA[columnId][self._COL_DTYPE] == DataField.DTYPE_NUMERIC: fieldValue = nullz(fieldValue)
		if self._GSHT_METADATA[columnId][self._COL_DTYPE] == DataField.DTYPE_DATE: 	fieldValue = DateParser().ParseDate(fieldValue).dateYMD()
		return DataField( columnId, self._GSHT_METADATA[columnId][self._COL_DTYPE],  self._GSHT_METADATA[columnId][self._COL_HEADER], fieldValue );

	#
	# Methods (public)
	#
	def SetRow(self,sheetRow):
		self._rowData = sheetRow
		
	def dataFields(self):
		return self._fieldData
		
	def isValidRow(self,rowCt):
		isValid = True
		self._validateMessage = ""
		if self.intelDate().isEmpty(): 	self._validateMessage = "Row {} Missing intel date".format(rowCt)
		if self.site().isEmpty(): 		self._validateMessage = "Row {} Missing reporting site".format(rowCt)
		if self.county().isEmpty(): 	self._validateMessage = "Row {} Missing county. intelDate={},site={}".format(rowCt,self.intelDate().value(),self.site().value())
		isValid = self._validateMessage == ""
		return isValid
		
	def isFilterMatchRow(self):
		return isBetween(self.intelDate().value(),AppSettings.glob().options().startDate(),AppSettings.glob().options().endDate())

	# Debug
	def DumpFields(self):
		for field in self.dataFields():
			print("RowField.{}.{}={}".format(field.fieldId(),field.headerText(),field.value()))

	#
	# Getters
	#
	def intelDate(self):
		return self._StatusField(self._GSHT_DATE)

	def site(self):
		return self._StatusField(self._GSHT_SITE)

	def county(self):
		return self._StatusField(self._GSHT_COUNTY)

	def utilities(self):
		return self._StatusField(self._GSHT_UTILITIES)

	def services(self):
		return self._StatusField(self._GSHT_SERVICES)

	def consumables(self):
		return self._StatusField(self._GSHT_CONSUMABLES)

	def checkins2M(self):
		return self._StatusField(self._GSHT_2M_CHECKINS)

	def participate2M(self):
		return self._StatusField(self._GSHT_2M_PARTICIPATE)

	def checkinsHF(self):
		return self._StatusField(self._GSHT_HF_CHECKINS)

	def participateHF(self):
		return self._StatusField(self._GSHT_HF_PARTICIPATE)

	def comments(self):
		return self._StatusField(self._GSHT_COMMENTS)

	def validateMessage(self):
		return copy.deepcopy(self._validateMessage)
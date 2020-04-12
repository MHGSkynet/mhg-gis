#
# ---------------------------------------------------------------------------------------------
# mhgGoogleSheet.py
#
# Description
#
# 	Class for working with source google spreadsheet
#
#                       .------..                                _------__--___.__.
#                    /            \_                           /            `  `    \
#                  /                \                         |.                     \
#                 /                   \                       \                       |
#                /    .--._    .---.   |                       \                      |
#                |  /      -__-     \   |                        ~-/--`-`-`-\         |
#                | |                |  |                         |          \        |
#                 ||                  ||                         |            |       |
#                 ||     ,_   _.      || Hey Beavis,             |            |       |
#                 ||      e   e      ||   smell my finger!       |   _--    |       |
#                  ||     _  |_      ||   Heh, HeH!!            _| =-.    |.-.    |
#                 @|     (o\_/o)     |@                          o|/o/       _.   |
#                   |     _____     |              No way,       /  ~          \ |
#                    \ ( /uuuuu\ ) /               ass wipe!!  (/___@)  ___~    |
#                     \  `====='  /  That's your                   |_===~~~.`    |
#                      \  -___-  /    mom, Bruh!                _ ______.--~     |
#                       |       |            //                 \________       |
#                       /-_____-\       .  _//_                          \      |
#                     /           \     \\/////                        __/-___-- -_
#                   /               \    \   /                        /            __\
#                  /__|  AC / DC  |__\   / /                          -| Metallica|| |
#                  | ||           |\ \  / /                           ||          || |
#                  | ||           | \ \/ /                            ||          || |
#
# Copyright
#
#	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#						non profit conservative organizations and individuals to use in support
#						of American freedom and the constitution. All other rights are reserved,
#						and any other use prohibited.
# TODO
#	Reject and report bad data; county, date, etc.
#
# Date			Version		Author			Description
# 2020.04.07	02.00		SquintMHG		New module
# ---------------------------------------------------------------------------------------------

# Python includes
import os
import os.path
from pathlib import Path

# MHGLIB includes
import mhgAppSettings
import mhgDataField
import mhgUtility

#
# Google Spreadsheet
#
class GoogleSheet():

	# Spreadsheet constants (private)
	_COVID_SPREADSHEET_ID			= '1ckdKCNIB-5-KSUlV2ehW3KPARVlu_CC2npjsAHrml7Q'	# Google Document ID to fetch
	_COVID_DATA_RANGE				= 'DailyData!A2:K'									# Spreadsheet range to fetch (minus header)

	# Spreadsheet data (private)
	_sheetService					= None										# Sheet Service on a shingle
	_gshtSheetRows					= None										# List of sheet rows
	_gshtSheetStatusRows			= None										# List of sheet rows filtered by date
	_gshtSheetStatusRowsFiltered	= None										# List of sheet rows filtered by date

    #
	# Constructor
	#
	def __init__(self):
		self.InitData()

	#
	# Private Methods
	#
	def _InitData(self):
		self._sheetService					= None								# Initialize Google sheet service object
		self._gshtSheetRows					= []								# Initialize list of raw sheet rows
		self._gshtSheetStatusRows			= []								# Initialize list of sheet Status Rows
		self._gshtSheetStatusRowsFiltered	= []								# Initialize list of sheet Status Rows filtered by date

	def _Login(self):
		self._sheetService = GoogleGoo.Login()
		return self._sheetService

	#
	# Public Methods
	#
	def GetData(self):
		success = True

		appOptions = AppSettings.glob().options()

		# Call google sheets API to get data									# Retrieve Data
		self.InitData()
		sheet = _sheetService.spreadsheets()
		result = sheet.values().get(spreadsheetId=self._COVID_SPREADSHEET_ID,range=self._COVID_DATA_RANGE).execute()
		self._gshtSheetRows = result.get('values', [])

		# Puke if no data returned
		if not self._gshtSheetRows:
			print('ERROR: No spreadsheet data found.')
			success = False
		else:
			# Filter data														# Generate list of Status Rows and Filtered Status Rows
			for sheetRow in self._gshtSheetRows:
				self._gshtSheetStatusRows.append(StatusRow(sheetRow))
				rowData = StatusRow(sheetRow)
				if isBetween(rowData.IntelDate(),appOptions.startDate(),appOptions.endDate()):
					self._gshtSheetStatusRowsFiltered.append(StatusRow(sheetRow))
		
		return success
		
	#
	# Getters
	#
	def rawRows(self):															# Sheet rows, as returned from google service
		return self._gshtSheetRows
		
	def statusRows(self):														# Sheet rows as list of Status Row objects
		return self._gshtSheetStatusRows
		
	def statusRowsFiltered(self):												# Sheet rows filtered by date, as list of Status Row objects
		return self._gshtSheetStatusRowsFiltered

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
	_GSHT_METADATA			= { _GSHT_DATE:				{ _COL_DTYPE: DataField.DTYPE_DATE,		_COL_HEADER: 'IntelDate'			} },
								{ _GSHT_SITE:			{ _COL_DTYPE: DataField.DTYPE_TEXT,		_COL_HEADER: 'Site' 				} },
								{ _GSHT_COUNTY:			{ _COL_DTYPE: DataField.DTYPE_TEXT,		_COL_HEADER: 'County'				} },
								{ _GSHT_UTILITIES:		{ _COL_DTYPE: DataField.DTYPE_TEXT,		_COL_HEADER: 'UtilityImpact'		} },
								{ _GSHT_SERVICES:		{ _COL_DTYPE: DataField.DTYPE_TEXT,		_COL_HEADER: 'ServicesImpact'		} },
								{ _GSHT_CONSUMABLES:	{ _COL_DTYPE: DataField.DTYPE_TEXT,		_COL_HEADER: 'ConsumablesImpact'	} },
								{ _GSHT_2M_CHECKINS:	{ _COL_DTYPE: DataField.DTYPE_NUMERIC,	_COL_HEADER: '2M Checkins'			} },
								{ _GSHT_2M_PARTICIPATE:	{ _COL_DTYPE: DataField.DTYPE_NUMERIC,	_COL_HEADER: '2M Participate'		} },
								{ _GSHT_HF_CHECKINS:	{ _COL_DTYPE: DataField.DTYPE_NUMERIC,	_COL_HEADER: 'HF Checkins'			} },
								{ _GSHT_HF_PARTICIPATE:	{ _COL_DTYPE: DataField.DTYPE_NUMERIC,	_COL_HEADER: 'HF Participate'		} },
								{ _GSHT_COMMENTS:		{ _COL_DTYPE: DataField.DTYPE_TEXT,		_COL_HEADER: 'Comments'				} }   }

	_rowData				= None
	_fieldData				= []

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
		if self._GSHT_METADATA[colId][self._COL_DTYPE] == DataType.DTYPE_NUMERIC: fieldValue = dateParser().parseDate(fieldValue).dateYMD()
		if self._GSHT_METADATA[colId][self._COL_DTYPE] == DataType.DTYPE_DATE: fieldValue = nullz(fieldValue)
		return DataField( columnId, self._GSHT_METADATA[colId][self._COL_DTYPE],  self._GSHT_METADATA[colId][self._COL_HEADER], None, fieldValue );

	#
	# Methods (public)
	#
	def SetRow(self,sheetRow):
		self._rowData = sheetRow
		
	def dataFields(self):
		return self._fieldData

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
	
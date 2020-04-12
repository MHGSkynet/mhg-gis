#
# ---------------------------------------------------------------------------------------------
# mhgCovidDataReader.py
#
# Description
#
# 	Class to pull MHG Covid data for a given day from Google spreadsheet, save detail and
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
# 2020.04.07	02.00		SquintMHG		New module
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
from mhgGoogleSheet import StatusRow

import mhgCountyStats
import mhgImpact
import mhgStateStats
import mhgUtility

#
# Fetch Corona Data
#
class CovidDataReader:

	# Private data
	_stateData				= None												# State Stats 
	_dailyCounts			= None												# Number of reports by day
	_gshtSheet				= None												# Google sheet

	#
	# Constructor
	#
    def __init__(self):															# CovidDataReader Constructor
		self._stateData				= StateStats('Michigan')					#	Initialize State Statistics
		self._dailyCounts			= {}										# 	Initialize daily report counts
		_gshtSheet					= None										#	Initialize sheet object

	#
	# Methods
	#
	def FetchCoronaData(self,service):											# Pull corona stats from Google spreadsheet

		_appOptions = AppSettings().glob().options()							# Get reference to application options

		barfd("CovidDataReader.FetchCoronaData().Enter(filterRang={}".format(_appOptions.filterRangeText()))

		# Initialize data
		fetchStatus 				= False										# Method status
		self._dailyCounts			= {}										# Initialize daily report counts
		shtMatchRowCt				= 0											# Initialize number of rows matching date filter

		self._gshtSheet = GoogleSheet()											# Get a sheet object
		if self._gshtSheet.GetData():											# Fetch the data
			shtMatchRowCt = len(self._gsheetSheet.statusRowsFiltered())			# Check that we got rows
			if shtMatchRowCt == 0:												# Whine and fail if no data matches date range
				shtRowCt = len(self._gsheetSheet.rowsRaw())
				print("WARNING: {} rows read from sheet. No rows match date filter of {}".format(shtRowCt,_appOptions.filterRangeText()) )
			else:
				self.TallyStats()												# Generate calculated fields
				fetchStatus = True												# Indicate success

		barfi("Fetch complete. {} records retrieved.".format(shtMatchRowCt))

		barfd("CovidDataReader.FetchCoronaData.countyStats:{}".format(countyStats['Kent']))
		barfd("CovidDataReader.FetchCoronaData().Exit(rowCt={},matchCt={})".format(len(self._gsheetSheet.rowsRaw()),shtMatchRowCt))

		return fetchStatus

	def TallyStats(self):
	
		barfd("CovidDataReader.TallyStats.Enter()")
		self._stateData.ClearCountyData()
		for stsRow in self._gshtSheet.StatusRowsFiltered():						# Iterate StatusRow objects from list of rows that match filter
			
			county = stsRow.county()											# Get county name of observation report
			
			self._stateData.AddDailyCount(stsRow.intelDate())						# Tally count of intel reports by date for state
			self._stateData.countyData(county).AddDailyCount(stsRow.intelDate())	# Tally count of intel reports by date for county

			if county == 'Kent':
				barfd("CovidDataReader.TallyStats.maxtest1(util:{},svc:{},cons:{},max:{})".format( \
							impactWeight(stsRow.utilities()), impactWeight(stsRow.services()), impactWeight(stsRow.consumables()), \
							self._stateData.countyData(county).maxImpact()))

			self._stateData.countyData(county).observationCount().AddValue(1)
			self._stateData.countyData(county).utilityWeight().AddValue(impactWeight(stsRow.utilities()))
			self._stateData.countyData(county).servicesWeight().AddValue(impactWeight(stsRow.services()))
			self._stateData.countyData(county).consumablesWeight().AddValue(impactWeight(stsRow.consumables()))

			self._stateData.countyData(county).AccumulateMaxScore(impactWeight(stsRow.utilities()),		\		# Single impact observation weight is same as score
																	impactWeight(stsRow.services()),	\
																	impactWeight(stsRow.consumables()))

			self._stateData.countyData(county).checkins2M().AddValue(stsRow.checkins2M())
			self._stateData.countyData(county).participate2M().AddValue(stsRow.participate2M())
			self._stateData.countyData(county).checkinsHF().AddValue(stsRow.checkinsHF())
			self._stateData.countyData(county).participateHF().AddValue(stsRow.participateHF())

			if county=='Kent':
				barfd("CovidDataReader.TallyStats.maxtest2(util:{},svc:{},cons:{},max:{})".format( \
							impactWeight(stsRow.utilities()), impactWeight(stsRow.services()), impactWeight(stsRow.consumables()), \
							self._stateData.countyData(county).maxImpact()))

		barfd("CovidDataReader.TallyStats.Exit()")

	#
	#  Getters
	#
	def stateData(self):
		return 	self._stateData
		
	def covidSheet(self):
		return self._gshtSheet
		
	#
	#  Setters
	#

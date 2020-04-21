#
# ---------------------------------------------------------------------------------------------
# mhgCovidDataReader.py
#
# Description
#
#   Class to pull MHG Covid data for a given day from Google spreadsheet, save detail and
#   statistics to CSV. Merge data into KML and save for daily report generation.
#
#   Sample Spreadsheet:
#       https://docs.google.com/spreadsheets/d/1ckdKCNIB-5-KSUlV2ehW3KPARVlu_CC2npjsAHrml7Q/edit?usp=sharing
#
# Input Resources
#   MHGCovidDetail.kml  Michigan KML file with 
#
# Copyright
#
#   Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#                       non profit conservative organizations and individuals to use in support
#                       of American freedom and the constitution. All other rights are reserved,
#                       and any other use prohibited.
#
# Date          Version     Author          Description
# 2020.04.20    02.00       SquintMHG       New module
# ---------------------------------------------------------------------------------------------

# Python includes
import copy
import os
import os.path
import re
import sys
from pathlib import Path
from datetime import datetime
from datetime import timedelta

# MHGLIB includes
from mhgAppCommandArgs	import AppCommandArgs
from mhgGoogleSheet 	import GoogleSheet,StatusRow
from mhgImpact			import Impact
from mhgCountyStats		import CountyStats
from mhgStateStats		import StateStats
from mhgUtility			import *

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
	def FetchCoronaData(self):													# Pull corona stats from Google spreadsheet

		_appOptions = AppSettings.glob().options()								# Get reference to application options

		barfd("CovidDataReader.FetchCoronaData().Enter(filterRange={})".format(_appOptions.filterRangeText()))

		# Initialize data
		fetchStatus 				= False										# Method status
		self._dailyCounts			= {}										# Initialize daily report counts

		self._gshtSheet = GoogleSheet()											# Get a sheet object
		if self._gshtSheet.GetData():											# Fetch the data
			if self._gshtSheet.rowMatchCt() == 0:								# Check that we got rows
				shtRowCt = self._gshtSheet.rowCt()								# Whine and fail if no data matches date range
				print("WARNING: {} rows read from sheet. No rows match date filter of {}".format(shtRowCt,_appOptions.filterRangeText()) )
			else:
				self.TallyStats()												# Generate calculated fields
				fetchStatus = True												# Indicate success

		barfi("Fetch complete. {} records retrieved.".format(self._gshtSheet.rowMatchCt()))

#		barfd("CovidDataReader.FetchCoronaData.countyStats:{})".format(countyStats['Kent']))
		barfd("CovidDataReader.FetchCoronaData().Exit(rowCt={},goodCt={},matchCt={})".format( \
				self._gshtSheet.rowCt(),self._gshtSheet.rowGoodCt(),self._gshtSheet.rowMatchCt()))

		return fetchStatus

	def TallyStats(self):

		barfd("CovidDataReader.TallyStats.Enter()")
		self._stateData.ClearCountyData()
		for stsRow in self._gshtSheet.statusRowsFiltered():						# Iterate StatusRow objects from list of rows that match filter

			county = stsRow.county().value()									# Get county name of observation report

			barfd("CovidDataReader.TallyRow.county=({}.{})".format(self._stateData.stateName(),county))
			self._stateData.AddDailyCount(stsRow.intelDate().value())						# Tally count of intel reports by date for state
			self._stateData.countyData(county).AddDailyCount(stsRow.intelDate().value())	# Tally count of intel reports by date for county

			if county == 'Kent':
				barfd("CovidDataReader.TallyStats.maxtest1(util:{},svc:{},cons:{},max:{})".format( \
							Impact.WeightFromCode(stsRow.utilities().value()), \
							Impact.WeightFromCode(stsRow.services().value()),	\
							Impact.WeightFromCode(stsRow.consumables().value()), \
							self._stateData.countyData(county).maxCode().value()))

			self._stateData.countyData(county).observationCount().AddValue(1)
			self._stateData.countyData(county).utilityWeight().AddValue(Impact.WeightFromCode(stsRow.utilities().value()))
			self._stateData.countyData(county).servicesWeight().AddValue(Impact.WeightFromCode(stsRow.services().value()))
			self._stateData.countyData(county).consumablesWeight().AddValue(Impact.WeightFromCode(stsRow.consumables().value()))

			self._stateData.countyData(county).AccumulateMaxScore(Impact.WeightFromCode(stsRow.utilities().value()),				# Single impact observation weight is same as score
																	Impact.WeightFromCode(stsRow.services().value()),	
																	Impact.WeightFromCode(stsRow.consumables().value()))

			self._stateData.countyData(county).checkins2M().AddValue(stsRow.checkins2M().value())
			self._stateData.countyData(county).participate2M().AddValue(stsRow.participate2M().value())
			self._stateData.countyData(county).checkinsHF().AddValue(stsRow.checkinsHF().value())
			self._stateData.countyData(county).participateHF().AddValue(stsRow.participateHF().value())

			if county=='Kent':
				barfd("CovidDataReader.TallyStats.maxtest2(util:{},svc:{},cons:{},max:{})".format( \
							Impact.WeightFromCode(stsRow.utilities().value()), Impact.WeightFromCode(stsRow.services().value()), Impact.WeightFromCode(stsRow.consumables().value()), \
							self._stateData.countyData(county).maxCode().value()))

		barfd("CovidDataReader.TallyStats.Exit()")
		
	def Close(self):															# Clean up resources
		barfd("CovidDataReader.Close.Enter()")
		self._gshtSheet.Close()
		barfd("CovidDataReader.Close.Exit()")
		return True

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

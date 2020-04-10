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
import mhgStateStats
import mhgUtility

#
# Fetch Corona Data
#
class CovidDataReader:

	# Private data
	_stateStats				= None												# State Stats 
	_dailyCounts			= None												# Number of reports by day
	_gshtSheet				= None												# Google sheet

	#
	# Constructor
	#
    def __init__(self):															# CovidDataReader Constructor
		self._stateStats			= StateStats('Michigan')					#	Initialize State Statistics
		self._dailyCounts			= {}										# 	Initialize daily report counts
		_gshtSheet					= None										#	Initialize sheet object

	#
	# Methods
	#
	def FetchCoronaData(self,service):											# Pull corona stats from Google spreadsheet

		_appOptions = AppSettings().glob().options()							# Get reference to application options

		barfd("CovidDataReader.FetchCoronaData().enter")
		barfd("CovidDataReader.FetchCoronaData: Fetching Data for {} ...".format(_appOptions.filterRangeText())

		# Intialize data
		fetchStatus 				= False										# Method status
		self._dailyCounts			= {}										# Initialize daily report counts
		shtMatchRowCt				= 0											# Initialize number of rows matching date filter

		self._gshtSheet = GoogleSheet()											# Get a sheet object
		if self._gshtSheet.GetData():											# Fetch the data
			shtMatchRowCt = len(self._gsheetSheet.statusRowsFiltered())
			if shtMatchRowCt == 0:												# Whine and fail if no data matches date range
				if _appOptions.isDateRange():
					print("WARNING: No spreadsheet data matches filter date range of {} to {}".format(_appOptions.startDate(),_appOptions.endDate()) )
				else:
					print("WARNING: No spreadsheet data matches filter date of {}".format(_appOptions.startDate()) )
			else:
				self.TallyStats()												# Generate calculated fields
				fetchStatus = True												# Indicate success

		barf("Fetch complete. {} records retrieved.".format(shtMatchRowCt))
		
		barfd("CovidDataReader.FetchCoronaData.countyStats:{}".format(countyStats['Kent']))
		
		barfd("fetchCoronaData.exit rowCt={},matchCt={}".format(len(self._gsheetSheet.rowsRaw()),shtMatchRowCt))
		return fetchStatus

	def TallyStats(self):
	
		barfd("CovidDataReader.TallyStats: Process sheet values")
		self._stateStats.countyStats()	= CountyStats()
		for stsRow in self._gshtSheet.StatusRowsFiltered():
			
			# Tally count of intel reports by Date
			if not stsRow.intelDate() in self._dailyCounts: self._dailyCounts[stsRow.intelDate()] = 0
			self._dailyCounts[stsRow.intelDate()] += 1

			county = stsRow.county()
			if county != "":
				if county == 'Kent':
					barfd("CovidDataReader.TallyStats.addStats1:(util:{},svc:{},cons:{},max:{})".format(impactWeight(stsRow.utilities()),	\
																									 impactWeight(stsRow.services()),	\
																									 impactWeight(stsRow.consumables()),	\
																									 self._countyStats.CountyStatistic(county,CountyStats.STAT_MAX_IMPACT))
				self.countStats.CountyStatistic(county,CountyStats.STAT_STATUS_REPORTS) 	+= 1
				self.countStats.CountyStatistic(county,CountyStats.STAT_UTILITIES_WEIGHT)	+= impactWeight(stsRow.utilities())
				self.countStats.CountyStatistic(county,CountyStats.STAT_SERVICES_WEIGHT)	+= impactWeight(stsRow.services()))
				self.countStats.CountyStatistic(county,CountyStats.STAT_CONSUMABLES_WEIGHT)	+= impactWeight(stsRow.consumables())
				self.countStats.CountyStatistic(county,CountyStats.STAT_MAX_IMPACT)			=  max(self._countyStats.CountyStatistic(county,CountyStats.STAT_MAX_IMPACT)),	\
																										impactWeight(stsRow.utilities()),	\
																										impactWeight(stsRow.services()),	\
																										impactWeight(stsRow.consumables()))

				if county=='Kent':
					barfd("CovidDataReader.TallyStats.addStats2:(util:{},svc:{},cons:{},max:{})".format(impactWeight(stsRow.utilities()),	\
																										 impactWeight(stsRow.services()),	\
																										 impactWeight(stsRow.consumables()),	\
																										 self.countyStats.CountyStatistic(county,CountyStats.STAT_MAX_IMPACT))

				self.countStats.CountyStatistic(county,CountyStats.STAT_2M_CHECKINS)		+= stsRow.checkins2M()
				self.countStats.CountyStatistic(county,CountyStats.STAT_2M_PARTICIPATE)		+= stsRow.participate2M()
				self.countStats.CountyStatistic(county,CountyStats.STAT_HF_CHECKINS)		+= stsRow.checkinsHF()
				self.countStats.CountyStatistic(county,CountyStats.STAT_HF_PARTICIPATE) 	+= stsRow.participateHF()

				if stsRow.intelDate() not in self.countStats.CountyStatistic(county,CountyStats.STAT_DAILY_COUNTS):
					self.countStats.CountyStatistic(county,CountyStats.STAT_DAILY_COUNTS)[infoYmd] = 0
				self.countStats.CountyStatistic(county,CountyStats.STAT_DAILY_COUNTS)[infoYmd] += 1

	#
	#  Getters
	#
	def countyStats(self):
		return 	self._countyStats
		
	def dailyCounts(self):
		return self._dailyCounts
		
	def covidSheet(self):
		return self._gshtSheet
		
	#
	#  Setters
	#

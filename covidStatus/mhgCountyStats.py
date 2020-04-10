#
# ---------------------------------------------------------------------------------------------
# mhgCountyStats.py
#
# Description
#
# 	Class for managing county statistics
#
# Copyright
#
#	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#						non profit conservative organizations and individuals to use in support
#						of American freedom and the constitution. All other rights are reserved,
#						and any other use prohibited.
#
# Date			Version		Author			Description
# 2020.04.07	02.00		SquintMHG		New Module
# ---------------------------------------------------------------------------------------------

import sys
from mhgDateParse import dateParser
from mhgDateParse import dateParseResult
import mhgDataField
import mhgImpact


class CountyStats(ObservationStats):

	# Statistics Constants (public)
	COUNTY_DEFAULT					= 'DEFAULT'											# Default county name

																						######## Volatile Fields #########
	STAT_COUNTY						= 'County'											# County Name
	STAT_DAILY_COUNTS				= 'DailyCounts'										# Counts of observations by date for county

	# Properties (private)
	_fieldData						= []
	_county							= None
	_dailyCounts					= None

	# Constructor
    def __init__(self):
		self._SetDefaults()
		pass
		
	#
	# Methods (private)
	#
	def _SetDefaults(self):
		_appOptions = AppSettings.glob().options
		super(CountyStats, self)._SetDefaults()
		self._county				= DataField(self.STAT_COUNTY,				DataField.DTYPE_TEXT,		'County',				self.COUNTY_DEFAULT)
		self._dailyCounts			= {}
	
	def _SetFieldData(self):
		self._fieldData = []
		self._fieldData.append(self._statusStartDate)							# Volatile fields
		self._fieldData.append(self._statusEndDate)
		self._fieldData.append(self._county)
		self._fieldData.append(self._statusNDays)
		self._fieldData.append(self._statusReportCount)
		self._fieldData.append(self._utilityWeight)
		self._fieldData.append(self._servicesWeight)
		self._fieldData.append(self._consumablesWeight)
		self._fieldData.append(self._checkins2M)
		self._fieldData.append(self._participate2M)
		self._fieldData.append(self._checkinsHF)
		self._fieldData.append(self._participateHF)
		self._fieldData.append(self.utilitiesScore())							# Calculated fields
		self._fieldData.append(self.servicesScore())
		self._fieldData.append(self.consumablesScore())		
		self._fieldData.append(self.overallScore())		
		self._fieldData.append(self.maxScore())		
		self._fieldData.append(self.utilitiesCode())							
		self._fieldData.append(self.servicesCode())
		self._fieldData.append(self.consumablesCode())		
		self._fieldData.append(self.overallCode())		
		self._fieldData.append(self.maxCode())		

	#
	# Methods (public)
	#
	def FieldFromId(self,fieldIdentifier):
		statusField = None
		for field in self.dataFields()
			if field.fieldId() == fieldIdentifier: statusField = field
			break

		return statusField

	#
	# Property Getters (public)
	#
	def countyName(self):
		return self._county
		
	def dailyCounts(self):
		return self._dailyCounts
		
	def dataFields(self):
		self._SetFieldData()
		return self._fieldData

	#
	# Property Getters, Calculated (public)
	#


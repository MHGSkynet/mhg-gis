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

import mhgCumulativeStats
import mhgDataField
import mhgImpact


class CountyStats(CumulativeStats):

	# Statistics Constants (public)
	COUNTY_DEFAULT					= 'DEFAULT'											# Default county name

																						######## Volatile Fields #########
	STAT_COUNTY						= 'County'											# County Name

	# Properties (private)
	_countyName						= None

	# Constructor
    def __init__(self,countyName=self.COUNTY_DEFAULT):
		self._SetDefaults()
		self._countyName			= DataField(self.STAT_COUNTY,	DataField.DTYPE_TEXT,	'County',	countyName)
		
	#
	# Methods (private)
	#
	def _SetDefaults(self):
		super(CountyStats, self)._SetDefaults()
		self._countyName			= DataField(self.STAT_COUNTY,	DataField.DTYPE_TEXT,	'County',	self.COUNTY_DEFAULT)
	
	def _SetFieldData(self):
		self._fieldData = []
		self._fieldData.append(self._statusStartDate)							# Volatile fields
		self._fieldData.append(self._statusEndDate)
		self._fieldData.append(self._countyName)
		self._fieldData.append(self._observeDays)
		self._fieldData.append(self._observeCount)
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

	#
	# Property Getters (public)
	#
	def countyName(self):
		return self._countyName.value()
		
	#
	# Property Getters, Calculated (public)
	#


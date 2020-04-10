#
# ---------------------------------------------------------------------------------------------
# mhgStateStats.py
#
# Description
#
# 	Class for managing state statistics
#
# Copyright
#
#	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#						non profit conservative organizations and individuals to use in support
#						of American freedom and the constitution. All other rights are reserved,
#						and any other use prohibited.
#
# Date			Version		Author			Description
# 2020.04.10	02.00		SquintMHG		New Module
# ---------------------------------------------------------------------------------------------

import mhgCountyStats
import mhgObservationStats
import mhgImpact

class StateStats(ObservationStats):

	# Statistics Constants (public)
	STATE_DEFAULT					= 'DEFAULT'											# Default state name
																						######## Volatile Fields #########
	STAT_STATE						= 'State'											# State Name

	# Properties (private)
	_fieldData						= []
	_stateName						= None
	_dailyCounts					= None
	_countyStats					= {}												# Hash of CountyStats objects, by county name

	# Constructor
    def __init__(self,stateName):
		self._SetDefaults()																# Set new object defaults
		self._stateName	= stateName														# Set state name
		self._countyStats			= {}												# Initialize Hash of CountyStats objects, by county name
		
	#
	# Methods (private)
	#
	def _SetDefaults(self):
		super(StateStats, self)._SetDefaults()
		self._state					= DataField(self.STAT_STATE,				DataField.DTYPE_TEXT,		'State',				self.STATE_DEFAULT)
		self._dailyCounts			= {}
	
	def _SetFieldData(self):
		self._fieldData = []
		self._fieldData.append(self._statusStartDate)
		self._fieldData.append(self._statusEndDate)
		self._fieldData.append(self._stateName)
		self._fieldData.append(self._observeDays)
		self._fieldData.append(self._observeCount)
		self._fieldData.append(self._utilityWeight)
		self._fieldData.append(self._servicesWeight)
		self._fieldData.append(self._consumablesWeight)
		self._fieldData.append(self._checkins2M)
		self._fieldData.append(self._participate2M)
		self._fieldData.append(self._checkinsHF)
		self._fieldData.append(self._participateHF)
		self._fieldData.append(self.utilitiesScore())							
		self._fieldData.append(self.servicesScore())
		self._fieldData.append(self.consumablesScore())		
		self._fieldData.append(self.overallScore())		
		self._fieldData.append(self.maxScore())		
		self._fieldData.append(self.utilitiesCode())							
		self._fieldData.append(self.servicesCode())
		self._fieldData.append(self.consumablesCode())		
		self._fieldData.append(self.overallCode())		
		self._fieldData.append(self.maxCode())		
		
	def _ZeroAccumulators(self):
		self._observeDays.SetValue(0)
		self._observeCount.SetValue(0)
		self._utilityWeight.SetValue(0)
		self._servicesWeight.SetValue(0)
		self._consumablesWeight.SetValue(0)
		self._checkins2M.SetValue(0)
		self._participate2M.SetValue(0)
		self._checkinsHF.SetValue(0)
		self._participateHF.SetValue(0)

	def _CrunchCountyData(self):
		self._ZeroAccumulators()
		for countyName in self.covidStats.keys()
			self._observeDays.SetValue( self._observeDays.value() + self._countyStats{countyName}.observeDays().value() )
			self._observeCount.SetValue( self._observeCount.value() + self._countyStats{countyName}.observeCount().value() )
			self._utilityWeight.SetValue( self._utilityWeight.value() + self._countyStats{countyName}.utilityWeight().value() )
			self._servicesWeight.SetValue( self._servicesWeight.value() + self._countyStats{countyName}.servicesWeight().value() )
			self._consumablesWeight.SetValue( self._consumablesWeight.value() + self._countyStats{countyName}.consumablesWeight().value() )
			self._checkins2M.SetValue( self._checkins2M.value() + self._countyStats{countyName}.checkins2M().value() )
			self._participate2M.SetValue( self._participate2M.value() + self._countyStats{countyName}.participate2M().value() )
			self._checkinsHF.SetValue( self._checkinsHF.value() + self._countyStats{countyName}.checkinsHF().value() )
			self._participateHF.SetValue( self._participateHF.value() + self._countyStats{countyName}.participateHF().value() )

	#
	# Methods (private)
	#

	#
	# Methods (public)
	#

	#
	# Property Getters (public)
	#
	def stateName(self):
		return self._statusStartDate
		
	def dailyCounts(self):
		return self._dailyCounts
		
	#
	# Property Getters, Calculated (public)
	#


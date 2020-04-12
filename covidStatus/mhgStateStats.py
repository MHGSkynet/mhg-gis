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

# MHGLIB includes
import mhgCountyStats
import mhgCumulativeStats
import mhgImpact

class StateStats(CumulativeStats):

	# Statistics Constants (public)
	STATE_DEFAULT					= 'DEFAULT'											# Default state name
																						######## Volatile Fields #########
	STAT_STATE						= 'State'											# State Name

	# Properties (private)
	_fieldData						= []
	_stateName						= None
	_countyData						= {}												# Hash of CountyStats objects, by county name

	# Constructor
    def __init__(self,stateName):
		self._SetDefaults()																# Set new object defaults
		self._stateName	= stateName														# Set state name
		
	#
	# Methods (private)
	#
	def _SetDefaults(self):
		super(StateStats, self)._SetDefaults()											# Do parent Initializations
		self._countyStats			= {}												# Initialize Hash of CountyStats objects, by county name
		self._stateName				= DataField(fldid:	self.STAT_STATE,						
												dtype:	DataField.DTYPE_TEXT,
												header:	'State',
												value: 	self.STATE_DEFAULT)

	def _SetFieldData(self):															# Create list of DataField items from properties
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
		for countyName in self._countyData.keys()
			self._observeDays.SetValue( self._observeDays.value() + self._countyData{countyName}.observeDays().value() )
			self._observeCount.SetValue( self._observeCount.value() + self._countyData{countyName}.observeCount().value() )
			self._utilityWeight.SetValue( self._utilityWeight.value() + self._countyData{countyName}.utilityWeight().value() )
			self._servicesWeight.SetValue( self._servicesWeight.value() + self._countyData{countyName}.servicesWeight().value() )
			self._consumablesWeight.SetValue( self._consumablesWeight.value() + self._countyData{countyName}.consumablesWeight().value() )
			self._checkins2M.SetValue( self._checkins2M.value() + self._countyData{countyName}.checkins2M().value() )
			self._participate2M.SetValue( self._participate2M.value() + self._countyData{countyName}.participate2M().value() )
			self._checkinsHF.SetValue( self._checkinsHF.value() + self._countyData{countyName}.checkinsHF().value() )
			self._participateHF.SetValue( self._participateHF.value() + self._countyData{countyName}.participateHF().value() )

	#
	# Methods (private)
	#

	#
	# Methods (public)
	#
	def ClearCountyData(self):
		self._countyData = {CountyStats.COUNTY_DEFAULT: CountyStats()}				# Initialize county data hash with a default county item

	#
	# Property Getters (public)
	#
	def stateName(self):
		return self._stateName.value()
		
	def countyList(self):
		return keys(self._countyData)
		
	def countyData(self,county):
		if not county in self._countyData:											# Add county, with default values, if not already in hash
			self._countyData[county]	= CountyStats(county)
		return self._countyData[county]
		
	#
	# Property Getters, Calculated (public)
	#


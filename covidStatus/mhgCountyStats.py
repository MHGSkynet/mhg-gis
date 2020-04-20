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

# Python includes
import sys

# MHGLIB includes
from mhgCumulativeStats		import CumulativeStats
from mhgDataField			import DataField
from mhgImpact				import Impact
from mhgUtility				import *

class CountyStats(CumulativeStats):

	# Statistics Constants (public)
	COUNTY_DEFAULT					= 'DEFAULT'											# Default county name

																						######## Volatile Fields #########
	STAT_COUNTY						= 'County'											# County Name

	# Properties (private)
	_countyName						= None
	_countyNameText					= None

	# Constructor
	def __init__(self,countyName=COUNTY_DEFAULT):
		self._countyNameText = countyName
		barfd("CountyStats.Constructor.entry(countyName={})".format(countyName))
		super(CountyStats,self).__init__()												# Call base class constructor
		self._SetDefaults()
		self._countyName			= DataField(self.STAT_COUNTY,	DataField.DTYPE_TEXT,	'County',	countyName)

	#
	# Methods (private)
	#
	def _SetDefaults(self):
		barft("CountyStats.SetDefaults.enter(countyName={})".format(self._countyNameText))
		self._countyName			= DataField(self.STAT_COUNTY,	DataField.DTYPE_TEXT,	'County',	self.COUNTY_DEFAULT)
		barft("CountyStats.SetDefaults.exit()")
		return True

	def _SetFieldData(self):
		barft("CountyStats._SetFieldData.enter()")
		super(CountyStats,self)._SetFieldData()
		self._fieldData.append(self._countyName)
		barft("CountyStats._SetFieldData.data({})".format(self._dataFieldsDumpsText()))
		barft("CountyStats._SetFieldData.exit(fieldCount={})".format(len(self._fieldData)))
		return True

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


#
# ---------------------------------------------------------------------------------------------
# mhgCumulativeStats.py
#
# Description
#
#   Class for managing statistics accumulation. Base class for StateStats, CountyStats.
#
# Copyright
#
#   Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#                       non profit conservative organizations and individuals to use in support
#                       of American freedom and the constitution. All other rights are reserved,
#                       and any other use prohibited.
#
# Date          Version     Author          Description
# 2020.04.20    02.00       SquintMHG       New Module
# ---------------------------------------------------------------------------------------------

# Python includes
import copy
import sys

# MHGLIB includes
from mhgDataField			import DataField
from mhgObservationStats	import ObservationStats
from mhgUtility				import *

class CumulativeStats(ObservationStats):

	# Constants (public)
	STAT_DAILY_COUNTS				= 'DailyCounts'							# Counts of observations by date

	# Properties (private)
	_dailyCounts					= None									# Hash of counts by date (ymd)
	_maxScore						= None									# Maximum score
	_test							= 'Class'

	#
	# Constructor
	#
	def __init__(self):
		super(CumulativeStats,self).__init__()								# Call base class constructor
		self._SetCumulativeDefaults()

	#
	# Methods (private)
	#
	def _SetCumulativeDefaults(self):
		self._dailyCounts			= {}									# Initialize Hash of counts by date (ymd)
		self._maxScore				= DataField(self.STAT_MAX_SCORE,	DataField.DTYPE_NUMERIC,	'MaxScore',	 0)
		self._test					= 'Instance'
		return True

	def _SetFieldData(self):												# Create list of DataField items from properties. (archetype)
		barft("CumulativeStats._SetFieldData.enter()")
		super(CumulativeStats,self)._SetFieldData()
		barft("CumulativeStats._SetFieldData.enter()")
		return True
		
	#
	# Methods (public)
	#
	def AccumulateMaxScore(self,*values):									# Keep track of maximum score encountered
		barft("CumulativeStats.AccumulateMaxScore.enter(maxScore={},values={})".format(self._maxScore.value(),values))
		score = max(self._maxScore.value(), max(values))
		self._maxScore				= DataField(self.STAT_MAX_SCORE,	DataField.DTYPE_NUMERIC,	'MaxScore',	 score)
		barft("CumulativeStats.AccumulateMaxScore.newMaxScore={}".format(self._maxScore.value()))
		barft("CumulativeStats.AccumulateMaxScore.exit()")
		return self.maxScore()

	def AddDailyCount(self,dateYmd,increment=1):							# Add to counter for given date
		if dateYmd not in self._dailyCounts: self._dailyCounts[dateYmd] = 0
		self._dailyCounts[dateYmd] += increment

	#
	# Property Getters (public)
	#
	def dailyCounts(self):
		return self._dailyCounts

	def maxScore(self):														# Override Max Score to accumulate max, rather than have max(avg score)
		return copy.deepcopy(self._maxScore)

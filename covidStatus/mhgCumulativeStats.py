#
# ---------------------------------------------------------------------------------------------
# mhgCumulativeStats.py
#
# Description
#
# 	Class for managing statistics accumulation. Base class for StateStats, CountyStats.
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

# Python includes
import sys

# MHGLIB includes
from mhgDateParse import dateParser
from mhgDateParse import dateParseResult
import mhgDataField
import mhgObservationStats

class CumulativeStats(ObservationStats):

	# Constants (public)
	STAT_DAILY_COUNTS				= 'DailyCounts'							# Counts of observations by date

	# Properties (private)
	_dailyCounts					= None									# Hash of counts by date (ymd)
	_maxScore						= None									# Maximum score

	#
	# Constructor
	#
    def __init__(self):
		self._SetDefaults()
		
	#
	# Methods (private)
	#
	def _SetDefaults(self):
		super(CumulativeStats, self)._SetDefaults()							# Do parent Initializations
		_dailyCounts				= {}									# Initialize Hash of counts by date (ymd)
		self._maxScore				= DataField(self.STAT_MAX_SCORE,	DataField.DTYPE_NUMERIC,	'MaxScore',	 0)
	
	#
	# Methods (public)
	#
	def AccumulateMaxScore(self,*values):									# Keep track of maximum score encountered
		score = max(self._maxScore.value(), values)
		self._maxScore

	def AddDailyCount(self,dateYmd,increment=1):							# Add to counter for given date
		if dateYmd not in self._dailyCounts: self._dailyCounts[dateYmd] = 0
		self._dailyCounts[dateYmd] += increment

	#
	# Property Getters (public)
	#
	def dailyCounts(self):
		return self._dailyCounts
		
	def maxScore(self):														# Override Max Score to accumulate max, rather than have max(avg score)
		return DataField(self.STAT_MAX_SCORE,			DataField.DTYPE_NUMERIC,	'MaxScore',			self._maxScore)

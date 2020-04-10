#
# ---------------------------------------------------------------------------------------------
# mhgObservationStats.py
#
# Description
#
# 	Base class for managing statistics
#
# Copyright
#
#	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#						non profit conservative organizations and individuals to use in support
#						of American freedom and the constitution. All other rights are reserved,
#						and any other use prohibited.
#
# Date			Version		Author			Description
# 2020.04.10	02.00		SquintMHG		Rewrite as app
# ---------------------------------------------------------------------------------------------

import mhgImpact

class ObservationStats(object):

	# Statistics Constants (public)
	STAT_STATUS_START_DATE			= 'IntelStartDate'									# End date of observations
	STAT_STATUS_END_DATE			= 'IntelEndDate'									# End date of observations
	STAT_OBSERVE_NDAYS				= 'OvserveNDays'									# Number of days having observations
	STAT_OBSERVE_COUNT				= 'ObserveCount'									# Number of observations
	STAT_UTILITIES_WEIGHT			= 'UtilitiesWeight'									# Total utility impact weight
	STAT_SERVICES_WEIGHT			= 'ServicesWeight'									# Total services impact weight
	STAT_CONSUMABLES_WEIGHT			= 'ConsumablesWeight'								# Total consumables impact weight
	STAT_2M_CHECKINS				= '2M Checkins'										# Total 2M check-ins by net control
	STAT_2M_PARTICIPATE				= '2M Participate'									# Total 2M nets participated in
	STAT_HF_CHECKINS				= 'HF Checkins'										# Total HF check-ins by net control
	STAT_HF_PARTICIPATE				= 'HF Participate'									# Total HF nets participated in

	STAT_UTILITIES_SCORE			= 'UtilitiesScore'									# Utilities Impact Score
	STAT_SERVICES_SCORE				= 'ServicesScore'									# Services Impact Score
	STAT_CONSUMABLES_SCORE			= 'ConsumablesScore'								# Consumables Impact Score
	STAT_OVERALL_SCORE				= 'OverallScore'									# Overall (Average-ish) Impact Score
	STAT_MAX_SCORE					= 'MaxScore'										# Maximum Impact Score
	STAT_UTILITIES_CODE				= 'UtilitiesCode'									# Utilities Impact Code
	STAT_SERVICES_CODE				= 'ServicesCode'									# Services Impact Code
	STAT_CONSUMABLES_CODE			= 'ConsumablesCode'									# Consumables Impact Code
	STAT_OVERALL_CODE				= 'OverallCode'										# Overall Impact Code
	STAT_MAX_CODE					= 'MaxCode'											# Maximum Impact Code

	# Properties (private)
	_statusStartDate				= None
	_statusEndDate					= None
	_observeDays					= None
	_observeCount					= None
	_utilityWeight					= None
	_servicesWeight					= None
	_consumablesWeight				= None
	_checkins2M						= None
	_participate2M					= None
	_checkinsHF						= None
	_participateHF					= None
	
	# Constructor
    def __init__(self):
		pass
		
	#
	# Methods (private)
	#
	def _SetDefaults(self):
		_appOptions = AppSettings.glob().options
		self._statusStartDate		= DataField(self.STAT_STATUS_START_DATE,	DataField.DTYPE_DATE,		'IntelStartDate',		_appOptions.startDate())
		self._statusEndDate			= DataField(self.STAT_STATUS_END_DATE,		DataField.DTYPE_DATE,		'IntelEndDate',			_appOptions.endDate())
		self._observeDays			= DataField(self.STAT_OBSERVE_NDAYS,		DataField.DTYPE_NUMERIC,	'ObserveDays',			0)
		self._observeCount			= DataField(self.STAT_OBSERVE_COUNT,		DataField.DTYPE_NUMERIC,	'ObserveCount',			0)
		self._utilityWeight			= DataField(self.STAT_UTILITIES_WEIGHT,		DataField.DTYPE_NUMERIC,	'UtilityWeight',		0)
		self._servicesWeight		= DataField(self.STAT_SERVICES_WEIGHT,		DataField.DTYPE_NUMERIC,	'ServicesWeight',		0)
		self._consumablesWeight		= DataField(self.STAT_CONSUMABLES_WEIGHT,	DataField.DTYPE_NUMERIC,	'ConsumablesWeight',	0)
		self._checkins2M			= DataField(self.STAT_2M_CHECKINS,			DataField.DTYPE_NUMERIC,	'2MCheckins',			0)
		self._participate2M			= DataField(self.STAT_2M_PARTICIPATE,		DataField.DTYPE_NUMERIC,	'2MParticipate',		0)
		self._checkinsHF			= DataField(self.STAT_HF_CHECKINS,			DataField.DTYPE_NUMERIC,	'HFCheckins',			0)
		self._participateHF			= DataField(self.STAT_HF_PARTICIPATE,		DataField.DTYPE_NUMERIC,	'HFParticipate',		0)
	
	#
	# Methods (private)
	#

	#
	# Methods (public)
	#

	#
	# Property Getters (public)
	#
	def startDate(self):
		return self._statusStartDate
		
	def endDate(self):
		return self._statusEndDate
		
	def stateName(self):
		return self._county
		
	def statusNdays(self):
		return self._statusNDays
		
	def restartDate(self):
		return self._statusReportCount
		
	def startDate(self):
		return self._utilityWeight
		
	def startDate(self):
		return self._servicesWeight
		
	def startDate(self):
		return self._consumablesWeight
		
	def startDate(self):
		return self._checkins2M
		
	def startDate(self):
		return self._participate2M
		
	def startDate(self):
		return self._checkinsHF
		
	def startDate(self):
		return self._participateHF

	def startDate(self):
		return self._dailyCounts
		
	#
	# Property Getters, Calculated (public)
	#
	def utilitiesScore(self):
		score = impactScore(self._utilityWeight.value(),self._statusReportCount.value()) 
		return DataField(self.STAT_UTILITIES_SCORE,		DataField.DTYPE_NUMERIC,	'UtilitiesScore',	score)
		
	def servicesScore(self):
		score = impactScore(self._servicesWeight.value(),self._statusReportCount.value()) 
		return DataField(self.STAT_SERVICES_SCORE,		DataField.DTYPE_NUMERIC,	'ServicesScore',	score)
		
	def consumablesScore(self):
		score = impactScore(self._consumablesWeight.value(),self._statusReportCount.value()) 
		return DataField(self.STAT_CONSUMABLES_SCORE,	DataField.DTYPE_NUMERIC,	'ConsumablesScore', score)
		
	def overallScore(self):
		score = int( (sum(self.utilitiesScore().value(),self.servicesScore().value(),self.consumablesScore().value()) / self._observeCount) + 0.7)
		return DataField(self.STAT_OVERALL_SCORE,		DataField.DTYPE_NUMERIC,	'OverallScore',		score)

	def maxScore(self):
		score = max(self.utilitiesScore().value(),self.servicesScore().value(),self.consumablesScore().value())
		return DataField(self.STAT_MAX_SCORE,			DataField.DTYPE_NUMERIC,	'MaxScore',			score)

	def utilitiesCode(self):
		impactCode = impactCodeFromScore(self.utilitiesScore())
		return DataField(self.STAT_UTILITIES_CODE,		DataField.DTYPE_NUMERIC,	'UtilitiesCode',	impactCode)

	def servicesCode(self):
		impactCode = impactCodeFromScore(self.servicesScore())
		return DataField(self.STAT_SERVICES_CODE,		DataField.DTYPE_NUMERIC,	'ServicesCode',		impactCode)

	def consumablesCode(self):
		impactCode = impactCodeFromScore(self.consumablesScore())
		return DataField(self.STAT_CONSUMABLES_CODE,	DataField.DTYPE_NUMERIC,	'ConsumablesCode',	impactCode)

	def overallCode(self):
		impactCode = impactCodeFromScore(self.overallScore())
		return DataField(self.STAT_CONSUMABLES_CODE,	DataField.DTYPE_NUMERIC,	'OverallCode',		impactCode)

	def maxCode(self):
		impactCode = impactCodeFromScore(self.maxScore())
		return DataField(self.STAT_CONSUMABLES_CODE,	DataField.DTYPE_NUMERIC,	'MaxCode',			impactCode)		

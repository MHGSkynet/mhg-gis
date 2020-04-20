#
# -------------------------------------------------------------------------------------------------------
# mhgObservationStats.py                IIIIMWMWMWMWMWMWMWMWMWMWMWMWMWMttii:        .           .
#                                 IIYVVXMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWxx...         .           .
# Description                  IWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMx..
#                             IWMWMWMWMWMWMWMWMWMW%MHG%SKYNET%MWMWMWMWMWMWMWMWMWMWMWMWMWMx..        .
#   Base class for managing   ""MWMWMWMWMWM"""""""".  .:..   ."""""MWMWMWMWMWMWMWMWMWMWMWMWMWti.
#   observation data             ""   . `  .: . :. : .  . :.  .  . . .  """"MWMWMWMWMWMWMWMWMWMWMWMWMti=
#                                 . .   :` . :   .  .'.' '....xxxxx...,'. '   ' ."""YWMWMWMWMWMWMWMWMWMW+
#                              ; . ` .  . : . .' :  . ..XXXXXXXXXXXXXXXXXXXXx.    `     . "YWMWMWMWMWMWMW
#                              .  .  .    . .   .  ..XXXXXXXXWWWWWWWWWWWWWWWWXXXX.  .     .     """""""
#                                 ' :  : . : .  ...XXXXXWWW"   W88N88@888888WWWWWXX.   .   .       . .
#                              ' .    . :   ...XXXXXXWWW"    M88N88GGGGGG888^8M "WMBX.          .   ..  :
#                                  :     ..XXXXXXXXWWW"     M88888WWRWWWMW8oo88M   WWMX.     .    :    .
#                                    "XXXXXXXXXXXXWW"       WN8888WWWWW  W8@@@8M    BMBRX.         .  : :
#                                   XXXXXXXX=MMWW":  .      W8N888WWWWWWWW88888W      XRBRXX.  .       .
#                              ....  ""XXXXXMM::::. .        W8@889WWWWWM8@8N8W      . . :RRXx.    .
#                                  ``...'''  MMM::.:.  .      W888N89999888@8W      . . ::::"RXV    .  :
#                                  ..'''''      MMMm::.  .      WW888N88888WW     .  . mmMMMMMRXx
#                               ..' .            ""MMmm .  .       WWWWWWW   . :. :,miMM"""  : ""`    .
#                                             .       ""MMMMmm . .  .  .   ._,mMMMM"""  :  ' .  :
#                                        .                  ""MMMMMMMMMMMMM""" .  : . '   .        .
# Copyright                                        .     .    .                      .         .
#
#	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#						non profit conservative organizations and individuals to use in support
#						of American freedom and the constitution. All other rights are reserved,
#						and any other use prohibited.
#
# Date			Version		Author			Description
# 2020.04.10	02.00		SquintMHG		Rewrite as app
# -------------------------------------------------------------------------------------------------------

# Python includes
import statistics

# MHGLIB includes
from mhgAppSettings		import AppSettings
from mhgDataField		import DataField
from mhgImpact			import Impact
from mhgUtility			import *

class ObservationStats(object):

	# Statistics Constants (public)
	STAT_STATUS_START_DATE			= 'IntelStartDate'									# Start date of observations
	STAT_STATUS_END_DATE			= 'IntelEndDate'									# End date of observations
	STAT_OBSERVE_NDAYS				= 'OvserveNDays'									# Number of days having observations
	STAT_OBSERVE_COUNT				= 'ObserveCount'									# Number of observations

	STAT_UTILITIES_WEIGHT			= 'UtilitiesWeight'									# Total utility impact weight
	STAT_SERVICES_WEIGHT			= 'ServicesWeight'									# Total services impact weight
	STAT_CONSUMABLES_WEIGHT			= 'ConsumablesWeight'								# Total consumables impact weight

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

	STAT_2M_CHECKINS				= '2M Checkins'										# Total 2M check-ins reported by net control
	STAT_2M_PARTICIPATE				= '2M Participate'									# Total 2M nets participated in
	STAT_HF_CHECKINS				= 'HF Checkins'										# Total HF check-ins reported by net control
	STAT_HF_PARTICIPATE				= 'HF Participate'									# Total HF nets participated in

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

	_dailyCounts					= {}
	_fieldData						= []

	# Constructor
	def __init__(self):
		self._SetObservationDefaults()

	#
	# Methods (private)
	#
	def _SetObservationDefaults(self):
		_appOptions = AppSettings.glob().options()
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
		dailyCounts					= {}

	def _SetFieldData(self):													# Create list of DataField items from properties. (archetype)
		barft("ObservationStats._SetFieldData.enter()")
		self._fieldData = []
		self._fieldData.append(self._statusStartDate)
		self._fieldData.append(self._statusEndDate)
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
		barft("ObservationStats._SetFieldData.exit()")
		return True

	def _dataFieldsDumpsText(self):
		dumpText = ""
		for field in self._fieldData:
			dumpText += "{}={},".format(field.fieldId(),field.value())
		return dumpText
	#
	# Methods (public)
	#
	def FieldFromId(self,fieldIdentifier):
		barft("ObservationStats.FieldFromId.enter(id={})".format(fieldIdentifier))
		statusField = None
		for field in self.dataFields():
			if field.fieldId() == fieldIdentifier:
				statusField = field
				break
		fieldText = "None"
		if not statusField is None: fieldText = statusField.value()
		barft("ObservationStats.FieldFromId.fields({})".format(self._dataFieldsDumpsText()))
		barft("ObservationStats.FieldFromId.exit(fieldct={},value={})".format(len(self._fieldData),fieldText))
		return statusField

	#
	# Property Getters (public)
	#
	def dataFields(self):
		self._SetFieldData()
		return self._fieldData

	
	def startDate(self):
		return self._statusStartDate

	def endDate(self):
		return self._statusEndDate

	def observationDays(self):
		return self._observeDays

	def observationCount(self):
		return self._observeCount

	def utilityWeight(self):
		return self._utilityWeight

	def servicesWeight(self):
		return self._servicesWeight

	def consumablesWeight(self):
		return self._consumablesWeight

	def checkins2M(self):
		return self._checkins2M

	def participate2M(self):
		return self._participate2M

	def checkinsHF(self):
		return self._checkinsHF

	def participateHF(self):
		return self._participateHF

	#
	# Property Getters, Calculated (public)
	#
	def utilitiesScore(self):
		score = Impact.EvalScore(self._utilityWeight.value(),self._observeCount.value()) 
		return DataField(self.STAT_UTILITIES_SCORE,		DataField.DTYPE_NUMERIC,	'UtilitiesScore',	score)

	def servicesScore(self):
		score = Impact.EvalScore(self._servicesWeight.value(),self._observeCount.value()) 
		return DataField(self.STAT_SERVICES_SCORE,		DataField.DTYPE_NUMERIC,	'ServicesScore',	score)

	def consumablesScore(self):
		score = Impact.EvalScore(self._consumablesWeight.value(),self._observeCount.value()) 
		return DataField(self.STAT_CONSUMABLES_SCORE,	DataField.DTYPE_NUMERIC,	'ConsumablesScore', score)

	def overallScore(self):
		score = int( statistics.mean([self.utilitiesScore().value(), \
										self.servicesScore().value(), \
										self.consumablesScore().value()] ) + 0.5 )
		return DataField(self.STAT_OVERALL_SCORE,		DataField.DTYPE_NUMERIC,	'OverallScore',		score)

	def maxScore(self):
		barfd("ObservationStats.maxScore.enter()")
		barfd("utilitiesScore={}".format(self.utilitiesScore().value()))
		barfd("servicesScore={}".format(self.servicesScore().value()))
		barfd("consumablesScore={}".format(self.consumablesScore().value()))
		score = max(self.utilitiesScore().value(),self.servicesScore().value(),self.consumablesScore().value())
		barfd("ObservationStats.maxScore.exit()")
		return DataField(self.STAT_MAX_SCORE,			DataField.DTYPE_NUMERIC,	'MaxScore',			score)

	def utilitiesCode(self):
		impactCode = Impact.CodeFromScore(self.utilitiesScore().value())
		return DataField(self.STAT_UTILITIES_CODE,		DataField.DTYPE_NUMERIC,	'UtilitiesCode',	impactCode)

	def servicesCode(self):
		impactCode = Impact.CodeFromScore(self.servicesScore().value())
		return DataField(self.STAT_SERVICES_CODE,		DataField.DTYPE_NUMERIC,	'ServicesCode',		impactCode)

	def consumablesCode(self):
		impactCode = Impact.CodeFromScore(self.consumablesScore().value())
		return DataField(self.STAT_CONSUMABLES_CODE,	DataField.DTYPE_NUMERIC,	'ConsumablesCode',	impactCode)

	def overallCode(self):
		impactCode = Impact.CodeFromScore(self.overallScore().value())
		return DataField(self.STAT_OVERALL_CODE,		DataField.DTYPE_NUMERIC,	'OverallCode',		impactCode)

	def maxCode(self):
		mscore=self.maxScore().value()
		impactCode = Impact.CodeFromScore(self.maxScore().value())
		return DataField(self.STAT_MAX_CODE,			DataField.DTYPE_NUMERIC,	'MaxCode',			impactCode)		

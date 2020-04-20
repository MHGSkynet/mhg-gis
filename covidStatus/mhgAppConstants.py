#
# ---------------------------------------------------------------------------------------------
# mhgAppConstants.py
#
# Copyright
#
#	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#						non profit conservative organizations and individuals to use in support
#						of American freedom and the constitution. All other rights are reserved,
#						and any other use prohibited.
#
# Date			Version		Author			Description
# 2020.04.20	02.00		SquintMHG		New Module
# ---------------------------------------------------------------------------------------------

# Python includes
import copy

#
# Application Constants
#
class AppConstants(object):										# Application Settings Class

	# Constants (public)
	PROGNM					= "mhgCovidStatus"					# Application program name
	FORMAT_YMD				= "%Y.%m.%d"						# date format YYYY.MM.DD
	TEMPLATE_DATE_TOKEN		= "YMD"								# Token for search/replace of date in file name templates

	# Constants (private)
	_COVID_SPREADSHEET_ID	= '1ckdKCNIB-5-KSUlV2ehW3KPARVlu_CC2npjsAHrml7Q'	# Google Document ID to fetch
	_COVID_DATA_RANGE		= 'DailyData!A2:K'									# Spreadsheet range to fetch (minus header)

	_currTimestamp			= None 								# current date and time (timestamp)
	_currDateYmd			= None 								# current date YYYY.MM.DD (text)
	_currDateTS				= None								# current date (timestamp)

	def __init__(self):
		raise RuntimeError('Call glob() instead')

	#
	#  Constructor (singleton)
	#
	@classmethod
	def glob(cls):												# Global (singleton) class reference

		# For first instance of class, initialize data
		if cls._instance is None:
			cls._instance = cls.__new__(cls)

			# System date
			cls._currTimestamp		= datetime.now() 										# current date and time (timestamp)
			cls._currDateYmd		= cls._currTimestamp.strftime(cls.FORMAT_YMD)			# current date YYYY.MM.DD (text)
			cls._currDateTS			= datetime.strptime(cls._currDateYmd,cls.FORMAT_YMD)	# current date (timestamp)

		return cls._instance


	def currTimestamp(cls):
		return copy.deepcopy(cls._currTimestamp)

	def currDateYmd(cls):
		return copy.deepcopy(cls._currDateYmd)

	def currDateTS(cls):
		return copy.deepcopy(cls._currDateTS)

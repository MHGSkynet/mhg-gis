#
# ---------------------------------------------------------------------------------------------
# mhgFetchCommandArgs.py
#
# Description
#
# 	Parse command line arguments for application.
#
# Copyright
#
#	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#						non profit conservative organizations and individuals to use in support
#						of American freedom and the constitution. All other rights are reserved,
#						and any other use prohibited.
#
# Date			Version		Author			Description
# 2020.04.05	01.03		SquintMHG		New Module
# ---------------------------------------------------------------------------------------------

import argparse
import textwrap
from textwrap import dedent
import os
import os.path
import re
import sys
from pathlib import Path
from datetime import datetime
from datetime import timedelta
from mhgDateParse import testDatePattern
from mhgDateParse import dateParser
from mhgDateParse import dateParseResult

_PROGRAM_NAME			= "mhgCovidDataFetch.py"
_MODULE_NAME			= "mhgFetchCommandArgs.py"

# System date
_currTimestamp			= datetime.now() 												# current date and time (timestamp)
_currDateYmd			= _currTimestamp.strftime("%Y.%m.%d")							# current date YYYY.MM.DD (text)
_currDateTS				= datetime.strptime(_currDateYmd,"%Y.%m.%d")					# current date (timestamp)

#
# COMMAND ARGUMENT PARSING
#
def _optionDate(dateString):															# Validate a date from command line. Parse and return in yyyy.mm.dd format
	
	parseResult = dateParser().parseDate(dateString)
	if parseResult.isBadDate():
		msg = "Not a valid date: '{0}'.".format(dateString)
		raise argparse.ArgumentTypeError(msg)

	retval = parseResult.dateYMD()
	return retval

def _optSw(optName):																	# Create option command line switch from option name
	return '--' + optName

def _noSw(optName):																		# Create negated option command line switch from option name
	return '--no' + optName

class _commandArgs(object):																# Command Arguments base class - holds constants
	# 
	#  Command Line Option Constants
	# 
	_ENV_APP_ALIAS			= "MHGGIS_APPALIAS"											# Environment variable containing alias program name to be used
	_OPT_CAPTURE_DETAIL		= 'detail'													# Whether to capture detail to daily CSV files.
	_OPT_GENERATE_SUMMARY	= 'summary'													# Whether to generate daily summary info CSV file.
	_OPT_FILTER_START_DATE	= 'start'													# Beginning date of range to select data by
	_OPT_FILTER_END_DATE	= 'end'														# End date of range to select data by
	_OPT_FILTER_DAYS		= 'ndays'													# Number of days from begin date to select data by
	_OPT_DEBUG				= 'debug'													# Debug enable
	_FORMAT_YMD				= '%Y.%m.%d'												# yyyy.mm.dd format 

class _optDateAction(argparse.Action,_commandArgs):										# Argument parser action to validate a date string. returns date in yyy.mm.dd format
	def __init__(self, option_strings, dest, nargs=None, **kwargs):
	#	if nargs is not None:
	#		raise ValueError("nargs not allowed")
		super(_optDateAction, self).__init__(option_strings, dest, **kwargs)
	def __call__(self, parser, namespace, values, option_string=None):
#		print('### DATE ACTION DEBUG: %r %r %r' % (namespace, values, option_string))
#		print('### DATE ACTION DEBUG option_string: %r' % option_string)
		optionDateYmd = _optionDate(values)
		setattr(namespace, self.dest, optionDateYmd)
		
		if option_string == _optSw(self._OPT_FILTER_START_DATE):
			setattr(namespace, self._OPT_FILTER_END_DATE, optionDateYmd)				# If setting start date, also set end date.

#
# Command Argument class for mhgFetch app
#
class mhgFetchCommandArgs(_commandArgs):

	def __init__(self):
		self._argsNamespace	= None
		self._argsHash		= {}

	#
	#  Get Command Line Arguments
	#
	def getArguments(self):
	
		success = False

		print("Alias var={}".format(self._ENV_APP_ALIAS))

		appAlias = os.environ.get(self._ENV_APP_ALIAS)									# See app alias is set. If so, use that for program name
		programName = _PROGRAM_NAME
		if not appAlias is None: programName = appAlias

		appTitle = 'MHG Covid Data Fetch'
		if 'Status' in programName: appTitle = 'MHG Covid Status Report'

		# Help epilogue text
		flawlessVictory = '''\
			Note:
				dates may be entered mm/dd, mm/dd/yyyy or yyyy.mm.dd
				nDays may be positive or negative.

			Examples:
				PROGNM                                  # Run for today
				PROGNM --start 2020.04.03               # Run for specific date
				PROGNM --start 04/03 --end 04/06        # Run for a date range
				PROGNM --start 04/03 --ndays 7          # Run for week following start date given
				PROGNM --start 04/03/2020 --ndays -7    # Run for week prior to start date given
				PROGNM --ndays -7                       # Run for the past week
			'''
		flawlessVictory = flawlessVictory.replace("PROGNM",programName)

		# Define arguments for parser
		parser = argparse.ArgumentParser( prog=programName,
											formatter_class=argparse.RawDescriptionHelpFormatter,
											description="=== {} ===".format(appTitle),
											epilog=textwrap.dedent(flawlessVictory))
											
		parser.add_argument(_optSw(self._OPT_FILTER_START_DATE), type=str,   nargs='?',				default=_currDateYmd,	action=_optDateAction,	help='Beginning date of range to select data by')
		parser.add_argument(_optSw(self._OPT_FILTER_END_DATE),   type=str,   nargs='?',				default=_currDateYmd,	action=_optDateAction,	help='End date of range to select data by')
		parser.add_argument(_optSw(self._OPT_FILTER_DAYS),       type=int,   nargs='?',				default=0,										help='Number of days from begin date to select data by')
		parser.add_argument(_noSw(self._OPT_CAPTURE_DETAIL),     dest=self._OPT_CAPTURE_DETAIL,		default=True, 			action='store_false',	help='Disables capture of detail to daily CSV files')
		parser.add_argument(_noSw(self._OPT_GENERATE_SUMMARY),   dest=self._OPT_GENERATE_SUMMARY,	default=True,			action='store_true',	help='Disables generation of summary info CSV file')
		parser.add_argument(_optSw(self._OPT_DEBUG),												default=False,			action='store_true',	help='Whether to barf debug info')

		# Parse Arguments
		self._argsNamespace = parser.parse_args()
		self._argsHash = vars(self._argsNamespace)

		print ("ARGS:{}".format(self._argsNamespace))

		# Post-parsing validation
		
		# Fix end date less than start date
		if self._argsHash[self._OPT_FILTER_START_DATE] > self._argsHash[self._OPT_FILTER_END_DATE]:
			swapDate = self._argsHash[self._OPT_FILTER_START_DATE]
			self._argsHash[self._OPT_FILTER_START_DATE] 	= self._argsNamespace.getattr(self._OPT_FILTER_END_DATE)
			self._argsHash[self._OPT_FILTER_END_DATE] 		= swapDate

		# If nDays is specified, and a date range isn't present, adjust range
		if self._argsHash[self._OPT_FILTER_START_DATE] == self._argsHash[self._OPT_FILTER_END_DATE] and \
				self._argsHash[self._OPT_FILTER_DAYS] != 0:
				
			if self._argsHash[self._OPT_FILTER_DAYS] > 1:
				startYmd = self._argsHash[self._OPT_FILTER_START_DATE]
				startTS = datetime.strptime(startYmd,self._FORMAT_YMD)
				deltaDays = timedelta(days=self._argsHash[self._OPT_FILTER_DAYS]-1)
				endTS = startTS + deltaDays
				self._argsHash[self._OPT_FILTER_END_DATE] = endTS.strftime(self._FORMAT_YMD)
			
			if self._argsHash[self._OPT_FILTER_DAYS] < 1:
				startYmd = self._argsHash[self._OPT_FILTER_START_DATE]
				endTS = datetime.strptime(startYmd,self._FORMAT_YMD)
				deltaDays = timedelta(days = -self._argsHash[self._OPT_FILTER_DAYS] - 1)
				startTS = endTS - deltaDays
				self._argsHash[self._OPT_FILTER_START_DATE]		= startTS.strftime(self._FORMAT_YMD)
				self._argsHash[self._OPT_FILTER_END_DATE]		= endTS.strftime(self._FORMAT_YMD)

		# If nDays was not specified, calculate it from start and end dates
		if self._argsHash[self._OPT_FILTER_DAYS] == 0:
			startTS = datetime.strptime(self._argsHash[self._OPT_FILTER_START_DATE],self._FORMAT_YMD)
			endTS   = datetime.strptime(self._argsHash[self._OPT_FILTER_END_DATE],self._FORMAT_YMD)
			deltaTime = endTS - startTS
			self._argsHash[self._OPT_FILTER_DAYS] = deltaTime.days + 1
		
		success = True
		return success

	def startDate(self):
		return self._argsHash[self._OPT_FILTER_START_DATE]
		
	def startDateTS(self):
		return datetime.strptime(self._argsHash[self._OPT_FILTER_START_DATE],self._FORMAT_YMD)

	def endDate(self):
		return self._argsHash[self._OPT_FILTER_END_DATE]

	def endDateTS(self):
		return datetime.strptime(self._argsHash[self._OPT_FILTER_END_DATE],self._FORMAT_YMD)
		
	def nDays(self):
		return self._argsHash[self._OPT_FILTER_DAYS]

	def isDateRange(self):
		return self._argsHash[self._OPT_FILTER_START_DATE] != self._argsHash[self._OPT_FILTER_END_DATE]
		
	def captureDetail(self):
		return self._argsHash[self._OPT_CAPTURE_DETAIL]
		
	def generateSummary(self):
		return self._argsHash[self._OPT_GENERATE_SUMMARY]

	def debug(self):
		return self._argsHash[self._OPT_DEBUG]

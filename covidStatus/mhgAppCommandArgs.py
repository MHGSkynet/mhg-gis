#
# ---------------------------------------------------------------------------------------------
# mhgAppCommandArgs.py
#
# Description       '-----------------------------------------------------------------'
#                                                 ||                   
#   Command Args Parsing Class               _____YY_____
#                                          .'@@@@@@@@@@@@'.
#                                         ///     ||     \\\
#                                        ///      ||      \\\
#                                        ||  ___  ||  _O_  ||
#                              .-_-.     || |   | || || ||     .-_-.
#                            .'d(x)b'.   |A'._Y_|_||_|_Y_.'A|   .'d(x)b'.
#                            |(x)O(x)|---|@@@@@@@@@@@@@@@@@@|---|(x)O(x)|
#                            |(x)O(x)|===|@@@@@@@@xxx@@@@@@@|===|(x)O(x)|
#                            '.g(x)P.'   '|g@@@@@xx%xx@@@@p|'   '.g(x)P.'
#                              '---'       '.g@@@@xxx@@@@p'       '---'
#                                         ==='.g@@@@@@@p.'===
#                                        //     \X_o_X/     \\
# Copyright                             (_)                 (_)
#
#	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#						non profit conservative organizations and individuals to use in support
#						of American freedom and the constitution. All other rights are reserved,
#						and any other use prohibited.
#
# Date			Version		Author			Description
# 2020.04.05	02.00		SquintMHG		New Module
# ---------------------------------------------------------------------------------------------

# Python includes
import argparse
import textwrap
from textwrap			import dedent
import copy
import os
import os.path
import re
import sys
from pathlib			import Path
from datetime			import datetime
from datetime			import timedelta

# MHGLIB includes
from mhgAppConstants	import AppConstants
from mhgDateParser		import DateParser

#
# COMMAND ARGUMENT PARSING
#

def _optSw(optName):																	# Create option command line switch from option name
	return '--' + optName

def _noSw(optName):																		# Create negated option command line switch from option name
	return '--no' + optName

class CommandOptions(object):															# Command Line options constants

	# 
	#  Command Line Option Constants 
	# 
	_OPT_CAPTURE_DETAIL		= 'detail'													# Whether to capture detail to daily CSV files.
	_OPT_GENERATE_SUMMARY	= 'summary'													# Whether to generate daily summary info CSV file.
	_OPT_GENERATE_PROJECT	= 'project'													# Whether to output a QGIS project as output
	_OPT_GENERATE_PDF		= 'pdf'														# Whether to output a PDF of the status
	_OPT_GENERATE_IMAGE		= 'image'													# Whether to output a JPG of the status

	_OPT_FILTER_START_DATE	= 'start'													# Beginning date of range to select data by
	_OPT_FILTER_END_DATE	= 'end'														# End date of range to select data by
	_OPT_FILTER_DAYS		= 'ndays'													# Number of days from begin date to select data by

	_OPT_INFO				= 'info'													# Info enable
	_OPT_DEBUG				= 'debug'													# Debug enable
	_OPT_TRACE				= 'trace'													# Trace enable
	_OPT_ZOMBIES			= 'zombies'													# Zombies enable
	
	_PROGRAM_NAME			= 'mhgCovidStatus.bat'


class _optDateAction(argparse.Action,CommandOptions):									# Argument parser action to validate a date string. returns date in yyy.mm.dd format
	def __init__(self, option_strings, dest, nargs=None, **kwargs):
	#	if nargs is not None:
	#		raise ValueError("nargs not allowed")
		super(_optDateAction, self).__init__(option_strings, dest, **kwargs)

	def __call__(self, parser, namespace, values, option_string=None):
		#barfd('AppCommandArgs._optDateAction(%r %r %r)' % (namespace, values, option_string))
		#barfd('AppCommandArgs._optDateAction(option_string: %r)' % option_string)
		optionDateYmd = self._optionDate(values)
		setattr(namespace, self.dest, optionDateYmd)
		
		if option_string == _optSw(CommandOptions._OPT_FILTER_START_DATE):
			setattr(namespace, CommandOptions._OPT_FILTER_END_DATE, optionDateYmd)		# If setting start date, also set end date.

	def _optionDate(self,dateString):													# Validate a date from command line. Parse and return in yyyy.mm.dd format
		parseResult = DateParser().ParseDate(dateString)
		if parseResult.isBadDate():
			msg = "Not a valid date: '{0}'.".format(dateString)
			raise argparse.ArgumentTypeError(msg)

		retval = parseResult.dateYMD()
		return retval

#
# Command Argument class for mhgFetch app
#
class AppCommandArgs(CommandOptions,AppConstants):

	# Constants (private)
	_ENV_APP_ALIAS			= "MHGGIS_APPALIAS"											# Environment variable containing alias program name to be used
	_FORMAT_YMD				= '%Y.%m.%d'												# yyyy.mm.dd format 

	#
	# Constructor
	#
	def __init__(self):
		self._argsNamespace	= None
		self._argsHash		= {}

	#
	#  Get Command Line Arguments
	#
	def GetArguments(self):
	
		success = False

		appAlias = os.environ.get(self._ENV_APP_ALIAS)									# See app alias is set. If so, use that for program name
		programName = self._PROGRAM_NAME
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
											
		parser.add_argument(_optSw(self._OPT_FILTER_START_DATE), type=str,   nargs='?',				default=self.currDateYmd(),	action=_optDateAction,	help='Beginning date of range to select data by')
		parser.add_argument(_optSw(self._OPT_FILTER_END_DATE),   type=str,   nargs='?',				default=self.currDateYmd(),	action=_optDateAction,	help='End date of range to select data by')
		parser.add_argument(_optSw(self._OPT_FILTER_DAYS),       type=int,   nargs='?',				default=0,										help='Number of days from and including begin date to select data by')
		parser.add_argument(_noSw(self._OPT_CAPTURE_DETAIL),     dest=self._OPT_CAPTURE_DETAIL,		default=True, 			action='store_false',	help='Disables capture of detail to daily CSV files')
		parser.add_argument(_noSw(self._OPT_GENERATE_SUMMARY),   dest=self._OPT_GENERATE_SUMMARY,	default=True,			action='store_true',	help='Disables generation of summary info CSV file')
		parser.add_argument(_noSw(self._OPT_GENERATE_PROJECT),   dest=self._OPT_GENERATE_PROJECT,	default=True,			action='store_true',	help='Disables saving of GIS Project')
		parser.add_argument(_noSw(self._OPT_GENERATE_PDF),		 dest=self._OPT_GENERATE_PDF,		default=True,			action='store_true',	help='Disables saving of PDF file')
		parser.add_argument(_noSw(self._OPT_GENERATE_IMAGE),   	 dest=self._OPT_GENERATE_IMAGE,		default=True,			action='store_true',	help='Disables saving of JPG image')
		parser.add_argument(_optSw(self._OPT_INFO),													default=False,			action='store_true',	help='Whether to barf progress info')
		parser.add_argument(_optSw(self._OPT_DEBUG),												default=False,			action='store_true',	help='Whether to barf debug info')
		parser.add_argument(_optSw(self._OPT_TRACE),												default=False,			action='store_true',	help='Whether to barf trace info')
		parser.add_argument(_optSw(self._OPT_ZOMBIES),												default=False,			action='store_true',	help='Whether to enable zombies')

		# Parse Arguments
		self._argsNamespace = parser.parse_args()
		self._argsHash = vars(self._argsNamespace)

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
			
		# Trace implies debug
		#if self._argsHash[self._OPT_TRACE]:		self._argsHash[self._OPT_DEBUG] = True

		# Debug implies info
		#if self._argsHash[self._OPT_DEBUG]:		self._argsHash[self._OPT_INFO] = True
		
		success = True
		return success

	#
	# Getters
	#
	def startDate(self):
		return copy.deepcopy(self._argsHash[self._OPT_FILTER_START_DATE])
		
	def startDateTS(self):
		return datetime.strptime(self._argsHash[self._OPT_FILTER_START_DATE],self._FORMAT_YMD)

	def endDate(self):
		return copy.deepcopy(self._argsHash[self._OPT_FILTER_END_DATE])

	def endDateTS(self):
		return datetime.strptime(self._argsHash[self._OPT_FILTER_END_DATE],self._FORMAT_YMD)
		
	def nDays(self):
		return copy.deepcopy(self._argsHash[self._OPT_FILTER_DAYS])

	def isDateRange(self):
		return self._argsHash[self._OPT_FILTER_START_DATE] != self._argsHash[self._OPT_FILTER_END_DATE]
		
	def captureDetail(self):
		return copy.deepcopy(self._argsHash[self._OPT_CAPTURE_DETAIL])
		
	def generateSummary(self):
		return copy.deepcopy(self._argsHash[self._OPT_GENERATE_SUMMARY])

	def generateProject(self):
		return copy.deepcopy(self._argsHash[self._OPT_GENERATE_PROJECT])

	def generatePdf(self):
		return copy.deepcopy(self._argsHash[self._OPT_GENERATE_PDF])

	def generateImage(self):
		return copy.deepcopy(self._argsHash[self._OPT_GENERATE_IMAGE])

	def infoEnabled(self):
		return self._argsHash[self._OPT_INFO] or self._argsHash[self._OPT_DEBUG]
		
	def debugEnabled(self):
		return copy.deepcopy(self._argsHash[self._OPT_DEBUG])
		
	def traceEnabled(self):
		return copy.deepcopy(self._argsHash[self._OPT_TRACE])

	def zombiesEnabled(self):
		return copy.deepcopy(self._argsHash[self._OPT_ZOMBIES])
		
	#
	#	Methods
	# 
	def filterRangeText(self):
		if self.isDateRange(): 				rangeText = "{} to {}".format(self.startDate(),self.endDate())
		if not self.isDateRange(): 			rangeText = self.endDate()
		return rangeText

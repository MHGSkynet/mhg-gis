#
# ---------------------------------------------------------------------------------------------
# mhgDateParse.py
#
# Description
#
# 	Date Parsing Routines
#
# Copyright
#
#	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#						non profit conservative organizations and individuals to use in support
#						of American freedom and the constitution. All other rights are reserved,
#						and any other use prohibited.
#
# Date			Version		Author			Description
# 2020.04.06	01.03		SquintMHG		New Module
# ---------------------------------------------------------------------------------------------

from datetime import datetime
import re
import sys

MODULE_NAME				= "mhgDateParse.py"

def testDatePattern(regex,parseString,strptimeFormat,strptimeString=''):				# Test a date string for pattern match, and parse to timestamp on match
	if strptimeString == '': strptimeString = parseString
	dateTS = None																		
	pattern = re.compile(regex)
	if pattern.match(parseString):
		dateTS = datetime.strptime(strptimeString, strptimeFormat)
		
	return dateTS

class dateParseResult(object):

	def __init__(self,aDateTS):
		self.parsedDateTS	= aDateTS
		self.parsedDateYMD	= None
		if not aDateTS is None: self.parsedDateYMD = aDateTS.strftime("%Y.%m.%d")

	def dateTS(self):
		return self.parsedDateTS

	def dateYMD(self):
		return self.parsedDateYMD
		
	def isBadDate(self):
		isBad = self.parsedDateTS is None
		return isBad

class dateParser(object):

	def __init__(self):
		self.dateTS			= None
		self.dateYMD		= None
		
	def parseDate(self,dateString):														# Parse a date string into a timestamp
		dateTS = None
		
		dateTS	= testDatePattern('^[0-9]+/[0-9]+$', dateString, '%Y/%m/%d', "{}/{}".format(datetime.now().strftime("%Y"),dateString))	#	mm/dd format
		if dateTS is None: dateTS	= testDatePattern('^[0-9]{4}[-][0-9]+[-][0-9]+$', dateString, '%Y-%m-%d', dateString)				#	yyyy-mm-dd
		if dateTS is None: dateTS	= testDatePattern('^[0-9]{4}[/][0-9]+[/][0-9]+$', dateString, '%Y/%m/%d', dateString)				#	yyyy/mm/dd
		if dateTS is None: dateTS	= testDatePattern('^[0-9]{4}[.][0-9]+[.][0-9]+$', dateString, '%Y.%m.%d', dateString)				#	yyyy.mm.dd

		parseResult = dateParseResult(dateTS)

		return parseResult

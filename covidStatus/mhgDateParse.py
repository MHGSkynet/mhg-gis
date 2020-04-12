#                                               ,--.
# -----------------------------------------    {    }      ------------------------------------
# mhgDateParse.py                              K,   }
#                                             /  `Y`
# Description                            _   /   /
#                                       {_'-K.__/
#   Date Parsing Classes and Routines     `/-.__L._
#                                         /  ' /`\_}
#                                        /  ' /     
#                                ____   /  ' /
#                         ,-'~~~~    ~~/  ' /_
#                       ,'             ``~~~%%',
#                      (                     %  Y
#                     {                      %% I
#                    {      -                 %  `.
#                    |       ',                %  )
#                    |        |   ,..__      __. Y
#                    |    .,_./  Y ' / ^Y   J   )|
#                    \           |' /   |   |   ||
#                     \          L_/    . _ (_,.'(
#                      \,   ,      ^^""' / |      )
#                        \_  \          /,L]     /
#                          '-_`-,       ` `   ./`
#                             `-(_            )
#                                 ^^\.._M_,N--`
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

# Python includes
from datetime import datetime
import re
import sys

class DateParseResult(object):

	# Properties (private)
	_parsedDateTS		= None
	_parsedDateYMD		= None

	# Constructor
	def __init__(self,aDateTS):
		self._parsedDateTS	= aDateTS
		self._parsedDateYMD	= None
		if not aDateTS is None: self._parsedDateYMD = aDateTS.strftime("%Y.%m.%d")

	#
	# Properties (public)
	#

	# Date as timestamp datatype 
	def dateTS(self):
		return self._parsedDateTS

	# Date as yyyy.mm.dd string
	def dateYMD(self):
		return self._parsedDateYMD
		
	# Your date sucks
	def isBadDate(self):
		isBad = self._parsedDateTS is None
		return isBad

class DateParser(object):

	# Constructor
	def __init__(self):
		pass
		
	#
	# Methods (public)
	#
	def ParseDate(self,dateString):														# Parse a date string into a timestamp
		dateTS = None
		
		dateTS	= self.TestDatePattern('^[0-9]+/[0-9]+$', dateString, '%Y/%m/%d', "{}/{}".format(datetime.now().strftime("%Y"),dateString))	#	mm/dd format
		if dateTS is None: dateTS	= self.TestDatePattern('^[0-9]{4}[-][0-9]+[-][0-9]+$', dateString, '%Y-%m-%d', dateString)				#	yyyy-mm-dd
		if dateTS is None: dateTS	= self.TestDatePattern('^[0-9]{4}[/][0-9]+[/][0-9]+$', dateString, '%Y/%m/%d', dateString)				#	yyyy/mm/dd
		if dateTS is None: dateTS	= self.TestDatePattern('^[0-9]{4}[.][0-9]+[.][0-9]+$', dateString, '%Y.%m.%d', dateString)				#	yyyy.mm.dd

		parseResult = DateParseResult(dateTS)

		return parseResult

	def TestDatePattern(regex,parseString,strptimeFormat,strptimeString=''):			# Test a date string for pattern match, and parse to timestamp on match
		if strptimeString == '': strptimeString = parseString
		dateTS = None																		
		pattern = re.compile(regex)
		if pattern.match(parseString):
			dateTS = datetime.strptime(strptimeString, strptimeFormat)
			
		return dateTS

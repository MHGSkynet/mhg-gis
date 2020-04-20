#                                      
# ---------------------------------------------------------------------------------------------------
# mhgDateParser                                                               ^__
#                                                             .-""""""-.     |* _)
# Description                                                /          \   /  /
#                                                           /            \_/  /
#   Date Parsing Classes        _                          /|                /
#                           _-'"/\                        / |    ____    _.-"            _
#                        _-'   (  '-_            _       (   \  |\  /\  ||           .-'".".
#                    _.-'       '.   `'-._   .-'"/'.      "   | |/ /  | |/        _-"   (   '-_
#                                 '.      _-"   (   '-_       \ | /   \ |     _.-'       )     "-._
#                               _.'   _.-'       )     "-._    ||\\   |\\  '"'        .-'
#                             '               .-'          `'  || \\  ||))
#                   ___ __  _  ___  _ ____________ _____  ___ _|\ _|\_|\\/ _______________  ___   _
#                                           c  c  " c C ""C  " ""  "" ""
#                                       c       C
#                                  C        C                                      
#                                       C                                          #givemeperlorgivemedeath
# Copyright              C     c                                                   #robisgreat
#
#	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#						non profit conservative organizations and individuals to use in support
#						of American freedom and the constitution. All other rights are reserved,
#						and any other use prohibited.
#
# Date			Version		Author			Description
# 2020.04.06	01.03		SquintMHG		New Module
# ---------------------------------------------------------------------------------------------------

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

	def TestDatePattern(self,regex,parseString,strptimeFormat,strptimeString=''):		# Test a date string for pattern match, and parse to timestamp on match
		if strptimeString == '': strptimeString = parseString
		dateTS = None																		
		pattern = re.compile(regex)
		if pattern.match(parseString):
			dateTS = datetime.strptime(strptimeString, strptimeFormat)
			
		return dateTS

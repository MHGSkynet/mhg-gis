#
# ---------------------------------------------------------------------------------------------
# mhgCsvWriter.py
#
# Description
#
# 	Base class for CSV writing
#
# Copyright
#
#	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#						non profit conservative organizations and individuals to use in support
#						of American freedom and the constitution. All other rights are reserved,
#						and any other use prohibited.
#
# Date			Version		Author			Description
# 2020.04.07	01.03		SquintMHG		New Module
# ---------------------------------------------------------------------------------------------

import sys
from mhgDateParse import DateParser
from mhgDateParse import DateParseResult
import mhgCsvField

class CsvWriter(object):										# Base CSV Writing Objec

	# Properties (private)
	_csvFH				= None									# File Handle for IO
	_csv_field_sep		= ','									# CSV field separator
	_csv_field_quote	= '"'									# CSV field quote bounds character

    def __init__(self):
		_csvFH				= None								# Initialize File Handle for IO
		_csv_field_sep		= ','								# Initialize CSV field separator
		_csv_field_quote	= '"'								# Initialize CSV field quote bounds character

	#
	# Methods (private) 
	#
	def _csvText(cls,dataValue,dataType,addSeparator=True):		# Format data as CSV text
		outText = ''
		if dataType == CsvField.DTYPE_NUMERIC:	outText = str(coalesce(dataValue,0))
		if dataType == CsvField.DTYPE_TEXT:		outText = cls._csv_field_quote + dataValue + cls._csv_field_quote
		if dataType == CsvField.DTYPE_DATE:		outText = DateParser().ParseDate(dataValue).dateYMD()
		if addSeparator:						outText += cls._csv_field_sep
		return outText

	#
	# Property Getters (public)
	#
	def fieldSep(self):
		return self._csv_field_sep
		
	def fieldQuote(self):
		return self._csv_field_quote

	#
	# Property Setters (public)
	#
	def SetFieldSep(self,separator):
		self._csv_field_sep = separator
	
	def SetFieldQuote(self,quotechar):
		self._csv_field_quote = quotechar
		


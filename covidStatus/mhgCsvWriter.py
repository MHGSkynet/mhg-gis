#
# ---------------------------------------------------------------------------------------------
# mhgCsvWriter.py
#
# Description
#
#   Base class for CSV writing
#
# Copyright
#
#   Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#                       non profit conservative organizations and individuals to use in support
#                       of American freedom and the constitution. All other rights are reserved,
#                       and any other use prohibited.
#
# Date          Version     Author          Description
# 2020.04.20    02.00       SquintMHG       New Module
# ---------------------------------------------------------------------------------------------

# Python includes
import copy
import sys

# MHGLIB includes
from mhgCsvField	import CsvField
from mhgDateParser	import DateParser
from mhgDateParser	import DateParseResult
from mhgUtility		import *

class CsvWriter(object):										# Base class for CSV writing

	# Properties (private)
	_fhCsv				= None									# File Handle for IO
	_csv_field_sep		= ','									# CSV field separator
	_csv_field_quote	= '"'									# CSV field quote bounds character
	_csv_file_spec		= None									# File spec of open csv

	def __init__(self):
		_fhCsv				= None								# Initialize File Handle for IO
		_csv_field_sep		= ','								# Initialize CSV field separator
		_csv_field_quote	= '"'								# Initialize CSV field quote bounds character
		_csv_file_spec		= None								# Initialize File spec CSV

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
	# Methods (public)
	# 
	def Write(self,text):										# Write text to CSV
		barfd("CsvWriter.Write({})".format(text))
		self._fhCsv.write(text + '\n')
		return True

	def Close(self):											# Close CSV
		barfd("CsvWriter.Close()")
		self._fhCsv.close()
		self._fhCsv = None
		return True

	#
	# Property Getters (public)
	#
	def fieldSep(self):
		return copy.deepcopy(self._csv_field_sep)

	def fieldQuote(self):
		return copy.deepcopy(self._csv_field_quote)

	def fileSpec(self):
		return copy.deepcopy(self._csv_file_spec)

	#
	# Property Setters (public)
	#
	def SetFieldSep(self,separator):
		self._csv_field_sep = copy.deepcopy(separator)

	def SetFieldQuote(self,quotechar):
		self._csv_field_quote = copy.deepcopy(quotechar)

	def SetFileSpec(self,filespec):
		self._csv_file_spec = copy.deepcopy(filespec)

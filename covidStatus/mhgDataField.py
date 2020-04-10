#
# ---------------------------------------------------------------------------------------------
# mhgDataField.py
#
# Description
#
# 	Class for Data Fields from CSVs and Spreadsheets
#
# Copyright
#
#	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#						non profit conservative organizations and individuals to use in support
#						of American freedom and the constitution. All other rights are reserved,
#						and any other use prohibited.
#
# Date			Version		Author			Description
# 2020.04.07	02.00		SquintMHG		New Module
# ---------------------------------------------------------------------------------------------

import sys

class DataField(object):

	# Data Type Constants (public)
	DTYPE_NUMERIC		= 'numeric'
	DTYPE_TEXT			= 'text'
	DTYPE_DATE			= 'date'

	# Field properties (private)
	_field_id			= None									# Field ID
	_field_dtype		= None									# Field data type
	_field_header_text	= None									# Field header text
	_field_value		= None									# Field value holder
	_column_number		= None									# Field Column Number
	_source_id			= None									# Field Source ID

	# Constructor
    def __init__(self,fldid=None,dtype=CsvField.DTYPE_TEXT,headertext="",value=None,colNo=None,srcid=None):

		self._field_id				= fldid
		self._field_dtype			= dtype
		self._field_header_text		= headertext
		self._field_value			= value
		self._column_number			= colNo
		self._source_id				= srcid
	
	#
	# Property getters (public)
	#
	def fieldId(self):
		return self._field_id
		
	def dataType(self):
		return self._field_dtype
		
	def headerText(self):
		return self._field_header_text
		
	def sourceId(self):
		return self._source_id
		
	def columnNo(self):
		return self._column_number

	def value(self):
		return self._field_value
		
	#
	# Property setters (public)
	#
	def SetFieldId(self,id):
		self._field_id = id
		
	def SetDataType(self,dtype):
		self._field_dtype = dtype
		
	def SetHeaderText(self,headerText):
		self._field_header_text = headerText
		
	def SetSourceId(self,srcId):
		self._source_id = srcId
		
	def SetColumnNo(self,colNo):
		self._column_number = colNo
	
	def SetValue(self,value):
		self._field_value = value
	

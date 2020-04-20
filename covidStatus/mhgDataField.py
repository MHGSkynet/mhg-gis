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

# Python includes
import copy
import sys

class DataField(object):

	# Data Type Constants (public)
	DTYPE_NUMERIC		= 'numeric'								# Numeric data type
	DTYPE_TEXT			= 'text'								# Text data type
	DTYPE_DATE			= 'date'								# Date data type

	# Field properties (private)
	_field_id			= None									# Field ID
	_field_dtype		= None									# Field data type
	_field_header_text	= None									# Field header text
	_field_value		= None									# Field value holder
	_column_number		= None									# Field Column Number
	_source_id			= None									# Field Source ID

	# Constructor
	def __init__(self,fldid=None,dtype=DTYPE_TEXT,header="",value=None,colNo=None,srcid=None):

		self._field_id				= fldid						# Initialize Field ID
		self._field_dtype			= dtype						# Initialize Field data type
		self._field_header_text		= header					# Initialize Field header text
		self._field_value			= value						# Initialize Field value
		self._column_number			= colNo						# Initialize Field Column Number
		self._source_id				= srcid						# Initialize Field Source ID
	#
	# Methods (public)
	#
	def AddValue(self,value):									# Add a value to this field's value
		self._field_value = self._field_value + value
		
	#
	# Property getters (public)
	#
	def fieldId(self):
		return copy.deepcopy(self._field_id)

	def dataType(self):
		return copy.deepcopy(self._field_dtype)

	def headerText(self):
		return copy.deepcopy(self._field_header_text)

	def sourceId(self):
		return copy.deepcopy(self._source_id)

	def columnNo(self):
		return copy.deepcopy(self._column_number)

	def value(self):
		return copy.deepcopy(self._field_value)
	
	#
	# Properties (static)
	#
	def isEmpty(self):
		return self._field_value is None or str(self._field_value).strip() == ""

	#
	# Property setters (public)
	#
	def SetFieldId(self,id):
		self._field_id = copy.deepcopy(id)

	def SetDataType(self,dtype):
		self._field_dtype = copy.deepcopy(dtype)

	def SetHeaderText(self,headerText):
		self._field_header_text = copy.deepcopy(headerText)

	def SetSourceId(self,srcId):
		self._source_id = copy.deepcopy(srcId)

	def SetColumnNo(self,colNo):
		self._column_number = copy.deepcopy(colNo)

	def SetValue(self,value):
		self._field_value = copy.deepcopy(value)

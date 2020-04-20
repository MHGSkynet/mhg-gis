#
# ---------------------------------------------------------------------------------------------
# mhgCsvField.py
#
# Description
#
# 	Class for CSV Fields
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
import sys

# MHGLIB includes
from mhgDataField	import DataField


class CsvField(DataField):

	# Constructor
	def __init__(self,fldid=None,dtype=DataField.DTYPE_TEXT,headertext="",value=None,colNo=None,srcid=None):

		self._field_id				= fldid
		self._field_dtype			= dtype
		self._field_header_text		= headertext
		self._field_value			= value
		self._column_number			= colNo
		self._source_id				= srcid

	#
	# Field property getters (public)
	#
	def fieldId(self):
		return self._field_id

	def fieldDtype(self):
		return self._field_dtype

	def fieldHeaderText(self):
		return self._field_header_text

	def sourceId(self):
		return self._source_id

	#
	# Field property setters (public)
	#
	def setFieldId(self,id):
		self._field_id = id

	def setDtype(self,dtype):
		self._field_dtype = dtype

	def setHeaderText(self,headerText):
		self._field_header_text = headerText

	def SetSourceId(self,srcId):
		self._source_id = srcId


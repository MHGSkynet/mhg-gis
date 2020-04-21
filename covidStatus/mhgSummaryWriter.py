#
# ---------------------------------------------------------------------------------------------
# mhgSummaryWriter.py
#
# Description
#
#   Class for writing Summary info
#
# Copyright
#
#    Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#                       non profit conservative organizations and individuals to use in support
#                       of American freedom and the constitution. All other rights are reserved,
#                       and any other use prohibited.
# TODOs
#    TODO: Add error trapping on file open, type conversion issues?
#
# Date          Version     Author          Description
# 2020.04.20    02.00       SquintMHG       New Module
# ---------------------------------------------------------------------------------------------

# Python includes
import sys

# MHGLIB includes
from mhgAppCommandArgs	import AppCommandArgs
from mhgCsvWriter		import CsvWriter
from mhgDataField		import DataField
from mhgUtility			import *

class SummaryWriter(CsvWriter):												# Summary CSV Writer class

	# Properties (private)

	#
	# Constructor
	#
	def __init__(self):
		pass

	#
	# Methods (public)
	#
	def Open(self,stats):													# Open Summary CSV for output
		success = False
		if self._fhCsv is None:
			self.SetFileSpec( AppSettings.glob().summaryCsvSpec() )
			barfd("SummaryWriter.Open(file={})".format(self._fhCsv))
			self._fhCsv = open(self.fileSpec(), 'w')
			if self._fhCsv is None:
				raise EnvironmentError("Can't open output Summary CSV ({})".format(self.fileSpec()))
			self.WriteHeader(stats)
			success = True

		return success

	def WriteHeader(self,stats):											# Write Summary CSV header
		barfd("SummaryWriter.WriteHeader()")
		csvLine = ''
		for field in stats.dataFields():
			csvLine += self._csvText(field.headerText(), DataField.DTYPE_TEXT)

		self.Write(csvLine)
		return True

	def WriteCountyStats(self,stats):										# Write a CountyStats object's field values to CSV
		self.Open(stats)
		csvLine = ''
		for field in stats.dataFields():
			csvLine += self._csvText(field.value(), field.dataType())
		self.Write(csvLine)	

	def WriteStateCountyStats(self,stateData):								# Dump everything in a hash of CountyStats to Summary CSV
		success = True

		barfd("SummaryWriter.WriteStateCountyStats()")
		barfi("Summary data generating ...")

		for countyName in stateData.countyList():
			countyStats	= stateData.countyData(countyName)
			self.WriteCountyStats(countyStats)

		self.Close()

		barfi("Summary data complete. Stats recorded for {} counties.".format(len(stateData.countyList())))

		return success
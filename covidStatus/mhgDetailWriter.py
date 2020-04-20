#
# ---------------------------------------------------------------------------------------------
# mhgDetailWriter.py
#
# Description
#
# 	Class for writing Detail info to CSV(s).  Data for separate dates are written to separate
#	files.
#
#
#             !      /-----\============@                           _,_
#             |_____/_______\_____                            _____/_o_\_____
#            /____________________\                          (==(/_______\)==)
#             \+__+__+__+__+__+__*/                           \==\/     \/==/
#
# Copyright
#
#	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#						non profit conservative organizations and individuals to use in support
#						of American freedom and the constitution. All other rights are reserved,
#						and any other use prohibited.
#
# Date			Version		Author			Description
# 2020.04.20	02.00		SquintMHG		New Module
# ---------------------------------------------------------------------------------------------

# Python includes
import sys

# MHGLIB includes
from mhgAppCommandArgs		import AppCommandArgs
from mhgCsvWriter			import CsvWriter
from mhgDataField			import DataField
from mhgUtility				import *


class DetailWriter(CsvWriter):												# Summary CSV Writer

	# Properties (private)
	_detailDateYmd						= None								# Date of current open CSV file

	# Constructor
	def __init__(self):
		_detailDateYmd					= None								# Initialize date of current open CSV file

	#
	# Methods (public)
	# 
	def CleanUp(self):														# Delete any existing output CSV files for date range being run
		barfd("DetailWriter.CleanUp().enter()")
		detailStartTS = AppSettings.glob().options().startDateTS()
		detailDateTS = detailStartTS
		deltaOneDay = timedelta(days=1)

		for dayNo in range(AppSettings.glob().options().nDays()):
			barfd("DetailWriter.Cleanup(cleanLoop.dayNo={})".format(dayNo))
			detailDateYmd = detailDateTS.strftime(AppSettings.FORMAT_YMD)
			self.SetFileSpec( AppSettings.glob().detailCsvTemplate().replace(AppSettings.TEMPLATE_DATE_TOKEN,detailDateYmd) )
			barfd("DetailWriter.Cleanup(dayNo={},date={},file={})".format(dayNo,detailDateYmd,self.fileSpec()))
			if os.path.isfile(self.fileSpec()):
				barfd("DetailWriter.Cleanup(deleteFile={})".format(self.fileSpec()))
				os.remove(self.fileSpec())
			detailDateTS = detailDateTS + deltaOneDay
		barfd("DetailWriter.CleanUp().exit()")
		return True

	def Close(self):														# Close Detail CSV
		barfd("DetailWriter.Close(date={})".format(self._detailDateYmd))
		super(DetailWriter, self).Close()
		self._detailDateYmd = None
		return True

	def Open(self,statRow):													# Open Detail CSV for output
		if not self._fhCsv is None and statRow.intelDate().value() != self._detailDateYmd:
			self.Close()

		if self._fhCsv is None:
			self.SetFileSpec( AppSettings.glob().detailCsvTemplate().replace(AppSettings.TEMPLATE_DATE_TOKEN,statRow.intelDate().value()) )
			isNew = not os.path.isfile(self.fileSpec())
			barfd("DetailWriter.Open(isNew={},file={})".format(isNew,self.fileSpec()))
			self._fhCsv = open(self.fileSpec(), 'a')
			if self._fhCsv is None:
				raise EnvironmentError("Can't open output Detail CSV ({})".format(self.fileSpec()))
			if isNew: self.WriteHeader(statRow)

		self._detailDateYmd = statRow.intelDate().value()
		return True

	def WriteHeader(self,statRow):											# Write Detail CSV header
		barfd("DetailWriter.WriteHeader()")
		csvLine = ''
		for field in statRow.dataFields():
			csvLine += self._csvText(field.headerText(), DataField.DTYPE_TEXT)

		self.Write(csvLine)
		return True

	def WriteRow(self,statRow):												# Write Google Sheet row to Detail CSV
		self.Open(statRow)
		csvLine = ''
		for field in statRow.dataFields():
			csvLine += self._csvText(field.value(), field.dataType())

		self.Write(csvLine)
		return True

	def WriteStatusRows(self,statRows):										# Take list of Google Sheet Rows and barf to a CSV
		self.CleanUp()
		for stsRow in statRows:
			self.WriteRow(stsRow)	
		self.Close()
		return True

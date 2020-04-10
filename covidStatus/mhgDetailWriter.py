#
# ---------------------------------------------------------------------------------------------
# mhgDetailWriter.py
#
# Description
#
# 	Class for writing Detail info to CSV(s).  Data for separate dates are written to separate
#	files.
#
# Copyright
#
#	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#						non profit conservative organizations and individuals to use in support
#						of American freedom and the constitution. All other rights are reserved,
#						and any other use prohibited.
#
# Date			Version		Author			Description
# 2020.04.08	02.00		SquintMHG		New Module
# ---------------------------------------------------------------------------------------------

import sys
import mhgCommandArgs
import mhgCsvWriter

class DetailWriter(CsvWriter):									# Summary CSV Writer

	# Properties (private)
	_fhDetailCSV							= None				# Detail CSV file handle
	_detailCSVDateYmd						= None				# Date of current open CSV file
	_detailCsvSpec							= None				# File spec of open Detail CSV

	# Constructor
    def __init__(self):
		_fhDetailCSV						= None				# Initialize detail CSV file handle
		_detailCSVDateYmd					= None				# Initialize date of current open CSV file
		_detailCsvSpec						= None				# File spec of open Detail CSV

	#
	# Methods (public)
	# 
	def Cleanup(self):																# Delete any existing output CSV files for date range being run
		barfd("DetailWriter.Cleanup()")
		detailStartTS = AppSettings.glob().options().startDateTS()
		detailDateTS = detailStartTS
		deltaOneDay = timedelta(days=1)
		
		for dayNo in range(AppSettings.glob().options().nDays()):
			barfd("DetailWriter.Cleanup(cleanLoop.dayNo={})".format(dayNo))
			detailDateYmd = detailDateTS.strftime(AppSettings.FORMAT_YMD)
			self._detailCsvSpec = AppSettings.glob().detailCsvTemplate().replace(AppSettings.TEMPLATE_DATE_TOKEN,detailDateYmd)
			barfd("DetailWriter.Cleanup(dayNo={},date={},file={})".format(dayNo,detailDateYmd,self._detailCsvSpec))
			if os.path.isfile(self._detailCsvSpec):
				barfd("DetailWriter.Cleanup(deleteFile={})".format(self._detailCsvSpec))
				os.remove(self._detailCsvSpec)
			detailDateTS = detailDateTS + deltaOneDay

		return True

	def Close(self):																# Close Detail CSV
		barfd("DetailWriter.Close(date={})".format(self._detailCSVDateYmd))
		self._fhDetailCSV.close()
		self._fhDetailCSV = None
		self._detailCSVDateYmd = None
		return True

	def Open(self,statRow):															# Open Detail CSV for output

		if not self._fhDetailCSV is None and statRow.intelDate() != self._detailCSVDateYmd:
			self.Close()

		if self._fhDetailCSV is None:
			self._detailCsvSpec = AppSettings.glob().detailCsvTemplate.replace(AppSettings.TEMPLATE_DATE_TOKEN,statRow.intelDate())
			isNew = not os.path.isfile(self._detailCsvSpec)
			barfd("DetailWriter.Open(isNew={},file={})".format(isNew,self._detailCsvSpec))
			fhDetailCSV = open(self._detailCsvSpec, 'a')
			if fhDetailCSV is None:
				raise EnvironmentError("Can't open output detailCsv ({})".format(self._detailCsvSpec)))
			if isNew: detailCsvWriteHeader(statRow)

		detailCSVDateYmd = statRow.intelDate()
		return True

	def WriteHeader(self,statRow):											# Write Detail CSV header
		barfd("DetailWriter.WriteHeader()")
		csvLine = ''
		for field in statRow.dataFields():
			csvLine += self._csvText(field.headerText(), field.dataType(), True)
		
		self.Write(csvLine)

	def Write(self,text):													# Write text to Detail CSV
		barfd("DetailWriter.Write({})".format(text))
		fhDetailCSV.write(text + '\n')

	def WriteRow(self,statRow):												# Write Google Sheet row to Detail CSV
		detailCsvOpen(statRow)
		csvLine = ''
		for field in statRow.dataFields():
			csvLine += csvText(field.value(), field.dataType(), True)		# TODO: type conversion problem possibilities? be careful mapping fields

		detailCsvWrite(statRow,csvLine)

	def WriteStatusRows(self,statRows)										# Take list of Google Sheet Rows and barf to a CSV
		self.CleanUp()
		for stsRow in statRows:
			self.WriteRow(stsRow)	
		self.Close()

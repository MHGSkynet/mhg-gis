#
# ---------------------------------------------------------------------------------------------
# mhgKmlWriter.py
#
# Description
#
# 	Class for reading and writing Detail info to KML
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
import re
import sys

# MHGLIB includes
import mhgCommandArgs
import mhgCountyStats
import mhgStateStats

class KmlWriter(object):									# KML Writer class

	#
	# Constants (public)
	#
	KDATA_SCHEMA					= '#OGRGeoJSON'						# OGR Schema
	KDATA_STATUS_START				= 'STATUS_START'					# Status Start Date
	KDATA_STATUS_END				= 'STATUS_START'					# Status End Date
	KDATA_STATUS_NDAYS				= 'STATUS_NDAYS'					# Number of days having ovservations
	KDATA_STATUS_OVERALL			= 'STATUS_OVERALL'					# Status code overall
	KDATA_STATUS_MAX				= 'STATUS_MAX'						# Max status code
	KDATA_STATUS_UTILITIES			= 'STATUS_UTILITIES'				# Utilities status code
	KDATA_STATUS_SERVICES			= 'STATUS_SERVICES'					# Services status code
	KDATA_STATUS_CONSUMBALES		= 'STATUS_CONSUMABLES'				# Consumables status code
	KDATA_2M_CHECKINS				= 'CHECKINS_2M'						# Number of 2M check-ins recorded by net control
	KDATA_2M_PARTICIPATE			= 'PARTICIPATE_2M'					# Number of 2M nets checked in to
	KDATA_HF_CHECKINS				= 'CHECKINS_HF'						# Number of HF check-ins recorded by net control
	KDATA_HF_PARTICIPATE			= 'PARTICIPATE_HF'					# Number of HF nets checked in to

	KSTYLE_IMPACT_UNKNOWN			= '#impactUnknown'					# KML rendering style for Unknown status
	KSTYLE_IMPACT_NONE				= '#impactNormal'					# KML rendering style for Normal status
	KSTYLE_IMPACT_MODERATE			= '#impactModerate'					# KML rendering style for Moderate Impact status
	KSTYLE_IMPACT_SEVERE			= '#impactSevere'					# KML rendering style for Severe Impact status
	KSTYLE_IMPACT_ZOMBIES			= '#impactZombies'					# KML rendering style for Zombie Outbreak status

	#
	# Constants (private)
	# 
	_IMPACT_STYLE_MAP			= { IMPACT_CODE_AVAILABLE: 		KSTYLE_IMPACT_NONE,							# Map of Impact Codes to KML Styles
									IMPACT_CODE_MODERATE:		KSTYLE_IMPACT_MODERATE,
									IMPACT_CODE_SEVERE:			KSTYLE_IMPACT_SEVERE,
									IMPACT_CODE_UNKNOWN:		KSTYLE_IMPACT_UNKNOWN,
									IMPACT_CODE_ZOMBIES:		KSTYLE_IMPACT_ZOMBIES }

	_STATE_SCHEMA_DATA_MAP		= { KDATA_STATUS_DATE: 			CountyStats.STAT_STATUS_END_DATE,			# Map of STAT_ items to KML Schema Data Items
									KDATA_STATUS_NDAYS: 		CountyStats.STAT_STATUS_NDAYS,
									KDATA_STATUS_OVERALL: 		CountyStats.STAT_OVERALL_IMPACT_CODE,
									KDATA_STATUS_MAX: 			CountyStats.STAT_MAX_IMPACT_CODE,
									KDATA_STATUS_UTILITIES:		CountyStats.STAT_UTILITIES_IMPACT_CODE,
									KDATA_STATUS_SERVICES:		CountyStats.STAT_SERVICES_IMPACT_CODE,
									KDATA_STATUS_CONSUMBALES:	CountyStats.STAT_CONSUMABLES_IMPACT_CODE,
									KDATA_2M_CHECKINS:			CountyStats.STAT_2M_CHECKINS,
									KDATA_2M_PARTICIPATE:		CountyStats.STAT_2M_PARTICIPATE,
									KDATA_HF_CHECKINS:			CountyStats.STAT_HF_CHECKINS,
									KDATA_HF_PARTICIPATE:		CountyStats.STAT_HF_PARTICIPATE }
	#
	# Properties (private)
	# 
	_kmlLines		= []												# Lines of KML
	_fhStatusKml	= None												# file handle for Status KML (output)

	#
	# Constructor
	#
    def __init__(self):													# KmlWriter Constructor
		_kmlLines		= []											# 	initialize KML buffer
		_fhStatusKml	= None											#	initialize file handle for Status KML (output)

	#
	# Methods (private)
	#

	# Merge Data
	def _MergeData(stateData):								# Merge State County data into buffered KML template, then barf to file(s)
		mergeKmlSuccess = True

		# Walk KML looking for placemarks, and set data values as appropriate from stats hash
		# Typical county placemark...
		#	<Placemark>
		#		<name>Alcona</name>
		#		<styleUrl>#countyDefault</styleUrl>												#TODO: update style based on STATUS_OVERALL
		#		<ExtendedData>
		#			<SchemaData schemaUrl="#MHGCoronaData">
		#				<SimpleData name="STATUS_OVERALL">U</SimpleData>
		#				<SimpleData name="STATUS_MAX">U</SimpleData>
		#				<SimpleData name="STATUS_UTILITIES">U</SimpleData>
		#				<SimpleData name="STATUS_SERVICES">U</SimpleData>
		#				<SimpleData name="STATUS_CONSUMABLES">U</SimpleData>
		#			</SchemaData>
		#		</ExtendedData>

		barfd("KmlWriter._MergeData().Enter")
		barfi("KML Generating...")

		with open(AppSettings.glob().kmlStatusTemplateSpec()) as fhTemplate:

			self._kmlLines = fhTemplate.readlines()
			barfd("KmlWriter._MergeData.readlines({} read)".format(len(self._kmlLines)))

			# TODO: Test for nothing loaded, then fail
			
			kmlCounty				= None
			
			# Define regex patterns to drive walking KML.      TODO: update to use legit KML or XML parser.   NOTE: Python regex ease of use sux compared to PERL. :P
			placemarkPattern 		= re.compile('^[\t ]*<Placemark>[\t ]*$')
			placemarkEndPattern		= re.compile('^[\t ]*</Placemark>[\t ]*$')
			countyNamePattern 		= re.compile('^[\t ]*<name>([A-Za-z]+)</name>[\t ]*$')
			stylePattern	 		= re.compile('(^[\t ]*<styleUrl>)([^<]+)(</styleUrl>[\t ]*)$')
			schemaDataStartPattern 	= re.compile('^[\t ]*<SchemaData schemaUrl="' + self.KDATA_SCHEMA + '">[\t ]*$')
			schemaDataItemPattern	= re.compile('^[\t ]*<SimpleData name="([A-Za-z_]+)">([^<]*)</SimpleData>[\t ]*$')
			schemaDataUpdatePattern	= re.compile('^([\t ]*<SimpleData name="[A-Za-z_]+">)([^<]*)(</SimpleData>[\t ]*)$')
			schemaDataEndPattern 	= re.compile('^[\t ]*</SchemaData>[\t ]*$')

			statsKey = None
			lookFor  = 'placemark'
			for kmlLineIndex in range(0,len(self._kmlLines)-1):
				self._kmlLines[kmlLineIndex] = self._kmlLines[kmlLineIndex].replace(chr(10),'')
				self._kmlLines[kmlLineIndex] = self._kmlLines[kmlLineIndex].replace(chr(13),'')
				kmlLine = self._kmlLines[kmlLineIndex]
				lookForLast = lookFor
				if lookFor == 'placemark' and placemarkPattern.match(kmlLine):  lookFor = 'county'
				if lookFor == 'county' and kmlCountyPattern.match(kmlLine):
					kmlCounty  = kmlCountyPattern.match(kmlLine).group(1)
					statsCounty  = kmlCounty
					barfd("KmlWriter._MergeData.MergeKmlData.evalCounty({})".format(kmlCounty))
					lookFor = 'style'
					#if not kmlCounty in covidStats: lookFor = 'placemark'
					if not kmlCounty in stateData.countyList(): 						# If we don't have stats for this county, use default values
						statsCounty = CountyStats.COUNTY_DEFAULT

				if lookFor == 'style' and stylePattern.match(kmlLine):
					styleMatch = stylePattern.match(kmlLine)
					newStyle = self._IMPACT_STYLE_MAP[stateData.CountyData(statsCounty).overallCode()]
					self._kmlLines[kmlLineIndex] = styleMatch.group(1) + newStyle + styleMatch.group(3)
					lookFor = 'schemaStart'

				if lookFor == 'schemaStart' and schemaDataStartPattern.match(kmlLine): lookFor = 'schemaData'
				if lookFor == 'schemaData'  and schemaDataItemPattern.match(kmlLine):
					if kmlCounty == 'Kent': barfd("KmlWriter._MergeData.EvaluatingData(kmlLine={})".format(kmlLine))
					schemaDataItemMatch = schemaDataItemPattern.match(kmlLine)
					schemaItemName	= schemaDataItemMatch.group(1)
					schemaItemValue	= schemaDataItemMatch.group(2)
					if schemaItemName in self._STATE_SCHEMA_DATA_MAP:
						statName = self._STATE_SCHEMA_DATA_MAP[schemaItemName]
						if kmlCounty == 'Kent': barfd("KmlWriter._MergeData.Updating kmlLine={}".format(kmlLine))
						schemaDataUpdateMatch = schemaDataUpdatePattern.match(kmlLine)
						newKmlValue = str(stateData.CountyData(statsCounty).FieldFromId(statName).Value())
						self._kmlLines[kmlLineIndex] = schemaDataUpdateMatch.group(1) + newKmlValue + schemaDataUpdateMatch.group(3)
						if kmlCounty == 'Kent': barfd("KmlWriter._MergeData.Updated kmlLine={}".format(self._kmlLines[kmlLineIndex]))

				if (lookFor == 'schemaData' or lookFor == lookForLast) and schemaDataEndPattern.match(kmlLine): lookFor = 'placemark'

		barfi("KML Data Merge complete.")
		barfd("KmlWriter._MergeData().Exit")

		return mergeKmlSuccess

	#
	# Methods (public)
	#

	# Status Kml (output)
	def Open(self,kmlSpec):												# Open KML for output
		success = False
		if self._fhStatusKml is None:
			barfd("KmlWriter.Open({})".format(kmlSpec))
			self._fhStatusKml = open(kmlSpec, 'w')
			success = True

		return success

	def Close(self):													# Close KML output file
		barfd("KmlWriter.Close()")
		self._fhStatusKml.close()
		self._fhStatusKml = None
		return True

	def Write(self,text):												# Write text to KML file
		self._fhStatusKml.write(text + '\n')
		return True

	def DumpKml(self,kmlSpec):											# Dump KML buffer to file
		barfd("KmlWriter.DumpKml.Enter({})".format(kmlSpec))
		self.Open(kmlSpec)
		for kmlLine in self._kmlLines:
			self.Write(kmlLine)

		self.Close()
		barfd("KmlWriter.DumpKml.Exit()")
		return True

	def WriteStateCountyStats(self,stateData):							# Merge State County data into buffered KML template, then barf to file(s)

		self._MergeData(stateData)										# Read template kml into buffer, and merge state data
		self.DumpKml( AppSettings.glob().statusKmlSpec() )				# Write to Daily Status file

		return True

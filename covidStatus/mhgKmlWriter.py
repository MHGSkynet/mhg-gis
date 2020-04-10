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
# 2020.04.07	01.03		SquintMHG		New Module
# ---------------------------------------------------------------------------------------------

import sys
import mhgCommandArgs
import csvWriter

class KmlWriter(object):									# KML Writer fa

    def __init__(self):

		pass


# KML Constants
KDATA_SCHEMA					= '#OGRGeoJSON'
KDATA_STATUS_DATE				= 'STATUS_DATE'
KDATA_STATUS_NDAYS				= 'STATUS_NDAYS'
KDATA_STATUS_OVERALL			= 'STATUS_OVERALL'
KDATA_STATUS_MAX				= 'STATUS_MAX'
KDATA_STATUS_UTILITIES			= 'STATUS_UTILITIES'
KDATA_STATUS_SERVICES			= 'STATUS_SERVICES'
KDATA_STATUS_CONSUMBALES		= 'STATUS_CONSUMABLES'
KDATA_2M_CHECKINS				= 'CHECKINS_2M'
KDATA_2M_PARTICIPATE			= 'PARTICIPATE_2M'
KDATA_HF_CHECKINS				= 'CHECKINS_HF'
KDATA_HF_PARTICIPATE			= 'PARTICIPATE_HF'

KSTYLE_IMPACT_UNKNOWN			= '#impactUnknown'
KSTYLE_IMPACT_NONE				= '#impactNormal'
KSTYLE_IMPACT_MODERATE			= '#impactModerate'
KSTYLE_IMPACT_SEVERE			= '#impactSevere'
KSTYLE_IMPACT_ZOMBIES			= '#impactZombies'


impactCodeStyleMap				= { IMPACT_CODE_AVAILABLE: 	KSTYLE_IMPACT_NONE,
									IMPACT_CODE_MODERATE:	KSTYLE_IMPACT_MODERATE,
									IMPACT_CODE_SEVERE:		KSTYLE_IMPACT_SEVERE,
									IMPACT_CODE_UNKNOWN:	KSTYLE_IMPACT_UNKNOWN }
#									IMPACT_CODE_ZOMBIES:	KSTYLE_IMPACT_ZOMBIES }

# Kml Data
kmlLines	= []

# Map of STAT_ items to KML Schema Data Items
statsSchemaDataMap			= { KDATA_STATUS_DATE: 			STAT_STATUS_END_DATE,
								KDATA_STATUS_NDAYS: 		STAT_STATUS_NDAYS,
								KDATA_STATUS_OVERALL: 		STAT_OVERALL_IMPACT_CODE,
								KDATA_STATUS_MAX: 			STAT_MAX_IMPACT_CODE,
								KDATA_STATUS_UTILITIES:		STAT_UTILITIES_IMPACT_CODE,
								KDATA_STATUS_SERVICES:		STAT_SERVICES_IMPACT_CODE,
								KDATA_STATUS_CONSUMBALES:	STAT_CONSUMABLES_IMPACT_CODE,
								KDATA_2M_CHECKINS:			STAT_2M_CHECKINS,
								KDATA_2M_PARTICIPATE:		STAT_2M_PARTICIPATE,
								KDATA_HF_CHECKINS:			STAT_HF_CHECKINS,
								KDATA_HF_PARTICIPATE:		STAT_HF_PARTICIPATE }


#
# Status Kml (output)
#
def statusKmlOpen(kmlSpec):																# Open Status KML for output
	global fhStatusKml
	if fhStatusKml is None:
		summmaryCsvSpec = summaryCsvTemplate.replace(TEMPLATE_DATE_TOKEN,_appOptions.endDate())
		barfd("statusKmlOpen({})".format(kmlSpec))
		fhStatusKml = open(kmlSpec, 'w')

def statusKmlClose():																	# Close Status KML
	global fhStatusKml
	barfd("statusKmlClose")
	fhStatusKml.close()
	fhStatusKml = None

def statusKmlWrite(text):																# Write text to Status KML
	fhStatusKml.write(text + '\n')

def statusKmlCreate(kmlLines,kmlSpec):													# Dump kml lines list to Status KML
	barfd("statusKmlCreate.Enter({})".format(kmlSpec))
	statusKmlOpen(kmlSpec)

	for kmlLine in kmlLines:
		statusKmlWrite(kmlLine)

	statusKmlClose()


"""
##########################################
		KML DATA MERGE
##########################################
"""

def mergeKmlData():
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

	barfd("mergeKmlData.enter")
	barf("KML Generating...")
	with open(statusTemplateSpec) as fhStatusTemplate:

		kmlLines = fhStatusTemplate.readlines()
		barfd("mergeKmlData.readlines({} read)".format(len(kmlLines)))
		
		errorText 				= ''
		countyName				= None
		
		placemarkPattern 		= re.compile('^[\t ]*<Placemark>[\t ]*$')
		placemarkEndPattern		= re.compile('^[\t ]*</Placemark>[\t ]*$')
		countyNamePattern 		= re.compile('^[\t ]*<name>([A-Za-z]+)</name>[\t ]*$')
		stylePattern	 		= re.compile('(^[\t ]*<styleUrl>)([^<]+)(</styleUrl>[\t ]*)$')
		schemaDataStartPattern 	= re.compile('^[\t ]*<SchemaData schemaUrl="' + KDATA_SCHEMA + '">[\t ]*$')
		schemaDataItemPattern	= re.compile('^[\t ]*<SimpleData name="([A-Za-z_]+)">([^<]*)</SimpleData>[\t ]*$')
		schemaDataUpdatePattern	= re.compile('^([\t ]*<SimpleData name="[A-Za-z_]+">)([^<]*)(</SimpleData>[\t ]*)$')
		schemaDataEndPattern 	= re.compile('^[\t ]*</SchemaData>[\t ]*$')

		statsKey = None
		lookFor  = 'placemark'
		for kmlLineIndex in range(0,len(kmlLines)-1):
			kmlLines[kmlLineIndex] = kmlLines[kmlLineIndex].replace(chr(10),'')
			kmlLines[kmlLineIndex] = kmlLines[kmlLineIndex].replace(chr(13),'')
			kmlLine = kmlLines[kmlLineIndex]
			lookForLast = lookFor
			if lookFor == 'placemark' and placemarkPattern.match(kmlLine):  lookFor = 'county'
			if lookFor == 'county' and countyNamePattern.match(kmlLine):
				countyName = countyNamePattern.match(kmlLine).group(1)
				statsKey   = countyName
				barfd("DmergeKmlData.evalCounty({})".format(countyName))
				lookFor = 'style'
				#if not countyName in covidStats: lookFor = 'placemark'
				if not countyName in covidStats: statsKey = COUNTY_DEFAULT				# If we don't have stats, use default values
				
			if lookFor == 'style' and stylePattern.match(kmlLine):
				styleMatch = stylePattern.match(kmlLine)
				newStyle = impactCodeStyleMap[covidStats[statsKey][STAT_OVERALL_IMPACT_CODE]]
				kmlLines[kmlLineIndex] = styleMatch.group(1) + newStyle + styleMatch.group(3)
				lookFor = 'schemaStart'

			if lookFor == 'schemaStart' and schemaDataStartPattern.match(kmlLine): lookFor = 'schemaData'
			if lookFor == 'schemaData'  and schemaDataItemPattern.match(kmlLine):
				if countyName == 'Kent': barfd("Evaluating DataItem kmlLine={}".format(kmlLine))
				schemaDataItemMatch = schemaDataItemPattern.match(kmlLine)
				schemaItemName	= schemaDataItemMatch.group(1)
				schemaItemValue	= schemaDataItemMatch.group(2)
				if schemaItemName in statsSchemaDataMap:
					statName = statsSchemaDataMap[schemaItemName]
					if countyName == 'Kent': barfd("Updating kmlLine={}".format(kmlLine))
					schemaDataUpdateMatch = schemaDataUpdatePattern.match(kmlLine)
					kmlLines[kmlLineIndex] = schemaDataUpdateMatch.group(1) + str(covidStats[statsKey][statName]) + schemaDataUpdateMatch.group(3)
					if countyName == 'Kent': barfd("Updated kmlLine={}".format(kmlLines[kmlLineIndex]))

			if (lookFor == 'schemaData' or lookFor == lookForLast) and schemaDataEndPattern.match(kmlLine): lookFor = 'placemark'

		statusKmlDailySpec = statusKmlDailyTemplate.replace(TEMPLATE_DATE_TOKEN,_appOptions.endDate())
		statusKmlCreate(kmlLines,statusKmlDailySpec)
		statusKmlCreate(kmlLines,statusKmlCurrentSpec)

	barf("KML Generation complete. File={}".format(statusKmlDailySpec))
	barfd("mergeKmlData.exit")
	return mergeKmlData

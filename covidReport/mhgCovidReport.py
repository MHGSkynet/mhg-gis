#
# ---------------------------------------------------------------------------------------------
# mhgCovidReport.py
#
# Description
#
# 	Render mhgCovidStatus.kml to a pdf, jpg, and/or QGIS project
#
# Copyright
#
#	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#						non profit conservative organizations and individuals to use in support
#						of American freedom and the constitution. All other rights are reserved,
#						and any other use prohibited.
#
# Date			Version		Author			Description
# 2020.04.07	01.03		SquintMHG		Command args, refactor for classes
# 2020.04.04	01.02		SquintMHG		Change to use STATUS_MAX for county labelling, rather than STATUS_OVERALL
# 2020.03.23	01.00		SquintMHG		Initial version
# ---------------------------------------------------------------------------------------------

import os
import os.path
import re
import sys
from pathlib 	import Path
from datetime	import datetime

from qgis.core 	import *
from qgis.core 	import QgsVectorLayer
from qgis.core 	import QgsAbstractVectorLayerLabeling
from qgis.core 	import QgsCategorizedSymbolRenderer
from qgis.core 	import QgsLayerTree
from qgis.core 	import QgsLayoutExporter
from qgis.core 	import QgsLayoutItem
from qgis.core 	import QgsLayoutItemLabel
from qgis.core 	import QgsLayoutItemLegend
from qgis.core 	import QgsLayoutItemMap
from qgis.core 	import QgsLayoutItemPage
from qgis.core 	import QgsLayoutItemPicture
from qgis.core 	import QgsLayoutPoint
from qgis.core 	import QgsLayoutSize
from qgis.core 	import QgsProject
from qgis.core 	import QgsPalLayerSettings
from qgis.core 	import QgsPrintLayout
from qgis.core 	import QgsPropertyDefinition
from qgis.core 	import QgsRectangle
from qgis.core 	import QgsRendererCategory
from qgis.core 	import QgsSimpleFillSymbolLayer
from qgis.core 	import QgsSymbol
from qgis.core 	import QgsTextBackgroundSettings
from qgis.core 	import QgsTextFormat
from qgis.core 	import QgsUnitTypes
from qgis.core 	import QgsVectorLayerSimpleLabeling
from qgis.gui  	import QgsLayerTreeMapCanvasBridge
from qgis.utils   import iface
from PyQt5.QtCore import QRectF
from PyQt5.QtGui  import QColor
from PyQt5.QtGui  import QFont
from PyQt5.QtGui  import QPageSize
#from pudb 		import set_trace; set_trace()
"""
##########################################
		INITIALIZATION
##########################################
"""

PROGNM				= "mhgCovidStatus"											# program name
ERR_NONE			= 0
ERR_BADENV			= 1
ERR_BADFILTER		= 2
ERR_FETCHFAIL		= 3
ERR_BADRENDER		= 4

print("####\n#### {} start\n####".format(PROGNM))

currDate			= datetime.now() 											# current date and time
currDateYmd 		= currDate.strftime("%Y.%m.%d")								# current date YYYY.MM.DD format

#
# Exit handler
#
def appExit(statusCode,errorText=''):
	statusText = ''
	if errorText != '': print(errorText)
	if statusCode != 0: statusText = " Status={}".format(statusCode)
	print("####\n#### {} complete.{}\n####".format(PROGNM,statusText))
	sys.exit(statusCode)

#
# Debug
#
def barfd(text):
	if DEBUG_ON:	print(text)

#
# Package Info
#
def getPackageRoot():															# Get package root folder
	global app_exit_code
	packageRoot = os.environ.get(ENV_PACKAGE_FOLDER)							# See if root folder is defined
	errorText 	= ''
	errorText2 	= ''
	if packageRoot is None:
		packageRoot = "./"
		errorText2 = "ERROR: {} environment var is not defined and current folder is not package root folder.".format(ENV_PACKAGE_FOLDER)
	else:
		packageRoot = packageRoot.replace("\\","/")
		packagePath = Path(packageRoot)
		if not packagePath.is_dir():
			errorText = "ERROR: {} environment var is not a valid folder".format(ENV_PACKAGE_FOLDER)
		else:
			errorText2 = "ERROR: {} environment var does not point to package root".format(ENV_PACKAGE_FOLDER)
	
	if packageRoot[-1:] != '/':		packageRoot = packageRoot + '/'

	if errorText == '':
		for packageFolder in ROOT_KEY_FOLDERS:
			keyFolderSpec = packageRoot + packageFolder
			keyFolderPath = Path(keyFolderSpec)
#			print("DEBUG: testing install folder keyFolderSpec={}".format(keyFolderSpec))
			if not keyFolderPath.is_dir():
				errorText = "ERROR: Folder {} not found in package root. Invalid installation.".format(packageFolder)
				break

	if errorText != '':
		print(errorText)
		appExit(1,errorText2)

	barfd("PACKAGE FOLDER={}".format(packageRoot))

	return packageRoot

def testDatePattern(regex,parseString,strptimeFormat,strptimeString=''):				# Test a date string for pattern match, and parse to timestamp on match
	if strptimeString == '': strptimeString = parseString
	dateTS = None																		
	pattern = re.compile(regex)
	if pattern.match(parseString):
		dateTS = datetime.strptime(strptimeString, strptimeFormat)
		
	return dateTS

XMIT_START_DATE		= 'StartDate'
XMIT_END_DATE		= 'EndDate'

#
# Get parameter from file
#
def getXmitParam(paramName):
	retval = None
	with open(reportInfoXmitSpec) as fhXmit:
		xmitLines = fhXmit.readlines()
		for xmitLine in xmitLines:
			if xmitLine.split("=")[0].strip() == paramName:
				barfd("DEBUG: getXmitParam(param={},val={})".format(paramName,xmitLine.split("=")[1]).replace("\n","").strip())
				retval = xmitLine.split("=")[1].replace("\n","").strip()
				break

	barfd("DEBUG: getXmitParamExit(param={},val={})".format(paramName,retval))
				
	return retval

#
# Get parameters
#
def getParam(paramName):
	paramVal = ''
	if paramName == ENV_FILTER_DATE:
		filterTS = datetime.now()
		dateSrc = "Environment Var"
		filterDate = os.environ.get(ENV_FILTER_DATE)
		if filterDate is None:
			if not sys.argv[1] is None and sys.argv[1] != "":
				filterDate = ""
				if sys.argv[1] == "XMIT":
					dateSrc = "Xmit File"
					filterDate = getXmitParam(XMIT_END_DATE)
				else:
					dateSrc = "Command Line"
					filterDate=sys.argv[1]

		barfd("DEBUG: getParam(ENV_FILTER_DATE source={},value={})".format(dateSrc,filterDate))
					
		dateTS	= testDatePattern('^[0-9]{4}[.][0-9]+[.][0-9]+$', filterDate, '%Y.%m.%d')		#	yyyy.mm.dd
		if dateTS is None:
			appExit(ERR_BADFILTER,"ERROR: Parameter {} value ({}) is not yyyy.mm.dd format from {}".format(ENV_FILTER_DATE,filterDate,dateSrc))
		else:
			filterTS = datetime.strptime(filterDate,"%Y.%m.%d")
			paramVal = filterTS
		
	return paramVal
	
#
# QGIS Package Root
#
def getQgisRoot():																# Get QGIS package root from environment variable
	rootFolder = os.environ.get(ENV_QGIS_ROOT)
	if rootFolder is None: appExit(1,"ERROR: required environment variable {} is not set".format(ENV_QGIS_ROOT))
	rootPath = Path(rootFolder)
	if not rootPath.is_dir(): appExit(2,errorText = "ERROR: Folder {} does not exist. Fix {} environment variable.".format(packageFolder,ENV_QGIS_ROOT))
	barfd("QGIS FOLDER={}".format(rootFolder))
	return rootFolder

"""
##########################################
		CONSTANTS
##########################################
"""
# Colors
COLOR_WHITE			= '#ffffff'													# White
COLOR_GREY			= '#c8c8c8'													# Grey
COLOR_BLACK			= '#000000'													# Black
COLOR_GREEN			= '#13e904'													# Green
COLOR_YELLOW		= '#e6f014'													# Yellow
COLOR_RED			= '#ff0014'													# Red

# Font info hash keys
FONT_NAME			= 'font'
FONT_SIZE			= 'size'
FONT_COLOR			= 'color'
FONT_COLORNAME		= 'colorname'

"""
##########################################
		DRIVING DATA
##########################################
"""
HEADLESS			= True														# Run HEADLESS
USE_GUI				= not HEADLESS												# Run with GUI
GENERATE_PROJECT	= True														# Whether to output a QGIS project as output
GENERATE_PDF		= True														# Whether to output a PDF of the status
GENERATE_IMAGE		= True														# Whether to output a JPG of the status
DEBUG_ON			= True														# Debug enable

# Environment 
ENV_QGIS_ROOT		= "MHGGIS_QGIS_ROOT"										# QGIS package root folder environment var
ENV_PACKAGE_FOLDER	= 'MHGGIS_ROOT'												# MHGGIS Package root folder environment var
ENV_FILTER_DATE		= 'MHGGIS_FILTER_DATE'										# Report Date

# Folders
ROOT_KEY_FOLDERS	= [ 'covidReport', 'data', 'kml', 'output', 'images' ] 		# MHGGIS Package folders for verification of install
PACKAGE_ROOT		= getPackageRoot()											# MHGGIS Package root folder for mgh-gis suite
qgisRoot 			= getQgisRoot()												# QGIS Package root
qgisBinFolder		= qgisRoot + "/apps/qgis-ltr"								# QGIS App install point
qgisPythonFolder 	= qgisBinFolder + "/python/plugins"							# QGIS Python plugins folder

codeFolder			= PACKAGE_ROOT + "qgis"										# Folder for code
kmlFolder			= PACKAGE_ROOT + "kml"										# Folder for template kml
dataFolder			= PACKAGE_ROOT + "data"										# Folder for data
outputFolder		= PACKAGE_ROOT + "output"									# Folder for output 
imagesFolder		= PACKAGE_ROOT + "images"									# Folder containing images as input

# Input resources
inputKml			= dataFolder + "/mhgCovidStatus.kml"						# KML generated by mhgCovidFetch with data set for given day
reportInfoXmitSpec	= dataFolder + "/mhgCovidReportXmit.ini"					# File to transmit report date to mhgCovidReport app.
KDATA_KEYFIELD		= 'STATUS_MAX'												# Schema field to drive labeling (county coloring)
MHGLogo				= imagesFolder + "/MHG-yellow.jpg"							# MHG Logo

# Date Filter
filterDateTS		= getParam(ENV_FILTER_DATE)									# Date report is being run for
filterDateYmd		= filterDateTS.strftime("%Y.%m.%d")							# Date report is being run for

# Output files
statusProject		= outputFolder + "/mhgCovidStatus-" + filterDateYmd + ".qgz"	# Output QGIS project file specification
statusPdf			= outputFolder + "/mhgCovidStatus-" + filterDateYmd + ".pdf"	# Output PDF file specification
statusImage			= outputFolder + "/mhgCovidStatus-" + filterDateYmd + ".jpg"	# Output JPG file specification
#statusKml			= outputFolder + "/mhgCovidStatus-" + filterDateYmd + ".kml"	# Output KML file specification

# Report Control
reportTitle			= 'MICHIGAN COVID IMPACT STATUS'								# Report Title
layerTitle			= "Status"														# Layer Title
reportDateFormat	= "%A, %B %d, %Y"												# Report Date format (Friday, July 04, 2020)
reportTitleFont		= { FONT_NAME: "MS Shell Dlg 2", FONT_SIZE: 16}					# Report Date Font
reportDateFont		= { FONT_NAME: "MS Shell Dlg 2", FONT_SIZE: 14}					# Report Date Font
legendTitleFont		= { FONT_NAME: "MS Shell Dlg 2", FONT_SIZE: 12}					# Legend Title Font
legendSymbolFont	= { FONT_NAME: "MS Shell Dlg 2", FONT_SIZE: 8}					# Legend Symbols Font
legendLabelFont		= { FONT_NAME: "MS Shell Dlg 2", FONT_SIZE: 8}					# Legend Labels Font
labelingFont		= { FONT_NAME: "Arial", FONT_SIZE: 6, FONT_COLORNAME: 'black'}	# Labeling Font (Counties)

"""
##########################################
		FUNCTIONS
##########################################
"""

#
# Category List - Add a Symbol
#
def addSymbolCategory(impactCode,impactDesc,symbolColor,categoryList):
	symbol = QgsSymbol.defaultSymbol(statusLayer.geometryType())				# create a symbol object
	layer_style = {}															# set the symbol's style
	layer_style['color']   = symbolColor										#   color
	layer_style['outline'] = '#000000'											#   outline (black)
	symbol_layer = QgsSimpleFillSymbolLayer.create(layer_style)
	if symbol_layer is not None:
		symbol.changeSymbolLayer(0, symbol_layer)								# replace default symbol layer with the configured one

	category = QgsRendererCategory(impactCode, symbol, impactDesc)				# create renderer object
	categoryList.append(category)												# add category to list


"""
##########################################
		MAIN
##########################################
"""

#
# Initialize QGIS
#
sys.path.append(qgisPythonFolder)												# Add QGIS Pytho plugins to search path
QgsApplication.setPrefixPath(qgisBinFolder, True)								# Define QGIS Install point
qgs = QgsApplication([], USE_GUI)												# Create a QGIS Application instance, HEADLESS or with GUI
qgs.initQgis()																	# Load QGIS providers
import processing
from processing.core.Processing import Processing
Processing.initialize()															# Start processing

#
# Create Project
#
barfd("DEBUG Create project")
project = QgsProject.instance()
if USE_GUI:
	bridge = QgsLayerTreeMapCanvasBridge( project.layerTreeRoot(), iface.mapCanvas())

#
# Load Status KML as a vector layer and display
#
if USE_GUI:
	statusLayer = iface.addVectorLayer(inputKml, layerTitle, "ogr")
else:
	barfd("DEBUG Create vector layer(file={})".format(inputKml))
	statusLayer = QgsVectorLayer(inputKml, layerTitle, "ogr")
	barfd("DEBUG Add vector layer to project")
	project.addMapLayer(statusLayer)

if not statusLayer.isValid():
	print("ERROR: KML layer failed to load!")
	sys.exit(1)
	

statusLayer.setName(layerTitle)

#
# Set to simple labeling, Arial 8pt, black
#
barfd("DEBUG Set Labeling")
label_settings = QgsPalLayerSettings()
label_settings.fieldName = 'name'
text_format = QgsTextFormat()
text_format.setColor(QColor(labelingFont[FONT_COLORNAME]))
text_format.setFont(QFont(labelingFont[FONT_NAME], labelingFont[FONT_SIZE]))
text_format.setSizeUnit(QgsUnitTypes.RenderPoints)
text_format.setSize(labelingFont[FONT_SIZE])
label_settings.setFormat(text_format)
statusLayer.setLabeling(QgsVectorLayerSimpleLabeling(label_settings))
statusLayer.setLabelsEnabled(True)

#
# Define Status Categories and set up Symbol Rendering
#
barfd("DEBUG Define Status Categories")
fni = statusLayer.fields().indexFromName(KDATA_KEYFIELD)
barfd("DEBUG Define Status Categories for KEYFIELD={},index={}".format(KDATA_KEYFIELD,fni))

if DEBUG_ON:
	print("##### FIELDS begin #####")
	fields = statusLayer.fields()
	print(fields.names())
	print("##### FIELDS end #####")

categories = []
addSymbolCategory('A', 'All Available',   COLOR_GREEN,  categories)
addSymbolCategory('M', 'Moderate Impact', COLOR_YELLOW, categories)
addSymbolCategory('S', 'Severe Impact',   COLOR_RED,    categories)
addSymbolCategory('', 'Unknown Impact',   COLOR_GREY,   categories)					# Handle U as well as any other code
#addSymbolCategory('Z', 'Zombies Oubreak', COLOR_BLACK,   categories)

barfd("DEBUG Create Symbol Renderer")
# create renderer object
statusRenderer = QgsCategorizedSymbolRenderer(KDATA_KEYFIELD, categories)
if statusRenderer is None:															# assign the created renderer to the layer
	appExit(ERR_BADRENDER,"ERROR: Can't create Category Symbol Renderer")
else:
	statusLayer.setRenderer(statusRenderer)

barfd("DEBUG Repaint")
statusLayer.triggerRepaint()

#
# Status Print Layout 
#
barfd("DEBUG Set up print layout")
statusLayoutName = "MGHStatus"
statusPrintLayout = QgsPrintLayout(project)
statusPrintLayout.initializeDefaults()
statusPrintLayout.setName(statusLayoutName)
statusPrintLayout.setUnits(QgsUnitTypes.LayoutMillimeters)
project.layoutManager().addLayout(statusPrintLayout)

barfd("DEBUG print layout add page")
pages = statusPrintLayout.pageCollection()
pages.beginPageSizeChange()
page = pages.page(0)
page.setPageSize('A4',  QgsLayoutItemPage.Landscape)
pages.endPageSizeChange()

page_center = page.pageSize().width() / 2

barfd("DEBUG print layout add map to page")									
extent = QgsRectangle(-91.000, 41.101, -80.550, 48.928)						# Michigan Extent: -90.4182894376677524,41.6961255762931202 : -82.4134779482332078,48.2626923653278865
map = QgsLayoutItemMap(statusPrintLayout)
map.setRect(QRectF(-91.000, 41.101, -80.550, 48.928))
map.setExtent(extent)
a4 = QPageSize().size(QPageSize.A4, QPageSize.Millimeter)
map.attemptResize(QgsLayoutSize(a4.height(),  a4.width()))
statusPrintLayout.addItem(map)

# Logo
barfd("DEBUG Print layout add logo 1")
logoPicture = QgsLayoutItemPicture(statusPrintLayout)
barfd("DEBUG Print layout add logo 2")
logoPicture.setPicturePath(MHGLogo)
barfd("DEBUG Print layout add logo 3")
logoPicture.setLinkedMap(map)
logoPicture.attemptResize(QgsLayoutSize(88.009, 85.375, QgsUnitTypes.LayoutMillimeters))
logoPicture.attemptMove(QgsLayoutPoint(21.537, 106.912, QgsUnitTypes.LayoutMillimeters))
statusPrintLayout.addItem(logoPicture)

# Date
barfd("DEBUG Print layout add date 01")
textDate = filterDateTS.strftime(reportDateFormat)
statusDateLabel = QgsLayoutItemLabel(statusPrintLayout)
barfd("DEBUG Print layout add date 02")
statusDateLabel.setText(textDate)
statusDateLabel.setFont(QFont(reportDateFont[FONT_NAME], reportDateFont[FONT_SIZE], QFont.Bold))
statusDateLabel.adjustSizeToText()
statusDateSize = statusDateLabel.sizeWithUnits()
statusDateLabelX = page.pageSize().width() - statusDateSize.width() - 4
statusDateLabel.attemptMove(QgsLayoutPoint(statusDateLabelX, 10))
statusPrintLayout.addItem(statusDateLabel)

# Title
barfd("DEBUG Print layout add title")
titleLabel = QgsLayoutItemLabel(statusPrintLayout)
titleLabel.setText(reportTitle)
titleLabel.setFont(QFont(reportTitleFont[FONT_NAME], reportTitleFont[FONT_SIZE], QFont.Bold))
titleLabel.adjustSizeToText()
titleLabel.setReferencePoint(QgsLayoutItem.UpperMiddle)
titleLabel.attemptMove(QgsLayoutPoint(page_center, 10))
statusPrintLayout.addItem(titleLabel)

# Legend
barfd("DEBUG Print layout add legend")
legend = QgsLayoutItemLegend(statusPrintLayout)
layerTree = QgsLayerTree()
layerTree.addLayer(statusLayer)
legend.model().setRootGroup(layerTree)
legend.setLinkedMap(map)
#legend.setTitle("Status")
legend.setStyleFont(QgsLegendStyle.Title, QFont(legendTitleFont[FONT_NAME],legendTitleFont[FONT_SIZE]))
legend.setStyleFont(QgsLegendStyle.Symbol, QFont(legendSymbolFont[FONT_NAME],legendSymbolFont[FONT_SIZE]))
legend.setStyleFont(QgsLegendStyle.SymbolLabel, QFont(legendLabelFont[FONT_NAME],legendLabelFont[FONT_SIZE]))
legend.attemptMove(QgsLayoutPoint(256.000, 159.600, QgsUnitTypes.LayoutMillimeters)) 	# 258.603, 168.270, 37.400, 37.700
legend.adjustBoxSize()
statusPrintLayout.addItem(legend)

#
#  Generate Outputs
#

# Barf to PDF
if GENERATE_PDF:
	barfd("DEBUG Write to PDF")
	exporter = QgsLayoutExporter(statusPrintLayout)
	exporter.exportToPdf(statusPdf, QgsLayoutExporter.PdfExportSettings())
	print("Exported to PDF. File=\"{}\"".format(statusPdf))

# Barf to Image
if GENERATE_IMAGE:
	barfd("DEBUG Write to Image")
	exporter = QgsLayoutExporter(statusPrintLayout)
	settings = QgsLayoutExporter.ImageExportSettings()
	settings.dpi      = 300
	exporter.exportToImage(statusImage, settings)
	print("Exported to JPG. File=\"{}\"".format(statusImage))

# Barf to QGIS project
if GENERATE_PROJECT:
	project.write(statusProject)
	print("Generating project complete. QGIS Project=\"{}\"".format(statusProject))

#
# Update canvas
#
if USE_GUI:
	if iface.mapCanvas().isCachingEnabled():
		layerTemplate.triggerRepaint()
	else:
		iface.mapCanvas().refresh()	
#
# Exit
#
if HEADLESS:
	qgs.exitQgis()																# remove provider and layer registries from memory
	
appExit(0)
#
# ---------------------------------------------------------------------------------------------
# mhgGisWriter.py
#
# Description
#
# 	Use QGIS Engine to build QGIS project and render mhgCovidStatus.kml to a PDF and/or JPG
#                _
#         ______,' `._______                   _______
#        (______(   }___,,__) .';-.;',`.;';.`=|_______)
#              .'  ,'  //
#             '    \  //
#            '      `'/
#        ----`-------~-------------------
#   
# Copyright
#
#	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#						non profit conservative organizations and individuals to use in support
#						of American freedom and the constitution. All other rights are reserved,
#						and any other use prohibited.
#
# Date			Version		Author			Description
# 2020.04.10	02.00		SquintMHG		Command args, refactor for OO classes
# 2020.04.04	01.02		SquintMHG		Change to use STATUS_MAX for county labeling, rather than STATUS_OVERALL
# 2020.03.23	01.00		SquintMHG		Initial version
# ---------------------------------------------------------------------------------------------

# Python includes
import os
import os.path
import re
import sys
from pathlib 	import Path
from datetime	import datetime

# QGIS includes
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

import processing
from processing.core.Processing import Processing

# MHGLIB includes
import mhgAppSettings
import mhgColors
import mhgFont
import mhgException


class GisWriter():

	#
	# Constants (private)
	#
	_HEADLESS			= True														# Run HEADLESS
	_USE_GUI			= not HEADLESS												# Run with GUI
	_KDATA_KEYFIELD		= 'STATUS_MAX'												# Schema field to drive labeling (county coloring)

	#
	# Properties (private)
	#
	_reportTitle		= 'MICHIGAN COVID IMPACT STATUS'							# Report Title
	_layerTitle			= "Status"													# Layer Title
	_reportDateFormat1	= "%A, %B %d, %Y"											# Report Date format, single date (Friday, July 04, 2020)
	_reportDateFormat2	= "%m/%d"													# Report Date format, date range  (06/04 to 07/05)
	_reportDateFormatW	= "Week Ending %m/%d/%Y"									# Report Date format, week range  (Week Ending 06/04/2020)
	_reportDateFormatM	= "%B %Y"													# Report Date format, month       (July 2020)
	
	_project			= None														# GIS Project object
	_statusLayer		= None														# Project KML Vector Layer object
	_statusPrintLayout	= None														# Print layout object for rendering

	_reportTitleFont	= None														# Report Title
	_reportDateFont		= None														# Report Date Font
	_legendTitleFont	= None														# Legend Title Font
	_legendSymbolFont	= None														# Legend Symbols Font
	_legendLabelFont	= None														# Legend Labels Font
	_labelingFont		= None														# Labeling Font (Counties)

	#
	# Constructor
	#
	def __init__(self):																# Constructor
		self._InitializeFonts()														#    Initialize fonts
		return self

	#
	# Properties (public)
	#
	def reportDateText(self):														# Generate report date text string.
		textDate = ''
		if 1 == AppSettings.glob().options().nDays():
			textDate = AppSettings.glob().options().endDateTS.strftime(self._reportDateFormat1)
		elif 7 == AppSettings.glob().options().nDays():
			textDate = AppSettings.glob().options().endDateTS.strftime(self._reportDateFormatW)
		elif 1 == AppSettings.glob().options().startDateTS().day and isBetween(AppSettings.glob().options().nDays(),28,31):
			textDate = AppSettings.glob().options().endDateTS.strftime(self._reportDateFormatM)
		else:
			startText = AppSettings.glob().options().startDateTS.strftime(self._reportDateFormat2)
			endText = AppSettings.glob().options().endDateTS.strftime(self._reportDateFormat2)
			textDate = "{} to {}".format(startText,endText)
		return textDate

	#
	# Methods (private)
	#
	def _InitializeFonts(self):														# Initialize Fonts
		self._reportTitleFont	= Font( Font.FONT_MS_SHELL_DLG2, 16 )				#    Report Title
		self._reportDateFont	= Font( Font.FONT_MS_SHELL_DLG2, 14,	\			#    Report Date Font
											Colors.COLOR_BLACK,			\			#
											Font.FONT_STYLE_BOLD )  				#
		self._legendTitleFont	= Font( Font.FONT_MS_SHELL_DLG2, 12 )				#    Legend Title Font
		self._legendSymbolFont	= Font( Font.FONT_MS_SHELL_DLG2, 8 )				#    Legend Symbols Font
		self._legendLabelFont	= Font( Font.FONT_MS_SHELL_DLG2, 8 )				#    Legend Labels Font
		self._labelingFont		= Font( Font.FONT_ARIAL, 6, Colors.COLOR_BLACK )	#    Labeling Font (Counties)
		return True

	def _InitializeQgis(self):														# Initialize QGIS
		sys.path.append(AppSettings.glob().qgisPythonFolder())						#    Add QGIS Pytho plugins to search path
		QgsApplication.setPrefixPath(AppSettings.glob().qgisBinFolder(), True)		#    Define QGIS Install point
		qgs = QgsApplication([], USE_GUI)											#    Create a QGIS Application instance, HEADLESS or with GUI
		qgs.initQgis()																#    Load QGIS providers
		Processing.initialize()														#    Start processing

	def _NewGisProject(self):														# Create GIS Project
		barfd("GisWriter.CreateProject().Enter()")									#
		self._project = QgsProject.instance()										#     Instance a GIS project
		if self._USE_GUI:															#     If not headless, create an interface bridge
			bridge = QgsLayerTreeMapCanvasBridge( self._project.layerTreeRoot(), iface.mapCanvas())
		barfd("GisWriter.CreateProject().Exit()")
		return True

	def _LoadKmlLayer(self):														# Load Status KML as a vector layer and display
		statusKml = AppSettings.glob().statusKmlSpec()								#    Get file spec of KML to load
		if self._USE_GUI:
			self._statusLayer = \
				iface.addVectorLayer(statusKml, self._layerTitle, "ogr")
		else:
			barfd("GisWriter._LoadKmlLayer.Load(file={})".format(statusKml))
			self._statusLayer = QgsVectorLayer(statusKml, self._layerTitle, "ogr")
			barfd("GisWriter._LoadKmlLayer.AddLayer()")
			self._project.addMapLayer(self._statusLayer)

		if not statusLayer.isValid():												#    If layer didn't load, hit the eject
			raise RenderError("GisWriter.ERROR: KML layer failed to load!")			#        button.
		
		self._statusLayer.setName(self._layerTitle)									#    Set title of layer
		barfd("GisWriter._LoadKmlLayer.Exit()")
		return True

	def _LayerSetLabeling(self):													# Set Project Labeling to simple labeling, Arial 8pt, black
		barfd("GisWriter._LayerSetLabeling.Enter()")
		label_settings = QgsPalLayerSettings()
		label_settings.fieldName = 'name'
		text_format = QgsTextFormat()
		text_format.setColor(self._labelingFont.qColor())
		text_format.setFont(self._labelingFont.qFont())
		text_format.setSizeUnit(QgsUnitTypes.RenderPoints)
		text_format.setSize(self._labelingFont.fontSize())
		label_settings.setFormat(text_format)
		self._statusLayer.setLabeling(QgsVectorLayerSimpleLabeling(label_settings))
		self._statusLayer.setLabelsEnabled(True)
		barfd("GisWriter._LayerSetLabeling.Exit()")
		return True

	def _AddSymbolCategory(self,statusLayer,impactCode,impactDesc, \				# Category List - Add a Symbol
							symbolColor,categoryList):	
		symbol = QgsSymbol.defaultSymbol(statusLayer.geometryType())				#    create a symbol object
		layer_style = {}															#    set the symbol's style
		layer_style['color']   = symbolColor										#       color
		layer_style['outline'] = Colors.COLOR_BLACK									#       outline (black)
		symbol_layer = QgsSimpleFillSymbolLayer.create(layer_style)
		if symbol_layer is not None:
			symbol.changeSymbolLayer(0, symbol_layer)								#    replace default symbol layer with the configured one

		category = QgsRendererCategory(impactCode, symbol, impactDesc)				#    create renderer object
		categoryList.append(category)												#    add category to list
		return True
	
	def _DebugDumpLayerFields(self):
		barfd("GisWriter._DebugDumpLayerFields.FIELDS-begin-#####")
		fields = self._statusLayer.fields()
		barfd(fields.names())
		barfd("GisWriter._DebugDumpLayerFields.FIELDS-end-#####")
		return True
	
	def _LayerSetCategories(self):													# Define Status Categories and set up Symbol Rendering
		barfd("GisWriter._LayerSetCategories.Enter()")
		fni = self._statusLayer.fields().indexFromName(self._KDATA_KEYFIELD)		#     Get index number of KML field to use as basis for categorization
		barfd("GisWriter._LayerSetCategories(KEYFIELD={},index={})".format(self._KDATA_KEYFIELD,fni))

		if AppSettings.glob().options.debugEnabled(): self._DebugDumpLayerFields()

		categories = []																#    Initialize a list of categories
		addSymbolCategory('A', 'All Available',   Colors.COLOR_GREEN,  categories)	#        Add statuses...
		addSymbolCategory('M', 'Moderate Impact', Colors.COLOR_YELLOW, categories)
		addSymbolCategory('S', 'Severe Impact',   Colors.COLOR_RED,    categories)
		if AppSettings.glob().options.zombiesEnabled():
			addSymbolCategory('Z', 'Zombies Oubreak', Colors.COLOR_BLACK,   categories)

		addSymbolCategory('', 'Unknown Impact',   Colors.COLOR_GREY,   categories)	#        ... use blank status to handle U as well as any other code

		barfd("GisWriter._LayerSetCategories.CreateSymbolRenderer()")
		statusRenderer = QgsCategorizedSymbolRenderer(self._KDATA_KEYFIELD, categories)	#    ... create renderer object
		if statusRenderer is None:													#        ... if renderer failed to instance itself, eject
			appExit(ERR_BADRENDER,"ERROR: Can't create Category Symbol Renderer")   #
		else:
			self._statusLayer.setRenderer(statusRenderer)							#        ... assign the created renderer to the layer

		barfd("DEBUG Repaint")
		self._statusLayer.triggerRepaint()
		barfd("GisWriter._LayerSetCategories.Exit()")
		return True

	def _ProjectAddPrintLayout(self):

		# Layout
		barfd("GisWriter._ProjectAddPrintLayout.Enter()")
		statusLayoutName = "MGHStatus"
		self._statusPrintLayout = QgsPrintLayout(project)
		self._statusPrintLayout.initializeDefaults()
		self._statusPrintLayout.setName(statusLayoutName)
		self._statusPrintLayout.setUnits(QgsUnitTypes.LayoutMillimeters)
		self._project.layoutManager().addLayout(self._statusPrintLayout)

		# Page
		barfd("GisWriter._ProjectAddPrintLayout.AddPage()")
		pages = self._statusPrintLayout.pageCollection()
		pages.beginPageSizeChange()
		page = pages.page(0)
		page.setPageSize('A4',  QgsLayoutItemPage.Landscape)
		pages.endPageSizeChange()

		page_center = page.pageSize().width() / 2

		# Map
		barfd("GisWriter._ProjectAddPrintLayout.AddMap2Paage()")					# Add Map to Page
		extent = QgsRectangle(-91.000, 41.101, -80.550, 48.928)						# Michigan Extent: -90.4182894376677524,41.6961255762931202 : -82.4134779482332078,48.2626923653278865
		map = QgsLayoutItemMap(self._statusPrintLayout)
		map.setRect(QRectF(-91.000, 41.101, -80.550, 48.928))
		map.setExtent(extent)
		a4 = QPageSize().size(QPageSize.A4, QPageSize.Millimeter)
		map.attemptResize(QgsLayoutSize(a4.height(), a4.width()))
		self._statusPrintLayout.addItem(map)

		# Logo
		barfd("GisWriter._ProjectAddPrintLayout.AddLogo1()")
		logoPicture = QgsLayoutItemPicture(self._statusPrintLayout)
		barfd("GisWriter._ProjectAddPrintLayout.AddLogo2()")
		logoPicture.setPicturePath(AppSettings.glob().mhgLogoSpec())
		barfd("GisWriter._ProjectAddPrintLayout.AddLogo3()")
		logoPicture.setLinkedMap(map)
		logoPicture.attemptResize(QgsLayoutSize(88.009, 85.375, QgsUnitTypes.LayoutMillimeters))
		logoPicture.attemptMove(QgsLayoutPoint(21.537, 106.912, QgsUnitTypes.LayoutMillimeters))
		self._statusPrintLayout.addItem(logoPicture)

		# Date
		barfd("GisWriter._ProjectAddPrintLayout.AddReportDate()")
		textDate = self.reportDateText()
		statusDateLabel = QgsLayoutItemLabel(self._statusPrintLayout)
		barfd("GisWriter._ProjectAddPrintLayout.AddReportDate()")
		statusDateLabel.setText(textDate)
		statusDateLabel.setFont(self._reportDateFont.qFont())
		statusDateLabel.adjustSizeToText()
		statusDateSize = statusDateLabel.sizeWithUnits()
		statusDateLabelX = page.pageSize().width() - statusDateSize.width() - 4
		statusDateLabel.attemptMove(QgsLayoutPoint(statusDateLabelX, 10))
		self._statusPrintLayout.addItem(statusDateLabel)

		# Title
		barfd("GisWriter._ProjectAddPrintLayout.AddTitle()")
		titleLabel = QgsLayoutItemLabel(self._statusPrintLayout)
		titleLabel.setText(reportTitle)
		titleLabel.setFont(self._reportTitleFont.qFont())
		titleLabel.adjustSizeToText()
		titleLabel.setReferencePoint(QgsLayoutItem.UpperMiddle)
		titleLabel.attemptMove(QgsLayoutPoint(page_center, 10))
		self._statusPrintLayout.addItem(titleLabel)

		# Legend
		barfd("GisWriter._ProjectAddPrintLayout.AddLegend()")
		legend = QgsLayoutItemLegend(self._statusPrintLayout)
		layerTree = QgsLayerTree()
		layerTree.addLayer(statusLayer)
		legend.model().setRootGroup(layerTree)
		legend.setLinkedMap(map)
		#legend.setTitle("Status")
		legend.setStyleFont(QgsLegendStyle.Title, self._legendTitleFont.qFont())
		legend.setStyleFont(QgsLegendStyle.Symbol, self._legendSymbolFont.qFont())
		legend.setStyleFont(QgsLegendStyle.SymbolLabel, self._legendLabelFont.qFont())
		legend.attemptMove(QgsLayoutPoint(256.000, 159.600, QgsUnitTypes.LayoutMillimeters)) 	# 258.603, 168.270, 37.400, 37.700
		legend.adjustBoxSize()
		self._statusPrintLayout.addItem(legend)
		
		return True
		
	def _CreateProject(self):
		self._NewGisProject()
		self._LoadKmlLayer()
		self._LayerSetLabeling()
		self._LayerSetCategories()
		self._ProjectAddPrintLayout()
		return True

	def _GuiRefresh(self):
		if self._USE_GUI:
			if iface.mapCanvas().isCachingEnabled():
				self._statusLayer.triggerRepaint()
			else:
				iface.mapCanvas().refresh()	
		return True

	#
	# Methods (public)
	#  
	def GenerateProject(self):															# Create GIS project from Status KML
		barfd("GisWriter.GenerateProject()")
		status_project = AppSettings.glob().gisProjectSpec()
		self._CreateProject()
		self._GuiRefresh()
		return True
		
	def SaveProject(self):																# Save GIS project
		self._project.write(AppSettings.glob().gisProjectSpec())
		return True

	def GeneratePDF(self):																# Barf to PDF
		barfd("GisWriter.GeneratePdf()")
		status_pdf = AppSettings.glob().gisPdfSpec()
		exporter = QgsLayoutExporter(self._statusPrintLayout)
		exporter.exportToPdf(status_pdf, QgsLayoutExporter.PdfExportSettings())
		print("Exported to PDF. File=\"{}\"".format(status_pdf)))
		return True
	
	def GenerateImage(self):															# Barf to JPG Image
		barfd("GisWriter.GenerateImage()")
		statusImage = AppSettings.glob().gisImageSpec()
		exporter = QgsLayoutExporter(self._statusPrintLayout)
		settings = QgsLayoutExporter.ImageExportSettings()
		settings.dpi      = 300
		exporter.exportToImage(statusImage, settings)
		print("Exported to JPG. File=\"{}\"".format(statusImage))
		return True
		
	def	Cleanup(self):
		if self._HEADLESS: qgs.exitQgis()												# remove provider and layer registries from memory
		return True

	#
	# Properties (public)
	#
	def project(self):
		if self._project is None: self.CreateProject()
		return self._project

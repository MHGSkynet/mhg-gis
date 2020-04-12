#
# ---------------------------------------------------------------------------------------------
# mhgAppSettings.py
#                                            |                  
# Description                               -+-
#                                         ---#---
#   Application settings handler          __|_|__            __
#                                         \_____/           ||\________
#                           __   __   __  \_____/            ^---------^
#                          ||\__||\__||\__|___  | '-O-`
#                          -^---------^--^----^___.-------------.___.--------.___.------
#                          `-------------|-------------------------------|-------------'
#                                 \___      |     \    o O o    /     |      ___/
#                                     \____/        \         /        \____/
#                                         |           \     /           |
#                                         |             \|/             |
#                                         |              |              |
# Copyright             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#						non profit conservative organizations and individuals to use in support
#						of American freedom and the constitution. All other rights are reserved,
#						and any other use prohibited.
#
# Date			Version		Author			Description
# 2020.04.06	02.00		SquintMHG		New Module
# ---------------------------------------------------------------------------------------------

import copy
import sys

import mhgAppEnvironment
import mhgCommandArgs
import mhgException
import mhgUtility

#
# Application Settings class
#
class AppSettings(object):										# Application Settings Class

	# Constants (public)
	PROGNM					= "mhgCovidStatus"					# Application program name
	FORMAT_YMD				= "%Y.%m.%d"						# date format YYYY.MM.DD
	TEMPLATE_DATE_TOKEN		= "YMD"								# Token for search/replace of date in file name templates

	# Constants (private)

	# Properties (private)
    _instance 				= None								# Class singleton object holder
	_appOptions				= None								# Parsed Command Options Object
	
	_package_root			= None								# MHGGIS Package root folder for mgh-gis suite
	_app_folder				= None								# Application folder
	_data_folder			= None								# Data folder
	_kml_folder				= None								# Kml folder
	_output_folder			= None								# Output folder
	_images_folder			= None								# Images folder
	
	_qgis_root				= None								# QGIS Root folder
	_qgis_bin_folder		= None								# QGIS Apps folder
	_qgis_python_folder		= None								# QGIS Python folder

	_currTimestamp			= None 								# current date and time (timestamp)
	_currDateYmd			= None 								# current date YYYY.MM.DD (text)
	_currDateTS				= None								# current date (timestamp)
	

    def __init__(self):
        raise RuntimeError('Call glob() instead')

	#
	#  Constructor (singleton)
	#
	def glob(cls):												# Global (singleton) class reference

        # For first instance of class, initialize data
		if cls._instance is None:
            barfd('Creating new AppSettings instance')
            cls._instance = cls.__new__(cls)
			
			# Get command arguments
			cls._appOptions = mhgFetchCommandArgs()
			success = cls._appOptions.getArguments()
			if not success:
				raise CommandArgError('AppSettings::Error processing command arguments')
				
			# Get Application Environment Info
			cls._package_root		= AppEnvironment.GetPackageRoot()												
			cls._app_folder			= cls._package_root + 'covidStatus/'
			cls._data_folder		= cls._package_root + 'data/'
			cls._images_folder		= cls._package_root + 'images/'
			cls._kml_folder			= cls._package_root + 'kml/'
			cls._output_folder		= cls._package_root + 'output/'
			
			# Get QGIS Environment Info
			cls._qgis_root			= AppEnvironment.GetQgisRoot()
			cls._qgis_bin_folder	= cls._qgis_root + "/apps/qgis-ltr"
			cls._qgis_python_folder	= cls._qgis_root + "/python/plugins"

			# System date
			cls._currTimestamp		= datetime.now() 									# current date and time (timestamp)
			cls._currDateYmd		= cls._currTimestamp.strftime(FORMAT_YMD)			# current date YYYY.MM.DD (text)
			cls._currDateTS			= datetime.strptime(cls._currDateYmd,FORMAT_YMD)	# current date (timestamp)

        return cls._instance


	#
	# Properties (public)
	#
	def options(cls):											# Get Application Options object
		return copy.deepcopy(cls._appOptions)

	def packageRoot(cls):										# Application Root Folder
		return copy.deepcopy(cls._package_root)
		
	def qgisRoot(cls):											# QGIS Root Folder
		return copy.deepcopy(cls._package_root)
		
	def qgisBinFolder(cls):										# QGIS Binaries Folder
		return copy.deepcopy(cls._package_root)

	def qgisPythonFolder(cls):									# QGIS Python Folder
		return copy.deepcopy(cls._package_root)

	def appFolder(cls):											# Covid Report application folder
		return copy.deepcopy(cls._app_folder)
		
	def dataFolder(cls):										# Data Folder (output)
		return copy.deepcopy(cls._data_folder)
		
	def imagesFolder(cls):										# Images Folder (input)
		return copy.deepcopy(cls._images_folder)

	def kmlFolder(cls):											# KML Folder (input)
		return copy.deepcopy(cls._kml_folder)
		
	def outputFolder(cls):										# Output Folder (output)
		return copy.deepcopy(cls._output_folder)
		
	def currTimestamp(cls):
		return copy.deepcopy(cls._currTimestamp)
		
	def currDateYmd(cls):
		return copy.deepcopy(cls._currDateYmd)
		
	def currDateTS(cls):
		return copy.deepcopy(cls._currDateTS)
																				#########   File specs  #############
	def googlePickleSpec(cls):
		return cls._app_folder + 'token.pickle'									# Google API pickle file										# GoogleGoo.Input

	def googleCredentialsSpec(cls):
		return cls._app_folder + 'credentials.json'								# Google API credentials file									# GoogleGoo.IO

	def kmlStatusTemplateSpec(cls):												# Template KML of Michigan counties and MHG Covid data schema	# KmlWriter:Input
		return cls._kml_folder + "mhgCovidStatusMichigan.kml"

	def statusKmlSpec(cls):														# Status KML file daily generated file 							# KmlWriter:Output, GisWriter.Input
		return "{}mhgCovidStatus-{}.kml".format(cls._output_folder,cls._appOptions.endDate())

	def detailCsvTemplate(cls):													# Detail CSV file specification									# DetailWriter.Output
		return "{}mhgCovidStatus-Detail-YMD.csv".format(cls._data_folder)

	def summaryCsvSpec(cls):													# Summary CSV file specification								# SummaryWriter.Output
		return "{}mhgCovidStatus-Summary-{}.csv".format(cls._data_folder,cls._appOptions.endDate())

	def mhgLogoSpec(cls):
		return cls._images_folder + "MHG-yellow.jpg"							# MHG Logo Image file specification								# GisWriter.Input
		
	def gisProjectSpec(cls):													# Report QGIS Project file specification						# GisWriter.Output
		return "{}mhgCovidStatus-{}.qgz".format(cls._output_folder,cls._appOptions.endDate())

	def gisPdfSpec(cls):														# Report PDF file specification									# GisWriter.Output
		return "{}mhgCovidStatus-{}.pdf".format(cls._output_folder,cls._appOptions.endDate())

	def gisImageSpec(cls):														# Report JPG image file specification							# GisWriter.Output
		return "{}mhgCovidStatus-{}.jpg".format(cls._output_folder,cls._appOptions.endDate())

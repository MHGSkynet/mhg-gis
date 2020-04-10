#
# ---------------------------------------------------------------------------------------------
# mhgAppSettings.py
#
# Description
#
# 	Application settings handler
#
# Copyright
#
#	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#						non profit conservative organizations and individuals to use in support
#						of American freedom and the constitution. All other rights are reserved,
#						and any other use prohibited.
#
# Date			Version		Author			Description
# 2020.04.06	02.00		SquintMHG		New Module
# ---------------------------------------------------------------------------------------------

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
	
	_currTimestamp			= None 								# current date and time (timestamp)
	_currDateYmd			= None 								# current date YYYY.MM.DD (text)
	_currDateTS				= None								# current date (timestamp)
	

    def __init__(self):
        raise RuntimeError('Call glob() instead')

    @classmethod												
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
				
			# Get Environment Info
			cls._package_root = AppEnvironment.getPackageRoot()												
			cls._app_folder		= cls._package_root + 'covidFetch/'
			cls._data_folder	= cls._package_root + 'data/'
			cls._kml_folder		= cls._package_root + 'kml/'
			cls._output_folder	= cls._package_root + 'output/'
			
			# System date
			cls._currTimestamp	= datetime.now() 									# current date and time (timestamp)
			cls._currDateYmd	= cls._currTimestamp.strftime(FORMAT_YMD)			# current date YYYY.MM.DD (text)
			cls._currDateTS		= datetime.strptime(cls._currDateYmd,FORMAT_YMD)	# current date (timestamp)

        return cls._instance
		
	def options(cls):											# Get Application Options Hash
		return cls._appOptions

	def packageRoot(cls):
		return cls._package_root
		
	def appFolder(cls):
		return cls._app_folder
		
	def dataFolder(cls):
		return cls._data_folder
		
	def kmlFolder(cls):
		return cls._kml_folder
		
	def outputFolder(cls):
		return cls._output_folder
		
	def currTimestamp(cls):
		return cls._currTimestamp
		
	def currDateYmd(cls):
		return cls._currDateYmd
		
	def currDateTS(cls):
		return cls._currDateTS
		
	#
	# File specs
	#
	def googlePickleSpec(cls):
		return cls._app_folder + 'token.pickle'									# Google API pickle file
		
	def googleCredentialsSpec(cls):
		return cls._app_folder + 'credentials.json'								# Google API credentials file
		
	# Fetch - Input
	def kmlStatusTemplateSpec(cls):												# Template KML of Michigan counties and MHG Covid data schema					
		return cls._kml_folder + "mhgCovidStatusMichigan.kml"

	# Fetch - Output
	def statusKmlSpec(cls):														# Status KML file daily generated file
		return "{}mhgCovidStatus-{}.kml".format(cls._output_folder,cls._appOptions.endDate())

	def detailCsvTemplate(cls):													# Detail CSV file specification (output)
		return "{}mhgCovidStatus-Detail-YMD.csv".format(cls._data_folder,cls._appOptions.endDate())

	def summaryCsvSpec(cls):													# Summary CSV file specification (output)
		return "{}mhgCovidStatus-Summary-{}.csv".format(cls._data_folder,cls._appOptions.endDate())

#	def statusKmlCurrentSpec(cls):												# Status KML file (for input to covidReport)
#		return "{}mhgCovidStatus.kml".format(cls._data_folder)


#
# ---------------------------------------------------------------------------------------------
# mhgAppEnvironment.py
#
# Description
#
# 	Get environment information for MHG application
#
# Copyright
#
#	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#						non profit conservative organizations and individuals to use in support
#						of American freedom and the constitution. All other rights are reserved,
#						and any other use prohibited.
#
# Date			Version		Author			Description
# 2020.04.06	01.03		SquintMHG		New Module
# ---------------------------------------------------------------------------------------------

import os
import os.path
import re
import sys
from pathlib import Path
from datetime import datetime

from mhgException import EnvironmentError
import mhgUtility

#
# Application Environment Info Class
#
class AppEnvironment:
	
	# Environment Constants (private)
	_ENV_PACKAGE_FOLDER		= 'MHGGIS_ROOT'								# MHGGIS Package root folder environment var
	_ROOT_KEY_FOLDERS		= [ 'data', 'kml', 'output' ] 				# MHGGIS Package folders for verification of install

    #
	# Constructor
	#
	def __init__(self):
		pass

	#
	#  Methods (public)
	#

	#
	# Package Info
	#
	def GetPackageRoot():																	# Get package root folder
		packageRoot = os.environ.get(ENV_PACKAGE_FOLDER)									# See if root folder is defined
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
				if not keyFolderPath.is_dir():
					errorText = "ERROR: Folder {} not found in package root. Invalid installation.".format(packageFolder)
					break

		if errorText != '':
			if errorText2 != '': errorText = errorText + "\n" + errorText2
			raise EnvironmentError(errorText)

		return packageRoot

	#                                                                     _,'/
# --------------------------------------------------             _.-''._:      ----------------
# mhgAppEnvironment.py                                  ,-:`-.-'    .:.|
#                                                       ;-.''       .::.|
# Description                            _..------.._  / (:.       .:::.|
#                                     ,'.   .. . .  .`/  : :.     .::::.|
#   Application Environment Info    ,'. .    .  .   ./    \ ::. .::::::.|
#                                 ,'. .  .    .   . /      `.,,::::::::.;\
#                                /  .            . /       ,',';_::::::,:_:
#                               / . .  .   .      /      ,',','::`--'':;._;
#                              : .             . /     ,',',':::::::_:'_,'
#                              |..  .   .   .   /    ,',','::::::_:'_,'
#                              |.              /,-. /,',':::::_:'_,'
#                              | ..    .    . /) /-:/,'::::_:',-'
#                              : . .     .   // / ,'):::_:',' ;
#                               \ .   .     // /,' /,-.','  ./
#                                \ . .  `::./,// ,'' ,'   . /
#                                 `. .   . `;;;,/_.'' . . ,'
#                                  ,`. .   :;;' `:.  .  ,'
#                                 /   `-._,'  ..  ` _.-'
#                                (     _,'``------''  MHG
# Copyright                       `--''
#
#	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#						non profit conservative organizations and individuals to use in support
#						of American freedom and the constitution. All other rights are reserved,
#						and any other use prohibited.
#
# Date			Version		Author			Description
# 2020.04.06	01.03		SquintMHG		New Module
# ---------------------------------------------------------------------------------------------

# Python includes
import os
import os.path
import re
import sys
from pathlib		import Path
from datetime		import datetime

# MHGLIB includes
from mhgException	import EnvironmentError
#from mhgUtility		import *

#
# Application Environment Information Class
#
class AppEnvironment:
	
	#
	# Constants (private)
	#
	_ENV_QGIS_ROOT			= 'MHGGIS_QGIS_ROOT'						# QGIS Package root folder environment var
	_ENV_PACKAGE_FOLDER		= 'MHGGIS_ROOT'								# MHGGIS Package root folder environment var
	_ROOT_KEY_FOLDERS		= [ 'data', 'kml', 'output', 'images' ]		# MHGGIS Package folders for verification of install

    #
	# Constructor
	#
	def __init__(self):
		pass

	#
	#  Methods (public)
	#

	# Package Info
	def GetPackageRoot():													# Get package root folder
		packageRoot = os.environ.get(AppEnvironment._ENV_PACKAGE_FOLDER)	# See if root folder is defined
		errorText 	= ''
		errorText2 	= ''
		if packageRoot is None:
			packageRoot = "./"
			errorText2 = "ERROR: {} environment var is not defined and current folder is not package root folder.".format(ENV_PACKAGE_FOLDER)
		else:
			packageRoot = packageRoot.replace("\\","/")
			packagePath = Path(packageRoot)
			if not packagePath.is_dir():
				errorText = "ERROR: {} environment var is not a valid folder".format(AppEnvironment._ENV_PACKAGE_FOLDER)
			else:
				errorText2 = "ERROR: {} environment var does not point to package root".format(AppEnvironment._ENV_PACKAGE_FOLDER)
		
		if packageRoot[-1:] != '/':		packageRoot = packageRoot + '/'

		if errorText == '':
			for packageFolder in AppEnvironment._ROOT_KEY_FOLDERS:
				keyFolderSpec = packageRoot + packageFolder
				keyFolderPath = Path(keyFolderSpec)
				if not keyFolderPath.is_dir():
					errorText = "ERROR: Folder {} not found in package root. Invalid installation.".format(packageFolder)
					break

		if errorText != '':
			if errorText2 != '': errorText = errorText + "\n" + errorText2
			raise EnvironmentError(errorText)

		return packageRoot

	# QGIS Package Root
	def GetQgisRoot():													# Get QGIS package root from environment variable
		rootFolder = os.environ.get(AppEnvironment._ENV_QGIS_ROOT)
		if rootFolder is None: appExit(1,"ERROR: required environment variable {} is not set".format(AppEnvironment._ENV_QGIS_ROOT))
		rootFolder = rootFolder.replace("\\","/")
		rootPath = Path(rootFolder)
		if not rootPath.is_dir(): appExit(2,errorText = "ERROR: Folder {} does not exist. Fix {} environment variable.".format(packageFolder,AppEnvironment._ENV_QGIS_ROOT))
		return rootFolder

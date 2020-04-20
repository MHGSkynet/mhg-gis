#
# ---------------------------------------------------------------------------------------------
# mhgException.py                              ...                            
#                                             ;::::;                           
# Description                               ;::::; :;                          
#                                         ;:::::'   :;                         
#   Application Exceptions               ;:::::;     ;.                        
#                                       ,:::::'  404  ;           OOO\         
#                                       ::::::;       ;          OOOOO\        
#                                       ;:::::;       ;         OOOOOOOO       
#                                      ,;::::::;     ;'         / OOOOOOO      
#                                    ;:::::::::`. ,,,;.        /  / DOOOOOO    
#                                  .';:::::::::::::::::;,     /  /     DOOOO   
#                                 ,::::::;::::::;;;;::::;,   /  /        DOOO  
#                                ;`::::::`'::::::;;;::::: ,#/  /          DOOO 
#                                :`:::::::`;::::::;;::: ;::#  /            DOOO
#                                ::`:::::::`;:::::::: ;::::# /              DOO
#                                `:`:::::::`;:::::: ;::::::#/               DOO
#                                 :::`:::::::`;; ;:::::::::##                OO
#                                 ::::`:::::::`;::::::::;:::#                OO
#                                 `:::::`::::::::::::;'`:;::#                O 
#                                  `:::::`::::::::;' /  / `:#                  
# Copyright                         ::::::`:::::;'  /  /   `#              
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
from mhgAppConstants	import AppConstants

#
# Severity Codes
#
class Severity():

	# Constants (public)
	FATAL				= 3
	WARNING				= 2
	INFO				= 1
	SUCCESS				= 0

	# Properties (private)
	_severityText		= { FATAL:		'Fatal',
							WARNING:	'Warning',
							INFO:		'Info',
							SUCCESS:	'Success' }

	_severityCodes		= { FATAL:		'F',
							WARNING:	'W',
							INFO:		'I',
							SUCCESS:	'S' }

	_severityValue		= SUCCESS

	# Constructor
	def __init__(self,severity):
		self._severityValue = severity

	# Properties (public)
	def text(self):
		return self._severityText[self._severityValue]

	def code(self):
		return self._severityCodes[self._severityValue]

#
# EXCEPTIONS
#
class AppError(Exception):														# Base class for application exceptions

	# Constants (public)
	ERR_NONE			= 0														# No error
	ERR_ERROR			= 1														# General error
	ERR_BADENV			= 2														# Bad environment setting
	ERR_BADCMD			= 3														# Bad command argument
	ERR_BADFILTER		= 4
	ERR_LOGINFAIL		= 6														# Google Login Failure
	ERR_FETCHFAIL		= 7														# Fetch data failure
	ERR_USERFAIL 		= 8														# User DOH
	ERR_BADRENDER		= 9														# Problem rendering KML thru QGIS


	# Properties (private)
	_err_ident			= { ERR_NONE:		'SUCCESS',
							ERR_ERROR:		'ERROR',
							ERR_BADENV:		'BADENV',
							ERR_BADCMD:		'BADCMD',
							ERR_BADFILTER:	'BADFILTER',
							ERR_FETCHFAIL:	'FETCHFAIL',
							ERR_USERFAIL:	'USERFAIL',
							ERR_BADRENDER:	'BADRENDER' }

	_err_number			= ERR_ERROR
	_err_severity 		= Severity(Severity.FATAL)
	_message			= None

	# Constructor
	def __init__(self,message='Application Error',errNo=ERR_ERROR):
		self._message		= message
		self._err_number	= errNo
		self._err_severity 	= Severity(Severity.FATAL)
		return self

	# Properties (public)
	def errIdent(self):
		return self._err_ident[self._err_number]

	def errSeverity(self):
		return self._err_severity

	# Properties (public)
	def errorNumber(self):
		return self._err_number

	def message(self):
		return self._message

	def formattedText(self):
		return "{}-{}-{}: {}".format(AppConstants.PROGNM,self.errSeverity().code(),self.errIdent(),self.message())

class CommandArgError(AppError):												# Command Args Error

	# Constructor
	def __init__(self, message, errNo=AppError.ERR_BADCMD):
		self._message		= message
		self._err_number	= errNo
		self._err_severity	= Severity(Severity.FATAL)

class EnvironmentError(AppError):												# Environment Error

	# Constructor
	def __init__(self, message, errNo=AppError.ERR_BADENV):
		self._message		= message
		self._err_number	= errNo
		self._err_severity	= Severity(Severity.FATAL)

class RenderError(AppError):													# GIS Rendering Error

	# Constructor
	def __init__(self, message, errNo=AppError.ERR_BADRENDER):
		self._message		= message
		self._err_number	= errNo
		self._err_severity	= Severity(Severity.FATAL)

class UserError(AppError):														# DWHUA (Driving With Head Up Ass) Error

	# Constructor
	def __init__(self, message, errNo=AppError.ERR_ERROR):
		self._message		= message
		self._err_number	= errNo
		self._err_severity	= Severity(Severity.FATAL)

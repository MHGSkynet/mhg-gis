#
# ---------------------------------------------------------------------------------------------
# mhgException.py
#
# Description
#
# 	Application exception handlers
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
		pass
	
	# Properties (public)
	def text(self):
		retval = self._severityText[self._severityValue]

	def code(self,severity):
		retval = self._severityCode[self._severityValue]

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
	ERR_FETCHFAIL		= 5														# Fetch data failure
	
	# Properties (private)
	_err_ident			= { ERR_NONE:		'SUCCESS',
							ERR_ERROR:		'ERROR',
							ERR_BADENV:		'BADENV',
							ERR_BADCMD:		'BADCMD',
							ERR_BADFILTER:	'BADFILTER'
							ERR_FETCHFAIL:	'FETCHFAIL',
							ERR_USERFAIL:	'USERFAIL'	}
							
	_err_number			= ERR_ERROR
	_err_severity 		= Severity(Severity.FATAL)
	_message			= None

    # Constructor
	def __init__(self,message='Application Error',errNo=AppError.ERR_ERROR):
        self._message		= message
		self._err_number	= errNo
		self._err_severity 	= Severity(Severity.FATAL)

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
		return "{}-{}-{}: {}".format(AppSettings.PROGNM,self._errSeverity.code(),self.errIdent())

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

class UserError(AppError):														# DWHUA (Driving With Head Up Ass) Error

    # Constructor
    def __init__(self, message, errNo=AppError.ERR_ERROR):
        self._message		= message
		self._err_number	= errNo
		self._err_severity	= Severity(Severity.FATAL)

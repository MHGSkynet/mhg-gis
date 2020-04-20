#
# ---------------------------------------------------------------------------------------------
# mhgFont.py
#
# Description
#
# 	Font Class
#
#        ██╗██╗███╗░░░███╗██╗░█████╗░██╗░░██╗██╗░██████╗░░█████╗░███╗░░██╗██╗██╗██╗
#        ╚═╝╚═╝████╗░████║██║██╔══██╗██║░░██║██║██╔════╝░██╔══██╗████╗░██║╚═╝╚═╝╚═╝
#        ░░░░░░██╔████╔██║██║██║░░╚═╝███████║██║██║░░██╗░███████║██╔██╗██║░░░░░░░░░
#        ░░░░░░██║╚██╔╝██║██║██║░░██╗██╔══██║██║██║░░╚██╗██╔══██║██║╚████║░░░░░░░░░
#        ██╗██╗██║░╚═╝░██║██║╚█████╔╝██║░░██║██║╚██████╔╝██║░░██║██║░╚███║██╗██╗██╗
#        ╚═╝╚═╝╚═╝░░░░░╚═╝╚═╝░╚════╝░╚═╝░░╚═╝╚═╝░╚═════╝░╚═╝░░╚═╝╚═╝░░╚══╝╚═╝╚═╝╚═╝
#
#        ██╗██╗██╗░░██╗░█████╗░███╗░░░███╗███████╗  ░██████╗░██╗░░░██╗░█████╗░██████╗░██████╗░
#        ╚═╝╚═╝██║░░██║██╔══██╗████╗░████║██╔════╝  ██╔════╝░██║░░░██║██╔══██╗██╔══██╗██╔══██╗
#        ░░░░░░███████║██║░░██║██╔████╔██║█████╗░░  ██║░░██╗░██║░░░██║███████║██████╔╝██║░░██║
#        ░░░░░░██╔══██║██║░░██║██║╚██╔╝██║██╔══╝░░  ██║░░╚██╗██║░░░██║██╔══██║██╔══██╗██║░░██║
#        ██╗██╗██║░░██║╚█████╔╝██║░╚═╝░██║███████╗  ╚██████╔╝╚██████╔╝██║░░██║██║░░██║██████╔╝
#        ╚═╝╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░░░░╚═╝╚══════╝  ░╚═════╝░░╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░
#
# Copyright
#
#	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#						non profit conservative organizations and individuals to use in support
#						of American freedom and the constitution. All other rights are reserved,
#						and any other use prohibited.
#
# Date			Version		Author			Description
# 2020.04.10	02.00		SquintMHG		New Constants
# ---------------------------------------------------------------------------------------------

# Python includes
import copy

# QGIS includes
from PyQt5.QtGui	import QColor
from PyQt5.QtGui	import QFont

# MHGLIB includes
from mhgColors		import Colors
from mhgUtility		import *

class Font():

	#
	# Constants (public)
	#
	FONT_ARIAL				= "Arial"
	FONT_MS_SHELL_DLG2		= "MS Shell Dlg 2"
	
	FONT_WEIGHT_NORMAL		= "Thin"
	FONT_WEIGHT_EXTRALIGHT	= "ExtraLight"
	FONT_WEIGHT_LIGHT		= "Light"
	FONT_WEIGHT_NORMAL		= "Normal"
	FONT_WEIGHT_MERIUM		= "Medium"
	FONT_WEIGHT_DEMIBOLD	= "DemiBold"
	FONT_WEIGHT_BOLD		= "Bold"
	FONT_WEIGHT_EXTRABOLD	= "ExtraBold"
	FONT_WEIGHT_BLACK		= "Black"
	
	_QFONT_WEIGHT_MAP		= { FONT_WEIGHT_NORMAL:		QFont.Thin,
								FONT_WEIGHT_EXTRALIGHT:	QFont.ExtraLight,
								FONT_WEIGHT_LIGHT:		QFont.Light,
								FONT_WEIGHT_NORMAL:		QFont.Normal,
								FONT_WEIGHT_MERIUM:		QFont.Medium,
								FONT_WEIGHT_DEMIBOLD:	QFont.DemiBold,
								FONT_WEIGHT_BOLD:		QFont.Bold,
								FONT_WEIGHT_EXTRABOLD:	QFont.ExtraBold,
								FONT_WEIGHT_BLACK:		QFont.Black	}
					
	#
	# Constants (private)
	#
	_DEFAULT_FONT_NAME		= "MS Shell Dlg 2"
	_DEFAULT_FONT_SIZE		= 8
	_DEFAULT_FONT_COLOR		= Colors.COLOR_BLACK
	_DEFAULT_FONT_WEIGHT	= FONT_WEIGHT_NORMAL

	#
	# Properties (private)
	#
	_fontName			= None
	_fontSize			= None
	_fontColor			= None
	_fontWeight			= None
	
	# Constructor
	def __init__(self,fontName=_DEFAULT_FONT_NAME,fontSize=_DEFAULT_FONT_SIZE,fontColor=_DEFAULT_FONT_COLOR,fontWeight=_DEFAULT_FONT_WEIGHT):
		self._fontName		= fontName
		self._fontSize		= fontSize
		self._fontColor		= fontColor
		self._fontWeight	= fontWeight
	
	#
	# Properties (public)
	#
	def fontName(self):
		return copy.deepcopy(self._fontName)
		
	def fontSize(self):
		return copy.deepcopy(self._fontSize)

	def fontColor(self):
		return copy.deepcopy(self._fontColor)
		
	def fontColorCode(self):
		return copy.deepcopy(self._fontColor)

	def fontWeight(self):
		return copy.deepcopy(self._fontWeight)

	def qColor(self):
		return QColor(self.fontColor())

	def qFontWeight(self):
		return copy.deepcopy(self._QFONT_WEIGHT_MAP[self._fontWeight])
	
	def qFont(self):
		return QFont(self.fontName(), self.fontSize(), self.qFontWeight())

	#
	# Methods (public)
	#


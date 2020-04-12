#
# ---------------------------------------------------------------------------------------------
# mhgColors.py                                o
#                                            /\
# Description                               /::\
#                                          /::::\
#   Colors Class             ,a__a        /\::::/\
#                           {/  '')      /\ \::/\ \
#                           {\ \_oo)    /\ \ \/\ \ \
#                           {/  ( W ___/  \ \ \ \ \ \
#                 .=.      {/ \__))))*)    \ \ \ \ \/
#                (.=.`\   {/   /=;  ~/      \ \ \ \/
#                    \ `\{/(   \/\  /        \ \ \/
#                     \  `. `\  ) )           \ \/
#                      \    // /_/_            \/
# Copyright             '==''---))))
#
#	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#						non profit conservative organizations and individuals to use in support
#						of American freedom and the constitution. All other rights are reserved,
#						and any other use prohibited.
#
# Date			Version		Author			Description
# 2020.04.10	02.00		SquintMHG		New Constants
# ---------------------------------------------------------------------------------------------

class Colors():

	#
	# Constants (public)
	#

	# Colors
	COLOR_WHITE			= 'White'													# White
	COLOR_GREY			= 'Grey'													# Grey
	COLOR_BLACK			= 'Black'													# Black
	COLOR_GREEN			= 'Green'													# Green
	COLOR_YELLOW		= 'Yellow'													# Yellow
	COLOR_RED			= 'Red'														# Red

	_COLOR_CODES		= { COLOR_WHITE:	'#ffffff',								# White
							COLOR_GREY:		'#c8c8c8',								# Grey
							COLOR_BLACK:	'#000000',								# Black
							COLOR_GREEN:	'#13e904',								# Green
							COLOR_YELLOW:	'#e6f014',								# Yellow
							COLOR_RED:		'#ff0014' }								# Red

	# Constructor
	def __init__(self):
		pass

	#
	# Properties (public)
	#
	def colorCode(self,color):
		cCode = None
		if color in self._COLOR_CODES: cCode = self._COLOR_CODES[color]
		return cCode

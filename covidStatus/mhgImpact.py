#
# ---------------------------------------------------------------------------------------------
# mhgImpact.py                                ,   _, .--.
#                                      (     '     (  / (  '-.  )
# Description                          (    {      .-=-.    ) -.  _)
#                                     (_   {      /   (  .' .   \_))
#   Impact Codes and Scoring            ((   {    \ ( ' ,_) ) \_/___)    . . 
#                                         (________(_ , /\  ,_/_)----'   .     .
#                                      .      /  /   '--\ `\--`           .
#                                       % .  _/ /  /    _\ _\      .   %       .
#                                    .      / /'   .    `\ \      %    %   .
#                                       .  _/ /           _\_\   .   .  .   %. .
#                                     .  //'     %  %    `\\     .   .  % .   . .
#                                       /'       .  .      \\       %   .    .  %
# Copyright                                   %   .      .'.`\.'.-
#
#   Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#                       non profit conservative organizations and individuals to use in support
#                       of American freedom and the constitution. All other rights are reserved,
#                       and any other use prohibited.
#
# Date          Version     Author          Description
# 2020.04.20    02.00       SquintMHG       New Module
# ---------------------------------------------------------------------------------------------

# Python includes
import copy
import sys

# MHGLIB includes
from mhgAppSettings		import AppSettings

class Impact(object):											# Impact

	#
	# Constants (public)
	#
	IMPACT_CODE_AVAILABLE	= 'A'								# All available
	IMPACT_CODE_MODERATE	= 'M'								# Moderate impact
	IMPACT_CODE_SEVERE		= 'S'								# Severe impact
	IMPACT_CODE_UNKNOWN		= 'U'								# Unkown status
	IMPACT_CODE_ZOMBIES		= 'Z'								# Zombie outbreak

	#
	# Properties (private)
	#
	_impactCode				= IMPACT_CODE_UNKNOWN				# Impact code
	
	# Constructor
	def __init__(self,impactCode=IMPACT_CODE_UNKNOWN):
		self._impactCode = impactCode
		return self

	#
	# Properties (public)
	#
	def code(self):																# Impact code
		return copy.deepcopy(self._impactCode)

	def weight(self,impactCode=None):											# Determine Impact Weight - numeric weight of an impact code (A,M,S)
		if impactCode is None: impactCode = self._impactCode
		return self.WeightFromCode(impactCode)

	#
	# Methods (public)
	#
	def SetCode(self,impactCode):
		self._impactCode = impactCode
		return True

	#
	# Methods (class public)
	#
	def EvalScore(totalWeight,observeCount):									# Calculate Impact Score
		score = 0.0
		if observeCount > 0: score = round(totalWeight / observeCount,2)
		return score

	def CodeFromScore(score):													# Derive Impact Code (A,M,S) from Impact Score
		impactCode = Impact.IMPACT_CODE_UNKNOWN
		score = round(score)
		if score == 1: impactCode = Impact.IMPACT_CODE_AVAILABLE
		if score == 2: impactCode = Impact.IMPACT_CODE_MODERATE
		if score == 3: impactCode = Impact.IMPACT_CODE_SEVERE
		if AppSettings.glob().options().zombiesEnabled() and score >= 4: impactCode = Impact.IMPACT_CODE_ZOMBIES
		return impactCode
		
	def WeightFromCode(impactCode):
		weight = 0
		if impactCode is None: impactCode = Impact.IMPACT_CODE_UNKNOWN
		impactCode = impactCode.strip()
		if impactCode == Impact.IMPACT_CODE_AVAILABLE:		weight = 1
		if impactCode == Impact.IMPACT_CODE_MODERATE:		weight = 2
		if impactCode == Impact.IMPACT_CODE_SEVERE:			weight = 3
		if impactCode == Impact.IMPACT_CODE_ZOMBIES and \
			AppSettings.glob().options().zombiesEnabled():	weight = 12
		return weight

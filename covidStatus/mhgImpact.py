#
# ---------------------------------------------------------------------------------------------
# mhgImpact.py
#
# Description
#
# 	Class for Impact codes and scoring
#
# Copyright
#
#	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#						non profit conservative organizations and individuals to use in support
#						of American freedom and the constitution. All other rights are reserved,
#						and any other use prohibited.
#
# Date			Version		Author			Description
# 2020.04.07	02.00		SquintMHG		New Module
# ---------------------------------------------------------------------------------------------

# Python includes
import sys

# Impact Codes
IMPACT_CODE_AVAILABLE	= 'A'
IMPACT_CODE_MODERATE	= 'M'
IMPACT_CODE_SEVERE		= 'S'
IMPACT_CODE_UNKNOWN		= 'U'
IMPACT_CODE_ZOMBIES		= 'Z'

"""
class Impact(object):											# Impact


    def __init__(self):

		pass
"""

#
# Scoring stuff
#
def impactWeight(impactSeverity):														# Determine Impact Weight - numeric weight of a severity code (A,M,S)
	weight = 0
	if impactSeverity.strip() == IMPACT_CODE_AVAILABLE:		weight = 1
	if impactSeverity.strip() == IMPACT_CODE_MODERATE:		weight = 2
	if impactSeverity.strip() == IMPACT_CODE_SEVERE:		weight = 3
	if AppSettings.glob().options().zombiesEnable() and 
			impactSeverity.strip() == IMPACT_CODE_ZOMBIES:	weight = 12
	return weight

def impactScore(totalWeight,observeCount):												# Calculate Impact Score
	score = 0.0
	if observeCount > 0: score = round(totalWeight / observeCount,2)
	return score
	
def impactCodeFromScore(score):															# Derive Impact Code (A,M,S) from Impact Score
	impactCode = 'U'
	score = round(score)
	if score == 1: impactCode = IMPACT_CODE_AVAILABLE
	if score == 2: impactCode = IMPACT_CODE_MODERATE
	if score == 3: impactCode = IMPACT_CODE_SEVERE
	if AppSettings.glob().options().zombiesEnable() and score >= 4: impactCode = IMPACT_CODE_ZOMBIES
	return impactCode

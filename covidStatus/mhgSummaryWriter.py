#
# ---------------------------------------------------------------------------------------------
# mhgSummaryWriter.py
#
# Description
#
# 	Class for writing Summary info
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

import sys
import mhgCommandArgs
import csvWriter

class SummaryWriter(CsvWriter):									# Summary CSV Writer

	# Summary CSV (output) metadata
	_SCSV_START_DATE			= 0
	_SCSV_END_DATE				= 1
	_SCSV_COUNTY				= 2
	_SCSV_NDAYS					= 3
	_SCSV_OBSERVATIONS			= 4
	_SCSV_UTILITIES_WEIGHT		= 5
	_SCSV_SERVICES_WEIGHT		= 6
	_SCSV_CONSUMABLES_WEIGHT	= 7
	_SCSV_UTILITIES_IMPACT		= 8
	_SCSV_SERVICES_IMPACT		= 9
	_SCSV_CONSUMABLES_IMPACT	= 10
	_SCSV_MAX_IMPACT			= 11
	_SCSV_2M_CHECKINS			= 12
	_SCSV_2M_PARTICIPATE		= 13
	_SCSV_HF_CHECKINS			= 14
	_SCSV_HF_PARTICIPATE		= 15
	_SCSV_METADATA		= [ { _COL_ID: _SCSV_START_DATE,			_COL_DTYPE: DTYPE_DATE,		_COL_HEADER: 'IntelStartDate'		},
							{ _COL_ID: _SCSV_END_DATE,				_COL_DTYPE: DTYPE_DATE,		_COL_HEADER: 'IntelEndDate'			},
							{ _COL_ID: _SCSV_COUNTY,				_COL_DTYPE: DTYPE_TEXT,		_COL_HEADER: 'County'				},
							{ _COL_ID: _SCSV_NDAYS,					_COL_DTYPE: DTYPE_NUMERIC,	_COL_HEADER: 'ObserveDays'			},
							{ _COL_ID: _SCSV_OBSERVATIONS,			_COL_DTYPE: DTYPE_NUMERIC,	_COL_HEADER: 'ObserveCount'			},
							{ _COL_ID: _SCSV_UTILITIES_WEIGHT,		_COL_DTYPE: DTYPE_NUMERIC,	_COL_HEADER: 'UtilityWeight'		},
							{ _COL_ID: _SCSV_SERVICES_WEIGHT,		_COL_DTYPE: DTYPE_NUMERIC,	_COL_HEADER: 'ServicesWeight'		},
							{ _COL_ID: _SCSV_CONSUMABLES_WEIGHT,	_COL_DTYPE: DTYPE_NUMERIC,	_COL_HEADER: 'ConsumablesWeight'	},
							{ _COL_ID: _SCSV_UTILITIES_IMPACT,		_COL_DTYPE: DTYPE_TEXT,		_COL_HEADER: 'UtilityImpact'		},
							{ _COL_ID: _SCSV_SERVICES_IMPACT,		_COL_DTYPE: DTYPE_TEXT,		_COL_HEADER: 'ServicesImpact'		},
							{ _COL_ID: _SCSV_CONSUMABLES_IMPACT,	_COL_DTYPE: DTYPE_TEXT,		_COL_HEADER: 'ConsumablesImpact'	},
							{ _COL_ID: _SCSV_MAX_IMPACT,			_COL_DTYPE: DTYPE_TEXT,		_COL_HEADER: 'MaxImpact'			},
							{ _COL_ID: _SCSV_2M_CHECKINS,			_COL_DTYPE: DTYPE_NUMERIC,	_COL_HEADER: '2MCheckins'			},
							{ _COL_ID: _SCSV_2M_PARTICIPATE,		_COL_DTYPE: DTYPE_NUMERIC,	_COL_HEADER: '2MParticipate'		},
							{ _COL_ID: _SCSV_HF_CHECKINS,			_COLD_TYPE: DTYPE_NUMERIC,	_COL_HEADER: 'HFCheckins'			},
							{ _COL_ID: _SCSV_HF_PARTICIPATE,		_COL_DTYPE: DTYPE_NUMERIC,	_COL_HEADER: 'HFParticipate'		}  ]

	# Properties (private)
	_fhDetailCSV							= None				# Detail CSV file handle

	def __init__(self):

		pass

	#
	# Methods (public)
	#
	def SummaryCsvOpen():																	# Open Summary CSV for output
		global fhSummaryCSV
		if fhSummaryCSV is None:
			summaryCsvSpec = summaryCsvTemplate.replace(TEMPLATE_DATE_TOKEN,_appOptions.endDate())
			barfd("SummaryWriter.SummaryCSVOpen(file={})".format(summaryCsvSpec))
			fhSummaryCSV = open(summaryCsvSpec, 'w')
			summaryCsvWriteHeader()

	def SummaryCsvClose():																	# Close Summary CSV
		global fhSummaryCSV
		barfd("SummaryWriter.SummaryCSVClose")
		fhSummaryCSV.close()
		fhSummaryCSV = None

	def SummaryCsvWriteHeader():															# Write Summary CSV header
		csvLine = ''
		for colMeta in _SCSV_METADATA:
			csvLine += csvText(colMeta[_COL_HEADER], DTYPE_TEXT, True)
		
		summaryCsvWrite(csvLine)

	def SummaryCsvWrite(text):																# Write text to Summary CSV
		summaryCsvOpen()
		fhSummaryCSV.write(text + '\n')

	def WriteCountyStats(countyStats):														# Dump County Statistics to Summary CSV
		success = True
		barfi("Summary data generating ...")
		for countyName in covidStats.keys():
			countyStats	= covidStats[countyName]
			csvLine 	= ''
			for colMeta in _SCSV_METADATA:
				if colMeta[_COL_ID] == _SCSV_START_DATE:			csvLine += csvText(_appOptions.startDate(), colMeta[_COL_DTYPE])
				if colMeta[_COL_ID] == _SCSV_END_DATE:			csvLine += csvText(_appOptions.endDate(), colMeta[_COL_DTYPE])
				if colMeta[_COL_ID] == _SCSV_NDAYS:				csvLine += csvText(_appOptions.nDays(), colMeta[_COL_DTYPE])
				if colMeta[_COL_ID] == _SCSV_COUNTY:				csvLine += csvText(countyName, colMeta[_COL_DTYPE])
				if colMeta[_COL_ID] == _SCSV_OBSERVATIONS:		csvLine += csvText(countyStats[STAT_STATUS_REPORTS], colMeta[_COL_DTYPE])
				if colMeta[_COL_ID] == _SCSV_UTILITIES_WEIGHT:	csvLine += csvText(countyStats[STAT_UTILITIES_WEIGHT], colMeta[_COL_DTYPE])
				if colMeta[_COL_ID] == _SCSV_SERVICES_WEIGHT:		csvLine += csvText(countyStats[STAT_SERVICES_WEIGHT], colMeta[_COL_DTYPE])
				if colMeta[_COL_ID] == _SCSV_CONSUMABLES_WEIGHT:	csvLine += csvText(countyStats[STAT_CONSUMABLES_WEIGHT], colMeta[_COL_DTYPE])
				if colMeta[_COL_ID] == _SCSV_UTILITIES_IMPACT:	csvLine += csvText(countyStats[STAT_UTILITIES_IMPACT_CODE], colMeta[_COL_DTYPE])
				if colMeta[_COL_ID] == _SCSV_SERVICES_IMPACT:		csvLine += csvText(countyStats[STAT_SERVICES_IMPACT_CODE], colMeta[_COL_DTYPE])
				if colMeta[_COL_ID] == _SCSV_CONSUMABLES_IMPACT:	csvLine += csvText(countyStats[STAT_CONSUMABLES_IMPACT_CODE], colMeta[_COL_DTYPE])
				if colMeta[_COL_ID] == _SCSV_MAX_IMPACT:			csvLine += csvText(countyStats[STAT_MAX_IMPACT_CODE], colMeta[_COL_DTYPE])
				if colMeta[_COL_ID] == _SCSV_2M_CHECKINS:			csvLine += csvText(countyStats[STAT_2M_CHECKINS], colMeta[_COL_DTYPE])
				if colMeta[_COL_ID] == _SCSV_2M_PARTICIPATE:		csvLine += csvText(countyStats[STAT_2M_PARTICIPATE], colMeta[_COL_DTYPE])
				if colMeta[_COL_ID] == _SCSV_HF_CHECKINS:			csvLine += csvText(countyStats[STAT_HF_CHECKINS], colMeta[_COL_DTYPE])
				if colMeta[_COL_ID] == _SCSV_HF_PARTICIPATE:		csvLine += csvText(countyStats[STAT_HF_PARTICIPATE], colMeta[_COL_DTYPE])

			summaryCsvWrite(csvLine)

		summaryCsvClose()
		
		barfi("Summary data complete. Stats recorded for {} counties.".format(len(covidStats)))
		return generateStatus
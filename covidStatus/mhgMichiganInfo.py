#
# ---------------------------------------------------------------------------------------------
# mhgMichiagnInfo.py
#
# Description
#
# 	Michigan static data by county
#
# Copyright
#
#	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#						non profit conservative organizations and individuals to use in support
#						of American freedom and the constitution. All other rights are reserved,
#						and any other use prohibited.
#
# Date			Version		Author			Description
# 2020.04.10	02.00		SquintMHG		New Module
# ---------------------------------------------------------------------------------------------

include mhgRegion

class MichiganInfo(object):

	MCI_POP		= 'population'
	MCI_REGION	= 'region'

	MICHIGAN_COUNTIES	= {
		'Alcona':			{ MCI_POP:10364,	MCI_REGION: MhgRegion.REGION_NE2	},
		'Alger':			{ MCI_POP:9194,		MCI_REGION: MhgRegion.REGION_SUP2	},
		'Allegan':			{ MCI_POP:115250,	MCI_REGION: MhgRegion.REGION_W2		},
		'Alpena':			{ MCI_POP:28612,	MCI_REGION: MhgRegion.REGION_NE1	},
		'Antrim':			{ MCI_POP:23177,	MCI_REGION: MhgRegion.REGION_NW1	},
		'Arenac':			{ MCI_POP:15165,	MCI_REGION: MhgRegion.REGION_NE3	},
		'Baraga':			{ MCI_POP:8507,		MCI_REGION: MhgRegion.REGION_SUP1	},
		'Barry':			{ MCI_POP:60057,	MCI_REGION: MhgRegion.REGION_W2		},
		'Bay':				{ MCI_POP:104786,	MCI_REGION: MhgRegion.REGION_E3		},
		'Benzie':			{ MCI_POP:17552,	MCI_REGION: MhgRegion.REGION_NW3	},
		'Berrien':			{ MCI_POP:154807,	MCI_REGION: MhgRegion.REGION_W3		},
		'Branch':			{ MCI_POP:43584,	MCI_REGION: MhgRegion.REGION_C1		},
		'Calhoun':			{ MCI_POP:134473,	MCI_REGION: MhgRegion.REGION_W3		},
		'Cass':				{ MCI_POP:51460,	MCI_REGION: MhgRegion.REGION_W3		},
		'Charlevoix':		{ MCI_POP:26219,	MCI_REGION: MhgRegion.REGION_NW1 	},
		'Cheboygan':		{ MCI_POP:25458,	MCI_REGION: MhgRegion.REGION_NE1 	},
		'Chippewa':			{ MCI_POP:37834,	MCI_REGION: MhgRegion.REGION_SUP3 	},
		'Clare':			{ MCI_POP:30616,	MCI_REGION: MhgRegion.REGION_NE3 	},
		'Clinton':			{ MCI_POP:77896,	MCI_REGION: MhgRegion.REGION_C2 	},
		'Crawford':			{ MCI_POP:13836,	MCI_REGION: MhgRegion.REGION_NE2 	},
		'Delta':			{ MCI_POP:36190,	MCI_REGION: MhgRegion.REGION_SUP2 	},
		'Dickinson':		{ MCI_POP:25570,	MCI_REGION: MhgRegion.REGION_SUP2	},
		'Eaton':			{ MCI_POP:109155,	MCI_REGION: MhgRegion.REGION_C2		},
		'Emmet':			{ MCI_POP:33039,	MCI_REGION: MhgRegion.REGION_NW1	},
		'Genesee':			{ MCI_POP:409361,	MCI_REGION: MhgRegion.REGION_E2		},
		'Gladwin':			{ MCI_POP:25289,	MCI_REGION: MhgRegion.REGION_NE3	},
		'Gogebic':			{ MCI_POP:15414,	MCI_REGION: MhgRegion.REGION_SUP1	},
		'Grand Traverse':	{ MCI_POP:91746,	MCI_REGION: MhgRegion.REGION_NW2	},
		'Gratiot':			{ MCI_POP:41067,	MCI_REGION: MhgRegion.REGION_C3		},
		'Hillsdale':		{ MCI_POP:45830,	MCI_REGION: MhgRegion.REGION_C1		},
		'Houghton':			{ MCI_POP:36360,	MCI_REGION: MhgRegion.REGION_SUP1	},
		'Huron':			{ MCI_POP:31543,	MCI_REGION: MhgRegion.REGION_E3		},
		'Ingham':			{ MCI_POP:289564,	MCI_REGION: MhgRegion.REGION_C1		},
		'Ionia':			{ MCI_POP:64176,	MCI_REGION: MhgRegion.REGION_C2		},
		'Iosco':			{ MCI_POP:25247,	MCI_REGION: MhgRegion.REGION_NE2	},
		'Iron':				{ MCI_POP:11212,	MCI_REGION: MhgRegion.REGION_SUP1	},
		'Isabella':			{ MCI_POP:70775,	MCI_REGION: MhgRegion.REGION_C3		},
		'Jackson':			{ MCI_POP:158913,	MCI_REGION: MhgRegion.REGION_C1		},
		'Kalamazoo':		{ MCI_POP:261573,	MCI_REGION: MhgRegion.REGION_W3		},
		'Kalkaska':			{ MCI_POP:17463,	MCI_REGION: MhgRegion.REGION_NW2	},
		'Kent':				{ MCI_POP:643140,	MCI_REGION: MhgRegion.REGION_W2		},
		'Keweenaw':			{ MCI_POP:2130,		MCI_REGION: MhgRegion.REGION_SUP1	},
		'Lake':				{ MCI_POP:11763,	MCI_REGION: MhgRegion.REGION_NW3	},
		'Lapeer':			{ MCI_POP:88202,	MCI_REGION: MhgRegion.REGION_E2		},
		'Leelanau':			{ MCI_POP:21639,	MCI_REGION: MhgRegion.REGION_NW1	},
		'Lenawee':			{ MCI_POP:98474,	MCI_REGION: MhgRegion.REGION_C1		},
		'Livingston':		{ MCI_POP:188482,	MCI_REGION: MhgRegion.REGION_E1		},
		'Luce':				{ MCI_POP:6364,		MCI_REGION: MhgRegion.REGION_SUP3	},
		'Mackinac':			{ MCI_POP:10817,	MCI_REGION: MhgRegion.REGION_SUP3	},
		'Macomb':			{ MCI_POP:868704,	MCI_REGION: MhgRegion.REGION_E2		},
		'Manistee':			{ MCI_POP:24444,	MCI_REGION: MhgRegion.REGION_NW3	},
		'Marquette':		{ MCI_POP:66939,	MCI_REGION: MhgRegion.REGION_SUP2	},
		'Mason':			{ MCI_POP:28884,	MCI_REGION: MhgRegion.REGION_NW3	},
		'Mecosta':			{ MCI_POP:43264,	MCI_REGION: MhgRegion.REGION_C3		},
		'Menominee':		{ MCI_POP:23234,	MCI_REGION: MhgRegion.REGION_SUP2	},
		'Midland':			{ MCI_POP:83389,	MCI_REGION: MhgRegion.REGION_E3		},
		'Missaukee':		{ MCI_POP:15006,	MCI_REGION: MhgRegion.REGION_NW2	},
		'Monroe':			{ MCI_POP:149699,	MCI_REGION: MhgRegion.REGION_E1		},
		'Montcalm':			{ MCI_POP:63209,	MCI_REGION: MhgRegion.REGION_C3		},
		'Montmorency':		{ MCI_POP:9261,		MCI_REGION: MhgRegion.REGION_NE1	},
		'Muskegon':			{ MCI_POP:173043,	MCI_REGION: MhgRegion.REGION_W1		},
		'Newaygo':			{ MCI_POP:48142,	MCI_REGION: MhgRegion.REGION_W1		},
		'Oakland':			{ MCI_POP:1250843,	MCI_REGION: MhgRegion.REGION_E1		},
		'Oceana':			{ MCI_POP:26417,	MCI_REGION: MhgRegion.REGION_W1		},
		'Ogemaw':			{ MCI_POP:20928,	MCI_REGION: MhgRegion.REGION_NE3	},
		'Ontonagon':		{ MCI_POP:5968,		MCI_REGION: MhgRegion.REGION_SUP1	},
		'Osceola':			{ MCI_POP:23232,	MCI_REGION: MhgRegion.REGION_NW3	},
		'Oscoda':			{ MCI_POP:8277,		MCI_REGION: MhgRegion.REGION_NE2	},
		'Otsego':			{ MCI_POP:24397,	MCI_REGION: MhgRegion.REGION_NE1	},
		'Ottawa':			{ MCI_POP:284034,	MCI_REGION: MhgRegion.REGION_W2		},
		'Presque Isle':		{ MCI_POP:12797,	MCI_REGION: MhgRegion.REGION_NE1	},
		'Roscommon':		{ MCI_POP:23877,	MCI_REGION: MhgRegion.REGION_NE3	},
		'Saginaw':			{ MCI_POP:192778,	MCI_REGION: MhgRegion.REGION_E3		},
		'Sanilac':			{ MCI_POP:41376,	MCI_REGION: MhgRegion.REGION_E2		},
		'Schoolcraft':		{ MCI_POP:8069,		MCI_REGION: MhgRegion.REGION_SUP3	},
		'Shiawassee':		{ MCI_POP:68493,	MCI_REGION: MhgRegion.REGION_C2		},
		'St Clair':			{ MCI_POP:159566,	MCI_REGION: MhgRegion.REGION_E2		},
		'St Joseph':		{ MCI_POP:60897,	MCI_REGION: MhgRegion.REGION_W3		},
		'Tuscola':			{ MCI_POP:53250,	MCI_REGION: MhgRegion.REGION_E3		},
		'Van Buren':		{ MCI_POP:75272,	MCI_REGION: MhgRegion.REGION_W3		},
		'Washtenaw':		{ MCI_POP:365961,	MCI_REGION: MhgRegion.REGION_E1		},
		'Wayne':			{ MCI_POP:1761382,	MCI_REGION: MhgRegion.REGION_E1		},
		'Wexford':			{ MCI_POP:33111,	MCI_REGION: MhgRegion.REGION_NW2	} }

	# Constructor
    def __init__(self,stateName):
		pass

	#
	# Property Getters (public)
	#
	mhgRegion(countyName):
		return self.MICHIGAN_COUNTIES[countyName][MCI_REG]

	countyPopulation(countyName):
		return self.MICHIGAN_COUNTIES[countyName][MCI_POP]
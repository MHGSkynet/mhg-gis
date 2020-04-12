@echo off
::
:: ---------------------------------------------------------------------------------------------
:: mhgCovidFetch.bat
::
:: Description
::
::     Batch file to run mhgCovidFetch.py application 
:: 
:: Usage
::
::      mhgCovidFetch.bat [-h] [--start START] [--end END] [--ndays [NDAYS]] [--nodetail] [--nosummary] [--debug]
::
::      optional arguments:
::          -h, --help       show this help message and exit
::          --start START    Beginning date of range to select data by
::          --end END        End date of range to select data by
::          --ndays [NDAYS]  Number of days from begin date to select data by
::          --nodetail       Disables capture of detail to daily CSV files
::          --nosummary      Disables generation of daily summary info CSV file
::          --debug          Whether to barf debug info
::
::      Note:
::          dates may be entered mm/dd, mm/dd/yyyy or yyyy.mm.dd
::          nDays may be positive or negative.
::
::      Examples:
::          mhgCovidFetch.bat                                  # Run for today
::          mhgCovidFetch.bat --start 2020.04.03               # Run for specific date
::          mhgCovidFetch.bat --start 04/03 --end 04/06        # Run for a date range
::          mhgCovidFetch.bat --start 04/03 --ndays 7          # Run for week following start date given
::          mhgCovidFetch.bat --start 04/03/2020 --ndays -7    # Run for week prior to start date given
::          mhgCovidFetch.bat --ndays -7                       # Run for the past week
::
:: Copyright
::
::	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
::						non profit conservative organizations and individuals to use in support
::						of American freedom and the constitution. All other rights are reserved,
::						and any other use prohibited.
::  
:: Date        Version     Author          Description
:: 2020.04.06  02.00       SquintMHG       App rewrite, add command line arguments, etc
:: 2020.04.04  01.02       SquintMHG       Fix folders with spaces
:: 2020.03.26  01.00       SquintMHG       Initial version
:: ---------------------------------------------------------------------------------------------

:: echo mhgCovidFetch running...

call mhgCovidEnv.bat

if "%MHGGIS_ROOT%"=="" (
	echo "mhgCovidFetch.bat.ERROR: MHGGIS_ROOT environment variable not defined. Run mhgCovidEnv.bat"
	exit 1
)

python "%MHGGIS_ROOT%\covidStatus\mhgCovidStatus.py" %*

exit /B %ERRORLEVEL%
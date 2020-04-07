@echo off
::
:: ---------------------------------------------------------------------------------------------
:: mhgCovidStatus.bat
::
:: Description
::
::     Batch file to run Covid data fetch and report
:: 
:: Usage
::
::      mhgCovidStatus.bat [-h] [--start START] [--end END] [--ndays [NDAYS]] [--nodetail] [--nosummary] [--debug]
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
::          mhgCovidStatus.bat                                  # Run for today
::          mhgCovidStatus.bat --start 2020.04.03               # Run for specific date
::          mhgCovidStatus.bat --start 04/03 --end 04/06        # Run for a date range
::          mhgCovidStatus.bat --start 04/03 --ndays 7          # Run for week following start date given
::          mhgCovidStatus.bat --start 04/03/2020 --ndays -7    # Run for week prior to start date given
::          mhgCovidStatus.bat --ndays -7                       # Run for the past week
::  
::
:: Date        Version     Author          Description
:: 2020.04.07  01.03       SquintMHG       Rework to classes, refactor, add command line parameters
:: 2020.04.04  01.02       SquintMHG       Fix handling folders with embedded spaces
:: 2020.03.29  01.00       SquintMHG       Initial version
:: ---------------------------------------------------------------------------------------------

:: echo mhgCovidStatus running...

call mhgCovidEnv.bat

set MHGGIS_APPALIAS=mhgCovidStatus.bat

call "%MHGGIS_ROOT%\covidFetch\mhgCovidFetch.bat" %*

echo mhgCovidStatus::MHGGIS_FILTER_DATE=%MHGGIS_FILTER_DATE%

set MHGGIS_APPALIAS=


if %ERRORLEVEL% == 0 (
	call "%MHGGIS_ROOT%\covidReport\mhgCovidReport.bat" XMIT
)


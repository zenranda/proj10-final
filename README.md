# README #

###CS322 Project 10: Google Calendar; Free & Busy Times + Database Integration###
###Author: Marc Leppold###

##Project Notes

The tenth and final project in CS322. A program that reads the user's Google Calendar data, then constructs two lists: one with the times the user is busy, and one with the times the user isn't busy. These lists will be saved to a database. The user will then be given a URL to view their schedule at any time. Another user with the same URL can have their own free/busy times be added (injected) to the first user's and calculated, to generate mutual free times. There are thus two main uses: creating a schedule, or entering your data into another schedule. Their operation are as such:

-Creating a new schedule of free/busy times: Enter the index page, select a date/time range then authorize your Google Calendar data. The lists of free/busy times will be created, written to the database and displayed in sorted order. You'll then be given a URL with a database tag (6 alphanumeric characters) that identifies your schedule's database entry. You may then share this URL with other users to add to, or use it yourself to view your schedule remotely.

-Entering your own free/busy times into an existing schedule: Enter in the schedule's URL. Once you do, you'll be shown its current free/busy times. There will be a button to inject your own free/busy times into the schedule: click it, and the page will prompt you for a date/time range and Google Calendar authorization. Once it's all been entered, your busy times will be added to the existing schedule and the new (mutual) free times will be calculated and listed, as well as the additional busy times. The database will be written back to and future users who use the same URL will see the new times.

Requires internet access in order to transact with Google. Requires the user to have a valid Google account and calendar data on Google Calendars with busy appointments on them. Attempting to use this program with a Google account that has no calendars will result in nothing being returned.

Usage note: Hour ranges are from 0...23. Entering an hour that doesn't fit this range or that isn't an integer will cause an error. Repeatedly injecting the same calendar data into an existing schedule may have adverse effects. The date/time range of the first calendar will remain the date/time range of the calendar following subsequent injections; the injector's date/time selection is only for determining which of their calendar events to include.

Database notes: The database will be created anew and cleared of all entries whenever this program is run.

Requires client credentials and admin credentials, as well as an API key from Google; none are included in this repository and are only supplied in certain distributions of this program. The user must supply their own otherwise. Comes with nose tests for checking the free/busy calculation capabilities as well as fundamental database operation.

### USAGE ###

Execute the following commands
```
git clone https://github.com/zenranda/gcal2 InstallDirectory
cd InstallDirectory
. configure
make run
```
where InstallDirectory is the directory you cloned the files to.

Then while it's running, enter
```
HOST:PORT
```
into an internet browser to create a new schedule, where HOST is the host IP of the computer the program is running on and PORT is the port it's configured to (default 5000).

If you want to inject your calendar data into an existing schedule, enter
```
HOST:PORT/db/KEY
'''
where KEY is the database tag given to the creator of a new schedule.

Please note that this program requires an internet connection in order to recieve and send calendar info and authorization.

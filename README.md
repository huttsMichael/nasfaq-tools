# nasfaq-tools
Some basic tools for logging and analyzing data from NASFAQ

## Scripts
### logLeaderboard
Pull leaderboard and log it to a file (this file will get pretty big). Here's an [old log](https://files.catbox.moe/06uz2p.zip) if you want historical data

### parseLeaderboard
Plot the historical data from leaderboard.json
#### Commands:
##### --users
Plot multiple users instead of a single user
##### --lower
Specify the lower bounds of the users positions to plot
##### --upper
Specify the upper bounds of the users positions to plot
##### --positions
Plot the user(s) positions instead of their networth
##### --id
The userID to plot

### optimalDividends
Just divide the current price by the most recent dividend price. Doesn't currently do anything with older dividends' data or most importantly factor in growth/numbers. 

### catchUnprivated
Unfinished script for catching videos getting privated/unprivated using holotools' api. Would love for someone to get this working (probably with a rewrite)

### logGatcha / nasfaqCommon
Unfinished and probably dead part of project. Initially created as part rework of overall codebase, but current implimentation is working fine. I also think the API has been updated so this is less jank to do now.
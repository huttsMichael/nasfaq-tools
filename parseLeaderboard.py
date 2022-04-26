import argparse
import ujson
import matplotlib
import matplotlib.pyplot
import datetime
import sys
from shutil import copyfile
from logLeaderboard import getLeaderboard

TOP_USERS = False # graph multiple users
GRAPH_POSITIONS = False # chart positions instead of balance
USER_LOWER_RANGE = 0
USER_UPPER_RANGE = 9
USER_ID = ["ab69d48e-d029-4a5d-bf2d-f7544b3f3018"] # not me btw :^)
LEGEND = True
LOG = False

for arg in range(len(sys.argv)):    # this should be switched to argparse eventually
    if sys.argv[arg] == '--users':
        TOP_USERS = True
    elif sys.argv[arg] == '--positions':
        GRAPH_POSITIONS = True
    elif sys.argv[arg] == '--lower':
        USER_LOWER_RANGE = int(sys.argv[arg + 1]) - 1
    elif sys.argv[arg] == '--upper':
        USER_UPPER_RANGE = int(sys.argv[arg + 1])
    elif sys.argv[arg] == '--id':
        USER_ID = [sys.argv[arg + 1]]
    elif sys.argv[arg] == '--no-legend':
        LEGEND = False
    elif sys.argv[arg] == '--log':
        LOG = True


COLOR = "#666666"
matplotlib.rcParams['text.color'] = COLOR
matplotlib.rcParams['axes.labelcolor'] = COLOR
matplotlib.rcParams['xtick.color'] = COLOR
matplotlib.rcParams['ytick.color'] = COLOR
matplotlib.rc('font', family='Arial')

# create a copy of the leaderboard just incase 
print("copying file")
source_file = "leaderboard.json"
dest_file = "bk_leaderboard.json"
copyfile(source_file, dest_file)

print("modifying file")
with open(dest_file, 'rb+') as f:
    f.seek(0,2)                 # end of file
    size=f.tell()               # the size...
    f.truncate(size-1)          # truncate at that size - how ever many characters
with open(dest_file, 'a') as outfile:
    outfile.write('}')

print("loading json")
with open(dest_file) as f:
    leaderboard = ujson.load(f)

if TOP_USERS:
    print("getting users from", USER_LOWER_RANGE, "to", USER_UPPER_RANGE)
    userid_list = []
    moment_leaderboard = getLeaderboard()
    for user_index in range(USER_LOWER_RANGE, USER_UPPER_RANGE):
        print(moment_leaderboard[user_index]['username'])
        userid_list.append(moment_leaderboard[user_index]['userid'])

else:
    userid_list = USER_ID


print("graph time")

date_list = []
position_list = []
networth_list = []
username_list = []
for p in range(len(userid_list)):
    position_list.append([])
    networth_list.append([])
    username_list.append("")

for date in leaderboard:
    date_list.append(datetime.datetime.fromtimestamp(int(date)/1000))
    for position in range(len(leaderboard[date])):
        for index in range(len(userid_list)):
            if leaderboard[date][position]['userid'] == userid_list[index]:
                username_list[index] = leaderboard[date][position]['username']
                position_list[index].append(position)
                if GRAPH_POSITIONS:
                    networth_list[index].append(position)
                else:
                    networth_list[index].append(leaderboard[date][position]['networth'])
        

fig, ax = matplotlib.pyplot.subplots()
matplotlib.pyplot.grid(color="#29282c")
fig.patch.set_facecolor('#2e2d31')
ax.patch.set_facecolor('#2e2d31')
if LOG:
    ax.set_yscale('log')
else:
    ax.set_yscale('linear')

for user in range(len(userid_list)):
    if not TOP_USERS:
        try:
            ax.plot(date_list, networth_list[user], label=username_list[user], color="#4bc0c0")
        except:
            print("trying to fix " + userid_list[user])
            date_len = len(date_list)
            networth_len = len(networth_list[user])
            len_dif = date_len - networth_len
            ax.plot(date_list[len_dif:], networth_list[user], label=username_list[user])
        #ax.plot(date_list[1478:], networth_list[user][1478:], label=username_list[user])

    else:
        try:
            print(userid_list[user])
            ax.plot(date_list, networth_list[user], label=username_list[user])
        except:
            print("trying to fix " + userid_list[user])
            date_len = len(date_list)
            networth_len = len(networth_list[user])
            len_dif = date_len - networth_len
            ax.plot(date_list[len_dif:], networth_list[user], label=username_list[user])


date_fmt = '%m/%d/%y %H:%M'
date_formatter = matplotlib.dates.DateFormatter(date_fmt)
ax.xaxis.set_major_formatter(date_formatter)
ax.xaxis.set_major_locator(matplotlib.dates.DayLocator())
ax.xaxis.set_minor_locator(matplotlib.dates.HourLocator())
matplotlib.pyplot.gca()
fig.autofmt_xdate()
if LEGEND:
    matplotlib.pyplot.legend(prop={'size':10})
if GRAPH_POSITIONS:
    matplotlib.pyplot.gca().invert_yaxis()
matplotlib.pyplot.show()
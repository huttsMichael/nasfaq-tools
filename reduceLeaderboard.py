import json
from pprint import pprint
from shutil import copyfile

ORIGINAL_NAME = 'leaderboard.json'
REDUCED_NAME = 'leaderboard_reduced.json'
UNREDUCED_NAME = 'leaderboard_unreduced.json'
STEP_INTERVAL = 8

'''
simple script to reduce the size of leaderboard.json (mine reached 16GB)
'''

print(f"copying {ORIGINAL_NAME} to {UNREDUCED_NAME}")
copyfile(ORIGINAL_NAME, UNREDUCED_NAME)

print(f"opening {ORIGINAL_NAME} and extracting JSON")
with open(ORIGINAL_NAME, 'r') as leaderboard_original_file:
    leaderboard_data = json.load(leaderboard_original_file)

leaderboard_reduced = {}

# pprint(leaderboard_data)

step = STEP_INTERVAL
print(f"parsing leaderboard")
for capture_index, capture_timestamp in enumerate(leaderboard_data):
    
    if step == STEP_INTERVAL:
        leaderboard_reduced[capture_timestamp] = leaderboard_data[capture_timestamp]
        step = 1
        print(capture_timestamp, capture_index)
    else:
        step += 1

print(f"dumping to file")
with open(REDUCED_NAME, 'w') as leaderboard_reduced_file:
    json.dump(leaderboard_reduced, leaderboard_reduced_file)

print(f"all done!")



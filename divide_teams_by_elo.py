
# open the Teams_ELO.txt file and read the lines
with open("Teams_ELO.txt", "r") as f:
    lines = f.readlines()

# create a list to store the teams
teams = []

# create a list to store the teams with less than 30 games played
teams_with_less_than_30_games = []

# loop through the lines one by one (skipping the header line)
for line in lines[1:]:
    # get the current line and split it by |
    parts = line.split("|")
    # check if the current line has three parts (Team, ELO Rating, Games Played)
    if len(parts) == 3:
        # get the team, the ELO rating and the games played and strip them of whitespace
        team = parts[0].strip()
        elo = parts[1].strip()
        games_played = parts[2].strip()
        # try to convert the ELO rating and the games played to integers
        try:
            elo = int(float(elo))
            games_played = int(games_played)
        except ValueError:
            # if the conversion fails, skip this line
            continue
        # add the team and its ELO rating to the teams list as a tuple
        teams.append((team, elo))
        # check if the team has less than 30 games played
        if games_played < 30:
            # add the team to the teams_with_less_than_30_games list
            teams_with_less_than_30_games.append(team)

# sort the teams list by ELO rating in descending order
teams.sort(key=lambda x: x[1], reverse=True)

# choose the minimum and maximum number of members per group
min_members_per_group = 5
max_members_per_group = 9

# calculate the number of groups to divide the teams into
num_groups = len(teams) // ((min_members_per_group + max_members_per_group) // 2)

# create a list to store the groups
groups = []

# loop through the range from 0 to the number of groups
for i in range(num_groups):
    # create a list to store the current group
    group = []
    # loop through the range from 0 to the maximum number of members per group
    for j in range(max_members_per_group):
        # check if there are still teams left in the teams list
        if len(teams) > 0:
            # there are still teams left, pop the first team from the teams list and add it to the current group
            group.append(teams.pop(0))
    # add the current group to the groups list
    groups.append(group)

# check if there are still teams left in the teams list
if len(teams) > 0:
    # there are still teams left, add them to a new group and add it to the groups list
    groups.append(teams)

# loop through the groups one by one
for i, group in enumerate(groups):
    # print a header for the current group
    print(f"Group {i + 1}:")
    # create a list to store the team names for the current group
    team_names = []
    # loop through the teams in the current group one by one
    for team, elo in group:
        # add the team name to the team_names list
        team_names.append(team)
    # print the team_names list for the current group using your desired format
    print(f"team_names = {team_names}")

# print a header for teams with less than 30 games played
print("Teams with less than 30 games played:")
# print these teams using your desired format
print(f"team_names = {teams_with_less_than_30_games}")

# create a dictionary to store the ELO rating for each team
team_elo = {}
# create a constant to store the initial ELO rating
INITIAL_ELO = 1200


# create a function to calculate the expected score for each team based on their ELO ratings
def expected_score(r1, r2):
    # use the formula: E = 1 / (1 + 10 ^ ((R2 - R1) / 400))
    return 1 / (1 + 10 ** ((r2 - r1) / 400))


# create a function to update the ELO rating for each team based on the actual score and the expected score
def update_elo(r, s, e, K):
    # use the formula: R' = R + K * (S - E)
    # use a constant K
    return r + K * (s - e)


try:
    with open("Teams_ELO.txt", "r") as f:
        lines = f.readlines()
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
            # store the team and its ELO rating and games played in the team_elo dictionary as a tuple
            team_elo[team] = (elo, games_played)
        else:
            # the current line is not valid, skip it
            pass
except FileNotFoundError:
    # the Teams_ELO.txt file does not exist, do nothing
    pass

# open the battles_info.txt file and read the lines
with open("battles_info.txt", "r") as f:
    lines = f.readlines()
# loop through the lines one by one
for i in range(len(lines)):
    # get the current line and split it by whitespace
    line = lines[i]
    parts = line.split()
    # check if the current line has three parts (Team1 vs Team2)
    if len(parts) == 3:
        # get the teams
        team1 = parts[0]
        team2 = parts[2]
        # check if there is a next line
        if i + 1 < len(lines):
            # there is a next line, get it and strip it of whitespace
            next_line = lines[i + 1].strip()
            # check if the next line is Estevoleiro or Estevoleiro2
            if next_line == "Estevoleiro2":
                # the next line is the winner of the match, team1 won and team2 lost
                # set the actual score for team1 to 1 and for team2 to 0
                s1 = 1
                s2 = 0
            elif next_line == "Estevoleiro":
                # the next line is the winner of the match, team2 won and team1 lost
                # set the actual score for team1 to 0 and for team2 to 1
                s1 = 0
                s2 = 1
            else:
                # the next line is not valid, skip this match
                continue
        else:
            # there is no next line, skip this match
            continue

        # check if team1 exists in the team_elo dictionary
        if team1 in team_elo:
            # team1 exists, get its ELO rating and games played
            r1, games_played1 = team_elo[team1]
        else:
            # team1 does not exist, create it with the initial ELO rating and zero games played
            r1 = INITIAL_ELO
            games_played1 = 0
            team_elo[team1] = (r1, games_played1)
        # check if team2 exists in the team_elo dictionary
        if team2 in team_elo:
            # team2 exists, get its ELO rating and games played
            r2, games_played2 = team_elo[team2]
        else:
            # team2 does not exist, create it with the initial ELO rating and zero games played
            r2 = INITIAL_ELO
            games_played2 = 0
            team_elo[team2] = (r2, games_played2)
        # calculate the expected score for each team based on their ELO ratings
        e1 = expected_score(r1, r2)
        e2 = expected_score(r2, r1)
        # choose a value of K for each team based on their ELO rating and games played
        if r1 < 2000 and games_played1 < 30:
            # use a high value of K for teams that have less than 2000 ELO rating and less than 25 games played
            K1 = 200
        elif r1 < 2000 and games_played1 >= 30:
            # use a medium value of K for teams that have less than 2000 ELO rating and more than 25 games played
            K1 = 120
        else:
            # use a low value of K for teams that have more than 2000 ELO rating
            K1 = 80

        if r2 < 2000 and games_played2 < 30:
            # use a high value of K for teams that have less than 2000 ELO rating and less than 25 games played
            K2 = 200
        elif r2 < 2000 and games_played2 >= 30:
            # use a medium value of K for teams that have less than 2000 ELO rating and more than 25 games played
            K2 = 120
        else:
            # use a low value of K for teams that have more than 2000 ELO rating
            K2 = 80

        # update the ELO rating for each team using the chosen values of K
        r1_new = update_elo(r1, s1, e1, K1)
        r2_new = update_elo(r2, s2, e2, K2)
        # increment the games played for each team by one
        games_played1 += 1
        games_played2 += 1
        # store the new ELO ratings and games played in the team_elo dictionary as tuples
        team_elo[team1] = (r1_new, games_played1)
        team_elo[team2] = (r2_new, games_played2)
    else:
        # the current line is not valid, skip it
        pass

# open the Teams_ELO file and write the ELO rating and the games played for each team
with open("Teams_ELO.txt", "w") as f:
    # write a header line with the format: Team | ELO Rating | Games Played
    f.write("Team | ELO Rating | Games Played\n")
    # loop through the team_elo dictionary and write each team and its ELO rating and games played in a new line
    for team, (elo, games_played) in team_elo.items():
        f.write("{} | {} | {}\n".format(team, elo, games_played))
# close the Teams_ELO file
f.close()

import math
import os
import subprocess
import logging
import re  # import regular expression module

env_file_template1 = """BATTLE_BOT=safest
WEBSOCKET_URI=sim.smogon.com:8000
PS_USERNAME=Estevoleiro2
PS_PASSWORD={PS_PASSWORD}
BOT_MODE=CHALLENGE_USER
POKEMON_MODE=gen6anythinggoes
RUN_COUNT=1

USER_TO_CHALLENGE=Estevoleiro
TEAM_NAME=gen6/anythinggoes/{team_name}
SAVE_REPLAY=True"""

env_file_template2 = """BATTLE_BOT=safest
WEBSOCKET_URI=sim.smogon.com:8000
PS_USERNAME=Estevoleiro
PS_PASSWORD={PS_PASSWORD}
BOT_MODE=ACCEPT_CHALLENGE
POKEMON_MODE=gen6anythinggoes
RUN_COUNT=1

USER_TO_CHALLENGE=Estevoleiro2
TEAM_NAME=gen6/anythinggoes/{team_name}
SAVE_REPLAY=True"""

env_file1 = 'env'
env_file2 = 'env2'

#team_names = ['Annoying_Trainer', 'Low_Kick_Trainer', 'Surfiyama', 'Leader_Elesa', 'Leader_Winone', 'Mean_Beartic', 'Team_A_C_T',
#             'First_Route_Boss', 'Sabrina_HG', 'Saturn']
# team_names = ['First_Route_Boss', 'Leader_Roxanne', 'Leader_Chili', 'Little_Raid_Boss', 'Furret_Lover', 'Leader_Viola',
#                'Lick_Gengar', 'Little_Champion', 'Bridge_May', 'Original_Whitney', 'Togemetro', 'Surfiyama']
# team_names = ['AZ', 'N', 'Ghetsis', 'Wally', 'Giovanni', 'Paul', 'Ash_Ketchum', 'Diantha', 'Iris', 'Alder_Nerf',
#               'Trace', 'Cynthia', 'Wallace', 'Steven', 'Prof_Oak', 'Vinho_X', 'Lance', 'Red_Nerf', 'GreenBlue',
#               'Vinho_Gold_Sigma', 'Palmer', 'E4_Flint', 'E4_Drake', 'Brandon', 'Alain', 'Me', 'Kid_Me', 'Rayquaza',
#               'Mewtwo', 'PokeDan', 'TheAuraGuardian', 'Eryizo', 'Kangascloud', 'MysticUmbreon', 'Esteelvo', 'Vinho_Reborn',
#               'Disappointing_Trainer', 'Irene', 'Mean_Beartic', 'Team_A_C_T', 'May', 'Silver', 'Barry', 'Hugh', 'Tierno',
#               'Trevor', 'Lt_Surge_HG', 'Sabrina_HG', 'Misty', 'Brock_HG', 'Blaine_HG', 'Bridge_May', 'Leader_Elesa', 'Leader_Winone',
#               'Boss_Magikarp', 'Maxie', 'Archie', 'Cyrus', 'Saturn', 'Lysandre']
# team_names = ['Ghetsis', 'Diantha', 'Iris', 'Alder_Nerf',
#               'Cynthia', 'Wallace', 'Steven', 'Prof_Oak', 'Vinho_X', 'Lance', 'Red_Nerf', 'GreenBlue',
#               'Palmer', 'E4_Flint', 'E4_Drake', 'Brandon', 'Alain', 'Me',
#               'Mewtwo', 'Disappointing_Trainer', 'Irene']
team_names = ['Leader_Winone', 'Leader_Roxanne', 'Leader_Elesa', 'Little_Raid_Boss', 'Boss_Magikarp', 'Lick_Gengar', 'Togemetro',
              'Little_Champion', 'Bridge_May', 'Eryizo', 'Furret_Lover', 'Trevor', 'Maxie', 'Saturn', 'Annoying_Trainer', 'Original_Whitney', 'Leader_Chili', 'Mean_Beartic', 'Leader_Viola']




team_wins = {team: 0 for team in team_names}  # a dictionary that maps each team name to its number of wins
team_losses = {team: 0 for team in team_names}  # a dictionary that maps each team name to its number of losses
match_results = {}  # a dictionary that maps each pair of teams to their match result
# create a new dictionary to store the winner of each match
match_winners = {}


def run_battle(team1, team2, env_file1, env_file2, env_file_template1, env_file_template2, team_wins, team_losses,
               match_results, match_winners):
    """Runs a battle between two teams using docker and updates the dictionaries with the results.

    Args:
        team1 (str): The name of the first team.
        team2 (str): The name of the second team.
        env_file1 (str): The name of the env file for the first team.
        env_file2 (str): The name of the env file for the second team.
        env_file_template1 (str): The template for the env file for the first team.
        env_file_template2 (str): The template for the env file for the second team.
        team_wins (dict): A dictionary that maps each team name to its number of wins.
        team_losses (dict): A dictionary that maps each team name to its number of losses.
        match_results (dict): A dictionary that maps each pair of teams to their result (W or L).
        match_winners (dict): A dictionary that maps each pair of teams to their winner.

    Returns:
        tuple: A tuple of four dictionaries: team_wins, team_losses, match_results, and match_winners.
    """

    # set up env file for team1 vs team2
    with open(env_file1, 'w') as h:
        h.write(env_file_template1.format(team_name=team1))
    with open(env_file2, 'w') as h:
        h.write(env_file_template2.format(team_name=team2))
    with open('battles_info.txt', 'a+') as h:
        h.write(f"{team1} vs {team2}\n")
        h.close()

    # loop until a valid winner is found
    while True:
        # start bots for team1 vs team2
        p1 = subprocess.Popen(
            ['docker', 'run', '--rm', '-v', '/c/Users/monos/PycharmProjects/showdown:/app', '-w', '/app',
             '--env-file',
             env_file1, 'showdown'])
        p2 = subprocess.Popen(
            ['docker', 'run', '--rm', '-v', '/c/Users/monos/PycharmProjects/showdown:/app', '-w', '/app',
             '--env-file',
             env_file2, 'showdown'])

        # wait for bots to finish
        p1.wait()
        p2.wait()

        # read the battles_info.txt file and get the last line
        with open('battles_info.txt', 'r') as f:
            lines = f.readlines()
            winner = lines[-1].strip()  # get the last line and remove any whitespace
            f.close()

        # update the dictionaries with the winner of each match
        if winner == "Estevoleiro2":
            winner_team = team1
            team_wins[team1] += 1
            team_losses[team2] += 1
            match_results[(team1, team2)] = "W"
            match_results[(team2, team1)] = "L"
            match_winners[(team1, team2)] = team1
            break  # exit the loop
        elif winner == "Estevoleiro":
            winner_team = team2
            team_wins[team2] += 1
            team_losses[team1] += 1
            match_results[(team1, team2)] = "L"
            match_results[(team2, team1)] = "W"
            match_winners[(team1, team2)] = team2
            break  # exit the loop
        else:
            print(f"Invalid winner: {winner}. Re-running battle between {team1} and {team2}.")
            # continue the loop

    # return the winner team
    return winner_team


# import random module
import random

# ask the user which method they want to run
method = input("Input tournament type: 1 (Single-round League - longest), 2 (Fast Tournament), 3 (World Cup), 4(Swiss-Type Tournament): ")

# check if the input is valid
if method not in ["1", "2", "3", "4"]:
    print("Invalid input. Please enter 1, 2, 3 or 4.")
    exit()

# check if there are enough teams for a tournament
if method == "2" and len(team_names) < 16 or method == "3" and len(team_names) < 12:
    print("Sorry, not enough teams for this type of tournament. Running it in method 1.")
    method = "1"

if method == "1":
    for i, team1 in enumerate(team_names):
        for j, team2 in enumerate(team_names[i + 1:], start=i + 1):
            run_battle(team1, team2, env_file1, env_file2, env_file_template1, env_file_template2, team_wins,
                       team_losses, match_results, match_winners)

if method == "2" or method == "3":
    print('Tournament Starting!')

    # read the Teams_ELO.txt file and create a dictionary that maps each team to its ELO rating

    with open("Teams_ELO.txt", "r") as f:
        lines = f.readlines()

    # loop through the lines one by one (skipping the header line)
    team_elo = {}
    for line in lines[1:]:
        # get the current line and split it by |
        parts = line.split("|")
        # check if the current line has three parts (Team, ELO Rating, Games Played)
        if len(parts) == 3:
            # get the team, the ELO rating and the games played and strip them of whitespace
            team = parts[0].strip()
            elo = parts[1].strip()
            # try to convert the ELO rating and the games played to integers
            try:
                elo = int(float(elo))
            except ValueError:
                # if the conversion fails, skip this line
                continue
            # store the team and its ELO rating and games played in the team_elo dictionary as a tuple
            team_elo.update({team: elo})
        else:
            # the current line is not valid, skip it
            pass

    # assign a default ELO rating of 1200 to any team that is not in the Teams_ELO.txt file
    for team in team_names:
        if team not in team_elo:
            team_elo[team] = 1200

    # filter the team_elo dictionary by only keeping the keys in team_names
    filtered_team_elo = {key: team_elo[key] for key in team_names if key in team_elo}

    # sort the teams in descending order of their ELO ratings
    sorted_teams = sorted(filtered_team_elo.items(), key=lambda x: x[1], reverse=True)
    # get only the team names from the sorted_teams list
    sorted_teams = [x[0] for x in sorted_teams]
    print(sorted_teams)

    # divide the teams into four lists: one with the first quarter of the teams, one with the second quarter, one with the third quarter, and one with the fourth quarter
    n = len(sorted_teams) / 4
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    for i, team in enumerate(sorted_teams):
        # get the position of the team in the sorted_teams list
        position = i + 1
        # check which list it belongs to based on its position and n
        if position <= n:
            # append it to list1
            list1.append(team)
        elif position <= 2 * n:
            # append it to list2
            list2.append(team)
        elif position <= 3 * n:
            # append it to list3
            list3.append(team)
        else:
            # append it to list4
            list4.append(team)

    import math

    # determine the number of groups and the number of teams in each group
    num_teams = len(team_names)
    print("Number of teams: " + str(num_teams) + "\n")
    num_groups = 2 ** math.floor(math.log(num_teams // 4, 2)) # find the largest power of 2 that is less than or equal to the number of teams divided by 4
    print("Number of groups: " + str(num_groups) + "\n")
    teams_per_group = num_teams // num_groups # find the quotient of dividing the number of teams by the number of groups
    print("Teams per group: " + str(teams_per_group) + "\n")
    remainder = num_teams % num_groups # find the remainder of dividing the number of teams by the number of groups
    print("remainder: " + str(remainder) + "\n")

    # create a list to store the groups
    groups = [[] for _ in range(num_groups)] # initialize with empty lists

    # create a variable to keep track of the current group index
    group_index = 0

    # for each team, take one team from each list in order, and add it to the current group
    for _ in range(num_teams):
        # take one team from each list randomly and append it to the current group
        if list1:
            team1 = random.choice(list1)
            groups[group_index].append(team1)
            list1.remove(team1)
        if list2:
            team2 = random.choice(list2)
            groups[group_index].append(team2)
            list2.remove(team2)
        if list3:
            team3 = random.choice(list3)
            groups[group_index].append(team3)
            list3.remove(team3)
        if list4:
            team4 = random.choice(list4)
            groups[group_index].append(team4)
            list4.remove(team4)

        # update the group index to move to the next group
        group_index = (group_index + 1) % num_groups # use modulo to wrap around

    # if there is a remainder, add one more team from any of the lists randomly to any of the groups
    if remainder > 0:
        lists = [list1, list2, list3, list4]
        non_empty_lists = [l for l in lists if l] # filter out any empty lists
        while remainder > 0 and non_empty_lists: # while there is still a remainder and some teams left
            random_list = random.choice(non_empty_lists) # choose a random non-empty list
            extra_team = random.choice(random_list) # choose a random team from that list
            random_group = random.choice(groups) # choose a random group
            random_group.append(extra_team) # append it to the group
            random_list.remove(extra_team) # remove it from that list
            remainder -= 1 # decrement the remainder
            non_empty_lists = [l for l in lists if l] # update the non-empty lists

    # create a new txt file called tournament_info.txt and write some data to it
    with open('tournament_info.txt', 'w') as f:
        # write some header information
        f.write(f"Tournament Results\n")
        f.write(f"Number of teams: {len(team_names)}\n")
        f.write(f"Number of groups: {num_groups}\n")
        f.write(f"Number of teams per group: {num_teams}\n")
        f.write(f"\n")
        f.write("The groups are:\n")
        for i, group in enumerate(groups):
            f.write(f"Group {i + 1}: {group}\n")

        # import the random module and set a seed for reproducibility
        import random
        random.seed(42)

        # define a function to split a list into equal parts
        def split (a, n):
            k, m = divmod (len (a), n)
            return (a [i*k+min (i, m): (i+1)*k+min (i+1, m)] for i in range (n))

        # define a function to get the subgroup winners of a group
        def get_subgroup_winners(group, team_elo):
            num_subgroups = 2
            # divide the group into subgroups using the split function
            subgroups = split(group, num_subgroups)
            # create a list to store the winners of each subgroup
            subgroup_winners = []
            # loop over each subgroup
            for subgroup in subgroups:
                # run battles between all pairs of teams in this subgroup
                subgroup_wins = {team: 0 for team in subgroup}
                for j, team1 in enumerate(subgroup):
                    for k, team2 in enumerate(subgroup[j + 1:], start=j + 1):
                        winner = run_battle(team1, team2, env_file1, env_file2, env_file_template1, env_file_template2, team_wins,
                           team_losses, match_results, match_winners)
                        subgroup_wins[winner] += 1
                # find the team with the most wins in this subgroup
                sorted_teams = sorted(subgroup, key=lambda x: (subgroup_wins[x], -team_elo[x]), reverse=True)
                subgroup_winner = sorted_teams[0]
                # add the winner to the list of subgroup winners
                subgroup_winners.append(subgroup_winner)
            return subgroup_winners

        # define a function to get the top two teams of a group
        def get_top_two_teams(group, team_elo):
            # run battles between all pairs of teams in this group
            group_wins = {team: 0 for team in group}
            for j, team1 in enumerate(group):
                for k, team2 in enumerate(group[j + 1:], start=j + 1):
                    winner = run_battle(team1, team2, env_file1, env_file2, env_file_template1,
                                        env_file_template2,
                                        team_wins,
                                        team_losses,
                                        match_results,
                                        match_winners)
                    group_wins[winner] += 1
            # find the top two teams with the most wins in this group
            sorted_teams = sorted(group, key=lambda x: (group_wins[x], -team_elo[x]), reverse=True)
            top_two_teams = sorted_teams[:2]
            return top_two_teams


        # create a list to store the teams that advance to the knockout stage
        knockout_teams = []

        # loop over each group and get the winners of each subgroup or top two teams based on method variable
        for i, group in enumerate(groups):
            if method == "2":
                # get the winners of each subgroup
                winners = get_subgroup_winners(group, team_elo)
                # run a mini knockout round between the winners of each subgroup to determine which team advances to the main knockout phase
                knockout_winner = run_battle(winners[0], winners[1], env_file1,
                                             env_file2,
                                             env_file_template1,
                                             env_file_template2,
                                             team_wins,
                                             team_losses,
                                             match_results,
                                             match_winners)
                # add the winner to the knockout teams list
                knockout_teams.append(knockout_winner)
                f.write(f"Group {i + 1}\n")
                f.write("Subgroup Winners\n")
                for j, winner in enumerate(winners):
                    f.write(f"Subgroup {j + 1}: {winner}\n")
                f.write(f"Advancing to Knockout Stage: {knockout_winner}\n")
            elif method == "3":
                # get the top two teams of this group
                top_two_teams = get_top_two_teams(group, team_elo)
                # add these teams to the knockout teams list
                knockout_teams.extend(top_two_teams)
                f.write(f"Group {i + 1}\n")
                f.write("Top Two Teams\n")
                for j, winner in enumerate(top_two_teams):
                    f.write(f"Team {j + 1}: {winner}\n")
        f.write("\n")

        # create a list to store the pairs of teams that will play in each round of the knockout stage
        knockout_pairs = []

        # create the first round pairs by matching first-placed teams with second-placed teams from different groups
        first_placed_teams = knockout_teams[::2]
        second_placed_teams = knockout_teams[1::2]

        # create a list to store the indices of the second-placed teams that have already been matched
        matched_indices = []

        for i in range(len(first_placed_teams)):
            # get the index of the first-placed team in the knockout_teams list
            index1 = knockout_teams.index(first_placed_teams[i])
            # get the group number of this team
            group1 = index1 // 2

            # find a second-placed team from a different group
            for j in range(len(second_placed_teams)):
                # check if this second-placed team has already been matched
                if j not in matched_indices:
                    # get the index of the second-placed team in the knockout_teams list
                    index2 = knockout_teams.index(second_placed_teams[j])
                    # get the group number of this team
                    group2 = index2 // 2

                    # check if the two teams are from different groups
                    if group1 != group2:
                        # create a tuple of two teams
                        pair = (first_placed_teams[i], second_placed_teams[j])
                        # add it to the knockout pairs list
                        knockout_pairs.append(pair)
                        # add the index of the second-placed team to the matched_indices list
                        matched_indices.append(j)
                        break

        # loop over each round of the knockout stage until there is only one pair left
        round = 1
        while len(knockout_pairs) > 1:
            # create a list to store the winners of each match in this round
            round_winners = []

            # loop over each pair of teams in this round
            for pair in knockout_pairs:
                # get the team names from the pair
                team1 = pair[0]
                team2 = pair[1]

                winner = run_battle(team1, team2, env_file1, env_file2, env_file_template1, env_file_template2, team_wins,
                       team_losses, match_results, match_winners)
                # write the knockout match result to the file
                f.write(f"Round {round}: {team1} vs {team2}, Winner: {winner}\n")
                round_winners.append(winner)

            # create the next round pairs by randomly matching the winners of this round
            knockout_pairs = []
            for i in range(0, len(round_winners), 2):
                # get two random teams from the round winners list
                team1 = random.choice(round_winners)
                # remove it from the list
                round_winners.remove(team1)
                team2 = random.choice(round_winners)
                # remove it from the list
                round_winners.remove(team2)
                # append the pair to the knockout pairs list
                knockout_pairs.append((team1, team2))

            # increment the round number
            round += 1

        # get the final pair of teams
        final_pair = knockout_pairs[0]
        # get the team names from the pair
        team1 = final_pair[0]
        team2 = final_pair[1]

        winner = run_battle(team1, team2, env_file1, env_file2, env_file_template1, env_file_template2, team_wins,
                       team_losses, match_results, match_winners)

        # write the final match result and tournament winner to the file
        f.write(f"Final: {team1} vs {team2}, Winner: {winner}\n")
        f.write(f"Tournament Winner: {winner}\n")

if method == "4":
    print('Swiss Tournament Starting!')

    # read the Teams_ELO.txt file and create a dictionary that maps each team to its ELO rating
    with open("Teams_ELO.txt", "r") as f:
        lines = f.readlines()

    # loop through the lines one by one (skipping the header line)
    team_elo = {}
    for line in lines[1:]:
        # get the current line and split it by |
        parts = line.split("|")
        # check if the current line has three parts (Team, ELO Rating, Games Played)
        if len(parts) == 3:
            # get the team, the ELO rating and the games played and strip them of whitespace
            team = parts[0].strip()
            elo = parts[1].strip()
            # try to convert the ELO rating and the games played to integers
            try:
                elo = int(float(elo))
            except ValueError:
                # if the conversion fails, skip this line
                continue
            # store the team and its ELO rating and games played in the team_elo dictionary as a tuple
            team_elo.update({team: elo})
        else:
            # the current line is not valid, skip it
            pass

    # assign a default ELO rating of 1200 to any team that is not in the Teams_ELO.txt file
    for team in team_names:
        if team not in team_elo:
            team_elo[team] = 1200

    # filter the team_elo dictionary by only keeping the keys in team_names
    filtered_team_elo = {key: team_elo[key] for key in team_names if key in team_elo}

    # sort the teams in descending order of their ELO ratings
    sorted_teams = sorted(filtered_team_elo.items(), key=lambda x: x[1], reverse=True)
    # get only the team names from the sorted_teams list
    sorted_teams = [x[0] for x in sorted_teams]

    num_rounds = int(math.ceil(math.log2(len(sorted_teams)))) + 2  # calculate the number of rounds needed

    scores = {team: 0 for team in sorted_teams}  # initialize scores for each team

    no_opponent_count = {team: 0 for team in sorted_teams}  # initialize count of no opponent found for each team

    random.shuffle(sorted_teams)

    for round_num in range(num_rounds):
        print(f"Round {round_num + 1}")

        # sort teams by their current scores
        sorted_teams = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        sorted_teams = [x[0] for x in sorted_teams]

        matches = []  # list to store matches for this round

        while len(sorted_teams) > 0:
            # take first team from list
            t1 = sorted_teams.pop(0)

            # find opponent with similar score who hasn't played against t1 yet
            opponent_found = False
            for i, t2 in enumerate(sorted_teams):
                if (t1, t2) not in match_results and (t2, t1) not in match_results:
                    opponent_found = True
                    sorted_teams.pop(i)
                    matches.append((t1, t2))
                    break

            if not opponent_found:
                print(f"No opponent found for {t1}.")
                if no_opponent_count[t1] == 0:
                    scores[t1] += 1
                    no_opponent_count[t1] += 1

        for match in matches:
            winner = run_battle(match[0], match[1], env_file1, env_file2, env_file_template1, env_file_template2,
                                team_wins, team_losses, match_results, match_winners)
            scores[winner] += 1

    winner = max(scores.items(), key=lambda x: x[1])[0]
    print(f"Winner: {winner}")

    with open("tournament_info.txt", "w") as f:
        f.write("Tournament Results:\n")
        results = sorted(scores.items(), key=lambda x: (-x[1], filtered_team_elo[x[0]]))
        total_games = num_rounds - no_opponent_count[winner]
        for result in results:
            f.write(f"{result[0]}: ({result[1]}/{total_games})\n")

##########################################################################

# create a new txt file called matches_results.txt and write some data to it
with open('matches_results.txt', 'w') as f:
    # write the names of all the teams
    f.write("Names of all the teams:\n")
    for team in team_names:
        f.write(team + "\n")
    f.write("\n")

    # write the times each team has won
    f.write("Times each team has won:\n")
    for team in team_names:
        f.write("{}: {}\n".format(team, team_wins[team]))
    f.write("\n")

    # write the ranking of teams based on number of wins
    # sort the team_wins dictionary by its values in descending order
    team_ranking = sorted(team_wins.items(), key=lambda x: x[1], reverse=True)

    # write the ranking of teams to the matches_results.txt file
    f.write("Ranking of teams based on number of wins:\n")
    for rank, (team, wins) in enumerate(team_ranking, start=1):
        f.write("{}: {} ({} wins)\n".format(rank, team, wins))
    f.write("\n")

    # write the winning percentage for each team in a table format
    f.write(f"Team\tWinning Percentage\n")
    for team in team_names:
        # check if the team has played any matches
        if team_wins[team] + team_losses[team] > 0:
            # calculate the winning percentage as the ratio of wins to total matches
            winning_percentage = team_wins[team] / (team_wins[team] + team_losses[team])
        else:
            # assign a default value of zero to the winning percentage
            winning_percentage = 0
        # write the team name and the winning percentage to the file
        f.write(f"{team}\t{winning_percentage}\n")

    # create a variable to store the current number of wins
    current_wins = 0
    # create a variable to store the maximum number of wins
    max_wins = 0
    # create a variable to store the winner of the longest winning streak
    longest_streak_winner = None
    # create a variable to store the current team
    current_team = None
    # loop through the match_winners dictionary and get the winner of each game
    for (team1, team2), winner in match_winners.items():
        # if there is no winner, reset the current number of wins and team to None
        if winner is None:
            current_wins = 0
            current_team = None
        else:
            # otherwise, check if the winner is the same as the current team
            if winner == current_team:
                # if yes, increment the current number of wins by one
                current_wins += 1
            else:
                # if no, reset the current number of wins to one and update the current team
                current_wins = 1
                current_team = winner
            # if the current number of wins is greater than the maximum number of wins, update them and store the winner as well
            if current_wins > max_wins:
                max_wins = current_wins
                longest_streak_winner = winner
    # write the longest winning streak overall to matches_results.txt file
    f.write("The longest winning streak overall was {} games by {}.\n".format(max_wins, longest_streak_winner))
    f.write("\n")

    # create a dictionary to store the inconsistency score for each team
    team_inconsistency = {team: 0 for team in team_names}
    # loop through the match_winners dictionary and get the winner and loser of each matchup
    for (team1, team2), winner in match_winners.items():
        # if there is no winner, skip this matchup
        if winner is None:
            continue
        else:
            # otherwise, get the loser of this matchup
            loser = team1 if winner == team2 else team2
            # get the number of wins of the winner and loser based on the final ranking (the ranking is calculated based on the number of wins)
            winner_wins = [w for t, w in team_ranking if t == winner][0]
            loser_wins = [w for t, w in team_ranking if t == loser][0]
            # get the absolute value of the win difference
            win_diff = abs(winner_wins - loser_wins)
            # check if the winner has less wins than the loser (this means it was an upset and the winner was more inconsistent)
            if winner_wins < loser_wins:
                # add the win difference to the winner's inconsistency score
                team_inconsistency[winner] += win_diff
            # check if the loser has more wins than the winner (this means it was an upset and the loser was more inconsistent)
            if loser_wins > winner_wins:
                # add the win difference to the loser's inconsistency score
                team_inconsistency[loser] += win_diff
    # sort the team_inconsistency dictionary by its values in descending order
    team_inconsistency_ranking = sorted(team_inconsistency.items(), key=lambda x: x[1], reverse=True)
    # get the most inconsistent team based on the highest inconsistency score
    most_inconsistent_team = team_inconsistency_ranking[0][0]
    # write the most inconsistent team to matches_results.txt file
    f.write("The most inconsistent team was {} with an inconsistency score of {}.\n".format(most_inconsistent_team,
                                                                                            team_inconsistency[
                                                                                                most_inconsistent_team]))
    f.write("\n")

    # create a list to store the upsets as tuples of (rank difference, winner, loser)
    upsets = []
    # loop through the match_winners dictionary and get the winner and loser of each matchup
    for (team1, team2), winner in match_winners.items():
        # if there is no winner, skip this matchup
        if winner is None:
            continue
        else:
            # otherwise, get the loser of this matchup
            loser = team1 if winner == team2 else team2
            # get the ranks of the winner and loser based on the final ranking (the ranking is calculated based on the number of wins)
            winner_rank = [i for i, (t, w) in enumerate(team_ranking) if t == winner][0] + 1
            loser_rank = [i for i, (t, w) in enumerate(team_ranking) if t == loser][0] + 1
            # check if the winner has a lower rank than the loser (this means it was an upset)
            if winner_rank > loser_rank:
                # get the absolute value of the rank difference
                rank_diff = abs(winner_rank - loser_rank)
                # append this upset to the upsets list as a tuple of (rank difference, winner, loser)
                upsets.append((rank_diff, winner, loser))
    # sort the upsets list by its first element (rank difference) in descending order
    upsets.sort(key=lambda x: x[0], reverse=True)
    # get only the first 5 elements of the sorted list as the top 5 biggest upsets
    top_5_upsets = upsets[:5]
    # write the top 5 biggest upsets to matches_results.txt file using top_5_upsets list
    f.write("The top 5 biggest upsets were:\n")
    for i, (rank_diff, winner, loser) in enumerate(top_5_upsets, start=1):
        f.write("{}. {} vs {}: {} won (rank difference: {})\n".format(i, winner, loser, winner, rank_diff))
    f.write("\n")

    # improve the table of matchups by adding the name of the opponent in parentheses next to the result
    # write each row with the results of each matchup
    print(method)
    if method == 1:
        for i, team1 in enumerate(team_names):
            f.write("{:<15}".format(team1))  # write the team name with 15 spaces to align the table
            for j, team2 in enumerate(team_names):
                if i == j:  # if the teams are the same, write a dash
                    f.write("{:<15}".format("-"))
                else:  # otherwise, write the result of the matchup and the name of the opponent in parentheses
                    f.write("{:<15}".format(match_results[(team1, team2)] + " (" + team2 + ")"))
            f.write("\n")  # write a new line after each row

    # create a list to store the wheels as lists of teams
    wheels = []
    # create a graph to represent the match results as a dictionary of lists
    graph = {}
    # loop through the match_winners dictionary and get the winner and loser of each matchup
    for (team1, team2), winner in match_winners.items():
        # if there is no winner, skip this matchup
        if winner is None:
            continue
        else:
            # otherwise, get the loser of this matchup
            loser = team1 if winner == team2 else team2
            # add the winner and the loser to the graph as keys if they are not already there
            if winner not in graph:
                graph[winner] = []
            if loser not in graph:
                graph[loser] = []
            # add an edge from the winner to the loser in the graph
            graph[winner].append(loser)


    # create a function to find all cycles in the graph using depth-first search
    def find_cycles(graph):
        # create a list to store the cycles as lists of nodes
        cycles = []
        # create a set to store the visited nodes
        visited = set()

        # create a recursive helper function to perform depth-first search from a given node
        def dfs(node, path):
            # mark the node as visited
            visited.add(node)
            # loop through the neighbors of the node in the graph
            for neighbor in graph[node]:
                # check if the neighbor is the same as the first node in the path (this means we found a cycle)
                if neighbor == path[0]:
                    # append this cycle to the cycles list (make a copy of the path to avoid mutation)
                    cycles.append(path[:])
                # check if the neighbor is not visited and not already in the path (this means we can continue exploring)
                elif neighbor not in visited and neighbor not in path:
                    # append the neighbor to the path
                    path.append(neighbor)
                    # recursively call dfs on the neighbor with the updated path
                    dfs(neighbor, path)
                    # remove the neighbor from the path (backtracking)
                    path.pop()

        # loop through all the nodes in the graph
        for node in graph:
            # check if the node is not visited (this means we can start a new search from this node)
            if node not in visited:
                # create a list to store the current path
                path = [node]
                # call dfs on this node with the current path
                dfs(node, path)
        # return the cycles list
        return cycles


    # call find_cycles on the graph and store the result in a variable called cycles
    cycles = find_cycles(graph)
    # loop through each cycle in cycles
    for cycle in cycles:
        # check if the cycle has at least 5 nodes (this means it is a valid wheel)
        if len(cycle) >= 5:
            # append this wheel to wheels list (make a copy of cycle to avoid mutation)
            wheels.append(cycle[:])
    # sort wheels list by its length in descending order
    wheels.sort(key=len, reverse=True)
    # write wheels list to matches_results.txt file
    f.write("\n\nThe wheels were:\n")
    for wheel in wheels:
        f.write("{}\n".format(wheel))
    f.write("\n")

    # close the matches_results.txt file
    f.close()

# update ELO
subprocess.run(['python', 'team_elo_update.py'])

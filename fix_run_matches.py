# Assuming the battles_info.txt file has one or two lines per fight, with the format: Team1 vs Team2\nEstevoleiro/Estevoleiro2 (optional)

# Define the run function that takes two team names as arguments and returns the winner as Estevoleiro or Estevoleiro2
import subprocess

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

# import the math module for calculating the standard deviation
import math

# create a list of team names
team_names = ['AZ', 'N', 'Ghetsis', 'Wally', 'Giovanni', 'Paul', 'Ash_Ketchum', 'Diantha', 'Iris', 'Alder_Nerf',
              'Trace', 'Cynthia', 'Wallace', 'Steven', 'Prof_Oak', 'Vinho_X', 'Lance', 'Red_Nerf', 'GreenBlue',
              'Vinho_Gold_Sigma', 'Palmer', 'E4_Flint', 'E4_Drake', 'Brandon', 'Alain', 'Me', 'Kid_Me', 'Rayquaza',
              'Mewtwo', 'PokeDan', 'TheAuraGuardian', 'Eryizo', 'Kangascloud', 'Esteelvo', 'Vinho_Reborn',
              'Disappointing_Trainer', 'Irene', 'Mean_Beartic', 'Team_A_C_T']

# create a dictionary to store the number of wins for each team
team_wins = {team: 0 for team in team_names}

# create a dictionary to store the number of losses for each team
team_losses = {team: 0 for team in team_names}

# create a dictionary to store the result of each matchup as W, L, or -
match_results = {}

# create a dictionary to store the winner of each matchup or None if there is no winner
match_winners = {}


def run(team1, team2):
    # set up env file for team1 vs team2
    with open(env_file1, 'w') as f:
        f.write(env_file_template1.format(team_name=team1))
    with open(env_file2, 'w') as f:
        f.write(env_file_template2.format(team_name=team2))

    # start bots for team1 vs team2
    p1 = subprocess.Popen(
        ['docker', 'run', '--rm', '-v', '/c/Users/monos/PycharmProjects/showdown:/app', '-w', '/app', '--env-file',
         env_file1, 'showdown'])
    p2 = subprocess.Popen(
        ['docker', 'run', '--rm', '-v', '/c/Users/monos/PycharmProjects/showdown:/app', '-w', '/app', '--env-file',
         env_file2, 'showdown'])

    # wait for bots to finish
    p1.wait()
    p2.wait()

    # read the battles_info.txt file and get the last line
    with open('battles_info.txt', 'r') as f:
        lines = f.readlines()
        winner = lines[-1].strip()  # get the last line and remove any whitespace

    # delete the last two lines from the file
    with open('battles_info.txt', 'w') as f:
        f.writelines(lines[:-2])

    # return the winner as Estevoleiro or Estevoleiro2
    return winner


# Open the file and read the lines
with open("battles_info.txt", "r") as f:
    lines = f.readlines()

# Create a list to store the updated lines
updated_lines = []

# Loop through the lines one by one
for i in range(len(lines)):
    # Get the current line and split it by whitespace
    line = lines[i]
    parts = line.split()
    # Check if the current line has three parts (Team1 vs Team2)
    if len(parts) == 3:
        # Get the teams
        team1 = parts[0]
        team2 = parts[2]
        # Check if there is a next line
        if i + 1 < len(lines):
            # There is a next line, get it and strip it of whitespace
            next_line = lines[i + 1].strip()
            # Check if the next line is Estevoleiro or Estevoleiro2
            if next_line not in ["Estevoleiro", "Estevoleiro2"]:
                # The next line is invalid, run the fight and get the winner
                winner = run(team1, team2)
                # Update the next line with the winner
                next_line = winner + "\n"
            # Add the current line and the next line to the updated list
            updated_lines.append(line)
            updated_lines.append(next_line + "\n")
        else:
            # There is no next line, run the fight and get the winner
            winner = run(team1, team2)
            # Add a next line with the winner to the updated list
            updated_lines.append(line)
            updated_lines.append(winner + "\n")
    else:
        # The current line is invalid, ignore it
        pass

# Open the file and write the updated lines
with open("battles_info.txt", "w") as f:
    f.writelines(updated_lines)

# Loop through the updated lines again and update the dictionaries with the winner of each match
for i in range(len(updated_lines)):
    # Get the current line and split it by whitespace
    line = updated_lines[i]
    parts = line.split()
    # Check if the current line has three parts (Team1 vs Team2)
    if len(parts) == 3:
        # Get the teams
        team1 = parts[0]
        team2 = parts[2]
        # Check if there is a next line
        if i + 1 < len(updated_lines):
            # There is a next line, get it and strip it of whitespace
            next_line = updated_lines[i + 1].strip()
            # Check if the next line is Estevoleiro or Estevoleiro2
            if next_line == "Estevoleiro2":
                # The next line is the winner of the match, update the dictionaries accordingly
                team_wins[team1] += 1
                team_losses[team2] += 1
                match_results[(team1, team2)] = "W"
                match_results[(team2, team1)] = "L"
                match_winners[(team1, team2)] = team1  # store the winner of the match
            elif next_line == "Estevoleiro":
                # The next line is the winner of the match, update the dictionaries accordingly
                team_wins[team2] += 1
                team_losses[team1] += 1
                match_results[(team1, team2)] = "L"
                match_results[(team2, team1)] = "W"
                match_winners[(team1, team2)] = team2  # store the winner of the match
            else:
                # The next line is not the winner of the match, something went wrong, raise an exception
                raise ValueError("Invalid winner: {}".format(next_line))
        else:
            # There is no next line, something went wrong, raise an exception
            raise ValueError("Missing winner for match: {} vs {}".format(team1, team2))
    else:
        # The current line is not a match, ignore it
        pass

# Recalculate the stats using the updated dictionaries
with open('fixed_matches_results.txt', 'w') as f:
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

    # write the winning percentage of each team as I explained before
    f.write("The winning percentage of each team was:\n")
    for team in team_names:
        # calculate the winning percentage by dividing the number of wins by the number of games played
        winning_percentage = team_wins[team] / (team_wins[team] + team_losses[team])
        f.write("{}: {:.2f}\n".format(team, winning_percentage))
    f.write("\n")

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
    f.write("The most inconsistent team was {} with an inconsistency score of {}.\n".format(most_inconsistent_team, team_inconsistency[most_inconsistent_team]))
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


# open the file in read mode
with open("battles_info.txt", "r") as f:
    # read the lines as a list
    lines = f.readlines()
    # initialize an empty list to store the formatted lines
    formatted_lines = []
    # loop through the lines
    for line in lines:
        # strip the newline character
        line = line.strip()
        print(line)
        # if the line contains "vs"
        if "vs" in line:
            # split the line by "vs" and get the two teams
            team1, team2 = line.split("vs")
            # strip any whitespace from the teams
            team1 = team1.strip()
            team2 = team2.strip()
            # check if the team name starts with "Estevoleiro"
            if team1.startswith("Estevoleiro"):
                # check if the team name has a "2" after "Estevoleiro"
                if team1[11] == "2":
                    # append "Estevoleiro2" to the list
                    formatted_lines.append(f"Estevoleiro2\n")
                    # remove the "2" from the team name
                    team1 = team1[:11] + team1[12:]
                else:
                    # append "Estevoleiro" to the list
                    formatted_lines.append(f"Estevoleiro\n")
                # remove "Estevoleiro" from the team name
                team1 = team1[11:]
                # append the formatted line to the list
                formatted_lines.append(f"{team1} vs {team2}\n")
            else:
                # append the formatted line to the list
                formatted_lines.append(f"{team1} vs {team2}\n")
        # else if the line starts with "Estevoleiro"
        elif line.startswith("Estevoleiro"):
            # append the formatted line to the list
            formatted_lines.append(f"{line}\n")
        # else ignore the line

# open the file in write mode
with open("battles_info.txt", "w") as f:
    # write the formatted lines to the file
    f.writelines(formatted_lines)

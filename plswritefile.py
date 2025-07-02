import sys
winner = sys.argv[1]
with open('battles_info.txt', 'a+') as f:
    print("i'm here yoooooooo")
    f.write(winner + "\n")
    f.flush()

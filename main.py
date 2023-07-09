from fantasy import *

hand_list = ['GG','gg','1s','1c','13h','13c','11s','9s','9h','8s','7c','7d','5s','4s','3c','2h']

hand_list_2 = hand_list.copy()
print('input hands are:')
print(hand_list)

aaaa = get_all_fantasy_combo(hand_list)
print('combo of fantasy with trip in front are below................')
for a in aaaa:
    print(a)
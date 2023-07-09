import itertools    
from itertools import combinations
import time

def get_fantasy_hand(hand_list):
    # get list containing trips quads straight flush royal straight flush
    gost_count = 0
    gost_list = []
    # check gost num in hand
    for h in hand_list:
        if(h == 'gg' or h == 'GG'):
            gost_count = gost_count + 1
            gost_list.append(h)
    for g in gost_list:
        hand_list.remove(g)
    # compute fantasy possible hand in each circustances
    dup_list = []
    # count trip
    trip_list = []
    quad_list = []
    straight_flush_list = []
    royal_straight_flush_list = []
    for i in range(1,14):
        dup_count = 0
        for h in hand_list:
            if(i == int(h[0:len(h)-1])):
                dup_count = dup_count + 1
        a = [i,dup_count]
        dup_list.append(a)
    for dup in dup_list:
        if(dup[1] == 4):
            temp = []
            for h in hand_list:
                if(h[0:len(h)-1] == str(dup[0])):
                    temp.append(h)
            for t in temp:
                temp_copy = temp.copy()
                temp_copy.remove(t)
                trip_list.append(temp_copy)
        elif(dup[1]>= (3-gost_count)):
            temp = []
            for h in hand_list:
                if(h[0:len(h)-1] == str(dup[0])):
                    temp.append(h)
            if(len(temp) == 2):
                temp.append(gost_list[0])
            if(len(temp) == 1):
                temp.append(gost_list[0])          
                temp.append(gost_list[1])                      
            trip_list.append(temp)
    # count quads
    for dup in dup_list:
        if(dup[1]>=(4-gost_count)):
            temp = []
            for h in hand_list:
                if(h[0:len(h)-1] == str(dup[0])):
                    temp.append(h)
            if(len(temp) == 3):
                temp.append(gost_list[0])
            if(len(temp) == 2):
                temp.append(gost_list[0])          
                temp.append(gost_list[1])   
            quad_list.append(temp)
    # count straight flush
    straight_list = [1, 2, 3, 4, 5]
    flush_color_list = ['c','d','h','s']
    for i in range (1,10):
        for color in flush_color_list:
            new_list = [x+i-1 for x in straight_list]
            check_straight_flush_list = [str(n) + color for n in new_list]
            match_num = 0
            temp = []
            for e in check_straight_flush_list:
                if(e in hand_list):
                    match_num = match_num +1
                    temp.append(e)
            if(match_num >= (5-gost_count)):
                if(match_num == 4):
                    temp.append(gost_list[0])
                if(match_num == 3):
                    temp.append(gost_list[0])
                    temp.append(gost_list[1])
                straight_flush_list.append(temp)         
    # count royal straight flush 
    straight_list = [10,11,12,13,1]
    flush_color_list = ['c','d','h','s']
    for color in flush_color_list:
        check_royal_straight_flush_list = [str(n) + color for n in straight_list]
        match_num = 0
        temp = []
        for e in check_royal_straight_flush_list:
            if(e in hand_list):
                match_num = match_num +1
                temp.append(e)
        if(match_num >= (5-gost_count)):
            if(match_num == 4):
                temp.append(gost_list[0])
            if(match_num == 3):
                temp.append(gost_list[0])
                temp.append(gost_list[1])
            royal_straight_flush_list.append(temp)
    return [trip_list,quad_list,straight_flush_list,royal_straight_flush_list]

def get_max_hand_list(input_hand_list):
    original_input_list = input_hand_list.copy()
    max_hand_list = []
    max_royal_straight_flush_list = []
    max_straight_flush_list = []
    max_quad_list = []
    max_fullhouse_list = []
    max_trip_list = []
    max_pair_list = []
    gost_count = 0
    gost_list = []
    dup_list = []
    # check gost num in hand
    for h in input_hand_list:
        if(h == 'gg' or h == 'GG'):
            gost_count = gost_count + 1
            gost_list.append(h)
    for g in gost_list:
        input_hand_list.remove(g)
    # check royal straight flush
    flush_kinds = ['c','d','h','s']
    straight_list = [10, 11, 12, 13, 1]
    for flush in flush_kinds:
        royal_straight_flush_list = [str(n) + flush for n in straight_list]
        match_num = 0
        temp = []
        for item in royal_straight_flush_list:
            if(item in input_hand_list):
                match_num = match_num +1
                temp.append(item)
        if(match_num >= (5-gost_count)):
            if(match_num == 4):
                temp.append(gost_list[0])
            if(match_num == 3):
                temp.append(gost_list[0])
                temp.append(gost_list[1])
            max_royal_straight_flush_list.append([royal_straight_flush_list,temp])
    
    # check straight flush
    straight_list_num = [9 ,10 ,11 ,12 ,13]
    for flush in flush_kinds:
        for i in range(0,9):
            straight_flush_list = [str(n -i )+ flush for n in straight_list_num]
            match_num = 0
            temp = []
            for item in straight_flush_list:
                if(item in input_hand_list):
                    match_num = match_num +1
                    temp.append(item)
            if(match_num >= (5-gost_count)):
                if(match_num == 4):
                    temp.append(gost_list[0])
                if(match_num == 3):
                    temp.append(gost_list[0])
                    temp.append(gost_list[1])
                max_straight_flush_list.append([straight_flush_list,temp])
    # check quads
    for i in range(1,14):
        if( i == 1):
            cc = i
        else:
            cc = 15-i         
        dup_count = 0
        for h in input_hand_list:
            if(cc == int(h[0:len(h)-1])):
                dup_count = dup_count + 1
        a = [cc,dup_count]
        dup_list.append(a)

    for dup in dup_list:
        if(dup[1]>=(4-gost_count)):
            temp = []
            for h in hand_list:
                if(h[0:len(h)-1] == str(dup[0])):
                    temp.append(h)
            if(len(temp) == 3):
                temp.append(gost_list[0])
            if(len(temp) == 2):
                temp.append(gost_list[0])          
                temp.append(gost_list[1])   
            max_quad_list.append([[str(dup[0])]*4,temp])
    # check fullhouse
    dup_list = []
    trip_list = []
    ## count all card duplicate
    for i in range(1,14):
        if( i == 1):
            cc = i
        else:
            cc = 15-i    
        dup_count = 0
        for h in input_hand_list:
            if(cc == int(h[0:len(h)-1])):
                dup_count = dup_count + 1
        a = [cc,dup_count]
        dup_list.append(a)
    ## get trip list
    for dup in dup_list:
        if(dup[1]>=(3-gost_count)):
            temp = []
            for h in input_hand_list:
                if(h[0:len(h)-1] == str(dup[0])):
                    temp.append(h)
            if(len(temp) == 2):
                temp.append(gost_list[0])
            if(len(temp) == 1):
                temp.append(gost_list[0])          
                temp.append(gost_list[1])   
            max_trip_list.append([[str(dup[0])]*3,temp])
    ## get pair list
    for dup in dup_list:
        if(dup[1]>=(2-gost_count)):
            temp = []
            for h in input_hand_list:
                if(h[0:len(h)-1] == str(dup[0])):
                    temp.append(h)
            if(len(temp) == 1):
                temp.append(gost_list[0])          
            max_pair_list.append([[str(dup[0])]*2,temp])
    ## compute all pair combo
    pair_list = max_pair_list.copy()
    pair_combo_list_mix = []
    for pair in pair_list:
        if(len(pair[1]) == 2):
            pair_combo_list_mix.append(pair[1])
        else:
            temp = []
            for i in range(0,len(pair[1])):
                for j in range(0,len(pair[1])):
                    if j > i:
                        pair_combo_list_mix.append([pair[1][i],pair[1][j]])
    ## compute all trip combo
    trip_list = max_trip_list.copy()
    trip_combo_list_mix = []
    for trip in trip_list:
        if(len(trip[1]) == 3):
            trip_combo_list_mix.append(trip[1])
        else:
            temp = []
            for i in range(0,len(trip[1])):
                for j in range(0,len(trip[1])):
                    for k in range(0,len(trip[1])):
                        if ( j > i and k > j):
                            trip_combo_list_mix.append([trip[1][i],trip[1][j],trip[1][k]])
    ## combine fullhouse with trip and pair
    for trip_mix in trip_combo_list_mix:
        for pair_mix in pair_combo_list_mix:
            same_gost = False
            if('gg' in trip_mix and 'gg' in pair_mix):
                same_gost = True
            if('GG' in trip_mix and 'GG' in pair_mix):
                same_gost = True                
            trip_num = trip_mix[0][0:len(trip_mix[0])-1]
            pair_num = pair_mix[0][0:len(pair_mix[0])-1]
            if(trip_num != pair_num and not same_gost):
                h_list = [str(trip_num)]*3
                h_list.append(str(pair_num))
                h_list.append(str(pair_num))
                c_combo_list = trip_mix.copy()
                c_combo_list.append(pair_mix[0])
                c_combo_list.append(pair_mix[1])
                max_fullhouse_list.append([h_list,c_combo_list])
    # check flush
    flush_list = ['c','d','h','s']
    max_flush_list = []
    for flush in flush_list:
        match_flush_hand_list = []
        for hand in input_hand_list:
            hand_len = len(hand)
            hand_flush = hand[hand_len-1:hand_len]
            if(hand_flush == flush):
                match_flush_hand_list.append(hand)
        temp_flush_list = []
        all_flush_combination = list(combinations(match_flush_hand_list,5))
        for flush_combination in all_flush_combination:
            max_flush_list.append([[],flush_combination])   
        if(len(match_flush_hand_list) == 4 and len(gost_list)>=1):
            match_flush_hand_list.append(gost_list[0])
            max_flush_list.append([[],match_flush_hand_list])   
        if(len(match_flush_hand_list) == 3 and len(gost_list) >= 2):        
            match_flush_hand_list.append(gost_list[0])
            match_flush_hand_list.append(gost_list[1])
            max_flush_list.append([[],match_flush_hand_list])   
            

    # check straight
    straight_list = [1,2,3,4,5]
    max_straight_list = []
    for i in range(0,10):
        if(i == 9):
            temp_straight_list = [10,11,12,13,1]
        else:
            temp_straight_list =  [x+8-i for x in straight_list]
        straight_fit_num = 0
        miss_num_list = []

        for s in temp_straight_list:
            b = 15 -s -1
            if(b == 13):
                b =0
            if(dup_list[b][1] != 0):
                straight_fit_num = straight_fit_num +1
            else:
                miss_num_list.append(s)
        if(straight_fit_num == 4 and len(gost_list) == 1):
            for i in range(0,len(temp_straight_list)):
                if(temp_straight_list[i] in miss_num_list):
                    temp_straight_list[i] = gost_list[0]
        if(straight_fit_num == 3 and len(gost_list) == 2):
            for i in range(0,len(temp_straight_list)):
                if(temp_straight_list[i] in miss_num_list):
                    if('gg' in temp_straight_list):
                        temp_straight_list[i] = gost_list[1]
                    else:
                        temp_straight_list[i] = gost_list[0]
        straight_combo_list_all = []
        for stra_num in temp_straight_list:
            fit_hand_list = []
            for h in input_hand_list:
                if(stra_num ==  int(h[0:len(h)-1])):
                    fit_hand_list.append(h)
            straight_combo_list_all.append(fit_hand_list)
        
        all_stright_combination =    list(itertools.product(*straight_combo_list_all))
        for a in all_stright_combination:
            max_straight_list.append([temp_straight_list,a])



            
        
    # check trips
    aaaa= []
    for t in trip_combo_list_mix:
        num = t[0][0:len(t[0])-1]
        h_list = [str(num)]*3
        aaaa.append([h_list,t])

    # check two pairs
    max_two_pair_list = []
    two_pair_combo_list_mix = list(combinations(max_pair_list,2))
    for two_pair in two_pair_combo_list_mix:
        num_1 = two_pair[0][0:len(two_pair[0])-1][0][0]
        num_2 = two_pair[1][0:len(two_pair[1])-1][0][0]
        h_list = [str(num_1)]*4
        h_list[2] = num_2
        h_list[3] = num_2
        two_pair_b = two_pair[0][1]+two_pair[1][1]
        max_two_pair_list.append([h_list,two_pair_b]) 
    # check pair
    max_pair_list = []
    for pair in pair_combo_list_mix:
        num = pair[0][0:len(pair[0])-1]
        # print('pair',pair)
        h_list = [str(num)]*2
        max_pair_list.append([h_list,pair]) 
    max_hand_list.append(['royal_straight_flush',max_royal_straight_flush_list])
    max_hand_list.append(['straight_flush',max_straight_flush_list])
    max_hand_list.append(['quads',max_quad_list])
    max_hand_list.append(['fullhouse',max_fullhouse_list])
    max_hand_list.append(['flush',max_flush_list])
    max_hand_list.append(['straight',max_straight_list])
    max_hand_list.append(['trip',aaaa])
    max_hand_list.append(['two_pair',max_two_pair_list])
    max_hand_list.append(['pair',max_pair_list])

    return max_hand_list


# hand_list = ['GG','gg','1s','1c','13h','13c','11s','9s','9h','8s','7c','7d','5s','4s','3c','2h']
# hand_list_2 = hand_list.copy()
# print('input hands are:')
# print(hand_list)
# try to make fantasy
def get_all_fantasy_combo(hand_list):
    hand_list_2 = hand_list.copy()
    fan_pos_list = get_fantasy_hand(hand_list_2)

    #[trip_list,quad_list,straight_flush_list,royal_straight_flush_list]

    front_middle_last_list = []
    for i in range (0, 4):
        # fantasy with trip on first board
        if(i == 0):
            front = None
            trip_list = fan_pos_list[0]
            trip_list.reverse()
            b = []
            if(len(trip_list )== 0):
                continue
            if(trip_list[len(trip_list)-1][0][0] == '1'):
                a = trip_list [ len(trip_list)-1]
                trip_list.remove(a)
                b.append(a)
                for t in trip_list:
                    b.append(t)
            for trip in trip_list:
                trip_num = trip[0][0:len(trip[0])-1]
                front = [[str(trip_num)]*3 , trip]
                hand_list_copy = hand_list.copy()
                for t in trip:
                    if(t in hand_list_copy):
                        hand_list_copy.remove(t)
                left_hand_list = hand_list_copy
                max_hand_list_1 = get_max_hand_list(left_hand_list.copy())
                # max_hand_list 必須由大到小
                for j in range(0, len(max_hand_list_1)):
                    if(len(max_hand_list_1[j][1]) == 0):
                        continue
                    elif(j > 6):
                        continue
                    else:
                        for k in range(0,len(max_hand_list_1[j][1])):
                            if(j == 6 ):
                                current_trip = int(max_hand_list_1[j][1][k][0][0])
                                front_trip = int(trip[0][0:len(trip[0])-1])
                                if(front_trip > current_trip):                              
                                    continue
                            temp_hand_list = left_hand_list.copy()
                            temp_middle_hand = max_hand_list_1[j][1][k]

                            middle = temp_middle_hand
                            for temp_m in temp_middle_hand[1]:
                                if(temp_m in temp_hand_list):
                                    temp_hand_list.remove(temp_m)
                            left_hand_list_2 = temp_hand_list.copy()
                            max_hand_list_2 = get_max_hand_list(left_hand_list_2.copy())
                            for d in range(0, len(max_hand_list_2)):
                                if(len(max_hand_list_2[d][1]) == 0):
                                    continue
                                if(d > j):
                                    continue
                                # if(d == j):
                                # compare last and middle, if middle > last, continue
                                    # print('call function')
                                last = max_hand_list_2[d][1][0]
                                front_middle_last_list.append([front,middle,last])
                                #break
        else:
            other_fan_pos_list = fan_pos_list[i]
            #other_fan_pos_list.reverse()
            for fan_pos in other_fan_pos_list:
                last = fan_pos
                hand_list_copy = hand_list.copy()
                for f_hand in fan_pos:
                    if(f_hand in hand_list_copy):
                        hand_list_copy.remove(f_hand)
                left_hand_list = hand_list_copy
                max_hand_list_1 = get_max_hand_list(left_hand_list.copy())
                # max_hand_list 必須由大到小
                for j in range(0, len(max_hand_list_1)):
                    for k in range(0,len(max_hand_list_1[j][1])):
                        temp_middle = max_hand_list_1[j][1][k]
                        left_hand_list_2 = left_hand_list.copy()
                        for card_temp_middle in temp_middle[1]:
                            # print('j',j)
                            # print('k',k)
                            # print(temp_middle[1])
                            # print(card_temp_middle)
                            left_hand_list_2.remove(card_temp_middle)

                        max_hand_list_2 = get_max_hand_list(left_hand_list_2.copy())

                        all_hand_0 = True
                        for d in range(0, len(max_hand_list_2)):
                                if(len(max_hand_list_2[d][1]) == 0):
                                    continue
                                front = max_hand_list_2[d][1][0]
                                last_final = [[],last]
                                front_middle_last_list.append([front,temp_middle,last_final])
                        if(all_hand_0):
                            last_final = [[],last]
                            front = [left_hand_list_2[0],left_hand_list_2[1],left_hand_list_2[2]]
                            front_middle_last_list.append([front,temp_middle,last_final])
    #print('combo of fantasy with trip in front are below................')

    # for front in front_middle_last_list:
    #     print(front)
    return front_middle_last_list



    # compute max point hand






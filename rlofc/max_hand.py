import nums_from_string as nfs
from mysql.connector.cursor import MySQLCursor
from tool import screenshot, ocr_basic
from my_enum import *
from tool import *
from time import sleep, strftime
import re
import datetime
import uuid

class CardType(Enum):
    Nothing = 0
    A_high = 1
    Bottom_pair = 2
    Hand_pair_with_hat = 3
    Middle_pair = 4
    Top_pair = 5
    Top_pair_good_kicker = 6
    Top_pair_top_kicker = 7
    Over_pair = 8
    Two_bottom_pair = 9
    Two_middle_pair = 10
    Two_top_pair = 11
    Two_over_pair = 12
    Triples = 13
    Set = 14
    Straight = 15
    Flush = 16
    Fullhouse = 17
    Quads = 18
    Straight_flush = 19
    Royal_straight_flush = 20

def card_classification(card_list):
    global table_info
    public_card_0 = card_list[0]
    public_card_1 = card_list[1]
    public_card_2 = card_list[2]
    public_card_3 = card_list[3]
    public_card_4 = card_list[4]
    duplicate_card_list = [[], [], []]
    duplicate_interrupt = False
    duplicate_count = 0
    flush_list = []
    s_flush_list = []
    h_flush_list = []
    d_flush_list = []
    c_flush_list = []
    straight_list = []
    straight_biggest = ''
    straight_last_num = 0
    straight_interrupt = False
    gutter = 0
    double_ended = 0
    gutter_maybe = False
    frontdoor_flush_draw = 0
    backdoor_flush_draw = 0
    potential_flush_list = []
    potential_card_type = []

    cards = [public_card_0, public_card_1, public_card_2, public_card_3, public_card_4]
    temp_board_list = [public_card_0, public_card_1, public_card_2, public_card_3, public_card_4]
    temp_all_list = [public_card_0, public_card_1, public_card_2, public_card_3, public_card_4]
    card_length = 5
    # 花色
    for i, card in enumerate(cards):
        result = ''.join(re.findall(r'[A-Za-z]', card))
        if nfs.get_nums(card)[0] == 1:
            cards[i] = '14' + result
            temp_all_list[i] = '14' + result
            temp_board_list[i - 2] = '14' + result
        if result == 's':
            s_flush_list.append(card)
        elif result == 'h':
            h_flush_list.append(card)
        elif result == 'd':
            d_flush_list.append(card)
        elif result == 'c':
            c_flush_list.append(card)
    cards.sort(key=lambda c: nfs.get_nums(c)[0])

    for color_list in [s_flush_list, h_flush_list, d_flush_list, c_flush_list]:
        if len(color_list) >= 5:
            flush_list = color_list
        elif (len(color_list) >= 3) & (len(potential_flush_list) < 4):
            potential_flush_list = color_list

    if (len(potential_flush_list) == 4):
        frontdoor_flush_draw = 1

    # if (process == Process.Flop):
        # if (len(potential_flush_list) == 4):
        #     frontdoor_flush_draw = 1
        # elif (len(potential_flush_list) == 3):
        #     backdoor_flush_draw = 1
    # elif (process == Process.Turn):
    #     if (len(potential_flush_list) == 4):
    #         backdoor_flush_draw = 1
    
    # 數字
    for i in range(card_length - 1):
        dif = nfs.get_nums(cards[i])[0] - nfs.get_nums(cards[i + 1])[0]
            
        if dif == 0:
            if (duplicate_interrupt) & (len(duplicate_card_list[0]) != 0):
                duplicate_count += 1
                duplicate_interrupt = False
            if len(duplicate_card_list[duplicate_count]) == 0:
                duplicate_card_list[duplicate_count] = [cards[i], cards[i + 1]]
                duplicate_interrupt = False
            else:
                duplicate_card_list[duplicate_count].append(cards[i + 1])
                duplicate_interrupt = False

            if (straight_last_num != nfs.get_nums(cards[i + 1])[0]):
                if len(straight_list) < 5:
                    straight_list = []
                else:
                    straight_interrupt = True
        elif dif == -1:
            duplicate_interrupt = True

            if not straight_interrupt:
                if len(straight_list) == 0:
                    straight_list = [cards[i], cards[i + 1]]
                else:
                    straight_list.append(cards[i + 1])
                straight_last_num = nfs.get_nums(cards[i + 1])[0]
        elif dif == -2:
            duplicate_interrupt = True

            if gutter_maybe:
                if len(straight_list) == 3:
                    gutter += 2
                gutter_maybe = False
            else:
                gutter_maybe = True

            if len(straight_list) == 4:
                straight_num_list = []
                for temp in straight_list:
                    straight_num_list.append(nfs.get_nums(temp)[0])
                if (14 in straight_num_list):
                    gutter += 1
                else:
                    double_ended += 1
                straight_interrupt = True
            elif len(straight_list) < 5:
                straight_list = []
            else:
                straight_interrupt = True
        else:
            duplicate_interrupt = True

            if len(straight_list) == 4:
                straight_num_list = []
                for temp in straight_list:
                    straight_num_list.append(nfs.get_nums(temp)[0])
                if (14 in straight_num_list):
                    gutter += 1
                else:
                    double_ended += 1
                straight_interrupt = True
            elif len(straight_list) == 3:
                if gutter_maybe:
                    gutter += 1
                straight_interrupt = True
            elif len(straight_list) < 5:
                straight_list = []
            else:
                gutter_maybe = False
                straight_interrupt = True

    # 1234  123,5  12,45  1,345  1,345,7
    if len(straight_list) < 5:
        cards_num_list = []
        for temp in cards:
            cards_num_list.append(nfs.get_nums(temp)[0])
        if (14 in cards_num_list):
            temp_two = False
            temp_three = False
            temp_four = False
            temp_five = False
            temp_seven = False
            for temp in cards_num_list:
                if temp == 2:
                    temp_two = True
                elif temp == 3:
                    temp_three = True
                elif temp == 4:
                    temp_four = True
                elif temp == 5:
                    temp_five = True
                elif temp == 7:
                    temp_seven = True
            if (temp_two & temp_three & temp_four):
                gutter += 1
            elif (temp_two & temp_three & temp_five):
                gutter += 1
            elif (temp_two & temp_four & temp_five):
                gutter += 1
            elif (temp_three & temp_four & temp_five & temp_seven):
                gutter += 2
            elif (temp_three & temp_four & temp_five):
                gutter += 1

    duplicate_card_list.sort(key=lambda x: len(x), reverse=True)
    temp_board_list.sort(key=lambda x: nfs.get_nums(x)[0], reverse=True)
    temp_all_list.sort(key=lambda x: nfs.get_nums(x)[0], reverse=True)
    public_biggest_card = nfs.get_nums(temp_board_list[0])[0]
    all_biggest_card = nfs.get_nums(temp_all_list[0])[0]
    all_smallest_card = nfs.get_nums(temp_all_list[card_length - 1])[0]
    try:
        pair_num_0 = nfs.get_nums(duplicate_card_list[0][0])[0]
    except:
        pair_num_0 = 0
    try:
        pair_num_1 = nfs.get_nums(duplicate_card_list[1][0])[0]
    except:
        pair_num_1 = 0
    try:
        pair_num_2 = nfs.get_nums(duplicate_card_list[2][0])[0]
    except:
        pair_num_2 = 0
    # 確認順子中最大的牌 & A - 5這組
    if len(straight_list) >= 5:
        straight_biggest = straight_list[len(straight_list) - 1]
    elif (all_biggest_card == 14):
        new_straight_list = []
        for i in [2, 3, 4, 5, 14]:
            for temp in temp_all_list:
                if i == nfs.get_nums(temp)[0]:
                    new_straight_list.append(temp)
                    break
        if len(new_straight_list) == 5:
            straight_list = new_straight_list
            
    if double_ended == 1:
        potential_card_type.append(PotentialCardType.Double_ended)
    if gutter == 2:
        potential_card_type.append(PotentialCardType.Double_gutter)
    elif gutter ==1:
        potential_card_type.append(PotentialCardType.Gutter)
    if frontdoor_flush_draw == 1:
        potential_card_type.append(PotentialCardType.Frontdoor_flush_draw)
    if backdoor_flush_draw == 1:
        potential_card_type.append(PotentialCardType.Backdoor_flush_draw)
    if len(potential_card_type) == 0:
        potential_card_type.append(PotentialCardType.Nothing)

    # print('flush_list:', flush_list)
    # print('straight_list:', straight_list)
    # print('duplicate_card_list:', duplicate_card_list)
    # print('cards:', cards)
    # Royal straight flush & Straight flush
    if ((len(flush_list) >= 5) & (len(straight_list) >= 5)):
        if (len(duplicate_card_list[0]) == 2):
            if (duplicate_card_list[0][0] in straight_list):
                straight_list.append(duplicate_card_list[0][1])
            elif (duplicate_card_list[0][1] in straight_list):
                straight_list.append(duplicate_card_list[0][0])
        elif len(duplicate_card_list[0]) == 3:
            if (duplicate_card_list[0][0] in straight_list):
                straight_list.append(duplicate_card_list[0][1])
                straight_list.append(duplicate_card_list[0][2])
            elif (duplicate_card_list[0][1] in straight_list):
                straight_list.append(duplicate_card_list[0][0])
                straight_list.append(duplicate_card_list[0][2])
            elif (duplicate_card_list[0][2] in straight_list):
                straight_list.append(duplicate_card_list[0][0])
                straight_list.append(duplicate_card_list[0][1])
        elif len(duplicate_card_list[0]) == 4:
            if (duplicate_card_list[0][0] in straight_list):
                straight_list.append(duplicate_card_list[0][1])
                straight_list.append(duplicate_card_list[0][2])
                straight_list.append(duplicate_card_list[0][3])
            elif (duplicate_card_list[0][1] in straight_list):
                straight_list.append(duplicate_card_list[0][0])
                straight_list.append(duplicate_card_list[0][2])
                straight_list.append(duplicate_card_list[0][3])
            elif (duplicate_card_list[0][2] in straight_list):
                straight_list.append(duplicate_card_list[0][0])
                straight_list.append(duplicate_card_list[0][1])
                straight_list.append(duplicate_card_list[0][3])
            elif (duplicate_card_list[0][3] in straight_list):
                straight_list.append(duplicate_card_list[0][0])
                straight_list.append(duplicate_card_list[0][1])
                straight_list.append(duplicate_card_list[0][2])
        if len(duplicate_card_list[1]) == 2:
            if (duplicate_card_list[1][0] in straight_list):
                straight_list.append(duplicate_card_list[1][1])
            elif (duplicate_card_list[1][1] in straight_list):
                straight_list.append(duplicate_card_list[1][0])
        elif len(duplicate_card_list[1]) == 3:
            if (duplicate_card_list[1][0] in straight_list):
                straight_list.append(duplicate_card_list[1][1])
                straight_list.append(duplicate_card_list[1][2])
            elif (duplicate_card_list[1][1] in straight_list):
                straight_list.append(duplicate_card_list[1][0])
                straight_list.append(duplicate_card_list[1][2])
            elif (duplicate_card_list[1][2] in straight_list):
                straight_list.append(duplicate_card_list[1][0])
                straight_list.append(duplicate_card_list[1][1])

        straight_list.sort(key=lambda x: nfs.get_nums(x)[0], reverse=True)
        s, h, d, c = 0, 0, 0, 0
        for i in range(len(straight_list)):
            if (''.join(re.findall(r'[A-Za-z]', straight_list[i])) == 's'):
                s += 1
            elif (''.join(re.findall(r'[A-Za-z]', straight_list[i])) == 'h'):
                h += 1
            elif (''.join(re.findall(r'[A-Za-z]', straight_list[i])) == 'd'):
                d += 1
            elif (''.join(re.findall(r'[A-Za-z]', straight_list[i])) == 'c'):
                c += 1
        for color_count in [s, h, d, c]:
            if color_count >= 5:
                if (nfs.get_nums(straight_biggest)[0] == 14):
                    return CardType.Royal_straight_flush, potential_card_type
                else:
                    return CardType.Straight_flush, potential_card_type
    if (len(duplicate_card_list[0]) == 4):
        return CardType.Quads, potential_card_type
    # Fullhouse
    if (len(duplicate_card_list[0]) == 3) & (len(duplicate_card_list[1]) >= 2):
        if (len(duplicate_card_list[1]) == 3):
            if pair_num_0 > pair_num_1:
                return CardType.Fullhouse, potential_card_type
            else:
                return CardType.Fullhouse, potential_card_type
        return CardType.Fullhouse, potential_card_type
    # Flush
    if len(flush_list) >= 5:
        return CardType.Flush, potential_card_type
    # Straight
    if len(straight_list) >= 5:
        return CardType.Straight, potential_card_type
    # Triples or Set
    if (len(duplicate_card_list[0]) == 3):
        return CardType.Triples, potential_card_type
    # Two pair
    if (len(duplicate_card_list[0]) == 2) & (len(duplicate_card_list[1]) == 2):
        if (len(duplicate_card_list[2]) == 2):
            pair_num_0 = pair_num_1
            pair_num_1 = pair_num_2
        if (pair_num_1 >= all_biggest_card):
            return CardType.Two_top_pair, potential_card_type
        # 有兩張牌比自己大
        bigger_count = 0
        for c in temp_board_list:
            d  = nfs.get_nums(c[0])[0]
            if (pair_num_1 < d ):
                bigger_count += 1
        if bigger_count >= 2:
            return CardType.Two_bottom_pair, potential_card_type
        return CardType.Two_middle_pair, potential_card_type
    # One pair
    if (len(duplicate_card_list[0]) == 2):
        if (pair_num_0 >= all_biggest_card):
            return CardType.Top_pair, potential_card_type
        # 有兩張牌比自己大
        bigger_count = 0
        for c in temp_board_list:
            d  = nfs.get_nums(c[0])[0]
            if (pair_num_0 < d):
                bigger_count += 1
        if bigger_count >= 2:
            return CardType.Bottom_pair, potential_card_type
        return CardType.Middle_pair, potential_card_type
    # 其他
    return CardType.Nothing, potential_card_type

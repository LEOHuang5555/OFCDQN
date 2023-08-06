from treys import Card
import random
from .royalty_calculator import RoyaltyCalculator
from .ofc_evaluator import OFCEvaluator
from .fantasy import get_all_fantasy_combo, get_max_hand_list
import itertools


evaluator = OFCEvaluator()
all_cards = [
    '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', 'Ts', 'Js', 'Qs', 'Ks', 'As',
    '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', 'Th', 'Jh', 'Qh', 'Kh', 'Ah',
    '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', 'Td', 'Jd', 'Qd', 'Kd', 'Ad',
    '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', 'Tc', 'Jc', 'Qc', 'Kc', 'Ac']

class OFCHand(object):
    """An OFC street (back, mid, or front).
    Accepts a list of cards and new cards as strings.
    """
    def __init__(self, card_strs):
        # self.cards = [Card.new(x) for x in card_strs]
        self.cards = []

    def add_card(self, new_card_str):
        # self.cards.append(Card.new(new_card_str))
        self.cards.append(new_card_str)
        

    def length(self):
        return len(self.cards)

    def get_rank(self):
        return evaluator.evaluate(self.cards, [])


class OFCBoard(object):
    """Represent the three streets of an OFC game for one player."""
    

    def __init__(self):
        self.clear()

    def clear(self):
        self.front = OFCHand([])
        self.mid = OFCHand([])
        self.back = OFCHand([])

    def pretty(self):
        print('Front:')
        try:
            Card.print_pretty_cards(self.front.cards)
        except:
            print(self.front.cards)
        print('Mid:')
        try:
            Card.print_pretty_cards(self.mid.cards)
        except:
            print(self.mid.cards)
        print('Back:')
        try:
            Card.print_pretty_cards(self.back.cards)
        except:
            print(self.back.cards)

    def get_royalties(self):
        if not self.is_complete():
            return 0
        
        if self.is_foul():
            return 0

        royalty_total = \
            RoyaltyCalculator.score_front_royalties(self.front.cards) + \
            RoyaltyCalculator.score_mid_royalties(self.mid.cards) + \
            RoyaltyCalculator.score_back_royalties(self.back.cards)

        return royalty_total

    def get_free_streets(self):
        """Return a binary list of available streets, FMB."""
        available = [
            1 if self.front.length() < 3 else 0,
            1 if self.mid.length() < 5 else 0,
            1 if self.back.length() < 5 else 0
        ]

        return available

    def get_free_street_indices(self):
        available = []
        if self.front.length() < 3:
            available.append(0)
        if self.mid.length() < 5:
            available.append(1)
        if self.back.length() < 5:
            available.append(2)
        return available

    def place_card_by_id(self, card, street_id):
        if street_id == 0:
            self.front.add_card(card)
        if street_id == 1:
            self.mid.add_card(card)
        if street_id == 2:
            self.back.add_card(card)

    def place_card_by_fantasy_rule(self, card):
        cards = [tranfer_cards_fantasy(i) for i in card]
        # cards = ['GG','gg','1s','1c','13h','13c','11s','9s','9h','8s','7c','7d','5s','4s','3c','2h']
        all_combo = get_all_fantasy_combo(cards)
        if len(all_combo) > 0:
            try:
                all_combo = process_all_combos(all_combo, cards)
                best_score, self.front.cards, self.mid.cards, self.back.cards =  calculate_fantasy_score(all_combo[0])
                if len(all_combo) == 1 and not self.is_fantasy():
                    self.not_refantasy_rule(card)

            except:
                # 
                self.not_refantasy_rule(card)
            
            best_front = self.front.cards
            best_mid = self.mid.cards
            best_back = self.back.cards
            if self.mid.get_rank() < self.back.get_rank():
                print('change')
                temp = self.mid.cards.copy()
                self.mid.cards = self.back.cards
                self.back.cards = temp

            for i in range(1, len(all_combo)):
                if not self.is_fantasy():
                    continue

                score, self.front.cards, self.mid.cards, self.back.cards = calculate_fantasy_score(all_combo[i])
                if score > best_score and not self.is_foul():
                    best_score = score
                    best_front = self.front.cards
                    best_mid = self.mid.cards
                    best_back = self.back.cards
            
            self.front.cards = best_front
            self.mid.cards = best_mid
            self.back.cards = best_back

            if self.mid.get_rank() < self.back.get_rank():
                print('change')
                temp = self.mid.cards.copy()
                self.mid.cards = self.back.cards
                self.back.cards = temp
                


        else:
            # No fantasy combination
            self.front.cards, self.mid.cards, self.back.cards  = self.not_refantasy_rule(card)
            # maximize score of current cards
        
    def not_refantasy_rule(self, card):
        # self.front.cards, self.mid.cards, self.back.cards  = calculate_joker(card[:3], card[3:8], card[8:13])
        print('not fantasy rule')
        card_pools = list(set(all_cards) -set([tranfer_int_cards(i) for i in card]))
        res = {}
        # evaluator = ofc_evaluator
        best_score = 0
        best_lines = []
        # 需要替換的鬼牌索引
        wildcards = [i for i, hand in enumerate(card) if hand == 'GG' or hand == 'gg']

        # 將鬼牌從手牌中移除
        hands = [tranfer_int_cards(hand) for hand in card if hand != 'GG' and hand != 'gg']
        all_combinations = itertools.combinations(card_pools, len(wildcards))
        for replace_wild in all_combinations:
            new_hands = hands + list(replace_wild)
            # new_hands = [tranfer_cards_fantasy(i) for i in new_hands]
            back = get_max_hand_list([tranfer_cards_fantasy(i) for i in new_hands])

            for num, (back_kind, back_combo) in enumerate(back):
                if not back_combo:
                    continue
                for left_back, right_back in back_combo:
                    if not right_back:
                        continue

                    remaining_mid = list(set(new_hands) - set(right_back))
                    right_back = fill_hand(back_kind, left_back, right_back, remaining_mid)
                    remaining_mid = list(set(new_hands) - set(right_back))
                    mid = get_max_hand_list([tranfer_cards_fantasy(i) for i in remaining_mid])

                    for mid_num, (mid_kind, mid_combo) in enumerate(mid):
                        if not mid_combo:
                            continue
                        
                        for left_mid, right_mid in mid_combo:
                            if not right_mid:
                                continue
                            
                            remaining_front = list(set(remaining_mid) - set(right_mid))
                            right_mid = fill_hand(mid_kind, left_mid, right_mid, remaining_front)
                            remaining_front = list(set(remaining_mid) - set(right_mid))

                            for fronts in itertools.combinations(remaining_front, 3):
                                
                                front = get_max_hand_list([tranfer_cards_fantasy(i) for i in fronts])

                                for front_num, (front_kind, front_combo) in enumerate(front):
                                    if not front_combo:
                                        continue
                                    for left_front, right_front in front_combo:
                                        if not right_front:
                                            continue
                                        remaining_last = list(set(remaining_front) - set(right_front))
                                        right_front = fill_hand(front_kind, left_front, right_front, remaining_last, line='front')
                                        remaining_last = list(set(remaining_front) - set(right_front))
                                        total_score, lines = calculate_scores(right_back, right_mid, right_front)
                                        if total_score > best_score:
                                            best_score = total_score
                                            best_lines = lines
                                            res[best_score] = best_lines
        front = res[max(res.keys())][0]
        mid = res[max(res.keys())][1]
        back = res[max(res.keys())][2]
        
        try:
            front = [Card.new(i) for i in front]
            mid = [Card.new(i) for i in mid]
            back = [Card.new(i) for i in back]

        except:
            print(front)
            print(mid)
            print(back)

        return front, mid, back

    def is_complete(self):
        if self.back.length() == 5 and \
                self.mid.length() == 5 and \
                self.front.length() == 3:
            return True
        return False

    def is_foul(self):
        if not self.is_complete():
            return True

        if self.front.get_rank() > \
                self.mid.get_rank() > \
                self.back.get_rank():
        # if RoyaltyCalculator.score_front_royalties(self.front.cards) < \
        #         RoyaltyCalculator.score_mid_royalties(self.mid.cards) < \
        #         RoyaltyCalculator.score_back_royalties(self.back.cards):
            return False

        return True
    
    def is_fantasy(self):
        next_open = 0
        # if self.front.get_rank() > \
        #         self.mid.get_rank() > \
        #         self.back.get_rank():
        # if RoyaltyCalculator.score_front_royalties(self.front.cards) < \
        #         RoyaltyCalculator.score_mid_royalties(self.mid.cards) < \
        #         RoyaltyCalculator.score_back_royalties(self.back.cards):
            
        if self.front.get_rank() < 2468.0:
            # 2468: 222 three of a kind. 
            next_open = 17
        
        elif self.front.get_rank() <= 3985.899 and self.front.get_rank() > 3765.8889:
            # 3985.899: QQ pair + 2c
            # 3765.8889: KK pair + 2c
            next_open = 14

        elif self.front.get_rank() <= 3765.8889 and self.front.get_rank() > 3545.8788:               
            # 3765.8889: KK pair + 2c
            # 3545.8788: AA pair + 2c
            next_open = 15
        
        elif self.front.get_rank() <= 3545.8788 and self.front.get_rank() > 2468.0:
            # 3545.8788: AA pair + 2c 
            # 2468.0: 222 three of a kind.
            next_open = 16
        
        else:
            pass

        if next_open > 0 and self.mid.get_rank() > self.back.get_rank():
            return next_open
        
        return 0
    
    def is_refantasy(self):
        next_open = 0
        if self.front.get_rank() < 2468.0 and self.mid.get_rank() > self.back.get_rank():
            # 2468: 222 three of a kind. 
            next_open = 17

        if self.mid.get_rank() < 1000 or self.back.get_rank() < 1000:
            next_open = 17
        
        return next_open
    
# def is_burst(front, mid, back):
#     front_score
#     if front.get_rank() >= \
#         self.mid.get_rank() >= \
#         self.back.get_rank():
#         return False

#     return True

def tranfer_cards_fantasy(x):
    if 'K' in x:
        res = x.replace('K', '13')
    elif 'Q' in x:
        res = x.replace('Q', '12')
    elif 'J' in x:
        res = x.replace('J', '11')
    elif 'T' in x:
        res = x.replace('T', '10')
    elif 'A' in x:
        res = x.replace('A', '1')
    else:
        res = x
    return res

def tranfer_int_cards(x):
    if '13' in x:
        res = x.replace('13', 'K')
    elif '12' in x:
        res = x.replace('12', 'Q')
    elif '11' in x:
        res = x.replace('11', 'J')
    elif '10' in x:
        res = x.replace('10', 'T')
    elif '1' in x:
        res = x.replace('1', 'A')
    else:
        res = x
    return res

def calculate_joker(front, mid, back):
    # jocker in the front line
    if 'gg' in front or 'GG' in front:
        if 'gg' in mid or 'GG' in mid:
            mid = get_max_hand(mid, back)
            front = get_max_hand(front, mid)
        else:
            front = get_max_hand(front, mid)

    # jocker in the middle line
    if 'gg' in mid or 'GG' in  mid:
        if 'gg' in back or 'GG' in back:
            back = get_max_hand(back, ['Ts', 'Js', 'Qs', 'Ks', 'As'])
            mid = get_max_hand(mid, back)
        else:
            mid = get_max_hand(mid ,back)

    # jocker in the back line
    if 'gg' in back or 'GG' in back:
        try:
            back = get_max_hand(back, ['Ts', 'Js', 'Qs', 'Ks', 'As'])
        except:
            print(back)
    
    try:
        front = [Card.new(i) for i in front]
        mid = [Card.new(i) for i in mid]
        back = [Card.new(i) for i in back]
    except:
        print(front)
        print(mid)
        print(back)
    
    return front, mid, back

def calculate_fantasy_score(board):

    front = [tranfer_int_cards(i) for i in board[0]]
    mid = [tranfer_int_cards(i) for i in board[1]]
    back = [tranfer_int_cards(i) for i in board[2]]
    front, mid, back = calculate_joker(front, mid, back)

    front_score = evaluator.evaluate([], front)
    mid_score = evaluator.evaluate([], mid)
    back_score = evaluator.evaluate([], back)
    score = front_score + mid_score + back_score

    return score, front, mid, back

def bigger_or_not(current_hand_list,max_hand_list):
    current_hand_score = evaluator.evaluate([],[Card.new(i) for i in current_hand_list])
    max_hand_score = evaluator.evaluate([],[Card.new(i) for i in max_hand_list])
    if current_hand_score < max_hand_score:
        return True
    else:
        return False

def smaller_or_not(current_hand_list, limit_hand_list):
    current_hand_score = evaluator.evaluate([],[Card.new(i) for i in current_hand_list])
    limit_hand_score = evaluator.evaluate([],[Card.new(i) for i in limit_hand_list])
    if current_hand_score > limit_hand_score:
        return True
    else:
        return False

def get_max_hand(input_hand_list, limit_hand_list):
    hand_list = input_hand_list.copy()
    gost_list = []
    for hand in hand_list:
        if(hand == 'GG' or hand == 'gg'):
            gost_list.append(hand)

    if 'gg' in hand_list:
        hand_list.remove("gg")
    
    if 'GG' in hand_list:
        hand_list.remove("GG")

    # all_cards = [
    # '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', 'Ts', 'Js', 'Qs', 'Ks', 'As',
    # '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', 'Th', 'Jh', 'Qh', 'Kh', 'Ah',
    # '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', 'Td', 'Jd', 'Qd', 'Kd', 'Ad',
    # '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', 'Tc', 'Jc', 'Qc', 'Kc', 'Ac']

    if(len(gost_list) == 1):
        max_hand_list = ['2c','3c','4c','5c','7d']
        for h in all_cards:
            if(h in hand_list):
                continue
            a_list = hand_list.copy()
            a_list.append(h)
            #print(a_list)
            #print(max_hand_list)
            #print(bigger_or_not(a_list,max_hand_list))
            if(bigger_or_not(a_list,max_hand_list) and smaller_or_not(a_list,limit_hand_list)):
                #print(a_list)
                max_hand_list = a_list
        return max_hand_list
    elif(len(gost_list) == 2):
        max_hand_list = ['2c','3c','4c','5c','7d']
        for h in all_cards:
            for h1 in all_cards:
                if(h in hand_list or h1 in hand_list):
                    continue
                if(h == h1):
                    continue
                a_list = hand_list.copy()
                a_list.append(h)
                a_list.append(h1)
                # print(a_list)
                if(bigger_or_not(a_list,max_hand_list) and smaller_or_not(a_list,limit_hand_list)):
                    # print(a_list)
                    max_hand_list = a_list
        return max_hand_list
    
def process_all_combos(combos, hand_list):
    new_all_combo = []
    for i in range(len(combos)):
        on_hands = list(combos[i][0][1])+list(combos[i][1][1])+list(combos[i][2][1])
        remaining_list = list(set(hand_list).difference(set(on_hands)))
        front = list(combos[i][0][1])
        mid = list(combos[i][1][1])
        back = list(combos[i][2][1])
        front_elem_len = list(map(lambda x: True if len(x) < 2 else False, front))
        mid_elem_len = list(map(lambda x: True if len(x) < 2 else False, front))
        back_elem_len = list(map(lambda x: True if len(x) < 2 else False, front))
        
        if any(front_elem_len) or any(mid_elem_len) or any(back_elem_len):
            continue

        if len(front) > 3:
            continue

        elif len(front) < 3:
            
            times = 3-len(front)
            for time in range(times):
                fill = random.choice(remaining_list)
                remaining_list.remove(fill)
                front.append(fill)

        if len(mid) > 5:
            continue

        elif len(mid) < 5:
            times = 5-len(mid)
            for time in range(times):
                fill = random.choice(remaining_list)
                remaining_list.remove(fill)
                mid.append(fill)
        
        if  len(back) > 5:
            continue

        elif len(back) < 5:
            times = 5-len(back)
            for time in range(times):
                fill = random.choice(remaining_list)
                remaining_list.remove(fill)
                back.append(fill)
        
        new_all_combo.append([front, mid, back])
    return new_all_combo

def maximize_score(all_hands):
    cards = get_max_hand_list(all_hands)
    for kind in range(len(cards)):
        # if there is no possibility for the certain kind, then next.
        if not cards[kind][1]:
            continue
        for combo in range(len(cards[kind][1])):
            if cards[kind][1][combo][1]:
                remaining_cards = list(set(all_hands).difference(set(cards[kind][1][combo][1])))
                
    return remaining_cards

def calculate_scores(back, mid, front):
    back_line = [Card.new(tranfer_int_cards(i)) for i in back]
    back_rank = evaluator.evaluate([], back_line)
    back_score = RoyaltyCalculator.score_back_royalties(back_line)

    mid_line = [Card.new(tranfer_int_cards(i)) for i in mid]
    mid_rank = evaluator.evaluate([], mid_line)
    mid_score = RoyaltyCalculator.score_mid_royalties(mid_line)

    front_line = [Card.new(tranfer_int_cards(i)) for i in front]
    front_rank = evaluator.evaluate([], front_line)
    front_score = RoyaltyCalculator.score_front_royalties(front_line)

    if front_rank > mid_rank > back_rank:
        total_score = front_score + mid_score + back_score
    else:
        # foul
        total_score = 0

    return total_score, [front, mid, back]

def fill_hand(kind, left_card, right_card, pools, line = 'back'):
    # all_cards = [
    # '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', 'Ts', 'Js', 'Qs', 'Ks', 'As',
    # '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', 'Th', 'Jh', 'Qh', 'Kh', 'Ah',
    # '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', 'Td', 'Jd', 'Qd', 'Kd', 'Ad',
    # '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', 'Tc', 'Jc', 'Qc', 'Kc', 'Ac']
    suits = ['s', 'h', 'd', 'c']
    all_hands = [tranfer_int_cards(i) for i in pools]
    left_card = [tranfer_int_cards(str(i)) for i in left_card]
    right_card = [tranfer_int_cards(i) for i in right_card]
        
    if kind in ['royal_straight_flush', 'straight_flush'] and len(right_card) == 5:
        # get left 
        return left_card
    
    elif kind == 'quads':
        # pick anyone from the pool, except the number already in the hand.
        pattern = itertools.Counter(left_card)
        pool = [i for i in all_hands if i[0] not in pattern]
        pick_one = random.sample(pool, k = 1)
        res = right_card + pick_one

    elif kind == 'fullhouse' and len(right_card) ==5:
        
        return right_card
            

    elif kind == 'flush':
        if len(right_card) < 5:
            one_suit = right_card[0][-1]
            pick_cards = random.sample([i for i in all_cards if one_suit in i and i not in right_card], k = 5-len(right_card))
            res = right_card + pick_cards
        else:
            return right_card

    elif kind == 'straight':

        return right_card

    elif kind == 'trip' and len(right_card)==3:
        if line == 'front':
            return right_card
        
        pattern = set(left_card)
        trip = [i for i in right_card if i[0] in pattern]
        pool = [i for i in all_hands if i[0] not in pattern]
        pick2 = random.choices(pool, k=2)
        while pick2[0][:-1]==pick2[1][:-1]:
            # pick again
            pick2 = random.sample(pool, k=2)

        res = trip + pick2

    elif kind == 'two_pair':
        pattern = list(set(left_card))
        pool = [i for i in all_hands if i[0] not in pattern]
        pick_one = random.sample(pool, k = 1)
        if len(right_card) > 4:
            pair_1s = [i for i in right_card if i[0] in pattern[0]]
            pair_2s = [i for i in right_card if i[0] in pattern[1]]
            try: 
                pair_1 = random.sample(pair_1s, k = 2)
            except:
                pair_1 = pair_1s
                
            try: 
                pair_2 = random.sample(pair_2s, k = 2)
            except:
                pair_2 = pair_2s

            res = pair_1 + pair_2 + pick_one
            
        else:
            res = right_card + pick_one

        
    elif kind == 'pair' and len(right_card) == 2:
        pattern = set(left_card)
        pool = [i for i in all_hands if i[0] not in pattern]
        if len(pool) == 0:
            pool = all_hands

        if line == 'front':
            pick1 = random.sample(pool, k = 1)
            res = right_card + pick1

        else:
            pick3 = random.sample(pool, k = 3)
            res = right_card + pick3

    else:
        # high card
        if line == 'front':

            res = random.sample(right_card+all_hands, k=3)
        else:
            res = random.sample(right_card+all_hands, k=5)
        
    return res
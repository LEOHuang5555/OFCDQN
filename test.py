from treys import Card, Evaluator

evaluator = ofc_evaluator.OFCEvaluator()

def bigger_or_not(current_hand_list,max_hand_list):
    current_hand_score = evaluator.evaluate([],current_hand_list)
    max_hand_score = evaluator.evaluate([],max_hand_list)
    if current_hand_score > max_hand_score:
        return True
    else:
        return False

def smaller_or_not(current_hand_list,limit_hand_list):
    current_hand_score = evaluator.evaluate([],current_hand_list)
    limit_hand_score = evaluator.evaluate([],limit_hand_list)
    if current_hand_score < limit_hand_score:
        return True
    else:
        return False

def get_max_hand(input_hand_list,limit_hand_list):
    hand_list = input_hand_list.copy()
    gost_list = []
    for hand in hand_list:
        if(hand == 'G' or hand == 'g'):
            gost_list.append(hand)
    hand_list.remove("g")
    hand_list.remove("G")
    all_cards = [
    '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', 'Ts', 'Js', 'Qs', 'Ks', 'As',
    '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', 'Th', 'Jh', 'Qh', 'Kh', 'Ah',
    '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', 'Td', 'Jd', 'Qd', 'Kd', 'Ad',
    '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', 'Tc', 'Jc', 'Qc', 'Kc', 'Ac']
    if(len(gost_list) == 1):
        max_hand_list = ['2c','3c','4c','5c','7d']
        for h in all_cards:
            a_list = hand_list.copy()
            a_list.append(h)
            if(bigger_or_not(a_list,max_hand_list) and smaller_or_not(a_list,limit_hand_list)):
                max_hand_list = a_list
        return max_hand_list
    elif(len(gost_list) == 2):
        max_hand_list = ['2c','3c','4c','5c','7d']
        for h in all_cards:
            for h1 in all_cards:
                a_list = hand_list.copy()
                a_list.append(h)
                a_list.append(h1)
                if(bigger_or_not(a_list,max_hand_list) and smaller_or_not(a_list,limit_hand_list)):
                    max_hand_list = a_list
        return max_hand_list
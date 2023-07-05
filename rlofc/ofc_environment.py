import random
# from rlofc.deck_generator import DeckGenerator
# from rlofc.ofc_board import OFCBoard
from rlofc.deck_generator import  DeckGenerator
from rlofc.ofc_board import OFCBoard
import numpy as np


class OFCEnv(object):
    """Handle an OFC game in a manner condusive to PG RL."""

    def __init__(self, opponent_1, num_opponent = 1, fantacy_state = [0, 0, 0], encoder_class=None):
        self.num_oppo = num_opponent
        if encoder_class is not None:
            self.encoder = encoder_class()

        if self.num_oppo == 1:
            # 2 players, 1 opponent
            self.opponent_1 = opponent_1
            self.plyr_fantasy = fantacy_state[0]
            self.oppo_fantasy = fantacy_state[1]
        
        if self.num_oppo == 2:
            # 3 players, 2 opponents
            
            pass

        self.reset()


    def reset(self):
        if self.plyr_fantasy > 0 and self.oppo_fantasy == 0:
            # player in state of fantasy
            self.plyr_board = OFCBoard()
            self.oppo_board = OFCBoard()
            self.i = 10
            self.drop_card = []

            self.game_over = False
            self.reward = 0

            self.deck = DeckGenerator.new_deck()
            # self.plyr_cards = sorted(self.deck[0:5])
            # self.oppo_cards = sorted(self.deck[5:10])
            # self.fantasy_draw = 
            self.plyr_cards = sorted(self.deck[0:self.plyr_fantasy])
            self.oppo_cards = sorted(self.deck[self.plyr_fantasy:self.plyr_fantasy+5])

            # each round draw three card from the deck, players have to choose 2 from 3 and drop the additional 1.
            self.plyr_goes_first = 0

            if self.plyr_goes_first == 0:
                # oppo goes first
                self.current_card = self.oppo_cards
                self.execute_opponent_turn()
            
            else:
                # I go first
                self.current_card = self.plyr_cards
                self.execute_my_turn()

        if self.num_oppo == 1:
            self.plyr_board = OFCBoard()
            self.oppo_board = OFCBoard()
            self.i = 10
            self.drop_card = []

            self.game_over = False
            self.reward = 0

            self.deck = DeckGenerator.new_deck()
            # self.plyr_cards = sorted(self.deck[0:5])
            # self.oppo_cards = sorted(self.deck[5:10])
            self.plyr_cards = sorted(self.deck[0:5])
            self.oppo_cards = sorted(self.deck[5:10])

            # self.current_card = self.plyr_cards.pop()
            # each round draw three card from the deck, players have to choose 2 from 3 and drop the additional 1.
             

            self.plyr_goes_first = random.choice([0, 1])

            if self.plyr_goes_first == 0:
                # oppo goes first
                self.current_card = self.oppo_cards
                self.execute_opponent_turn()
            
            else:
                # I go first
                self.current_card = self.plyr_cards
                self.execute_my_turn()

    def draw(self):
        drop = random.choice([0, 1, 2])
        self.current_card = self.deck[self.i:self.i+3]
        
        if len(self.current_card) < 3:
            sample = 3-len(self.current_card)
            draw_from_drop = random.choices(self.drop_card, k = sample)
            self.current_card.append(draw_from_drop)

        else:
            self.drop_card +=  self.current_card[drop]

        self.current_card.remove(self.current_card[drop])
        self.i += 3

    def step(self, action):
        """Advance the game state by one decision."""

        # for i in range(len(self.current_card)):
        #     # print(self.current_card[i])
        #     self.plyr_board.place_card_by_id(self.current_card[i], action[i])

        #     # Only do opponent turn if we have no cards left to lay
        #     if len(self.plyr_cards) == 0:
        #         self.plyr_cards.append(self.deck.pop())
        #         self.execute_opponent_turn()

            # if len(self.deck) > 35:
            #     self.current_card = self.plyr_cards.pop()
            # else:
            #     self.current_card = None
            #     self.execute_endgame()\
        

        if self.board_sum(0) == 13 and self.board_sum(0) == 13:
            self.execute_endgame()

        if self.plyr_goes_first == 0:
            # oppo goes first
            self.execute_opponent_turn(action)
            
        else:
            # I go first
            self.execute_my_turn(action)
    
    def board_sum(self, player_code):
        if player_code == 0:
            return self.plyr_board.front.length()+self.plyr_board.mid.length()+self.plyr_board.back.length()
        
        else:
            return self.oppo_board.front.length()+self.oppo_board.mid.length()+self.oppo_board.back.length()


    def observe(self):
        """Return information about the game state."""
        game_state = (self.plyr_board,
                      self.oppo_board,
                      self.current_card,  # Current decision card
                      self.plyr_cards,    # i.e. remaining starting hand
                      self.game_over,     # Whether the game is over
                      self.reward)        # Score, or None
        
        return game_state

    def execute_opponent_turn(self, action):
        if not self.oppo_board.is_complete():
            if len(self.oppo_cards) == 0:
                self.draw()
                self.oppo_cards = self.current_card

            while len(self.oppo_cards) > 0:
                oppo_card = self.oppo_cards.pop()
                free_streets = self.oppo_board.get_free_street_indices()
                # if action
                oppo_action = random.choice(free_streets)  # For now!
                # oppo_action = 2
                self.oppo_board.place_card_by_id(oppo_card, oppo_action)

            # change
            if 
            self.plyr_goes_first = 1

        
    
    def execute_my_turn(self, action):
        if not self.plyr_board.is_complete():
            if len(self.plyr_cards) == 0:
                # self.plyr_cards.append(self.deck.pop())
                self.draw()
                self.plyr_cards = self.current_card

            while len(self.plyr_cards) > 0:
                plyr_card = self.plyr_cards.pop()
                free_streets = self.plyr_board.get_free_street_indices()
                plyr_action = random.choice(free_streets)  # For now!
                # oppo_action = 2
                self.plyr_board.place_card_by_id(plyr_card, plyr_action)

            # change
            self.plyr_goes_first = 0

        

    def execute_endgame(self):
        self.reward = self.calculate_score()
        self.game_over = True
        self.plyr_fantasy = self.plyr_board.is_fantasy()
        self.oppo_fantasy = self.oppo_board.is_fantasy()


    def calculate_score(self):
        plyr_royalties = self.plyr_board.get_royalties()
        oppo_royalties = self.oppo_board.get_royalties()

        if self.plyr_board.is_foul() and self.oppo_board.is_foul():
            score = 0

        elif self.plyr_board.is_foul():
            score = (-1 * oppo_royalties) - 6

        elif self.oppo_board.is_foul():
            score = plyr_royalties + 6

        else:
            each = self.calculate_scoop(self.plyr_board,
                                        self.oppo_board)
            score = each + plyr_royalties - oppo_royalties

        return score

    def calculate_scoop(self, lhs_board, rhs_board):
        lhs_won = 0

        lhs_won += self.calculate_street(lhs_board.front, rhs_board.front)
        lhs_won += self.calculate_street(lhs_board.mid, rhs_board.mid)
        lhs_won += self.calculate_street(lhs_board.back, rhs_board.back)

        if lhs_won in [3, -3]:   # Scoop, one way or the other
            lhs_won = lhs_won * 2

        return lhs_won

    def calculate_street(self, lhs_hand, rhs_hand):
        lhs_rank = lhs_hand.get_rank()
        rhs_rank = rhs_hand.get_rank()

        if lhs_rank < rhs_rank:
            return 1
        if rhs_rank < lhs_rank:
            return -1
        return 0


class OFCEnvironment(object):
    """Handle OFC game state and rewards."""

    def __init__(self, lhs_agent, rhs_agent):
        self.lhs_agent = lhs_agent
        self.rhs_agent = rhs_agent

    def play_game(self):
        """Rollout one OFC game and return the LHS score and LHS/RHS boards."""
        deck = DeckGenerator.new_deck()

        lhs_board = OFCBoard()
        rhs_board = OFCBoard()

        lhs_start = deck[0:5]
        rhs_start = deck[6:11]

        # Starting hand one card at a time for now. In future, give
        # all cards at once
        for i in xrange(5):
            card = lhs_start[i]
            street_id = self.lhs_agent.place_new_card(card, lhs_board)
            lhs_board.place_card_by_id(card, street_id)

            card = rhs_start[i]
            street_id = self.rhs_agent.place_new_card(card, rhs_board)
            rhs_board.place_card_by_id(card, street_id)

        # Eight cards one at a time
        for i in xrange(8):
            card = deck.pop()
            street_id = self.lhs_agent.place_new_card(card, lhs_board)
            lhs_board.place_card_by_id(card, street_id)

            card = deck.pop()
            street_id = self.rhs_agent.place_new_card(card, rhs_board)
            rhs_board.place_card_by_id(card, street_id)

        lhs_royalties = lhs_board.get_royalties()
        rhs_royalties = rhs_board.get_royalties()

        if lhs_board.is_foul() and rhs_board.is_foul():
            lhs_score = 0

        elif lhs_board.is_foul():
            lhs_score = (-1 * rhs_royalties) - 6

        elif rhs_board.is_foul():
            lhs_score = lhs_royalties + 6

        else:
            exch = self.calculate_scoop(lhs_board,
                                        rhs_board)
            lhs_score = exch + lhs_royalties - rhs_royalties

        return lhs_score, lhs_board, rhs_board

    def calculate_scoop(self, lhs_board, rhs_board):
        lhs_won = 0

        lhs_won += self.calculate_street(lhs_board.front, rhs_board.front)
        lhs_won += self.calculate_street(lhs_board.mid, rhs_board.mid)
        lhs_won += self.calculate_street(lhs_board.back, rhs_board.back)

        if lhs_won in [3, -3]:   # Scoop, one way or the other
            lhs_won = lhs_won * 2

        return lhs_won

    @staticmethod
    def calculate_street(lhs_hand, rhs_hand):
        lhs_rank = lhs_hand.get_rank()
        rhs_rank = rhs_hand.get_rank()

        if lhs_rank < rhs_rank:
            return 1
        if rhs_rank < lhs_rank:
            return -1
        return 0

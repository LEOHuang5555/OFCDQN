import random
# from rlofc.deck_generator import DeckGenerator
from rlofc.ofc_board import OFCBoard
from treys import Card
from .ofc_evaluator import OFCEvaluator
from rlofc.deck_generator import  DeckGenerator
from rlofc.ofc_board import OFCBoard
import numpy as np


class OFCEnv(object):
    """Handle an OFC game in a manner condusive to PG RL."""

    def __init__(self, num_opponent = 1, fantacy_state = [0, 0, 0], with_jocker = True ,encoder_class=None):

        self.num_oppo = num_opponent
        self.jocker = with_jocker

        if encoder_class is not None:
            self.encoder = encoder_class()

        if self.num_oppo == 1:
            # 2 players, 1 opponent
            # self.opponent = opponent_1
            self.plyr_fantasy = fantacy_state[0]
            self.oppo_fantasy = fantacy_state[1]
        
        if self.num_oppo == 2:
            # 3 players, 2 opponents
            # self.opponent = opponent_1
            # self.opponent2 = opponent_2
            self.plyr_fantasy = fantacy_state[0]
            self.oppo_fantasy = fantacy_state[1]
            self.oppo1_fantasy = fantacy_state[2]
            

        self.reset()


    def reset(self):
        # Create random cards pool
        self.deck = DeckGenerator.new_deck()
        if self.jocker:
            # Add two jockers to the pool. 
            self.deck += ['GG', 'gg']
            # Shuffle the pool.
            random.shuffle(self.deck)

        if self.num_oppo == 1:
            # Create shared attributes.
            self.plyr_board = OFCBoard()
            self.oppo_board = OFCBoard()
            self.drop_card = []
            self.game_over = False
            self.reward = 0

            if self.plyr_fantasy > 0 and self.oppo_fantasy == 0:
                # player in state of fantasy
                self.i = self.plyr_fantasy+5

                self.plyr_cards = sorted(self.deck[0:self.plyr_fantasy])
                self.oppo_cards = sorted(self.deck[self.plyr_fantasy:self.plyr_fantasy+5])

                self.plyr_goes_first = 0

                self.execute_game()
            
            elif self.plyr_fantasy == 0 and self.oppo_fantasy > 0:
                # player not in state of fantasy, but oppo in state of fantasy.
                self.i = self.oppo_fantasy+5

                self.deck = DeckGenerator.new_deck()
                self.oppo_cards = sorted(self.deck[0:self.oppo_fantasy])
                self.plyr_cards = sorted(self.deck[self.oppo_fantasy:self.oppo_fantasy+5])

                self.plyr_goes_first = 1

                self.execute_game()

            elif self.plyr_fantasy > 0 and self.oppo_fantasy > 0:
                # Both player and opponent are in the state of fantasy.
                self.i = self.oppo_fantasy+self.oppo_fantasy

                self.plyr_cards = sorted(self.deck[0:self.plyr_fantasy])
                self.oppo_cards = sorted(self.deck[self.plyr_fantasy:self.plyr_fantasy+self.oppo_fantasy])

                self.plyr_goes_first = 0

                self.execute_game()

                
            else:
                # normal condition
                self.i = 10
                self.plyr_cards = sorted(self.deck[0:5])
                self.oppo_cards = sorted(self.deck[5:10])             

                self.plyr_goes_first = random.choice([0, 1])

                self.execute_game()


        else:
            # There has 3 player in the game.
            # Create shared attributes.
            self.plyr_board = OFCBoard()
            self.oppo_board = OFCBoard()
            self.oppo1_board = OFCBoard()
            self.drop_card = []
            self.game_over = False
            self.reward = 0
            self.current_card = []

            if self.plyr_fantasy > 0 and self.oppo_fantasy == 0 and self.oppo1_fantasy == 0:
                # player in state of fantasy
                self.i = self.plyr_fantasy+10
                self.plyr_cards = sorted(self.deck[0:self.plyr_fantasy])
                self.oppo_cards = sorted(self.deck[self.plyr_fantasy:self.plyr_fantasy+5])
                self.oppo1_cards = sorted(self.deck[self.plyr_fantasy+5:self.plyr_fantasy+10])

                self.plyr_goes_first = random.choice([0, 2])

                self.execute_game()
            
            elif self.plyr_fantasy == 0 and self.oppo_fantasy > 0 and self.oppo1_fantasy == 0:
                # player and oppo1 are not in state of fantasy, but oppo is in state of fantasy.
                self.i = self.oppo_fantasy+10
                self.oppo_cards = sorted(self.deck[0:self.oppo_fantasy])
                self.plyr_cards = sorted(self.deck[self.oppo_fantasy:self.oppo_fantasy+5])
                self.oppo1_cards = sorted(self.deck[self.oppo_fantasy+5:self.oppo_fantasy+10])

                self.plyr_goes_first = random.choice([1, 2])

                self.execute_game()

            elif self.plyr_fantasy == 0 and self.oppo_fantasy == 0 and self.oppo1_fantasy > 0:
                # player and oppo are not in state of fantasy, but oppo1 is in state of fantasy.
                self.i = self.oppo1_fantasy+10
                self.oppo1_cards = sorted(self.deck[0:self.oppo1_fantasy])
                self.plyr_cards = sorted(self.deck[self.oppo1_fantasy:self.oppo1_fantasy+5])
                self.oppo_cards = sorted(self.deck[self.oppo1_fantasy+5:self.oppo1_fantasy+10])

                self.plyr_goes_first = random.choice([0, 1])

                self.execute_game()

                
            elif self.plyr_fantasy > 0 and self.oppo_fantasy > 0 and self.oppo1_fantasy == 0:
                # player and oppo are in state of fantasy, but oppo1 is not in state of fantasy.
                self.i = self.plyr_fantasy + self.oppo_fantasy + 5
                self.plyr_cards = sorted(self.deck[0:self.plyr_fantasy])
                self.oppo_cards = sorted(self.deck[self.plyr_fantasy:(self.plyr_fantasy+self.oppo_fantasy)])
                self.oppo1_cards = sorted(self.deck[(self.plyr_fantasy+self.oppo_fantasy):(self.plyr_fantasy + self.oppo_fantasy + 5)])

                self.plyr_goes_first = 2

                self.execute_game()
            
            elif self.plyr_fantasy > 0 and self.oppo_fantasy == 0 and self.oppo1_fantasy > 0:
                # player and oppo1 are in state of fantasy, but oppo is not in state of fantasy.
                self.i = self.plyr_fantasy + self.oppo1_fantasy + 5

                self.plyr_cards = sorted(self.deck[0:self.plyr_fantasy])
                self.oppo1_cards = sorted(self.deck[self.plyr_fantasy:(self.plyr_fantasy+self.oppo1_fantasy)])
                self.oppo_cards = sorted(self.deck[(self.plyr_fantasy+self.oppo1_fantasy):(self.plyr_fantasy + self.oppo1_fantasy + 5)])

                self.plyr_goes_first = 0

                self.execute_game()

            elif self.plyr_fantasy == 0 and self.oppo_fantasy > 0 and self.oppo1_fantasy > 0:
                # oppo and oppo1 are in state of fantasy, but player is not in state of fantasy.
                self.i = self.oppo_fantasy + self.oppo1_fantasy + 5

                self.oppo_cards = sorted(self.deck[0:self.oppo_fantasy])
                self.oppo1_cards = sorted(self.deck[self.oppo_fantasy:(self.oppo_fantasy+self.oppo1_fantasy)])
                self.plyr_cards = sorted(self.deck[(self.oppo_fantasy+self.oppo1_fantasy):(self.oppo_fantasy + self.oppo1_fantasy + 5)])

                self.plyr_goes_first = 1

                self.execute_game()

            elif self.plyr_fantasy > 0 and self.oppo_fantasy > 0 and self.oppo1_fantasy > 0:
                # All of the player in the game reach the state of fantasy
                self.i = self.oppo_fantasy + self.oppo1_fantasy + self.plyr_fantasy

                self.plyr_cards = sorted(self.deck[0:self.plyr_fantasy])
                self.oppo_cards = sorted(self.deck[self.plyr_fantasy:(self.plyr_fantasy + self.oppo_fantasy)])
                self.oppo1_cards = sorted(self.deck[(self.plyr_fantasy + self.oppo_fantasy):(self.oppo_fantasy + self.oppo1_fantasy + self.plyr_fantasy)])

                self.plyr_goes_first = 0

                self.execute_game()
                
            else:
                # normal condition
                self.i = 15
                self.plyr_cards = sorted(self.deck[0:5])
                self.oppo_cards = sorted(self.deck[5:10]) 
                self.oppo1_cards = sorted(self.deck[10:15])       

                self.plyr_goes_first = random.choice([0, 1, 2])

                self.execute_game()


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

    def step(self, action:list = None):
        """Advance the game state by one decision."""
        if self.num_oppo == 1:
            if self.board_sum(0) == 13 and self.board_sum(1) == 13:
                self.execute_endgame()

            else:
                self.execute_game(action)

        else:
            if self.board_sum(0) == 13 and self.board_sum(1) == 13 and self.board_sum(2) == 13:
                self.execute_endgame()

            else:
                self.execute_game(action)
        

        
    
    def board_sum(self, player_code):
        if player_code == 0:
            # oppo
            return self.oppo_board.front.length()+self.oppo_board.mid.length()+self.oppo_board.back.length()
            
        
        elif player_code == 1:
            # player
            return self.plyr_board.front.length()+self.plyr_board.mid.length()+self.plyr_board.back.length()
             
        else:
            # oppo1
            return self.oppo1_board.front.length()+self.oppo1_board.mid.length()+self.oppo1_board.back.length()


    def observe(self):
        """Return information about the game state."""
        # if self.current_card is None:
        #     self.current_card = []
        if self.num_oppo == 1:
            game_state = (self.plyr_board,
                        self.oppo_board,
                        self.current_card,  # Current decision card
                        self.plyr_cards,    # i.e. remaining starting hand
                        self.oppo_cards,
                        self.plyr_fantasy,
                        self.oppo_fantasy,
                        self.game_over,     # Whether the game is over
                        self.reward)        # Score, or None
            
        else:
            game_state = (self.plyr_board,
                        self.oppo_board,
                        self.oppo1_board,
                        self.current_card,  # Current decision card
                        self.plyr_cards,    # i.e. remaining starting hand
                        self.oppo_cards,
                        self.oppo1_cards,
                        self.plyr_fantasy,
                        self.oppo_fantasy,
                        self.oppo1_fantasy,
                        self.game_over,     # Whether the game is over
                        self.reward)        # Score, or None
        
        return game_state

    def execute_opponent_turn(self, action=None):
        if not self.oppo_board.is_complete():
            if self.oppo_fantasy > 0:
                self.oppo_board.place_card_by_fantasy_rule(self.oppo_cards)
                # change
                self.next_player()
                return

            if len(self.oppo_cards) == 0:
                self.draw()
                self.oppo_cards = self.current_card.copy()

            while len(self.oppo_cards) > 0:
                oppo_card = self.oppo_cards.pop()
                free_streets = self.oppo_board.get_free_street_indices()

                if action is None:
                    oppo_action = random.choice(free_streets)  # For now!

                else:
                    oppo_action = action.pop()

                self.oppo_board.place_card_by_id(oppo_card, oppo_action)

            # change
            self.next_player()

    def execute_opponent1_turn(self, action=None):
        if not self.oppo1_board.is_complete():
            if self.oppo1_fantasy > 0:
                self.oppo1_board.place_card_by_fantasy_rule(self.oppo1_cards)
                self.next_player()
                return 

            if len(self.oppo1_cards) == 0:
                self.draw()
                self.oppo1_cards = self.current_card.copy()

            while len(self.oppo1_cards) > 0:
                oppo1_cards = self.oppo1_cards.pop()
                free_streets = self.oppo1_board.get_free_street_indices()

                if action is None:
                    oppo1_action = random.choice(free_streets)  # For now!

                else:
                    oppo1_action = action.pop()
                
                # oppo_action = 2
                self.oppo1_board.place_card_by_id(oppo1_cards, oppo1_action)

            # change
            self.next_player()
        
    
    def execute_my_turn(self, action=None):
        if not self.plyr_board.is_complete():
            if self.plyr_fantasy > 0:
                self.plyr_board.place_card_by_fantasy_rule(self.plyr_cards)
                self.next_player()
                return
            
            if len(self.plyr_cards) == 0:
                self.draw()
                self.plyr_cards = self.current_card.copy()

            while len(self.plyr_cards) > 0:
                plyr_card = self.plyr_cards.pop()
                free_streets = self.plyr_board.get_free_street_indices()

                if action is None:
                    plyr_action = random.choice(free_streets) # For now!

                else:
                    plyr_action = action.pop()

                self.plyr_board.place_card_by_id(plyr_card, plyr_action)

            self.next_player()

    def execute_game(self, action=None):
        if self.plyr_goes_first == 0:
            # oppo goes first
            if self.oppo_fantasy ==0:
                self.current_card = self.oppo_cards

            self.execute_opponent_turn(action)
        
        elif self.plyr_goes_first == 2:
            # oppo1 goes first
            if self.oppo1_fantasy == 0:
                self.current_card = self.oppo1_cards

            self.execute_opponent1_turn(action)
        
        else:
            # I go first
            if self.plyr_fantasy == 0:
                self.current_card = self.plyr_cards

            self.execute_my_turn(action)

    def next_player(self):
        if self.num_oppo == 1:
            # Only 1 player in the game 
            if self.plyr_fantasy == 0 and self.oppo_fantasy == 0:
                if self.plyr_goes_first == 0:
                    self.plyr_goes_first = 1

                else:
                    self.plyr_goes_first = 0
            
            elif self.plyr_fantasy == 0 and self.oppo_fantasy > 0:
                # oppo is in the state of fantasy
                # player goes first
                # if the player fully filled the board, oppo places the cards. 
                if self.board_sum(1) == 13:
                    self.plyr_goes_first = 0

                else:
                    self.plyr_goes_first = 1
            
            elif self.plyr_fantasy > 0 and self.oppo_fantasy == 0:
                # player is in the state of fantasy
                # oppo goes first
                if self.board_sum(0) == 13:
                    self.plyr_goes_first = 1

                else:
                    self.plyr_goes_first = 0

            else:
                # both player and oppo are in the state of fantasy
                if self.plyr_goes_first == 0:
                    self.plyr_goes_first = 1

                else:
                    self.plyr_goes_first = 0 

        else:
            # 2 opponents in the game
            if self.plyr_fantasy == 0 and  self.oppo_fantasy == 0 and self.oppo1_fantasy == 0:
                if self.plyr_goes_first == 0:
                    self.plyr_goes_first = 1

                elif self.plyr_goes_first == 1:
                    self.plyr_goes_first = 2

                else:
                    self.plyr_goes_first = 0

            
            elif  self.plyr_fantasy > 0 and  self.oppo_fantasy == 0 and self.oppo1_fantasy == 0:
                if self.board_sum(0) == 13 and self.board_sum(2) == 13:
                    self.plyr_goes_first = 1

                if self.plyr_goes_first == 0:
                    self.plyr_goes_first = 2

                elif self.plyr_goes_first == 2:
                    self.plyr_goes_first = 0

                else:
                    self.plyr_goes_first = 1
            
            elif  self.plyr_fantasy == 0 and  self.oppo_fantasy > 0 and self.oppo1_fantasy == 0:
                if self.board_sum(1) == 13 and self.board_sum(2) == 13:
                    self.plyr_goes_first = 0

                if self.plyr_goes_first == 1:
                    self.plyr_goes_first = 2

                elif self.plyr_goes_first == 2:
                    self.plyr_goes_first = 1

                else:
                    self.plyr_goes_first = 0

            elif  self.plyr_fantasy == 0 and  self.oppo_fantasy == 0 and self.oppo1_fantasy > 0:
                if self.board_sum(0) == 13 and self.board_sum(1) == 13:
                    self.plyr_goes_first = 2

                if self.plyr_goes_first == 0:
                    self.plyr_goes_first = 1

                elif self.plyr_goes_first == 1:
                    self.plyr_goes_first = 0

                else:
                    self.plyr_goes_first = 2
            
            elif self.plyr_fantasy > 0 and  self.oppo_fantasy > 0 and self.oppo1_fantasy == 0:
                if self.board_sum(2) == 13:
                    self.plyr_goes_first = 0
                
                if self.board_sum(2) == 13 and self.board_sum(0) == 13:
                    self.plyr_goes_first = 1

                if self.plyr_goes_first == 2 and self.board_sum(2) < 13:
                    self.plyr_goes_first = 2

            elif self.plyr_fantasy > 0 and  self.oppo_fantasy == 0 and self.oppo1_fantasy > 0:
                if self.board_sum(0) == 13:
                    self.plyr_goes_first = 1
                
                if self.board_sum(0) == 13 and self.board_sum(1) == 13:
                    self.plyr_goes_first = 2

                if self.plyr_goes_first == 0 and self.board_sum(0) < 13:
                    self.plyr_goes_first = 0
            
            elif self.plyr_fantasy == 0 and  self.oppo_fantasy > 0 and self.oppo1_fantasy > 0:
                if self.board_sum(1) == 13:
                    self.plyr_goes_first = 2
                
                if self.board_sum(1) == 13 and self.board_sum(2) == 13:
                    self.plyr_goes_first = 0

                if self.plyr_goes_first == 1 and self.board_sum(1) < 13:
                    self.plyr_goes_first = 1

            else:
                # All of the player in the game reach to the state of fantasy. 
                if self.board_sum(0) == 13:
                    self.plyr_goes_first = 1
                
                if self.board_sum(0) == 13 and self.board_sum(1) == 13:
                    self.plyr_goes_first = 2
                


    def execute_endgame(self):
        self.reward = self.calculate_score()
        self.game_over = True
        if self.plyr_fantasy > 0:
            self.plyr_fantasy = self.plyr_board.is_refantasy()
        else:
            self.plyr_fantasy = self.plyr_board.is_fantasy()

        if self.oppo_fantasy > 0:
            self.oppo_fantasy = self.oppo_board.is_refantasy()
        else:
            self.oppo_fantasy = self.oppo_board.is_fantasy()
        
        if self.num_oppo == 2:
            if self.oppo1_fantasy > 0:
                self.oppo1_fantasy = self.oppo1_board.is_refantasy()
            else:
                self.oppo1_fantasy = self.oppo1_board.is_fantasy()



    def calculate_score(self):
        self.calculate_joker()
        if self.num_oppo == 1:
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
        else:
            plyr_royalties = self.plyr_board.get_royalties()
            oppo_royalties = self.oppo_board.get_royalties()
            oppo1_royalties = self.oppo1_board.get_royalties()

            if self.plyr_board.is_foul() and self.oppo_board.is_foul() and self.oppo1_board.is_foul():
                score = 0
            elif (not self.plyr_board.is_foul()) and self.oppo_board.is_foul() and self.oppo1_board.is_foul():
                score = plyr_royalties + 12

            elif self.plyr_board.is_foul() and (not self.oppo_board.is_foul()) and (not self.oppo1_board.is_foul()):
                score = (-1) * (oppo_royalties + oppo1_royalties) - 12

            else:
                each = self.calculate_scoop(self.plyr_board,
                                            self.oppo_board,
                                            self.oppo1_board)
                
                score = each + plyr_royalties - oppo_royalties - oppo1_royalties

        return score
    
    def calculate_joker(self):
        
        # jocker in the front line
        if 'gg' in self.plyr_board.front.cards or 'GG' in  self.plyr_board.front.cards:
            if 'gg' in self.plyr_board.mid.cards or 'GG' in self.plyr_board.mid.cards:
                self.plyr_board.mid.cards = get_max_hand(self.plyr_board.mid.cards ,self.plyr_board.back.cards)
                self.plyr_board.front.cards = get_max_hand(self.plyr_board.front.cards ,self.plyr_board.mid.cards)
            else:
                self.plyr_board.front.cards = get_max_hand(self.plyr_board.front.cards ,self.plyr_board.mid.cards)

        # jocker in the middle line
        if 'gg' in self.plyr_board.mid.cards or 'GG' in  self.plyr_board.mid.cards:
            if 'gg' in self.plyr_board.back.cards or 'GG' in self.plyr_board.back.cards:
                self.plyr_board.back.cards = get_max_hand(self.plyr_board.back.cards, ['Ts', 'Js', 'Qs', 'Ks', 'As'])
                self.plyr_board.mid.cards = get_max_hand(self.plyr_board.mid.cards, self.plyr_board.back.cards)
            else:
                self.plyr_board.mid.cards = get_max_hand(self.plyr_board.mid.cards ,self.plyr_board.back.cards)
        
        # jocker in the back line
        if 'gg' in self.plyr_board.back.cards or 'GG' in self.plyr_board.back.cards:
            self.plyr_board.back.cards = get_max_hand(self.plyr_board.back.cards, ['Ts', 'Js', 'Qs', 'Ks', 'As'])

        if self.plyr_fantasy == 0:
            self.plyr_board.front.cards = [Card.new(i) for i in self.plyr_board.front.cards]
            self.plyr_board.mid.cards = [Card.new(i) for i in self.plyr_board.mid.cards]
            self.plyr_board.back.cards = [Card.new(i) for i in self.plyr_board.back.cards]

    
        # jocker in the front line
        if 'gg' in self.oppo_board.front.cards or 'GG' in  self.oppo_board.front.cards:
            if 'gg' in self.oppo_board.mid.cards or 'GG' in self.oppo_board.mid.cards:
                self.oppo_board.mid.cards = get_max_hand(self.oppo_board.mid.cards ,self.oppo_board.back.cards)
                self.oppo_board.front.cards = get_max_hand(self.oppo_board.front.cards ,self.oppo_board.mid.cards)
            else:
                self.oppo_board.front.cards = get_max_hand(self.oppo_board.front.cards ,self.oppo_board.mid.cards)
    
        # jocker in the middle line
        if 'gg' in self.oppo_board.mid.cards or 'GG' in  self.oppo_board.mid.cards:
            if 'gg' in self.oppo_board.back.cards or 'GG' in self.oppo_board.back.cards:
                self.oppo_board.back.cards = get_max_hand(self.oppo_board.back.cards, ['Ts', 'Js', 'Qs', 'Ks', 'As'])
                self.oppo_board.mid.cards = get_max_hand(self.oppo_board.mid.cards, self.oppo_board.back.cards)
            else:
                self.oppo_board.mid.cards = get_max_hand(self.oppo_board.mid.cards ,self.oppo_board.back.cards)
        
        # jocker in the back line
        if 'gg' in self.oppo_board.back.cards or 'GG' in self.oppo_board.back.cards:
            self.oppo_board.back.cards = get_max_hand(self.oppo_board.back.cards, ['Ts', 'Js', 'Qs', 'Ks', 'As'])

        if self.oppo_fantasy == 0:   
            self.oppo_board.front.cards = [Card.new(i) for i in self.oppo_board.front.cards]
            self.oppo_board.mid.cards = [Card.new(i) for i in self.oppo_board.mid.cards]
            self.oppo_board.back.cards = [Card.new(i) for i in self.oppo_board.back.cards]
            
        if self.num_oppo == 2:
            # jocker in the front line
            if 'gg' in self.oppo1_board.front.cards or 'GG' in  self.oppo1_board.front.cards:
                if 'gg' in self.oppo1_board.mid.cards or 'GG' in self.oppo1_board.mid.cards:
                    self.oppo1_board.mid.cards = get_max_hand(self.oppo1_board.mid.cards ,self.oppo1_board.back.cards)
                    self.oppo1_board.front.cards = get_max_hand(self.oppo1_board.front.cards ,self.oppo1_board.mid.cards)
                else:
                    self.oppo1_board.front.cards = get_max_hand(self.oppo1_board.front.cards ,self.oppo1_board.mid.cards)

            # jocker in the middle line
            if 'gg' in self.oppo1_board.mid.cards or 'GG' in  self.oppo1_board.mid.cards:
                if 'gg' in self.oppo1_board.back.cards or 'GG' in self.oppo1_board.back.cards:
                    self.oppo1_board.back.cards = get_max_hand(self.oppo1_board.back.cards, ['Ts', 'Js', 'Qs', 'Ks', 'As'])
                    self.oppo1_board.mid.cards = get_max_hand(self.oppo1_board.mid.cards, self.oppo1_board.back.cards)
                else:
                    self.oppo1_board.mid.cards = get_max_hand(self.oppo1_board.mid.cards ,self.oppo1_board.back.cards)
            
            # jocker in the back line
            if 'gg' in self.oppo1_board.back.cards or 'GG' in self.oppo1_board.back.cards:
                self.oppo1_board.back.cards = get_max_hand(self.oppo1_board.back.cards, ['Ts', 'Js', 'Qs', 'Ks', 'As'])

            if self.oppo1_fantasy == 0:
                self.oppo1_board.front.cards = [Card.new(i) for i in self.oppo1_board.front.cards]
                self.oppo1_board.mid.cards = [Card.new(i) for i in self.oppo1_board.mid.cards]
                self.oppo1_board.back.cards = [Card.new(i) for i in self.oppo1_board.back.cards]
        


    def calculate_scoop(self, plyr_board, oppo_board, oppo1_board = None):
        lhs_won = 0

        lhs_won += self.calculate_street(plyr_board.front, oppo_board.front)
        lhs_won += self.calculate_street(plyr_board.mid, oppo_board.mid)
        lhs_won += self.calculate_street(plyr_board.back, oppo_board.back)

       
        if self.num_oppo == 1:
            lhs_won += self.calculate_street(plyr_board.front, oppo_board.front)
            lhs_won += self.calculate_street(plyr_board.mid, oppo_board.mid)
            lhs_won += self.calculate_street(plyr_board.back, oppo_board.back)

            if lhs_won in [3, -3]:   # Scoop, one way or the other
                lhs_won = lhs_won * 2

        else:
            lhs_won += self.calculate_street(plyr_board.front, oppo_board.front)
            lhs_won += self.calculate_street(plyr_board.mid, oppo_board.mid)
            lhs_won += self.calculate_street(plyr_board.back, oppo_board.back)

            lhs_won += self.calculate_street(plyr_board.front, oppo1_board.front)
            lhs_won += self.calculate_street(plyr_board.mid, oppo1_board.mid)
            lhs_won += self.calculate_street(plyr_board.back, oppo1_board.back)

        return lhs_won

    def calculate_street(self, lhs_hand, rhs_hand):
        lhs_rank = lhs_hand.get_rank()
        rhs_rank = rhs_hand.get_rank()

        if lhs_rank < rhs_rank:
            return 1
        if rhs_rank < lhs_rank:
            return -1
        return 0

evaluator = OFCEvaluator()

def bigger_or_not(current_hand_list,max_hand_list):
    current_hand_score = evaluator.evaluate([],[Card.new(i) for i in current_hand_list])
    max_hand_score = evaluator.evaluate([],[Card.new(i) for i in max_hand_list])
    if current_hand_score < max_hand_score:
        return True
    else:
        return False

def smaller_or_not(current_hand_list,limit_hand_list):
    current_hand_score = evaluator.evaluate([],[Card.new(i) for i in current_hand_list])
    limit_hand_score = evaluator.evaluate([],[Card.new(i) for i in limit_hand_list])
    if current_hand_score > limit_hand_score:
        return True
    else:
        return False

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

    all_cards = [
    '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', 'Ts', 'Js', 'Qs', 'Ks', 'As',
    '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', 'Th', 'Jh', 'Qh', 'Kh', 'Ah',
    '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', 'Td', 'Jd', 'Qd', 'Kd', 'Ad',
    '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', 'Tc', 'Jc', 'Qc', 'Kc', 'Ac']

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
                    print(a_list)
                    max_hand_list = a_list
        return max_hand_list

# class OFCEnvironment(object):
#     """Handle OFC game state and rewards."""

#     def __init__(self, lhs_agent, rhs_agent):
#         self.lhs_agent = lhs_agent
#         self.rhs_agent = rhs_agent

#     def play_game(self):
#         """Rollout one OFC game and return the LHS score and LHS/RHS boards."""
#         deck = DeckGenerator.new_deck()

#         lhs_board = OFCBoard()
#         rhs_board = OFCBoard()

#         lhs_start = deck[0:5]
#         rhs_start = deck[6:11]

#         # Starting hand one card at a time for now. In future, give
#         # all cards at once
#         for i in xrange(5):
#             card = lhs_start[i]
#             street_id = self.lhs_agent.place_new_card(card, lhs_board)
#             lhs_board.place_card_by_id(card, street_id)

#             card = rhs_start[i]
#             street_id = self.rhs_agent.place_new_card(card, rhs_board)
#             rhs_board.place_card_by_id(card, street_id)

#         # Eight cards one at a time
#         for i in xrange(8):
#             card = deck.pop()
#             street_id = self.lhs_agent.place_new_card(card, lhs_board)
#             lhs_board.place_card_by_id(card, street_id)

#             card = deck.pop()
#             street_id = self.rhs_agent.place_new_card(card, rhs_board)
#             rhs_board.place_card_by_id(card, street_id)

#         lhs_royalties = lhs_board.get_royalties()
#         rhs_royalties = rhs_board.get_royalties()

#         if lhs_board.is_foul() and rhs_board.is_foul():
#             lhs_score = 0

#         elif lhs_board.is_foul():
#             lhs_score = (-1 * rhs_royalties) - 6

#         elif rhs_board.is_foul():
#             lhs_score = lhs_royalties + 6

#         else:
#             exch = self.calculate_scoop(lhs_board,
#                                         rhs_board)
#             lhs_score = exch + lhs_royalties - rhs_royalties

#         return lhs_score, lhs_board, rhs_board

#     def calculate_scoop(self, lhs_board, rhs_board):
#         lhs_won = 0

#         lhs_won += self.calculate_street(lhs_board.front, rhs_board.front)
#         lhs_won += self.calculate_street(lhs_board.mid, rhs_board.mid)
#         lhs_won += self.calculate_street(lhs_board.back, rhs_board.back)

#         if lhs_won in [3, -3]:   # Scoop, one way or the other
#             lhs_won = lhs_won * 2

#         return lhs_won

#     @staticmethod
#     def calculate_street(lhs_hand, rhs_hand):
#         lhs_rank = lhs_hand.get_rank()
#         rhs_rank = rhs_hand.get_rank()

#         if lhs_rank < rhs_rank:
#             return 1
#         if rhs_rank < lhs_rank:
#             return -1
#         return 0


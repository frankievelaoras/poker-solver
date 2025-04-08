import cv2
import numpy as np
import easyocr
from PIL import ImageGrab
import time
from config import *

class OCR:
    def __init__(self, game_state):
        self.game_state = game_state
        self.reader = easyocr.Reader(['en'])
        self.previous_board = []
        self.previous_pot = None
        self.bankrolls = {}
        self.vpips = {}
        self.positions = {}
        self.actions = {}
        self.bets = {}

    def capture_screen(self, region, color=False):
        img = np.array(ImageGrab.grab(bbox=region))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        if not color:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, (0, 0), fx=2, fy=2)
        return img

    def extract_text(self, img):
        results = self.reader.readtext(img, detail=0)
        print("Raw OCR Output:", results)
        return results

    def extract_single_value(self, region):
        text = self.extract_text(self.capture_screen(region))
        return text[0] if text else "N/A"

    def extract_pot_value(self, text_list):
        for text in text_list:
            text = text.replace(",", "").strip()
            if text.replace(".", "").isdigit():
                return text
        return None

    def detect_suit_from_region(self, region):
        img = self.capture_screen(region, color=True)
        avg_color = np.mean(img.reshape(-1, 3), axis=0)
        suit_colors = {
            '♣': (27, 108, 27),
            '♥': (21, 82, 145),
            '♦': (162, 32, 33),
            '♠': (41, 43, 41)
        }
        def color_distance(c1, c2):
            return np.sqrt(sum((e1 - e2) ** 2 for e1, e2 in zip(c1, c2)))
        return min(suit_colors, key=lambda k: color_distance(avg_color, suit_colors[k]))

    def extract_cards_with_suits(self, text_list, suit_region, max_cards=1):
        valid_values = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
        for text in text_list:
            clean = text.strip()
            if clean == '0':
                clean = 'Q'
            if clean in valid_values:
                suit = self.detect_suit_from_region(suit_region)
                return [f"{clean}{suit}"]
        return []

    def extract_hero_cards(self):
        values = self.extract_text(self.capture_screen(HERO_CARDS_REGION))
        valid = []
        seen = set()
        for v in values:
            v = v.strip()
            if v == "0":
                v = "Q"
            if v in ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"] and v not in seen:
                valid.append(v)
                seen.add(v)
        return valid[:2]

    def extract_bankrolls(self):
        return {
            "Hero": self.extract_single_value(BANK_HERO),
            "Player 2": self.extract_single_value(BANK_PLAYER_2),
            "Player 3": self.extract_single_value(BANK_PLAYER_3),
            "Player 4": self.extract_single_value(BANK_PLAYER_4),
            "Player 5": self.extract_single_value(BANK_PLAYER_5),
            "Player 6": self.extract_single_value(BANK_PLAYER_6),
            "Player 7": self.extract_single_value(BANK_PLAYER_7),
        }

    def extract_vpips(self):
        players = {
            "Hero": VPIP_HERO,
            "Player 2": VPIP_PLAYER_2,
            "Player 3": VPIP_PLAYER_3,
            "Player 4": VPIP_PLAYER_4,
            "Player 5": VPIP_PLAYER_5,
            "Player 6": VPIP_PLAYER_6,
            "Player 7": VPIP_PLAYER_7,
        }
        return {p: self.extract_single_value(region) + "%" for p, region in players.items()}

    def detect_dealer_position(self):
        dealer_color = (99, 182, 231)
        positions_regions = {
            "Hero": POSITION_HERO,
            "Player 2": POSITION_PLAYER_2,
            "Player 3": POSITION_PLAYER_3,
            "Player 4": POSITION_PLAYER_4,
            "Player 5": POSITION_PLAYER_5,
            "Player 6": POSITION_PLAYER_6,
            "Player 7": POSITION_PLAYER_7,
        }

        def color_distance(c1, c2):
            return np.sqrt(np.sum((np.array(c1) - np.array(c2)) ** 2))

        # Identify dealer position by closest color match
        distances = {}
        for player, region in positions_regions.items():
            img = self.capture_screen(region, color=True)
            avg_color = np.mean(img.reshape(-1, 3), axis=0)
            distances[player] = color_distance(avg_color, dealer_color)

        dealer_player = min(distances, key=distances.get)
        player_order = ["Hero", "Player 2", "Player 3", "Player 4", "Player 5", "Player 6", "Player 7"]
        dealer_index = player_order.index(dealer_player)

        position_labels = ["BTN", "SB", "BB", "UTG", "MP", "CO", "HJ"]
        rotated = player_order[dealer_index:] + player_order[:dealer_index]
        assigned = {}
        for i, player in enumerate(rotated):
            label = ["BTN", "SB", "BB", "UTG", "MP", "CO", "HJ"][i % 7]
            assigned[player] = label
        return assigned

    def extract_player_actions(self):
        actions = {}
        regions = {
            "Hero": ACTION_HERO,
            "Player 2": ACTION_2,
            "Player 3": ACTION_3,
            "Player 4": ACTION_4,
            "Player 5": ACTION_5,
            "Player 6": ACTION_6,
            "Player 7": ACTION_7,
        }
        for player, region in regions.items():
            text = self.extract_text(self.capture_screen(region))
            action = "Unknown"
            for word in text:
                word = word.lower()
                if "call" in word:
                    action = "Call"
                elif "raise" in word:
                    action = "Raise"
                elif "fold" in word:
                    action = "Fold"
            actions[player] = action
        return actions

    def extract_bet_sizes(self):
        return {
            "Hero": self.extract_single_value(BET_AMOUNT_HERO),
            "Player 2": self.extract_single_value(BET_AMOUNT_2),
            "Player 3": self.extract_single_value(BET_AMOUNT_3),
            "Player 4": self.extract_single_value(BET_AMOUNT_4),
            "Player 5": self.extract_single_value(BET_AMOUNT_5),
            "Player 6": self.extract_single_value(BET_AMOUNT_6),
            "Player 7": self.extract_single_value(BET_AMOUNT_7),
        }

    def parse_text(self, pot_text, hero_cards_text):
        pot_size = self.extract_pot_value(pot_text)
        board_regions = [BOARD_CARD_1, BOARD_CARD_2, BOARD_CARD_3, BOARD_CARD_4, BOARD_CARD_5]
        suit_regions = [SUIT_CARD_1, SUIT_CARD_2, SUIT_CARD_3, SUIT_CARD_4, SUIT_CARD_5]
        board_cards = []

        for i in range(5):
            text = self.extract_text(self.capture_screen(board_regions[i]))
            card = self.extract_cards_with_suits(text, suit_regions[i])
            if card:
                board_cards.extend(card)

        if len(board_cards) < 3:
            self.previous_board = []
        elif len(board_cards) >= len(self.previous_board):
            self.previous_board = board_cards[:5]

        self.previous_pot = pot_size if pot_size else "N/A"
        hero_cards = self.extract_hero_cards()

        self.bankrolls = self.extract_bankrolls()
        self.vpips = self.extract_vpips()
        self.positions = self.detect_dealer_position()
        self.actions = self.extract_player_actions()
        self.bets = self.extract_bet_sizes()

        self.game_state.update_pot(self.previous_pot)
        self.game_state.update_board(self.previous_board)
        self.game_state.update_hero_cards(hero_cards)

    def display_game_state(self):
        print(f"\n--- GAME STATE ---")
        print(f"Pot: {self.game_state.pot}")
        print(f"Board: {', '.join(self.game_state.board) if self.game_state.board else 'N/A'}")
        print(f"Hero Cards: {', '.join(self.game_state.hero_cards) if self.game_state.hero_cards else 'N/A'}")
        for player in self.bankrolls:
            print(f"{player}:")
            print(f"  Bankroll: {self.bankrolls[player]}")
            print(f"  VPIP: {self.vpips.get(player, 'N/A')}")
            print(f"  Position: {self.positions.get(player, 'Unknown')}")
            print(f"  Action: {self.actions.get(player, 'Unknown')}")
            print(f"  Bet: {self.bets.get(player, 'N/A')}")

    def start(self):
        print("Starting OCR loop...")
        while True:
            pot_img = self.capture_screen(POT_REGION)
            pot_text = self.extract_text(pot_img)

            hero_img = self.capture_screen(HERO_CARDS_REGION)
            hero_text = self.extract_text(hero_img)

            self.parse_text(pot_text, hero_text)
            self.display_game_state()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            time.sleep(1)

if __name__ == "__main__":
    from MockGameState import MockGameState
    game_state = MockGameState()
    ocr = OCR(game_state)
    ocr.start()

class MockGameState:
    def __init__(self):
        self.pot = None
        self.board = []
        self.hero_cards = []

    def update_pot(self, pot):
        self.pot = pot
        print(f"[GameState] Updated Pot: {pot}")

    def update_board(self, board):
        self.board = board
        print(f"[GameState] Updated Board: {board}")

    def update_hero_cards(self, hero_cards):
        self.hero_cards = hero_cards
        print(f"[GameState] Updated Hero Cards: {hero_cards}")

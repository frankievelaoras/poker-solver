class GameLogic:
    def __init__(self, game_state):
        self.game_state = game_state

    def get_gto_feedback(self):
        # Basic GTO feedback logic (expandable)
        pot = self.game_state.pot_size
        board = self.game_state.board
        hero_hand = self.game_state.players[6]

        if pot > 100:
            return "Big pot - consider cautious play."
        elif len(board) >= 3:
            return "Board is built - time to evaluate ranges."
        elif hero_hand:
            return f"Hero: {hero_hand} - evaluate equity."
        else:
            return "Waiting for board state..."

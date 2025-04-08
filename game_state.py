class GameState:
    def __init__(self):
        self.pot_size = 0
        self.board = []
        self.players = [""] * 7  # 7 players max

    def update_pot(self, line):
        try:
            self.pot_size = int(line.split("$")[1].strip())
        except (IndexError, ValueError):
            self.pot_size = 0

    def update_board(self, line):
        self.board = line.replace("Board:", "").strip().split()

    def update_players(self, line):
        parts = line.split(":")
        if len(parts) == 2:
            player_index = int(parts[0].replace("Player", "").strip()) - 1
            if 0 <= player_index < len(self.players):
                self.players[player_index] = parts[1].strip()

import tkinter as tk
from tkinter import ttk

class PokerApp:
    def __init__(self, game_state, game_logic):
        self.game_state = game_state
        self.game_logic = game_logic
        self.root = tk.Tk()
        self.root.title("Poker GTO Overlay")
        self.create_widgets()

    def create_widgets(self):
        # Main frame
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Pot and Board info
        self.pot_label = ttk.Label(frame, text="Pot: $0")
        self.pot_label.grid(row=0, column=0, sticky=tk.W)

        self.board_label = ttk.Label(frame, text="Board: ")
        self.board_label.grid(row=1, column=0, sticky=tk.W)

        # Player info
        self.player_labels = []
        for i in range(7):
            label = ttk.Label(frame, text=f"Player {i+1}: --")
            label.grid(row=i + 2, column=0, sticky=tk.W)
            self.player_labels.append(label)

        # Feedback
        self.feedback_label = ttk.Label(frame, text="GTO Feedback: ")
        self.feedback_label.grid(row=10, column=0, sticky=tk.W)

        # Refresh button
        self.refresh_button = ttk.Button(frame, text="Refresh", command=self.update_display)
        self.refresh_button.grid(row=11, column=0, sticky=tk.W)

    def update_display(self):
        # Update labels with game state
        self.pot_label.config(text=f"Pot: ${self.game_state.pot_size}")
        self.board_label.config(text=f"Board: {self.game_state.board}")

        for i, player in enumerate(self.game_state.players):
            self.player_labels[i].config(text=f"Player {i+1}: {player}")

        feedback = self.game_logic.get_gto_feedback()
        self.feedback_label.config(text=f"GTO Feedback: {feedback}")

    def run(self):
        self.root.mainloop()

import threading
from gui import PokerApp
from ocr import OCR
from game_state import GameState
from game_logic import GameLogic

def main():
    game_state = GameState()
    ocr = OCR(game_state)
    game_logic = GameLogic(game_state)

    # Start OCR in a separate thread
    ocr_thread = threading.Thread(target=ocr.start, daemon=True)
    ocr_thread.start()

    # Launch GUI
    app = PokerApp(game_state, game_logic)
    app.run()

if __name__ == "__main__":
    main()

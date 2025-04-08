import cv2
import numpy as np
from PIL import ImageGrab

regions = {
    "POT_REGION": (377, 230, 470, 255),
    "HERO_CARDS_REGION": (365, 465, 479, 517),
    "BOARD_CARD_1": (266, 304, 327, 350),
    "BOARD_CARD_2": (333, 304, 392, 350),
    "BOARD_CARD_3": (396, 304, 457, 350),
    "BOARD_CARD_4": (463, 304, 522, 350),
    "BOARD_CARD_5": (531, 304, 588, 350),
    "SUIT_CARD_1": (293, 269, 325, 280),
    "SUIT_CARD_2": (364, 269, 388, 280),
    "SUIT_CARD_3": (426, 269, 453, 280),
    "SUIT_CARD_4": (493, 269, 518, 280),
    "SUIT_CARD_5": (551, 269, 586, 280),
    "BANK_HERO": (371, 571, 476, 588),
    "BANK_PLAYER_2": (125, 518, 212, 535),
    "BANK_PLAYER_3": (45, 270, 130, 293),
    "BANK_PLAYER_4": (271, 153, 354, 175),
    "BANK_PLAYER_5": (490, 155, 578, 176),
    "BANK_PLAYER_6": (716, 271, 800, 292),
    "BANK_PLAYER_7": (631, 516, 721, 537),
    "POSITION_HERO": (465, 429, 493, 454),
    "POSITION_PLAYER": (240, 432, 256, 444),
    "POSITION_PLAYER_3": (100, 332, 132, 361),
    "POSITION_PLAYER_4": (223, 189, 264, 215),
    "POSITION_PLAYER_5": (587, 188, 617, 213),
    "POSITION_PLAYER_6": (711, 332, 748, 362),
    "POSITION_PLAYER_7": (592, 427, 608, 443),
    "BET_AMOUNT_HERO": (397, 406, 450, 445),
    "BET_AMOUNT_2": (220, 388, 264, 424),
    "BET_AMOUNT_3": (149, 297, 198, 341),
    "BET_AMOUNT_4": (288, 185, 342, 225),
    "BET_AMOUNT_5": (503, 184, 563, 219),
    "BET_AMOUNT_6": (645, 300, 706, 345),
    "BET_AMOUNT_7": (575, 387, 630, 426),
    "ACTION_HERO": (387, 518, 465, 537),
    "ACTION_2": (139, 475, 198, 490),
    "ACTION_3": (62, 231, 119, 246),
    "ACTION_4": (287, 115, 344, 134),
    "ACTION_5": (506, 117, 566, 134),
    "ACTION_6": (729, 230, 792, 247),
    "ACTION_7": (652, 477, 708, 491),
}

img = np.array(ImageGrab.grab(bbox=(0, 0, 852, 625)))
img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

for name, (x1, y1, x2, y2) in regions.items():
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
    cv2.putText(img, name, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)

cv2.imwrite("debug_overlay.png", img)
print("Saved debug overlay to 'debug_overlay.png'")

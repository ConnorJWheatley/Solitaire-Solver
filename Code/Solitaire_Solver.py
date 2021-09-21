"""
This is my CE301 Capstone project. This program will solve a game of Microsoft Windows 10 solitaire.
"""
import pyautogui as pag
import sys
import os
import random
import copy
random.seed(1) # helping me to test the zobrist hashing as this gives me the same random values

class SolitaireSolver:

    # x and y co-ordinates of each position
    position_regions = {"deck":[564,135], "foundation_1":[906,135], "foundation_2":[1078,135], "foundation_3":[1248,135], "foundation_4":[1420,135],
                        "column_1":[392,360], "column_2":[564,360], "column_3":[735,360], "column_4":[906,360], "column_5":[1078,360], "column_6":[1248,360], "column_7":[1420,360]} 

    # the regions I can search to update a card position
    position_regions_search = {"deck":(545, 105, 100, 60), "foundation":(888, 105, 662, 195), "column_1":(375, 340, 35, 545), "column_2":(545, 340, 35, 545), "column_3":(720, 340, 35, 545), 
                                "column_4":(890, 340, 35, 545), "column_5":(1060, 340, 35, 545), "column_6":(1230, 340, 35, 545), "column_7":(1400, 340, 35, 545)}

    def __init__(self, game_state, list_cards_not_found, length_of_deck, zobrist_keys, hash_table):
        self.game_state = game_state
        self.list_cards_not_found = list_cards_not_found
        self.length_of_deck = length_of_deck
        self.zobrist_keys = zobrist_keys
        self.hash_table = hash_table

        # fills the list that stores what cards have not been found with all of the cards in the deck
        directory = "C:\\Users\\Connor\\Documents\\University\\Year 3\\CE301\\ce301_wheatley_connor_j\\Code\\all_cards_symbols"
        list_cards_not_found = []
        for filename in os.listdir(directory):
            self.list_cards_not_found.append(filename[:-4])

    def printVariables(self):
        print(self.game_state, self.list_cards_not_found, self.length_of_deck, self,zobrist_keys, self.hash_table)

    def cards_to_dictionary(self):
        """Look at the screen and place cards into a dictionary

        This function will take every card on screen and add it to a nested dictionary
        along with its position on the screen. Depending on it's position it will be 
        placed in a nested dictionary that corresponds to where it is.

        Args:
            None
        Returns:
            Dictionary: contains card info and the cards position. Example ('red_01_hrt': Point(x=150, y=500))
        Raises:
            None
        """
        cards_on_screen = {
                            "deck" : {}, "foundation" : {}, "column_1" : {},
                            "column_2" : {}, "column_3" : {}, "column_4" : {},
                            "column_5" : {}, "column_6" : {}, "column_7" : {},
                        }
        directory = "C:\\Users\\Connor\\Documents\\University\\Year 3\\CE301\\ce301_wheatley_connor_j\\Code\\all_cards_symbols"

        # this for loop will go through the directory that stores the card images
        for filename in os.listdir(directory):
            image_location = pag.locateCenterOnScreen(f"C:\\Users\\Connor\\Documents\\University\\Year 3\\CE301\\ce301_wheatley_connor_j\\Code\\all_cards_symbols\\{filename}", grayscale=False, region=(370,105,1065,780), confidence=0.956)
            # image_location = pag.locateCenterOnScreen(f"C:\\Users\\Connor\\Documents\\University\\Year 3\\CE301\\ce301_wheatley_connor_j\\Code\\all_cards_faces\\{filename}", grayscale=False, region=(375,340,1170,300), confidence=0.65)
            if image_location is not None: # if a card is found

                global list_cards_not_found
                list_cards_not_found.remove(filename[:-4]) # remove card from list

                if image_location.y < 320: # foundation or deck
                    if image_location.x < 640: # deck
                        temp_dict = {filename[:-4] : image_location}
                        cards_on_screen["deck"].update(temp_dict)
                    else: # foundation
                        temp_dict = {filename[:-4] : image_location}
                        cards_on_screen["foundation"].update(temp_dict)
                else: # a column
                    if image_location.x < 440: # column_1
                        temp_dict = {filename[:-4] : image_location}
                        cards_on_screen["column_1"].update(temp_dict)
                    elif image_location.x > 440 and image_location.x < 600: # column_2
                        temp_dict = {filename[:-4] : image_location}
                        cards_on_screen["column_2"].update(temp_dict)
                    elif image_location.x > 600 and image_location.x < 760: # column_3
                        temp_dict = {filename[:-4] : image_location}
                        cards_on_screen["column_3"].update(temp_dict)
                    elif image_location.x > 760 and image_location.x < 935: # column_4
                        temp_dict = {filename[:-4] : image_location}
                        cards_on_screen["column_4"].update(temp_dict)
                    elif image_location.x > 935 and image_location.x < 1100: # column_5
                        temp_dict = {filename[:-4] : image_location}
                        cards_on_screen["column_5"].update(temp_dict)
                    elif image_location.x > 1100 and image_location.x < 1270: # column_6
                        temp_dict = {filename[:-4] : image_location}
                        cards_on_screen["column_6"].update(temp_dict)
                    elif image_location.x > 1270:  # column_7
                        temp_dict = {filename[:-4] : image_location}
                        cards_on_screen["column_7"].update(temp_dict)

        return cards_on_screen


game_state = None
list_cards_not_found = []
length_of_deck = 24
zobrist_keys = None
hash_table = []

solitaire_solver = SolitaireSolver(game_state, list_cards_not_found, length_of_deck, zobrist_keys, hash_table)
solitaire_solver.printVariables()

if __name__ == "__main__":
    game_state = solitaire_solver.cards_to_dictionary() # gets all the cards on screen and enters them into a dictionary data structure
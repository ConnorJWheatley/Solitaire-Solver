"""
This is my CE301 Capstone project. This program will solve a game of Microsoft Windows 10 solitaire.
"""
import pyautogui as pag
import sys
import os
import random
import copy
import time
random.seed(1) # helping me to test the zobrist hashing as this gives me the same random values
# python package opencv-python needs to be installed for confidence keyword but does not need to be imported
pag.FAILSAFE = True # moving mouse to top left corner will abort program

# global variables that will be a class variable
# class structure seeming more likely here as I am now using many global variables
global global_game_state
global list_cards_not_found
global length_of_deck
global zobrist_keys
global hash_table
list_cards_not_found = []
length_of_deck = 24
hash_table = []

# x and y co-ordinates of each position
position_regions = {"deck":[564,135], "foundation_1":[906,135], "foundation_2":[1078,135], "foundation_3":[1248,135], "foundation_4":[1420,135],
                    "column_1":[392,360], "column_2":[564,360], "column_3":[735,360], "column_4":[906,360], "column_5":[1078,360], "column_6":[1248,360], "column_7":[1420,360]} 

# the regions I can search to update a card position
position_regions_search = {"deck":(545, 105, 100, 60), "foundation":(888, 105, 662, 195), "column_1":(375, 340, 35, 545), "column_2":(545, 340, 35, 545), "column_3":(720, 340, 35, 545), 
                            "column_4":(890, 340, 35, 545), "column_5":(1060, 340, 35, 545), "column_6":(1230, 340, 35, 545), "column_7":(1400, 340, 35, 545)}

directory = "C:\\Users\\Connor\\Documents\\University\\Year 3\\CE301\\ce301_wheatley_connor_j\\Code\\all_cards_symbols"
list_cards_not_found = []
for filename in os.listdir(directory):
    list_cards_not_found.append(filename[:-4])

def cards_to_dictionary():
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
        image_location = pag.locateCenterOnScreen(f"C:\\Users\\Connor\\Documents\\University\\Year 3\\CE301\\ce301_wheatley_connor_j\\Code\\all_cards_symbols\\{filename}", grayscale=False, region=(370,105,1065,780), confidence=0.955)
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

global_game_state = cards_to_dictionary()
print(global_game_state)

def face_cards_to_dict(cards_on_screen):
    """Using previous dictionary, make a new one with just face cards

    This function will take the dictonary that contains all of the cards on screen
    and will make a new dictionary that only contains the cards that show the full
    face of the card.

    Args:
        param1 (dictionary): the only parameter.
    Returns:
        Dictionary: contains card info and the cards position of the face cards.
    Raises:
        None
    """
    face_cards = {
                  "deck" : {}, "foundation" : {}, "column_1" : {},
                  "column_2" : {}, "column_3" : {}, "column_4" : {},
                  "column_5" : {}, "column_6" : {}, "column_7" : {},
                 }
    categories = ["deck", "foundation", "column_1", "column_2", "column_3", "column_4", "column_5", "column_6", "column_7",]
    category_count = 0
    # this loop will go through each category of the dictionary that stores the card names and positions
    for category in cards_on_screen.values():
        current_category = categories[category_count]
        category_count += 1
        biggest_position = 0
        y_position = ""
        x_position = ""
        foundation_check = False
        temp_list = []
        for j in category.items():
            temp_list.append({j[0] : j[1]})
            co_ord = j[1]
            y_position = co_ord.y
            x_position = co_ord.x
            if y_position < 320: # deck or foundation
                if x_position < 640: # deck
                    if x_position > biggest_position:
                        biggest_position = x_position
                else: # foundation
                    foundation_check = True
            else: # a column
                if x_position < 440: # column_1
                    if y_position > biggest_position:
                        biggest_position = y_position
                elif x_position > 440 and x_position < 600: # column_2
                    if y_position > biggest_position:
                        biggest_position = y_position
                elif x_position > 600 and x_position < 760: # column_3
                    if y_position > biggest_position:
                        biggest_position = y_position
                elif x_position > 760 and x_position < 935: # column_4
                    if y_position > biggest_position:
                        biggest_position = y_position
                elif x_position > 935 and x_position < 1100: # column_5
                    if y_position > biggest_position:
                        biggest_position = y_position
                elif x_position > 1100 and x_position < 1270: # column_6
                    if y_position > biggest_position:
                        biggest_position = y_position
                elif x_position > 1240:  # column_7
                    if y_position > biggest_position:
                        biggest_position = y_position
        if foundation_check == True:
            for card in temp_list:
                face_cards[current_category].update(card)
            continue
        for card in temp_list:
            if str(biggest_position) in str(card):
                face_cards[current_category].update(card)
        
    return face_cards

def ace_card_to_foundation(cards_on_screen):
    """Make a check to see if an ace card can be moved to the foundation

    This function will make a check to see if there any ace cards in the current
    game state that can be moved to the foundation pile.

    Args:
        cards_on_screen: A dictionary of the current game state
    Returns:
        cards_to_move: A list containing the cards that can be moved and where they can be moved to
    Raises:
        None
    """
    foundation_positions = [[960, 200], [1130, 200], [1300, 200], [1470, 200]] # the x co-ord of each foundation - the y co-ord is 200
    empty_foundation = [] # the places where there are no cards in the foundation pile
    ace_positions = []
    cards_to_move = []

    foundation_len = len(cards_on_screen["foundation"])
    for i in range(foundation_len, len(foundation_positions)):
        empty_foundation.append(foundation_positions[i])

    if len(empty_foundation) == 0: # if there is a card on every foundation pile
        return cards_to_move

    # there are only four aces, I can just see if there is an ace in any of the positions i.e. check for blk_01_clb in deck, foundation, columns
    ace_cards = ["blk_01_clb", "blk_01_spa", "red_01_dia", "red_01_hrt"]
    face_cards = face_cards_to_dict(cards_on_screen)
    for card in ace_cards:
        for key in face_cards:
            if key != "foundation":
                if card in face_cards[key]:
                    ace_positions.append([face_cards[key][card], card])

    if len(ace_positions) == 0:
        return cards_to_move

    index = 0
    for i in ace_positions:
        cards_to_move.append(ace_positions[index]) # position and then name
        cards_to_move.append(empty_foundation[index]) # x and y co-ords of foundation positions
        index += 1

    return cards_to_move

    # ======================================================================== previous code, keeping it here in case I need to go back to this code =================================================================================
    # for i in range(1,5):
    #     foundation_location = pag.locateCenterOnScreen(f"C:\\Users\\Connor\\Documents\\University\\Year 3\\CE301\\ce301_wheatley_connor_j\\Code\\foundation_images\\foundation_{i}.png", grayscale=False, region=(365,100,1205,935), confidence=0.55) # can make region smaller
    #     if foundation_location is not None:
    #         foundation_positions.append(foundation_location) #  need to change, this, a name is not needed since no card needs to change

    # # this loop will find all of the aces on screen
    # for i in range(1,5):
    #     ace_location = pag.locateCenterOnScreen(f"C:\\Users\\Connor\\Documents\\University\\Year 3\\CE301\\ce301_wheatley_connor_j\\Code\\ace_cards\\{i}.png", grayscale=True, region=(365,100,1205,935), confidence=0.6)
    #     if ace_location is not None:
    #         ace_positions.append(ace_location)
    
    # index = 0
    # for i in ace_positions:
    #     # if ace_positions[index] == None:
    #     #     break
    #     if ace_positions[index].y < 300: # don't want to move ace cards already placed in the foundation
    #         continue
    #     cards_to_move.append(ace_positions[index])
    #     cards_to_move.append(foundation_positions[index])
    #     index += 1
    # ===============================================================================================================================================================================================================================

def card_to_foundation(cards_on_screen):
    """Make a check to see if a card can be moved to the foundation

    This function will make a check to see if there any cards in the current
    game state that can be moved into the foundaton. This can be cards from
    the deck or the columns

    Args:
        cards_on_screen: A dictionary of the current game state
    Returns:
        cards_to_move: A list containing the cards that can be moved and where they can be moved to
    Raises:
        None
    """
    foundation_cards = []
    cards_to_move = []
    face_cards = face_cards_to_dict(cards_on_screen)
    # this will add the current cards in the foundation to an array
    for key in cards_on_screen["foundation"].items():
        foundation_cards.append(key)

    if len(foundation_cards) == 0:
        return cards_to_move

    for card in foundation_cards:
        card_name = card[0]
        card_num = card_name[4:6]
        new_card_num = ""
        if card_num.startswith("0"):
            card_num = int(card_num[1]) + 1
            new_card_num = "0" + str(card_num)
        else:
            card_num = int(card_num) + 1
            new_card_num = str(card_num)
        card_to_find = card_name[:3] + "_" + new_card_num + "_" + card_name[7:]
        for i in face_cards.values():
            for j in i.items():
                if j[0].startswith(card_to_find) and j[1].y < 300 and j[1].x < 750: # moving a card from the deck
                    card_moving = [j[1], j[0]]
                    card_destination = [card[1], card[0]]
                    cards_to_move.append(card_moving)
                    cards_to_move.append(card_destination)
                elif j[0].startswith(card_to_find) and j[1].y > 300: # moving a card from a column
                    card_moving = [j[1], j[0]]
                    card_destination = [card[1], card[0]]
                    cards_to_move.append(card_moving)
                    cards_to_move.append(card_destination)

    return cards_to_move

def move_from_deck_to_column(cards_on_screen):
    """Check if a card can be moved to a column from the deck.

    This function will take the card that's on top of the deck and will search the bottom
    of every column to see if the card from the deck can be moved onto the column.

    Args:
        cards_on_screen: A dictionary of the current game state
    Returns:
        cards_to_move: A list containing the cards that can be moved and where they can be moved to
    Raises:
        None
    """
    deck_card_to_move = []
    cards_to_move = []
    biggest_x = 0
    face_cards_on_screen = face_cards_to_dict(cards_on_screen)
    # deck_card_to_move.append() - can get rid of for loop here, just need to figure out how to add just a single card
    for key in cards_on_screen["deck"].items():
        position = str(key[1])
        x_val = int(position[8:11])
        if x_val > biggest_x:
            biggest_x = x_val
            deck_card_to_move.clear()
            deck_card_to_move.append(key)
    # does not need to be for loop as it only loops once, but this works
    for card in deck_card_to_move:
        card_name = card[0]
        card_num = card_name[4:6]
        new_card_num = ""
        if int(card_num) < 9:
            card_num = int(card_num[1]) + 1
            new_card_num = "0" + str(card_num)
        else:
            card_num = int(card_num) + 1
            new_card_num = str(card_num)
        new_colour = ""
        if card_name[:3] == "red":
            new_colour = "blk_"
        elif card_name[:3] == "blk":
            new_colour = "red_"
        card_to_find = new_colour + new_card_num
        for i in face_cards_on_screen.values():
            for j in i.items():
                if j[0].startswith(card_to_find) and j[1].y > 300: # don't move to a deck or foundation card
                    card_moving = [card[1], card[0]]
                    card_destination = [j[1], j[0]]
                    cards_to_move.append(card_moving)
                    cards_to_move.append(card_destination)

    return cards_to_move  

def move_king_to_empty_space(cards_on_screen):
    """Check if a king card can be moved into an empty column.

    This function will try to find a king card that is not in a stack and then check
    to see if there is an empty column where that king can go. It will move the first
    king found and the first empty space found.

    Args:
        cards_on_screen: A dictionary of the current game state
    Returns:
        cards_to_move: A list containing the cards that can be moved and where they can be moved to
    Raises:
        None
    """
    king_positions = []
    board_positions = {"column_1" : [390, 360], "column_2" : [565, 360], "column_3" : [735, 360], "column_4" : [905, 360], "column_5" : [1078, 360], "column_6" : [1250, 360], "column_7" : [1420, 360]}
    empty_columns = []
    cards_to_move = []

    # this will give a list of the columns a king could move to
    for key in cards_on_screen:
        if key.startswith("c"):
            if len(cards_on_screen[key]) == 0:
                empty_columns.append(key)

    if len(empty_columns) == 0: # if there are no places for a king to move to
        return cards_to_move

    for key, value in cards_on_screen.items():
        for key1, value1 in value.items():
            if "13" in key1 and len(cards_on_screen[key]) == 1: # if the king card is by itself, don't want to move a king that is the top of a stack
                king_positions.append([value1, key1]) # adds the position followed by name

    if len(king_positions) == 0: # if there are no kings to move
        return cards_to_move

    cards_to_move.append(king_positions[0]) # position and name
    position = board_positions[empty_columns[0]]
    cards_to_move.append(position) # x and y co-ords of the column to move to

    return cards_to_move
    
    # ======================================================================== previous code, keeping it here in case I need to go back to this code =================================================================================
    # if len(king_positions) == 0 or (king_positions[0].y > 420 and king_positions[0].y < 440) or (king_positions[0].y > 345 and king_positions[0].y < 395): # or (king_positions[0].y > 300 and len(board_positions) == 2) 430
    #     return cards_to_move
    # else:
    #     cards_to_move.append(king_positions[0]) # just moving the first king that is found
    #     cards_to_move.append(board_positions[0]) # moving to the first empty space
    #     return cards_to_move

    # # this loop will find empty columns on the screen
    # for i in range(1,8):
    #     board_location = pag.locateCenterOnScreen(f"C:\\Users\\Connor\\Documents\\University\\Year 3\\CE301\\ce301_wheatley_connor_j\\Code\\column_images\\column_{i}.png", grayscale=True, region=(365,100,1205,935), confidence=0.6)
    #     if board_location is not None:
    #         board_positions.append(board_location)

    # if len(board_positions) == 0:
    #     return cards_to_move

    # this loop will find all kings on screen, including ones that are in a stack
    # for i in range(1,9):
    #     king_location = pag.locateCenterOnScreen(f"C:\\Users\\Connor\\Documents\\University\\Year 3\\CE301\\ce301_wheatley_connor_j\\Code\\king_cards\\{i}.png", grayscale=False, region=(365,100,1205,935), confidence=0.8)
    #     if king_location is not None:
    #         king_positions.append(king_location)
    # ===============================================================================================================================================================================================================================

def move_card_across_columns(cards_on_screen):
    """This function will check if a card can move from one column to another

    This function will look at all of the cards at the bottom of a column
    and see if those cards can be moved to other columns

    Args:
        cards_on_screen: A dictionary of the current game state
    Returns:
        cards_to_move: A list containing the cards that can be moved and where they can be moved to
    Raises:
        None
    """
    
    face_cards_on_screen = face_cards_to_dict(cards_on_screen)
    categories = ["column_1", "column_2", "column_3", "column_4", "column_5", "column_6", "column_7",]
    cards_to_move = []
    category_count = 0
    while category_count != 7:
        face_cards = []
        current_category = categories[category_count]
        # this adds the card that is on the bottom of the stack to an array
        for card in face_cards_on_screen[current_category].items():
            face_cards.append(card)
        category_count += 1
        # this loop will take the card and increase the number by one and switch the colour, to find a card it can move to
        for card in face_cards:
            card_name = card[0]
            card_num = card_name[4:6]
            new_card_num = ""
            if int(card_num) < 9:
                card_num = int(card_num[1]) + 1
                new_card_num = "0" + str(card_num)
            else:
                card_num = int(card_num) + 1
                new_card_num = str(card_num)
            new_colour = ""
            if card_name[:3] == "red":
                new_colour = "blk_"
            elif card_name[:3] == "blk":
                new_colour = "red_"
            card_to_find = new_colour + new_card_num
            count = 0
            for i in face_cards_on_screen.values():
                if count < 2: # don't want to move cards to the deck or foundation
                    count += 1
                    continue
                else:
                    for j in i.items():
                        if j[0].startswith(card_to_find):
                            card_moving = [card[1], card[0]]
                            card_destination = [j[1], j[0]]
                            cards_to_move.append(card_moving)
                            cards_to_move.append(card_destination)
                        
    return cards_to_move
                
def stack_to_another_column(cards_on_screen):
    """This function will check if it can move a stack of cards to another stack of cards

    This function will look at every card in a column, except the bottom card, and will
    check if that stack can be moved to the bottom of the other columns.

    Args:
        cards_on_screen: A dictionary of the current game state
    Returns:
        cards_to_move: A list containing the cards that can be moved and where they can be moved to
    Raises:
        None
    """
    cards_on_screen_copy = copy.deepcopy(cards_on_screen)
    face_cards_on_screen = face_cards_to_dict(cards_on_screen)
    categories = ["column_1", "column_2", "column_3", "column_4", "column_5", "column_6", "column_7"]
    cards_to_move = []
    category_count = 0
    while category_count != 7:
        current_card = []
        current_category = categories[category_count]
        if len(cards_on_screen_copy[current_category]) <= 1:
            pass
        elif len(cards_on_screen_copy[current_category]) >= 2: 
            biggest_y = 0
            card_to_remove = ""
            # this will find the card on the bottom of the stack to remove
            for card in cards_on_screen_copy[current_category].items():
                if card[1].y > biggest_y:
                    biggest_y = card[1].y
                    card_to_remove = str(card[0])
            del(cards_on_screen_copy[current_category][card_to_remove]) # removes the last card in the stack so that it does not try to move cards
                                                                        # from the bottom as it won't be a stack
            for card in cards_on_screen_copy[current_category].items():
                current_card.append(card)
        category_count += 1
        for card in current_card:
            card_name = card[0]
            card_num = card_name[4:6]
            new_card_num = ""
            if int(card_num) < 9:
                card_num = int(card_num[1]) + 1
                new_card_num = "0" + str(card_num)
            else:
                card_num = int(card_num) + 1
                new_card_num = str(card_num)
            new_colour = ""
            if card_name[:3] == "red":
                new_colour = "blk_"
            elif card_name[:3] == "blk":
                new_colour = "red_"
            card_to_find = new_colour + new_card_num
            count = 0
            for i in face_cards_on_screen.values():
                if count < 2: # don't want to move cards to the deck or foundation
                    count += 1
                    continue
                else:
                    for j in i.items():
                        difference_in_x_val = abs(j[1].x - card[1].x) # this will stop cards from trying to move to the card above it on the same stack
                        if j[0].startswith(card_to_find) and difference_in_x_val > 30:
                            card_moving = [card[1], card[0]]
                            card_destination = [j[1], j[0]]
                            cards_to_move.append(card_moving)
                            cards_to_move.append(card_destination)
                            

    return cards_to_move                       
                
def draw_new_card():
    """Draw a new card from the top deck if there are no other moves to make.

    Args:
        None
    Returns:
        None
    Raises:
        None
    """
    # check to see if point is green, if so, double click
    # update the deck part of the dictionary
    pag.moveTo(445, 200)
    pag.leftClick()
    temp_list = []
    for card in global_game_state["deck"]:
        temp_list.append(card)
    for card in temp_list:
        del global_game_state["deck"][card]
    directory = "C:\\Users\\Connor\\Documents\\University\\Year 3\\CE301\\ce301_wheatley_connor_j\\Code\\all_cards_symbols"
    for filename in os.listdir(directory):
        image_location = pag.locateCenterOnScreen(f"C:\\Users\\Connor\\Documents\\University\\Year 3\\CE301\\ce301_wheatley_connor_j\\Code\\all_cards_symbols\\{filename}", grayscale=False, region=(545, 105, 100, 60), confidence=0.96)
        if image_location is not None: # if a card is found
            global_game_state["deck"][filename[:-4]] = image_location

def move_cards(card_list, move, game_state):
    """Move cards that were chosen to be moved by one of the functions that checks for moves

    Args:
        card_list: This list will contain cards that need to be moved and where to move them to.
        move: A string that says what move is being made, e.g. moving ace card to foundation
        game_state: The current game state
    Returns:
        move_made: A boolean value that returns true if any move was made during this function. A move won't be made if it is a repeating move.
    Raises:
        None
    """
    from_card = 0 # the card that will be moved
    to_card = 1 # the card another card is being moved to
    list_size = len(card_list)
    iterations = int(list_size / 2)
    move_made = False # if a repetive move tries to happen, this stays false. If a move is made, this turns true
    move_to_foundation = False # if a move to the foundation is happenning
    cards_moved = []

    # x and y co-ordinates of each position
    position_regions = {"deck":[564,135], "foundation_1":[906,135], "foundation_2":[1078,135], "foundation_3":[1248,135], "foundation_4":[1420,135],
                        "column_1":[392,360], "column_2":[564,360], "column_3":[735,360], "column_4":[906,360], "column_5":[1078,360], "column_6":[1248,360], "column_7":[1420,360]} 

    # the regions I can search to update a card position
    position_regions_search = {"deck":(545, 105, 100, 60), "foundation":(888, 105, 662, 195), "column_1":(375, 340, 35, 545), "column_2":(545, 340, 35, 545), "column_3":(720, 340, 35, 545), 
                               "column_4":(890, 340, 35, 545), "column_5":(1060, 340, 35, 545), "column_6":(1230, 340, 35, 545), "column_7":(1400, 340, 35, 545)}

    # =====================================================================================================================
    original_game_state = copy.deepcopy(game_state) # creates a copy of the original game state to come back to if needed
    all_moves = []
    # =====================================================================================================================

    for i in range(iterations):
        card_to_move_name = card_list[from_card][1] # the name of the card that will move
        if card_to_move_name in cards_moved:
            from_card += 2
            to_card += 2
        else:
            cards_moved.append(card_to_move_name)

            if move == ("moving ace card to foundation") or move == ("moving card to foundation"):
                move_to_foundation = True

            # depending on what move is made, the 'to_card' will either be a card or an x,y list
            destination_coords = []
            card_destination_name = ""

            if move == ("moving ace card to foundation") or move == ("moving king to empty space"): # with these two functions, the to_card will be a list that holds the x,y co-ordinates of the destination
                destination_coords = card_list[to_card]
            else: # the other functions return the position followed by name
                card_destination_name = card_list[to_card][1] # the name of the destination card

            position_name = ""
            position_name_destination = ""

            # this loop can find the positions of both cards in one loop
            for key in game_state:
                if card_to_move_name in game_state[key]: # if the name of the card is in the nested dictionary of deck, foundation, columns
                    position_name = key # gets the position the card is in
                if card_destination_name in game_state[key]:
                    position_name_destination = key # gets the position the destination card is in

            if position_name_destination == "": # if the place it is moving to use x,y co-ords and not the name of the card
                # figure out the column it is in according to x and y value
                destination_coords_x = destination_coords[0]
                destination_coords_y = destination_coords[1]
                if destination_coords_y < 350: # it is the foundation
                    # check the length of the foundation in dict
                    # depending on length, depends which foundation pile to put it in
                    foundation_len = len(game_state["foundation"]) # might not need this line of code
                    position_name_destination = "foundation"
                else: # it is a column
                    for position in position_regions:
                        difference_in_x_val = abs(destination_coords_x - position_regions[position][0]) # this will work out the difference in the x val
                        if difference_in_x_val < 20:
                            position_name_destination = position

            # working out the zobrist hash for the move that wants to be made
            # this can check for game states that have already been visited and therefore stop repeating moves
            global zobrist_keys
            current_hash = hash_table[-1] # the current hash of the game will be the last hash in the list
            current_hash_dec = 0
            # gets the hash value and turns it into decimal
            for bit in current_hash:
                current_hash_dec = current_hash_dec*2 + int(bit)

            position_no = 1 # position is deck, foundation, or columns - gets the position the card is originally in before being moved
            for position in position_regions_search:
                if position == position_name:
                    break
                position_no += 1

            position_dest_no = 1 # this gets the number for the position the card will move to
            for position in position_regions_search:
                if position == position_name_destination:
                    break
                position_dest_no += 1
            
            directory = "C:\\Users\\Connor\\Documents\\University\\Year 3\\CE301\\ce301_wheatley_connor_j\\Code\\all_cards_symbols"

            if move == ("moving stacks across columns"):
                card_to_move_no = card_to_move_name[4:6]
                cards_to_hash = []
                for card in game_state[position_name].items():
                    if int(card[0][4:6]) < int(card_to_move_no):
                        cards_to_hash.append(card[0]) # adding the cards that need to be deleted to a list
                for card in cards_to_hash:
                    card_value = 0
                    for filename in os.listdir(directory):
                        if filename[:-4] == card_to_move_name:
                            break
                        card_value += 1
                    card_hash_val = zobrist_keys[position_no][card_value] # gives binary string
                    card_hash_dec = 0
                    for bit in card_hash_val:
                        card_hash_dec = card_hash_dec*2 + int(bit)
                    # gets the hash value of the destination
                    dest_hash_val = zobrist_keys[position_dest_no][card_value]
                    dest_hash_dec = 0
                    for bit in dest_hash_val:
                        dest_hash_dec = dest_hash_dec*2 + int(bit)
                    current_hash_dec = (f"{int(current_hash_dec) ^ card_hash_dec}") # XOR out the card from original position
                    current_hash_dec = (f"{int(current_hash_dec) ^ dest_hash_dec}") # XOR in the card in the new position
            else:
                # each card is assigned a value from 0-51
                card_value = 0
                for filename in os.listdir(directory):
                    if filename[:-4] == card_to_move_name:
                        break
                    card_value += 1
                card_hash_val = zobrist_keys[position_no][card_value] # gives binary string
                card_hash_dec = 0
                for bit in card_hash_val:
                    card_hash_dec = card_hash_dec*2 + int(bit)

                    # gets the hash value of the destination
                dest_hash_val = zobrist_keys[position_dest_no][card_value]
                dest_hash_dec = 0
                for bit in dest_hash_val:
                    dest_hash_dec = dest_hash_dec*2 + int(bit)

                current_hash_dec = (f"{int(current_hash_dec) ^ card_hash_dec}") # XOR out the card from original position
                current_hash_dec = (f"{int(current_hash_dec) ^ dest_hash_dec}") # XOR in the card in the new position

            new_hash = (f"{int(current_hash_dec):064b}")
            if new_hash in hash_table:
                from_card += 2
                to_card += 2
            else:
                move_made = True

                card_to_move_no = card_to_move_name[4:6]
                last_card = None
                smallest_card_no = 14

                if len(game_state[position_name_destination]) == 0:
                    if move == ("moving ace card to foundation") or move == ("moving card to foundation"):
                        foundation_pos = position_regions["foundation_1"]
                        last_card = pag.Point(x = foundation_pos[0], y = foundation_pos[1])
                    if move == ("moving king to empty space"):
                        column_pos = position_regions[position_name_destination]
                        last_card = pag.Point(x = column_pos[0], y = column_pos[1])
                else:
                    for card in game_state[position_name_destination].items():
                        # if len(game_state[position_name_destination]) == 0:
                        #     pass # put it in the column it needs to, I know the destination
                        # i don't think there is any situation with the other moves where I'm moving a card to an empty space
                        if move == ("moving ace card to foundation") or move == ("moving card to foundation"):
                            temp_card = card[1]
                            last_card = pag.Point(x = (temp_card[0] + 172), y = temp_card[1])
                        else:
                            if len(game_state[position_name_destination]) == 1:
                                last_card = card[1]
                                break
                            card_no = int(card[0][4:6])
                            if card_no < smallest_card_no:
                                smallest_card_no = card_no
                                last_card = card[1]

                new_pos_x = last_card[0]
                new_pos_y = 0
                new_location = None

                if move != ("moving ace card to foundation") or move != ("moving card to foundation") or move != ("moving king to empty space"): # I don't need to adjust x and y values for these moves
                    if len(game_state[position_name_destination]) >= 9: # this is when cards to shift in place
                        new_pos_y = last_card[1] # i found that when cards shifted up, the new card that would be put on the bottom would actually be where the previous card was and so the y value will be the same
                    else:
                        new_pos_y = last_card[1] + 56

                    new_location = pag.Point(x = new_pos_x, y = new_pos_y)
                else:
                    new_location = last_card
                
                card_movement_dict(game_state, position_name, position_name_destination, card_to_move_name, move, new_location) # will move the cards in memory

                score = 0
                card_reveal = card_reveal_check(position_name) # check to see if the column the card(s) was moved from revealed a new card
                if move_to_foundation == True:
                    score += 5
                if card_reveal == True:
                    score += 3

                level_deep_moves = move_check() # this gives me a list of the new moves that can be made from the new gamestate

                # add up the total score of all the moves found
                # more points means potentially more oppurtunity for moves and decisions
                for move in level_deep_moves:
                    score += move[0]

                potential_move_list = [[score], [position_name, position_name_destination, card_to_move_name, move, new_location, card_list[from_card], card_list[to_card]]]
                all_moves.append(potential_move_list)

                from_card += 2
                to_card += 2

    # makes the move based on scoring used when searching one level deep
    game_state = original_game_state
    all_moves = sorted(all_moves, key=lambda x: x[0], reverse=True)
    if len(all_moves) == 0:
        # no move was made here, just return move made False
        return move_made
    move_to_make = all_moves[0][1] # the move with the highest score
    # print(move_to_make) # sometimes get list index out of range error
    new_location = card_movement_real(game_state, move_to_make[0], move_to_make[1], move_to_make[2], move_to_make[5], move_to_make[6]) # this will perform the physical movement on screen and return the new location of the card moved
    card_movement_dict(game_state, move_to_make[0], move_to_make[1], move_to_make[2], move_to_make[3], move_to_make[4]) # will move the cards in memory
    
    pag.moveTo(335, 200) # moves the mouse cursor away so it does obstruct any cards
    pag.leftClick()
    global_game_state = game_state

    # return a boolean to check for a move
    return move_made

def move_selection(moves, game_state):
    """This function will either go to a function to draw a new card or to do some other possible move

    This function will either call the function to draw new card from the deck, or to call the function that will perform
    one of many possible moves. That function will also look for moves one move ahead to try and pick better
    decisions.

    Args:
        moves: A list containing all of the possible moves that could happen, the amount of points that move can give, 
               and a string describing that move
        game_state: A dictionary of the current game state
    Returns:
        None
    Raises:
        None
    """
    # check array for moves that can be done, choose the move that gives the most points, will probably be the first entry in the dictionary

    global global_game_state
    if moves[0][1] == None:
        draw_new_card()
    else:
        move_card_check = move_cards(moves[0][1], moves[0][2], global_game_state) # the second square bracket is the list of moves that can be done
        if move_card_check == False:
            draw_new_card()

def init_zobrist_keys():
    """This function will create a 2D array of random binary numbers

    This function produces a 2D array using the Zobrist hashing method.
    It creates a table of randomly generated bitstrings for each possible element of the game.

    Args:
        None
    Returns:
        zobrist_board: The 2D list that contains all of the randomly generated keys
    Raises:
        None
    """
    cards = 52
    locations = 13
    n_bits = 64
    zobrist_board = []
    for i in range(locations):
        temp_list = []
        for i in range(cards):
            temp_list.append("".join(random.choice("01") for j in range(n_bits))) # randomly picks either 0 or 1 to create a binary string
        zobrist_board.append(temp_list)
    return zobrist_board

def hash_board(zobrist_keys, game_state):
    """This function will hash the current game state with the keys generated

    This function produce a hash value of the current game state. 
    It uses the keys that were generated in the function init_zobrist_keys to hash each card
    in the game state and then produce a hash for the whole board by continously XOR each new hash.

    Args:
        zobrist_keys: A 2D list of the randomly generated keys
        game_state: A dictionary of the current game state
    Returns:
        hash_binary: A 64 bit hash value of the board, cast as a string.
    Raises:
        None
    """
    card_values = {}
    directory = "C:\\Users\\Connor\\Documents\\University\\Year 3\\CE301\\ce301_wheatley_connor_j\\Code\\all_cards_symbols"
    i = 0
    for filename in os.listdir(directory):
        card_values[filename[:-4]] = i
        i += 1
    
    hash_val = 0
    card_positions = ["deck", "foundation", "column_1", "column_2", "column_3", "column_4", "column_5", "column_6", "column_7"]
    position_count = 1
    for position in card_positions:
        for card in game_state[position].keys():
            card_at_pos = card_values[card] # card value given, i.e. blk_01_clb = 1
            binary = zobrist_keys[position_count][card_at_pos]
            zobrist_dec = 0
            for bit in binary:
                zobrist_dec = zobrist_dec*2 + int(bit)
            hash_val = (f"{int(hash_val) ^ zobrist_dec}")
        position_count += 1
    hash_binary = (f"{int(hash_val):064b}")
    return hash_binary

def move_check():
    """This function will make checks for moves that can be performed

    This function will all of the other functions made that check for all of the possible moves.
    These are then added to a list along with a score those moves give and a string describing the move.

    Args:
        None
    Returns:
        possible_moves: A list of that contains all of the moves that can be made
    Raises:
        None
    """
    start = time.time()
    possible_moves = [] # this will be used to store the different moves that can be made
    global global_game_state

    ace_card_to_foundation_check = ace_card_to_foundation(global_game_state)
    if(len(ace_card_to_foundation_check) != 0):
        possible_moves.append([5, ace_card_to_foundation_check, "moving ace card to foundation"])
        
    card_to_foundation_check = card_to_foundation(global_game_state)
    if(len(card_to_foundation_check) != 0):
        possible_moves.append([5, card_to_foundation_check, "moving card to foundation"])

    move_from_deck_to_column_check = move_from_deck_to_column(global_game_state)
    if(len(move_from_deck_to_column_check) != 0):
        possible_moves.append([2, move_from_deck_to_column_check, "moving card from deck to column"])

    move_king_to_empty_space_check = move_king_to_empty_space(global_game_state)
    if(len(move_king_to_empty_space_check) != 0):
        possible_moves.append([2, move_king_to_empty_space_check, "moving king to empty space"])

    move_card_across_columns_check = move_card_across_columns(global_game_state)
    if(len(move_card_across_columns_check) != 0):
        possible_moves.append([1, move_card_across_columns_check, "moving card across columns"])

    stack_to_another_column_check = stack_to_another_column(global_game_state)
    if(len(stack_to_another_column_check) != 0):
        possible_moves.append([1, stack_to_another_column_check, "moving stack across columns"])

    # when making a move from the deck, keep track of how many cards are in the deck
    # if there cards in the deck, then drawing a new card is a possible move
    if length_of_deck > 0:
        possible_moves.append([0, None, "drawing a card"])

    return possible_moves

def card_reveal_check(column_name): # checks to see if a move would reveal a new card
    card_reveal = False
    smallest_y = 1080
    column_top_card = ""
    # this will find the card on the bottom of the stack to remove
    for card in global_game_state[column_name].items(): # cards_on_screen is global_game_state
        if card[1].y < smallest_y:
            smallest_y = card[1].y
            column_top_card = str(card[0])
    if smallest_y > 375: # i know there is at least one more card to be revealed
        card_reveal = True
    # print(column_top_card)
    return card_reveal

def card_movement_real(game_state, position_name, position_name_destination, card_to_move_name, card_origin, card_dest):
    card_to_move_pos = game_state[position_name][card_to_move_name] # this gives the position with Point(x=..., y=...)
    # this will give me the x co-ord of the card I want to move
    card_to_move_pos_str = str(card_to_move_pos)
    x_coord = card_to_move_pos_str.split()
    number = ""
    for i in x_coord[0]:
        if i.isdigit():
            number += i

    card_to_move_x = int(number)
    position_x = position_regions[position_name][0]
    difference_in_x_val = abs(card_to_move_x - position_x)

    if difference_in_x_val < 30: # it's in the correct position
        pag.moveTo(card_origin[0])
        pag.doubleClick()
        if isinstance(card_dest[0], int) == True: # so if the first item in the list is a integer, then it's the list with x,y co-ord
            pag.moveTo(card_dest[0], card_dest[1]) # use the x and y co-ordinates to move
            pag.leftClick()
        else: # it uses Point() to give the co-ordinates instead
            pag.moveTo(card_dest[0])
            pag.leftClick()
    else: 
        # the cards position is not up to date
        # searches the right position to find the new co-ordinate of the card
        card_position = pag.locateCenterOnScreen(f"C:\\Users\\Connor\\Documents\\University\\Year 3\\CE301\\ce301_wheatley_connor_j\\Code\\all_cards_symbols\\{card_to_move_name}.png", 
                                                    grayscale=False, region=position_regions_search[position_name], confidence=0.95)
        pag.moveTo(card_position)
        pag.leftClick()
        # same code as if the card was in the correct position
        if isinstance(card_dest[0], int) == True:
            pag.moveTo(card_dest[0], card_dest[1])
            pag.leftClick()
        else:
            pag.moveTo(card_dest[0])
            pag.leftClick()

    # problems can happen here if no card is found and position is set to None
    new_location = pag.locateCenterOnScreen(f"C:\\Users\\Connor\\Documents\\University\\Year 3\\CE301\\ce301_wheatley_connor_j\\Code\\all_cards_symbols\\{card_to_move_name}.png", 
                                                    grayscale=False, region=position_regions_search[position_name_destination], confidence=0.95)

    return new_location

def card_movement_dict(game_state, position_name, position_name_destination, card_to_move_name, move, new_location):
    # if I am moving a stack, I need to move the other cards that were in the column to the column the card was moved to as a stack move
    # in this situation, the position for the cards will no longer be correct
    if move == ("moving stacks across columns"):
        # need to do update the zobrist hash as cards are being moved and so the hash value needs to change too

        card_to_move_no = card_to_move_name[4:6]
        cards_to_del = []
        for card in game_state[position_name].items():
            if int(card[0][4:6]) < int(card_to_move_no):
                game_state[position_name_destination][card[0]] = card[1] # adds the card below the top of the stack to the correct column
                cards_to_del.append(card[0]) # adding the cards that need to be deleted to a list

        # removing all of the cards from the column they originally came from
        for card in cards_to_del:
            del game_state[position_name][card]

        if len(game_state[position_name]) == 0: # all cards were moved
            # can make this a function
            for card in list_cards_not_found:
                new_card_search = pag.locateCenterOnScreen(f"C:\\Users\\Connor\\Documents\\University\\Year 3\\CE301\\ce301_wheatley_connor_j\\Code\\all_cards_symbols\\{card}.png", 
                                                        grayscale=False, region=position_regions_search[position_name], confidence=0.95)
                if new_card_search is not None:
                    game_state[position_name][card] = new_card_search
                    break
    
    global length_of_deck
    if move == ("moving card from deck to column"):
        length_of_deck -= 1
    
    if move == ("moving card to foundation"):
        if position_name == "deck":
            length_of_deck -= 1

    game_state[position_name_destination][card_to_move_name] = new_location # this will add the card to the destination it needs to and give it the correct position

    if len(game_state[position_name]) == 1: # there is one card in that column and when moving could reveal a new card
        # moving a whole stack
        # can make this function
        for card in list_cards_not_found:
            new_card_search = pag.locateCenterOnScreen(f"C:\\Users\\Connor\\Documents\\University\\Year 3\\CE301\\ce301_wheatley_connor_j\\Code\\all_cards_symbols\\{card}.png", 
                                                        grayscale=False, region=position_regions_search[position_name], confidence=0.95)
            if new_card_search is not None:
                game_state[position_name][card] = new_card_search
                break             

    del game_state[position_name][card_to_move_name] # this removes the card from the position it was in before the card moved

# this version is used for testing the functionality of the function
def cards_to_dictionary_test():
    """Look at the screen and place cards into a dictionary. (Test Version)

    This function will take every card on screen and add it to a nested dictionary
    along with its position on the screen. Depending on it's position it will be 
    placed in a nested dictionary that corresponds to where it is.

    Args:
        None
    Returns:
        Dictionary: contains card info and the cards position (test version so returns position as string). 
                    Example ('red_01_hrt': Point(x=150, y=500))
    Raises:
        None
    """
    cards_on_screen = {
                        "deck" : {}, "foundation" : {}, "column_1" : {},
                        "column_2" : {}, "column_3" : {}, "column_4" : {},
                        "column_5" : {}, "column_6" : {}, "column_7" : {},
                      }
    directory = "C:\\Users\\Connor\\Documents\\University\\Year 3\\CE301\\ce301_wheatley_connor_j\\all_cards_symbols"

    # card_regions = [(542,105,898,55), (375,340,33,545), (548,340,33,545), (720,340,33,545), (890,340,33,545), (1060,340,33,545), (1230,340,33,545), (1402,340,33,545)]

    for filename in os.listdir(directory):
        image_location = pag.locateCenterOnScreen(f"all_cards_symbols\\{filename}", grayscale=False, region=(370,105,1065,780), confidence=0.948) # smaller regions to look for cards
        if image_location is not None:                                                                                                            # would speed up time
            if image_location.y < 320: # foundation or deck
                if image_location.x < 640: # deck
                    temp_dict = {filename[:-4] : str(image_location)}
                    cards_on_screen["deck"].update(temp_dict)
                else: # foundation
                    temp_dict = {filename[:-4] : str(image_location)}
                    cards_on_screen["foundation"].update(temp_dict)
            else: # a column
                if image_location.x < 440: # column_1
                    temp_dict = {filename[:-4] : str(image_location)}
                    cards_on_screen["column_1"].update(temp_dict)
                elif image_location.x > 440 and image_location.x < 600: # column_2
                    temp_dict = {filename[:-4] : str(image_location)}
                    cards_on_screen["column_2"].update(temp_dict)
                elif image_location.x > 600 and image_location.x < 760: # column_3
                    temp_dict = {filename[:-4] : str(image_location)}
                    cards_on_screen["column_3"].update(temp_dict)
                elif image_location.x > 760 and image_location.x < 935: # column_4
                    temp_dict = {filename[:-4] : str(image_location)}
                    cards_on_screen["column_4"].update(temp_dict)
                elif image_location.x > 935 and image_location.x < 1100: # column_5
                    temp_dict = {filename[:-4] : str(image_location)}
                    cards_on_screen["column_5"].update(temp_dict)
                elif image_location.x > 1100 and image_location.x < 1270: # column_6
                    temp_dict = {filename[:-4] : str(image_location)}
                    cards_on_screen["column_6"].update(temp_dict)
                elif image_location.x > 1270:  # column_7
                    temp_dict = {filename[:-4] : str(image_location)}
                    cards_on_screen["column_7"].update(temp_dict)

    return cards_on_screen

zobrist_keys = init_zobrist_keys()

# possible_moves = move_check() # this will be used to store the different moves that can be made

# print(move_check())
# print(face_cards_to_dict(global_game_state))

if __name__ == "__main__":
    """This main method will be used to run the program

    Args:
        None
    Returns:
        None
    Raises:
        None
    """

    while True:
        command_input = input("Type 'start' to begin program\nType 'info' to bring up info on this project: ").lower()
        if command_input == "info":
            print("This program tries to play and solve a game of Solitaire.")
            print("It does this by parsing the screen to find cards and then injecting mouse movements/actions on the screen")
        if command_input == "start":
            while True:
                try:
                    print("=====")
                    print(global_game_state)
                    print("=====\n")
                    board_hash = hash_board(zobrist_keys, global_game_state)
                    hash_table.append(board_hash)

                    possible_moves = move_check() # this will be used to store the different moves that can be made

                    print("~~~~~~~~~~~~~~~~~~")
                    print(possible_moves)
                    print("~~~~~~~~~~~~~~~~~~")

                    move_selection(possible_moves, global_game_state) # sends the array of moves to the move_selection function to find the move that gives the highest score

                except KeyboardInterrupt:
                    print("Program closed.")
                    try:
                        sys.exit(0)
                    except SystemExit:
                        os._exit(0)

        else:
            print("That's not a command")
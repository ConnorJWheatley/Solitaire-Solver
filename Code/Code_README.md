# Introduction to the code

My code is broken down into many functions that each have single job to do. I will go through the functions to describe what it is they do and how that contributes to solving a game of Solitaire.

## Storing the cards on screen in the code
Using a python library called [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/index.html), I can search the screen within a specified region and locate images based on a reference image.

![image](../Code/all_cards_symbols/red_01_hrt.png "Ace of hearts, red") I have a folder that contains all of the suits and values of every card. The reason why I don't search for the whole card, is that most times the whole card is obscured and the part of the card that is always visible is the suit and value in the top left.

With every card symbol/suit stored in a folder, I can go through every image in the folder and search the screen for that card.

```
image_location = pag.locateCenterOnScreen(f"C:\\Users\\Connor\\Documents\\University\\Year 3\\CE301\\ce301_wheatley_connor_j\\Code\\all_cards_symbols\\{filename}", grayscale=False, region=(370,105,1065,780), confidence=0.950)
```
This line of code is what searches for a card. It uses a confidence value so that it can have some leniency in finding the correct card, because if the confidence value was 1 it would need to match pixel for pixel.

Once a card is found, some logic is used to determine what part of the screen it was found. I can do this as PyAutoGUI will give a position of the symbol found in the form of X,Y co-ordinates, which in this case would be pixel distance from the top left of the screen.
The different positions are the deck, the foundation (where the cards are moved to at the top), and then each of the 7 columns. Once the position has been determined I then store the name of the card, in the format "colour_number_suit" so an example would be "red_02_hrt", and a "Point" object which is created when the image is found and that is what gives the x and y co-ordinates. 
With those two pieces of information, I store them as a key-value pair in a dictionary which already has keys for each destination. 
```
cards_on_screen = {
    "deck" : {}, "foundation" : {}, "column_1" : {},
    "column_2" : {}, "column_3" : {}, "column_4" : {},
    "column_5" : {}, "column_6" : {}, "column_7" : {},
    }
```
This is the nested dictionary I create to store the cards.

## Checking for moves

I have 6 functions that check for possible moves that can be made in the game and I will breifly describe how each function works.

### Ace card to foundation
For this function, it looks for any ace cards on screen and will try to move them to the foundation pile which is at the top of the scrren.
The first thing it checks is to see if there are already 4 cards up on the foundation. If that is the case, the ace cards have already been moved and so the function returns an empty list.
If not, a list of the empty foundation piles are added to a list. These foundation piles have been given a pre-determined x and y co-ordinate which I figured out. The code will then check to see if there are any ace cards on screen. Again, if there are none, an empty list is returned. If not, those ace card are also added to another list. Finally, a for loop is used that simply adds an ace card that can move and a position it can move to in a list that is then returned.

### Card to foundation
This function is similar to the one describe above, except that is searches the deck and the bottom of the columns to see if any card can be moved onto any of the foundation piles. 
First, the code will look at the cards that are currently in the foundation. It will then work out what cards can then be put on top of them. It does this by taking the card in the foundation and changing the colour and number.
```
if card_num.startswith("0"):
    card_num = int(card_num[1]) + 1
    new_card_num = "0" + str(card_num)
else:
    card_num = int(card_num) + 1
    new_card_num = str(card_num)
card_to_find = card_name[:3] + "_" + new_card_num + "_" + card_name[7:]
```
Here is snippet of the code that performs. I'll give an example to help understand it better. If for example there was an ace of hearts in the foundation, it would see that as red_01_hrt. So to find what card could go on that ace, it would find just change the value from 01 to 02.

### Moving a card from the deck to the column
This function will look at the card that can move from the deck and see if it can move to any of the columns below. To do this, it uses a similar system to moving cards to the foundation. This time however, it will look for cards differently. When moving a card from the deck to the column, it needs to move to a card of the opposite colour and also a number higher. For example, moving a black three of clubs to the red four of diamond. So the code will look at the card in the deck, flip the colour from red to black or vice versa, and then increase the number by four. However, the suit is not important as the suit does not need to be the same, and so this information is not needed.

### Moving king to an empty column
This function will simply look for any king cards on the screen that can be moved and move them to an empty column.
However, I do not want to move kings if they are a part of a stack, since moving a stack like that would be pointless.
I can check to see what columns are emptry by checking the length of each column dictionary and if any column is empty, that column name is added to a list. Again, I have a dictionary that stores pre-defined co-ordinates for where the kings can move to.
If any kings are found and there is an empty space it can move to, the king card will be added to a list along with the position it can move to. It can also move kings from the deck as well.

### Moving a card across columns
This function uses a similar structure to most of the other functions. It will look at the bottom card of every column to see if it can be moved to another column. Again, it look at each card, flip the color and then increase the number. It will then check the other columns to see if it can be moved there.

### Moving stacks across columns
To move stacks across columns, it again uses the same ideas as the previous functions. This time, it will look at the top of each stack to see whether or not it can be moved to the bottom of any other stack, using the same process as described above.

## Storing game states (zobrist hashing)
To help stop infinte loop moves, I have implemented a hash method that can take any game state and give it a unique value.
```
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
```
Here is the code for the function that creates random bitstring keys that can represent a specific game state. For example, an ace of hearts in the first foundation pile. Every card in the game can represented in this sort of way.
With this in mind, I create a table of randomly bitstring keys.

After I have done this, I can get the key for each card on screen and then use XOR with every value. After it XORs every key, it gives a single hash value that can represent a game state
This value can then be used when the code wants to make a move. If a move wants to happen that would result in a game state already seen i.e. looping, then the move will not happen. This prevents infinite looping in my code and could also be used as a way to see what game states were found during the course of solving a game of Solitaire.

## Solving the game
The way that my code solves the game is by making choices on what move would be best to help win the game.
I have a function called move_cards where the move evaulation is done.
The idea that I have implemented is to use a sort of tree structure represent the possible game states that can be seen from the current game state.

``` original_game_state = copy.deepcopy(game_state) # creates a copy of the original game state to come back to if needed ```

The first thing I do is create a copy of the current game state that I can come back to. That way I don't have to worry about making a mistake. Then the code will perform each possible move that has been passed into the function. These moves were obtained from the movement checking functions described above.
However, I do not move the cards on screen yet and only make changes in the dictionary. Once the move has been made, I have created a new game state that came from the original game state. The code will then use two factors to judge how good the move was.
```
score = 0
card_reveal = card_reveal_check(position_name) # check to see if the column the card(s) was moved from revealed a new card
if move_to_foundation == True:
    score += 5
if card_reveal == True:
    score += 3
```
Using a scoring system, I check to see whether this game state has moved a card to the foundation or revealed a new card.
From this new game state, the code will then also check what moves are possible from that game state. The moves that are found are also scored. Each move has it's own score associated with it and so every move that is found, its score is added to the total.

Once this has been done, I store the score and some variables needed to make the move on the screen and in the dictionary in an list. This is done with every move and I end up with a list of lists that contain possible game states to move to.
This list is then sorted by score. Which means I can select the first item in that list and this will be the move that will give the highest score and therefore the most potential for a good move.

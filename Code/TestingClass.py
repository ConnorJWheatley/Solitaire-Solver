import unittest
import SolitaireSolver
import pyautogui as pag

game_state = {'deck': {'blk_11_spa': pag.Point(x=621, y=137), 'red_08_hrt': pag.Point(x=593, y=138), 'red_09_dia': pag.Point(x=563, y=137)}, 
'foundation': {'blk_01_spa': pag.Point(x=906, y=136)}, 
'column_1': {'blk_02_spa': pag.Point(x=392, y=426), 'red_03_hrt': pag.Point(x=393, y=370)},
'column_2': {'blk_08_spa': pag.Point(x=563, y=445), 'red_09_hrt': pag.Point(x=563, y=389)}, 
'column_3': {'blk_03_spa': pag.Point(x=735, y=558), 'blk_05_spa': pag.Point(x=735, y=445), 'red_04_dia': pag.Point(x=736, y=501), 'red_06_hrt': pag.Point(x=737, y=390)}, 
'column_4': {'red_03_dia': pag.Point(x=906, y=389)}, 
'column_5': {'blk_13_spa': pag.Point(x=1078, y=425)}, 
'column_6': {'blk_12_spa': pag.Point(x=1249, y=517), 'red_13_hrt': pag.Point(x=1250, y=462)}, 
'column_7': {'red_13_dia': pag.Point(x=1421, y=479)}}

class TestingClass(unittest.TestCase):
    """
    This testing will be done on an image of the game state game_state.png in the testing folder
    """

    def test_ace_card_to_foundation(self):
        self.assertFalse(SolitaireSolver.ace_card_to_foundation(game_state)) # should be False

    def test_card_to_foundation(self):
        self.assertTrue(SolitaireSolver.card_to_foundation(game_state)) # should be True

    def test_move_from_deck_to_column(self):
        self.assertFalse(SolitaireSolver.move_from_deck_to_column(game_state)) # should be False

    def test_king_to_empty_space(self): # can do
        self.assertFalse(SolitaireSolver.move_king_to_empty_space(game_state)) # should be False

    def test_card_across_columns(self):
        self.assertTrue(SolitaireSolver.move_card_across_columns(game_state)) # should be True

    def test_stack_to_another_column(self):
        self.assertFalse(SolitaireSolver.stack_to_another_column(game_state)) # should be False

if __name__ == "__main__":
    # creates the suite from the test cases above
    suite = unittest.TestLoader().loadTestsFromTestCase(TestingClass)
    # runs that test suite
    unittest.TextTestRunner(verbosity=2).run(suite)


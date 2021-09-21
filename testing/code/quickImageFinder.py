import pyautogui as pag

position_regions_search = {"deck":(545, 640, 95, 55), "column_1":(375, 340, 35, 545), "column_2":(545, 340, 35, 545), "column_3":(720, 340, 35, 545), 
                            "column_4":(890, 340, 35, 545), "column_5":(1060, 340, 35, 545), "column_6":(1230, 340, 35, 545), "column_7":(1400, 340, 35, 545)}


# image_location = pag.locateCenterOnScreen("all_cards_symbols\\blk_09_clb.png", grayscale=False, region=(1230,340,33,545), confidence=0.948)
image_location = None

image_location = pag.locateCenterOnScreen("C:\\Users\\Connor\\Documents\\University\\Year 3\\CE301\\all_cards_tops\\blk_05_spa.png", grayscale=False, region = (370,105,1065,780), confidence=0.94)
print(image_location)
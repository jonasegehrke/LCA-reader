import numpy as np
import cv2
import pyautogui
import time

index = 0
old_overview_coords_top = 0
amountOfEmissions = 0


def findNextEmission(old_overview_coords_top):
    overview_coords = pyautogui.locateOnScreen('locators/overviewLocator.PNG', confidence=0.9)
    if(int(overview_coords.top) > 700):
        pyautogui.moveTo(overview_coords.left, overview_coords.top)
        pyautogui.scroll(-10)
        pyautogui.scroll(-10)
        pyautogui.scroll(-10)
        pyautogui.scroll(-10)
        pyautogui.scroll(-10)
        pyautogui.scroll(-10)
        print("scrolling")
        time.sleep(0.2)
        overview_coords = pyautogui.locateOnScreen('locators/overviewLocator.PNG', confidence=0.9)
    expected_RGB = pyautogui.pixel(int(overview_coords.left), int(overview_coords.top))
    yCord = 2
    xCord = 2
    
    while(True):

        if(pyautogui.pixelMatchesColor(int(overview_coords.left) + xCord, int(overview_coords.top) + yCord, expected_RGB)):
            yCord = yCord + 10
        else:
            if(int(old_overview_coords_top) == int(overview_coords.top)):
                return False
            pyautogui.click(int(overview_coords.left) + xCord, int(overview_coords.top) + yCord)
            return overview_coords.top
            

    #move the cursor pixel by pixel down
    
        #check if rgb is 255,255,255
            #if true -> click & remember coords


def takeScreens():
    #get coords for top image
    top_img_coordinates = pyautogui.locateOnScreen('locators/topLocator.PNG', confidence=0.9)
    #take topimage screenshot
    topImage = pyautogui.screenshot(region=(top_img_coordinates.left, top_img_coordinates.top, 570, top_img_coordinates.height - 60));
    #Prep the mouse for scrolling
    pyautogui.moveTo(top_img_coordinates.left + 100, top_img_coordinates.top + 200)
    #scroll
    pyautogui.scroll(-10)
    pyautogui.scroll(-10)
    pyautogui.scroll(-10)
    pyautogui.scroll(-10)
    #buffer
    time.sleep(0.2)
    #get coords for bottom image
    bottom_img_coordinates = pyautogui.locateOnScreen('locators/bottomLocator.PNG', confidence=0.9)
    #take bottom image screenshot
    bottomImage = pyautogui.screenshot(region=(bottom_img_coordinates.left, bottom_img_coordinates.top, 550, 360));

    #reset scroll
    pyautogui.scroll(10)
    pyautogui.scroll(10)
    pyautogui.scroll(10)
    pyautogui.scroll(10)

    #save images
    topImage = cv2.cvtColor(np.array(topImage), cv2.COLOR_RGB2BGR)
    bottomImage = cv2.cvtColor(np.array(bottomImage), cv2.COLOR_RGB2BGR)

    cv2.imwrite('results/{}-top.png'.format(index), topImage)
    cv2.imwrite("results/{}-bottom.png".format(index), bottomImage)


for y in range(200):
    for x in range(10):
        takeScreens()
        old_overview_coords_top = findNextEmission(old_overview_coords_top)
        index += 1
        amountOfEmissions += 1
        print(amountOfEmissions)
        if(old_overview_coords_top is False):
            print("done")
            break
    else:
        continue
    break
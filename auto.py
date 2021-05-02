import time
import pyautogui as pg

i = 0
targets = []

time.sleep(1)

while i <= 5:  # Stopper
    cell = pg.locateCenterOnScreen('Cell.png')
    print(cell)
    i += 1
    if cell:
        i = 0
        targets.append((cell[0], cell[1]))
    time.sleep(0.1)  # Sleep after each shot

for target in targets:
    pg.click(target)
    time.sleep(0.1)  # Timer not to be a bot too much
    
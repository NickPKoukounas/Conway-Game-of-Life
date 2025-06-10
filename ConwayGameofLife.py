from matplotlib.colors import ListedColormap
import numpy as np
import matplotlib as plt
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter


def initializegame():

    #Initializes game of life board
    
    rows = 20
    col = 20
    x = np.zeros((rows, col), dtype = int)
    x[8:11, 10] = 1 #add live cells
    x[9, 8] = 1
    x[10, 9] = 1
    return x

def alive(grid, x, y): 

#counts the amount of live cells around current index 

    count = 0
    length = len(grid)
    for deltaX in [-1, 0 ,1]:
        for deltaY in [-1, 0, 1]:
            if deltaY  == 0 and deltaX == 0: #doesnt count itself if alive
                continue
            newx, newy = (x + deltaX) % length, (y + deltaY) % length #modulo takes remainder to warp grid.
            count += grid[newx][newy]
    return count


def evolve(grid):

#Based on alive count and rules of the game, cells will either remain, become alive, or die.

    newgrid = [[0 for i in range(len(grid))] for j in range(len(grid))] #creates new grid to place next generation
    for x in range(len(grid)):
        for y in range(len(grid)):
            alivecount = alive(grid, x, y)
            if grid[x][y] == 1:
                if alivecount < 2: 
                    newgrid[x][y] = 0 #underpopulation
                if alivecount > 3: #overpopulation
                    newgrid[x][y] = 0
                if alivecount == 2 or alivecount == 3:#stasis
                    newgrid[x][y] = 1
            if grid[x][y] == 0: 
                if alivecount == 3: #reproduction
                    newgrid[x][y] = 1
    return newgrid

def update(image):
    global x #needed so x is not local in function
    ax.clear()
    ax.imshow(x, cmap = color) #creates image of x
    x = evolve(x) #changes x to next gen so it can get the image when looped
    return image

color = ListedColormap(['white', 'black'])
k = int(input("Enter number of generations: ")) #enters amount of generations wanted.(project based on 100 generations) 
if k < 0:
    print("An error occurred: k is a Non-negative k value")
else:

    x = initializegame()


    for _ in range(k):
        #Main function that evolves x by k iterations
        newgrid = evolve(x)
        x = newgrid

fig, ax = plt.subplots()
im = ax.imshow(x, cmap = color) #creates image of x which is the last evolution after main function is ran
try:
    fig.savefig('game_of_life.png')
except:
    print("Error saving image file")

ani = animation.FuncAnimation(fig, func = update, frames= k, repeat = False) #creates animation using update() to create images.

try:
    ani.save('game_of_life.gif', writer = PillowWriter(fps=10))
except:
    print("Error saving gif")

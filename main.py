"""
A simple Python/matplotlib implementation of Conway's Game of Life.

Author: Maosen Hu
"""

import sys, argparse
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

from src.conway import Conway

# main() function
def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.")
    # add arguments
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--glider', action='store_true', required=False)
    parser.add_argument('--gosper', action='store_true', required=False)
    args = parser.parse_args()
    
    conway = Conway()
    # set grid size
    conway.setGridSize(100)
    if args.N and int(args.N) > 8:
        conway.setGridSize(int(args.N))
        
    # set animation update interval
    updateInterval = 50
    if args.interval:
        updateInterval = int(args.interval)

    # check if "glider" demo flag is specified
    grid = conway.initGrid()
    if args.glider:        
        conway.addGlider(1, 1, grid)
    elif args.gosper:
        conway.addGosperGliderGun(10, 10, grid)
    else:
        # populate grid with random on/off - more off than on
        grid = conway.randomGrid()

    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, conway.update, fargs=(img, grid),
                                  frames = 10,
                                  interval=updateInterval,
                                  save_count=50)

    # # of frames? 
    # set output file
    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()

# call main
if __name__ == '__main__':
    main()
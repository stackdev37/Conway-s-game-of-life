import numpy as np

class Conway:
    CVC_ON: int
    CVC_OFF: int
    IV_vals = [int, int]
    IV_size: int
    
    def __init__(self) -> None:
        self.CVC_ON = 255
        self.CVC_OFF = 0
        self.IV_size = 100
        self.IV_vals = [self.CVC_ON, self.CVC_OFF]
    
    def initGrid(self):
        return np.zeros(self.IV_size * self.IV_size).reshape(self.IV_size, self.IV_size)
        
    def setGridSize(self, size):
        self.IV_size = size

    def randomGrid(self):
        """returns a grid of NxN random values"""
        return np.random.choice(self.IV_vals, self.IV_size * self.IV_size, p=[0.2, 0.8]).reshape(self.IV_size, self.IV_size)

    def addGlider(self, i, j, grid):
        """adds a glider with top left cell at (i, j)"""
        glider = np.array([[0,    0, 255], 
                        [255,  0, 255], 
                        [0,  255, 255]])
        grid[i:i+3, j:j+3] = glider

    def addGosperGliderGun(self, i, j, grid):
        """adds a Gosper Glider Gun with top left cell at (i, j)"""
        gun = np.zeros(11*38).reshape(11, 38)

        gun[5][1] = gun[5][2] = 255
        gun[6][1] = gun[6][2] = 255

        gun[3][13] = gun[3][14] = 255
        gun[4][12] = gun[4][16] = 255
        gun[5][11] = gun[5][17] = 255
        gun[6][11] = gun[6][15] = gun[6][17] = gun[6][18] = 255
        gun[7][11] = gun[7][17] = 255
        gun[8][12] = gun[8][16] = 255
        gun[9][13] = gun[9][14] = 255

        gun[1][25] = 255
        gun[2][23] = gun[2][25] = 255
        gun[3][21] = gun[3][22] = 255
        gun[4][21] = gun[4][22] = 255
        gun[5][21] = gun[5][22] = 255
        gun[6][23] = gun[6][25] = 255
        gun[7][25] = 255

        gun[3][35] = gun[3][36] = 255
        gun[4][35] = gun[4][36] = 255

        grid[i:i+11, j:j+38] = gun

    def update(self, frameNum, img, grid):
        # copy grid since we require 8 neighbors for calculation
        # and we go line by line 
        newgrid = grid.copy()
        for i in range(self.IV_size):
            for j in range(self.IV_size):
                # compute 8-neghbor sum
                # using toroidal boundary conditions - x and y wrap around 
                # so that the simulaton takes place on a toroidal surface.
                total = int((grid[i, (j-1)%self.IV_size] + grid[i, (j+1)%self.IV_size] + 
                            grid[(i-1)%self.IV_size, j] + grid[(i+1)%self.IV_size, j] + 
                            grid[(i-1)%self.IV_size, (j-1)%self.IV_size] + grid[(i-1)%self.IV_size, (j+1)%self.IV_size] + 
                            grid[(i+1)%self.IV_size, (j-1)%self.IV_size] + grid[(i+1)%self.IV_size, (j+1)%self.IV_size])/255)
                # apply Conway's rules
                if grid[i, j]  == self.CVC_ON:
                    if (total < 2) or (total > 3):
                        newgrid[i, j] = self.CVC_OFF
                else:
                    if total == 3:
                        newgrid[i, j] = self.CVC_ON
        # update data
        img.set_data(newgrid)
        grid[:] = newgrid[:]
        return img
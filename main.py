import pygame, sys, random
pygame.init()

size = 40
clock = pygame.time.Clock()
height, width = int(size * 12 * 1.61) , size * 12
surface = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sand")

drawing = False
timeStop = False
static = False

font = pygame.font.Font("freesansbold.ttf", 4*size//5)

lstSize = 300
sands = []
selectedSandSize = 4

rand = lambda a,b : random.randint(a,b)

clickedInArea = lambda e, mouse, left, top, right, bottom: e.type == pygame.MOUSEBUTTONDOWN and mouse[0] > left and mouse[1] > top and mouse[0] < right and mouse[1] < bottom

colors = {"red" : (255,0,0), "white" : (255,255,255), "blue" : (0,0,255), 
			"green" : (0,255,0), "cyan" : (0,255,255), "orange" : (255,170,0), 
			"yellow" : (255,255,0), "brown" : (192, 85, 0), "purple" : (201, 0, 211), "black" : (0,0,0)}
selectedColor = colors["white"]


class Sand(pygame.Rect):
	def __init__(self, isStatic, color, position, sandSize, index):
		self.isStatic = isStatic
		self.color = color
		self.index = index
		self.speed = 0
		self.g = 0.1
		self.sandSize = sandSize
		super().__init__(position[0], position[1], self.sandSize, self.sandSize)

	def draw(self):
		pygame.draw.ellipse(surface, self.color, (self.x, self.y, self.sandSize, self.sandSize))

	def update(self):
		global sands, height, lstSize
		if not self.isStatic:
			if self.left > 0 and self.right < width and self.bottom+1 < height:
				if surface.get_at((self.left, self.bottom + 1)) != (0,0,0) or surface.get_at((self.right, self.bottom + 1)) != (0,0,0):
					self.g = 0
					self.speed = 0
			self.speed += self.g
			self.bottom += self.speed
			self.g = 0.1
			if self.y > height:
				sands.remove(self)
				lstSize -= 1
				del self
				return


class Buttons():
	def __init__(self):
		self.drawColorBar()
		self.drawClock()
		self.drawEraser()
		self.drawPenSize()
		self.drawFixedOrFree()

	def drawColorBar(self):
		i = 0
		for color in colors:
			pygame.draw.rect(surface, color, (i * size + i*0.2*size, height - size, 1.23*size, size))
			i += 1
		pygame.draw.aaline(surface, colors["white"], (0, height - size - 2), (width, height - size - 2))
			
	def drawClock(self):
		clockColor = None
		if timeStop:	clockColor = colors["red"]
		else:			clockColor = colors["white"]
		pygame.draw.ellipse(surface, clockColor, (width - 40, 10, 30,30))
		pygame.draw.ellipse(surface, colors["black"], (width - 37, 13, 24, 24))
		pygame.draw.aaline(surface, clockColor, (width - 25, 19), (width - 25, 25))
		pygame.draw.aaline(surface, clockColor, (width - 30, 30), (width - 25, 25))
		pygame.draw.rect(surface, clockColor, (width - 27, 7, 4, 3))
		pygame.draw.rect(surface, clockColor, (width - 29, 4, 8, 3))

	def drawEraser(self):
		pygame.draw.aaline(surface, colors["white"], (5*width/12-15,10), (5*width/12+15,25))
		pygame.draw.aaline(surface, colors["white"], (5*width/12-25,25), (5*width/12+5,40))
		pygame.draw.aaline(surface, colors["white"], (5*width/12-15,10), (5*width/12-25,25))
		pygame.draw.aaline(surface, colors["white"], (5*width/12+15,25), (5*width/12+5,40))
		for i in range(1,8):
			pygame.draw.aaline(surface, colors["white"], (5*width/12-15+i, 10 + i-4), (5*width/12-25+i, 25 + i-4))
		pygame.draw.aaline(surface, colors["black"], (5*width/12-15,10-1), (5*width/12+15,25-1))
		pygame.draw.aaline(surface, colors["black"], (5*width/12-15,10-2), (5*width/12+15,25-2))
		pygame.draw.aaline(surface, colors["black"], (5*width/12-15,10-3), (5*width/12+15,25-3))
		
		# pygame.draw.rect(surface, colors["white"], (width/2 - 15, 10, 40, 20))
		# pygame.draw.rect(surface, colors["black"], (width/2 - 12, 13, 34, 14))
		# pygame.draw.rect(surface, colors["white"], (width/2 - 12, 13, 10, 14))
		# pygame.draw.rect(surface, colors["black"], (width/2 - 12, 13, 7, 14))

	def drawPenSize(self):
		pygame.draw.rect(surface, selectedColor, (5*width/8, 10, size,size))
		pygame.draw.rect(surface, colors["black"], (5*width/8 + 5, 15, size - 10, size - 10))
		# pygame.draw.ellipse(surface, colors["white"], (5*width/8 + 30 - selectedSandSize/2, 45 - selectedSandSize/2, selectedSandSize, selectedSandSize))
		pygame.draw.ellipse(surface, selectedColor, (5*width/8 + size/2 - selectedSandSize/2, 10 + size/2 - selectedSandSize/2, selectedSandSize, selectedSandSize))
	
	def drawFixedOrFree(self):
		if static:
			surface.blit(font.render("Fixed", True, colors["white"]), (10, 10))
		else:
			surface.blit(font.render("Free", True, colors["white"]), (10, 10))
			

def eventCheck():
	global drawing, static, sands, lstSize, timeStop, selectedColor, selectedSandSize

	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			sys.exit()
		elif e.type == pygame.MOUSEBUTTONDOWN:
			if e.button == 1:            
				drawing = True
		elif e.type == pygame.MOUSEBUTTONUP:
			if e.button == 1:            
				drawing = False
		elif e.type == pygame.MOUSEMOTION:
			if drawing:
				mouse_x, mouse_y = e.pos
				sands.append(Sand(static, selectedColor, (mouse_x, mouse_y), selectedSandSize, len(sands)))
				lstSize += 1

		mouse = pygame.mouse.get_pos()
		if clickedInArea(e, mouse, width-40, 0, width, 40):
			timeStop = not timeStop
		if clickedInArea(e, mouse, 0, height - size, width, height):
			selectedColor = surface.get_at((mouse[0], mouse[1]))
		if clickedInArea(e, mouse, 0, 0, 2*size, size):
			static = not static
		if clickedInArea(e, mouse, 5*width/12-25, 10, 5*width/12+15, 40):
			sands = []
			lstSize = 0
			surface.fill(colors["black"])
		if clickedInArea(e, mouse, 5*width/8, size//3, 5*width/8 + size, size * 1.25):
			if selectedSandSize > size // 3:
				selectedSandSize = 0
			selectedSandSize += size // 16

for i in range(lstSize):
	sands.append(Sand(False, (rand(0,255), rand(0,255), rand(0,255)), (rand(0,width), rand(0,height//3)), selectedSandSize, i))

while True:
	clock.tick(100)
	eventCheck()

	surface.fill(colors["black"])
	for sand in sands:
		sand.draw()
	if not timeStop:
		for sand in sands:
			sand.update()
	Buttons()

	pygame.display.update()
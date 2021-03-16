import pygame
from pygame.locals import *  
from random import randrange
pygame.mixer.pre_init(22050, -16, 2, 1024)  
pygame.init()

size = (640, 480) #must play on this resolution since mostly everything is hardcoded for this
screen = pygame.display.set_mode(size)
pygame.display.set_caption("farmgame")

bg_colour = (50,205,50)
background = pygame.Surface(size).convert()
background.fill(bg_colour)
screen.blit(background, (0,0))
    
clock = pygame.time.Clock()
keep_going = True

tomatoes = 0
seeds = 0
cash = 2000

fertility = 1


class Plot(pygame.sprite.Sprite): #plot will have a tomato on it
    
    def __init__(self, top_left_corner):
        '''
        P.Plot([x,y]) --> Plot
        Construct a (locked) plot class at the coordinates x,y
        
        Plot class has variables responsible for water level and an associated plant object.
        '''
        pygame.sprite.Sprite.__init__(self)  
        self.image = pygame.image.load("locked_plot.png").convert()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.water_level = 0
        self.unlocked = False
        self.plant_in_plot = None #reference to the plant in the plot
        self.rect.topleft = top_left_corner

    def get_water(self):
        '''
        P.get_water() --> int
        Returns int variable of what the water level of the plot is
        '''
        
        return self.water_level
    
    def is_unlocked(self):
        '''
        P.is_unlocked() --> boolean
        Returns boolean of the plots unlocked status
        '''
        return self.unlocked
    
    def plant_here(self):
        '''
        P.plant_here() --> None or Plant
        Returns the reference to the plant linked to this plot
        '''
        return self.plant_in_plot
    
    def unlock(self):
        '''
        P.unlock() --> None
        Unlocks the plot
        '''
        
        self.unlocked = True
        self.image = pygame.image.load("dirt1.png").convert()
        self.image = pygame.transform.scale(self.image, (50, 50))
        
    def plantplant(self): #the only way to create a plant class is through this function
        '''
        P.plantplant() --> None
        Plants a plant in this plot
        '''
        
        if self.plant_in_plot == None and self.unlocked:
        
            self.plant_in_plot = Plant(self.rect.topleft, self)

    def update_plot(self): #should be renamed dry_up, but too late for that
        '''
        P.update_plot() --> None
        Updates the plots water so it dries up over time, calls water_change()
        '''
        if randrange(0,1000) == 0 and self.get_water() > 0 and self.is_unlocked() == True:
            self.water_change(False) #dries up 
    
    def water_change(self, change_boolean): #true for more water, false for less
        '''
        P.water_change(boolean) --> None
        Put True if want to increase water; False to decrease. Updates the sprite along with the water change
        that occured. Water level can only change by one incriment at a time.
        '''
        
        if self.is_unlocked() == True:

            if change_boolean == True and self.get_water() < 8:

                self.water_level += 1
                
            if change_boolean == False and self.get_water() > 0:

                self.water_level -= 1
            
            image_name = ""
            if self.get_water() == 0:             
                image_name = "dirt1.png"
                
            elif self.get_water() == 1:
                image_name = "dirt2.png"
                                
            elif self.get_water() == 2:
                image_name = "dirt3.png"
                                
            elif self.get_water() == 3:
                image_name = "dirt4.png"
                                
            elif self.get_water() == 4:
                image_name = "dirt5.png"
                                
            elif self.get_water() == 5:
                image_name = "dirt6.png"
                                
            elif self.get_water() == 6:
                image_name = "dirt7.png"
                                
            elif self.get_water() == 7:
                image_name = "dirt8.png"
            
            if self.get_water() >= 0 and self.get_water() < 8:
                self.image = pygame.image.load(image_name).convert()
                self.image = pygame.transform.scale(self.image, (50, 50))              

class Plant(pygame.sprite.Sprite):
        def __init__(self, top_left_corner, plot_reference):
            '''
            P.Plant([x,y], Plot)
            Initializes a Plant class, through Plot functions plantplant().
            '''
            pygame.sprite.Sprite.__init__(self)  
            self.image = pygame.image.load("tomato32.png").convert()
            self.image.set_colorkey(self.image.get_at((0,0)))
            self.rect = self.image.get_rect()
            self.harvest = False
            self.plants_plot = plot_reference #reference to the plot that the plant is in. use plot class 

            self.rect.topleft = top_left_corner
            plant_group.add(self)
            
            self.reference() #constructs reference to plot. necessary dont delete in future it wont work if deleted
        
        def reference(self): #this is to reference it to the plot, since plantplant() makes plant_in_plot = Plant(whatever)
            '''
            P.reference() --> Plant
            A helper class for the constructor that creates a reference for the associated Plot to use, since this doesn't
            work in the constructor
            '''
            return self
        
        def get_plant_water(self):
            '''
            P.get_plant_water() --> p.plants_plot.get_water() --> int
            Calls the plants plot class to return its level of water
            '''
            
            return self.plants_plot.get_water()

        
        def update_plant(self):
            '''
            P.update_plant() --> None
            Updates the plant so it has a chance to be harvestable.
            '''
            
            global fertility
            harvest_chance = self.get_plant_water() * fertility #fertilizer growth upgrade
            
            while harvest_chance > 0:
                harvest_chance -= 1
                if randrange(0, 10000) == 69:
                    self.harvest = True
            
            if self.harvest == True:
                self.harvest_time()
        
            
        
        def harvest_time(self): #only callable through update_plant
            '''
            P.harvest_time() --> None
            Only callable through update_plant(). Updates plant sprite so that it represents a harvestable tomato plant.
            It is not harvested yet.
            '''
            
            self.image = pygame.image.load("tomato32ripe.png").convert()
            self.image.set_colorkey(self.image.get_at((0,0)))
            #self.image = pygame.transform.scale(self.image, (10, 10))                   
            
        def harvested(self):
            '''
            P.harvested() --> None
            Harvests the tomato plant for tomatoes. Adds tomatoes and deletes the plant after getting the tomatoes from it.
            '''
            
            
            global tomatoes #dont delete this line
            self.plants_plot.plant_in_plot = None
            tomatoes += randrange(1,20)
            self.kill()

class Button(pygame.sprite.Sprite): #rip off of Plot() retitled as button
    
    def __init__(self, top_left_corner, button_type):
        '''
        Initializes a button class with three working types but four types in total. A tomato button
        that sells tomatoes, a fertilizer button that buys fertilizer, a plot button that does not work but 
        is intended to purchase plots (redundant since you can click), and a seeds button that buys seeds.
        '''
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("{}_button.png".format(button_type)).convert()
        self.image = pygame.transform.scale(self.image, (125, 75))
        self.rect = self.image.get_rect()
        self.button_job = button_type
        self.rect.topleft = top_left_corner   

class Market():
    def __init__(self):
        '''
        Market class is responsible for dictating the prices and change in inventory.
        '''
        self.tomato_price = randrange(2,15) #can be replaced with calling update_tomato_price()?
        self.seed_price = randrange(5, 20)
        self.plot_price = randrange(200, 1000)
        
        self.fertilizer_price = 200
        
    def tomato_price(self):
        '''
        m.tomato_price() --> int
        Returns the price of a tomato
        '''
        return self.tomato_price
    
    def seed_price(self):
        '''
        m.seed_price() --> int
        Returns the price of a seed
        '''
        return self.seed_price
    
    def plot_price(self):
        '''
        m.plot_price() --> int
        Returns the price of a plot
        '''
        return self.plot_price
    
    def update_prices(self):
        '''
        m.update_prices() --> None
        Calls all variables for updating prices to update every price
        '''
        self.update_tomato_price()
        self.update_seed_price()
        self.update_plot_price()
    
    def update_tomato_price(self):
        '''
        m.update_tomato_price() --> None
        Updates the selling price of tomatoes
        '''
        self.tomato_price = randrange(2,10)
    
    def update_seed_price(self):
        '''
        m.update_seed_price() --> None
        Updates the price of seeds cost
        '''
        self.seed_price = randrange(5, 20)
        
    def update_plot_price(self):
        '''
        m.update_plot_price() --> None
        Updates the cost of buying a plot
        '''
        self.plot_price = randrange(200, 1000)
    
    def buy_fertility(self):
        '''
        m.buy_fertility() --> None
        Buys a level of fertility. Is also updated through this class since the price multiplies by 
        a factor of two each purchase
        '''
        global cash
        global fertility
        if cash > self.fertilizer_price:
            fertility += 1 
            cash -= self.fertilizer_price
            self.fertilizer_price = self.fertilizer_price * 2
        
    def sell_tomato(self):
        '''
        m.sell_tomato()
        Sells tomatoes. Originally intended to sell one tomato, hence the wrong name, but to prevent carpal tunnel from excessive clicking
        it now sells all of the tomatoes.
        '''
        global tomatoes
        global cash
        if tomatoes > 0:
            cash += self.tomato_price * tomatoes
            tomatoes -= tomatoes #sell all tomatoes to avoid carpal tunnel
    
    def buy_seed(self):
        '''
        m.buy_seed()
        Buys a seed.
        '''
        global seeds
        global cash
        if cash > self.seed_price:
            seeds += 1
            cash -= self.seed_price
    
    def buy_plot(self, purchasing_plot):
        '''
        m.buy_plot()
        Buys a plot.
        '''
        global cash
        if cash > self.plot_price:
            cash -= self.plot_price
            purchasing_plot.unlock()

font_end = pygame.font.Font('freesansbold.ttf', 32) 

font_market = pygame.font.Font('freesansbold.ttf', 16)

market = Market() #create the market

plot_group = pygame.sprite.OrderedUpdates() # the Group object for the plots, starting top left then continuing down each column

plant_group = pygame.sprite.OrderedUpdates()

button_group = pygame.sprite.OrderedUpdates() #buttons should be the same as plots, clickable

for row in range(5): #rows are --
    for column in range(5): #columns are |
        
        plot = Plot((50 + row * 50, 50 + column * 50)) 
        plot_group.add(plot)

for row in range(2): # --

    for column in range(2): # |
        if row == 0 and column == 0:
            button = Button((325 + row *125, 220 + column * 75), "seed")
        elif row == 0 and column == 1:
            button = Button((325 + row *125, 220 + column * 75), "tomato")
        elif row == 1 and column == 0:
            button = Button((325 + row *125, 220 + column * 75), "fertilizer")  
            
        button_group.add(button)

market_timer = 0

while keep_going:
    clock.tick(60)
    for ev in pygame.event.get():
        if ev.type == QUIT:
            keep_going = False
            
        elif ev.type == MOUSEBUTTONDOWN:

            for p in plot_group.sprites(): 
                if p.rect.collidepoint(ev.pos) and p.unlocked: #IF PLOT IS UNLOCKED
                    
                    if p.plant_in_plot == None and seeds > 0: #if no plant, plant one
                        p.plantplant()
                        seeds -= 1
                    
                    elif p.plant_in_plot != None and p.plant_in_plot.harvest == True: #IF A PLANT HARVESTABLE, DON'T WATER
                        p.plant_in_plot.harvested() 
                        
                    else: #elsecase, just water the plot if plant unharvestable or no plant
                        
                        p.water_change(True)
                    
                if p.rect.collidepoint(ev.pos) and p.unlocked == False: #IF LOCKED
                    market.buy_plot(p)
            
            
            for b in button_group.sprites():
                if b.rect.collidepoint(ev.pos):
                    
                    if b.button_job == "tomato":
                        market.sell_tomato()
                    elif b.button_job == "seed":
                        market.buy_seed()
                    elif b.button_job == "fertilizer":
                        market.buy_fertility()
            
        elif ev.type == KEYDOWN:
            pass #originally intended for future endeavors 

    
    plot_group.clear(screen, background) 
    plant_group.clear(screen, background)
    button_group.clear(screen, background)
    
    
    screen.blit(background, (0,0)) #do not move this
    
    market_title = font_end.render("market",True,[0,0,0])
    
    screen.blit(market_title, [110, 310])
    
    tomato_price = font_market.render("tomato price: {}".format(market.tomato_price),True,[178,34,34])
    
    screen.blit(tomato_price, [110, 350])
    
    seed_price = font_market.render("seeds price: {}".format(market.seed_price),True,[139,69,19])
    
    screen.blit(seed_price, [110, 370])
    
    plot_price = font_market.render("plot price: {}".format(market.plot_price),True,[112, 84, 49])
    
    screen.blit(plot_price, [110, 390])
    
    fertilizer_price = font_market.render("fertilizer price: {}".format(market.fertilizer_price),True,[237, 166, 14])
    
    screen.blit(fertilizer_price, [110, 410])
    
    tomato_text = font_end.render("tomatoes: {}".format(tomatoes),True,[178,34,34])
    
    screen.blit(tomato_text, [375,20])
    
    cash_text = font_end.render("cash: {}".format(cash),True,[113, 244, 66])
    
    screen.blit(cash_text, [375, 70])
    
    seeds_text = font_end.render("seeds: {}".format(seeds),True,[139,69,19])
    
    screen.blit(seeds_text, [375, 120])
    
    fertility_text = font_end.render("fertility: {}".format(fertility),True,[237, 166, 14])
    
    screen.blit(fertility_text, [375, 170])
    
    
    for p in plot_group:
        p.update_plot()
    
    for plant in plant_group:
        plant.update_plant()
        
    market_timer += 1
    if market_timer == 120:
        market.update_prices()
        market_timer -= 120

    
    plant_group.update(screen)
    plot_group.update(screen)
    button_group.update(screen)
    
    plot_group.draw(screen)
    plant_group.draw(screen)
    button_group.draw(screen)
    pygame.display.flip()                
    
    
    
#!/usr/bin/env python

from __future__ import division

import curses
import curses.panel
import logging
import time
import random
import textwrap

### Classes
#
#   objects:
#       Games   OR
#       Things:
#           Actors:
#               Humans  OR
#               Rats    OR
#               Shades
#
###


#TODO: turn gamelogger into a class
#TODO: add minimum and maximum arguments to creation call logic

def main(stdscr):

    global game     # must be global for reference by other objects
    
    # initialize game
    game = Game(stdscr) # must hand-off stdscr on initialization
                        # so that curses can properly initialize

    # initialize the Game Log window
    game.initGameLog()

    # initialize the stat display window
    game.initStatDisplay()

    game.initMenu()

    # start the game itself
    game.startGame()

    # while game is being played, execute main loop
    while game.playing:
        game.doLoop()

class Game:
    #TODO: add other funtion calls to docstring
    """
    Game objects hold the entire logic and all objects for creating and
        maintaining the game within themselves. All flow is tracked through
        the game object except for curses calls.

        __init__()  =   initializes a game instance
    """

    def __init__(self,
        stdscr):
        #TODO: rewrite docstring
        """ compulsory init function """

        # initializes the logger module and gives it to game instance
        self.logger = self.initLogger()
           
        # initialize serial as integer with value 0
        self.serial = self.initSerial(0)

        # initialize terminal_mode as boolean True
        self.terminal_mode = self.initTerminalMode(True)

        # give the game an empty list to keep track of things on
        self.things = self.initThings()

        # define the loop counter as an integer at 0
        self.loop_count = self.initLoopCount(0)

        # time in seconds
        self.time = 0

        self.exp_base = 10

        # initialize playing boolean to False
        self.playing = self.initPlaying(False)

        # initialize the curses module/objects and give it to game
        self.curses = self.initCurses(stdscr)

        # initialize the color dictionary for the game
        self.colors = self.initColors()
          
        # initialize the game board object and give to game 
        self.board = self.initBoard() 
  
 
    def getSerial(self):
        """
        Increments by one and returns a new serial string.
        """

        self.logger.debug('getting serial number . . .')
        self.logger.debug('self.serial was <%s>', 
            str(format(self.serial, '07d')))        

        # increment the serial value by one
        self.serial += 1

        self.logger.debug('self.serial is <%s>', 
            str(format(self.serial, '07d')))

        # return the serial number in as a 7 digit string
        return str(format(self.serial, '07d'))

    
    def startGame(self):
        #TODO: improve this docstring
        """
        Starts the game
        """

        self.logger.info('starting game . . .')

        # load the game map
        self.loadMap(fast=True)

        # initialize the player thing
        #self.initHero(
        #    board.camera_center_y,
        #    board.camera_center_x)
        self.logger.critical('camera y,x is <%s>,<%s>',
            str(board.camera_center_y), str(board.camera_center_x))

        # toggle the playing state
        self.togglePlaying()

        
    def doLoop(self):
        #TODO: improve this docstring        
        """ this is the main loop of the game """

        game.logger.debug('= = = = = new loop = = = = =')
        
        #game.logger.debug('TEST7: player level is <%s>', str(hero.level))
        #game.logger.debug('TEST7: player experience is <%s>', str(hero.experience))
        #game.logger.debug('TEST7: player level is <%s>', str(hero.level))
        #game.logger.debug('testing humanoid class: <%s>', str(hero.test_attribute))


        # increment the loop count
        self.incrementLoop()



        self.time += 1

        self.logger.debug('player hp: <%s>/<%s>',
            #str(hero.actor.hp), str(hero.actor.max_hp))
            str(hero.hp), str(hero.max_hp))

        self.logger.critical('equipped: <%s>',
            str(hero.hand.equipped))

        # loop things
        for thing in self.things:

            # move actors
            if isinstance(thing, Actor):
                if not thing.corpse:
                    thing.logic.takeTurn()

            # tick terrains
            if isinstance(thing, Terrain):
                thing.doTick()

        # ticks
        #for thing in self.things:
            #if isinstance(thing, Terrain):
            #    thing.doTick()

        # clear the stat display
        self.statdisplay.canvas.addstr(
            2,
            2,
            '                                          ')
        self.statdisplay.canvas.addstr(
            3,
            2,
            '                                          ')
        self.statdisplay.canvas.addstr(
            4,
            2,
            '                                          ')

        health = ('hp: ' 
            + str(hero.hp) 
            + ' / ' + str(hero.max_hp))
        self.statdisplay.canvas.addstr(
            2,
            2,
            str(health))

        experience = ('exp: '
            + str(hero.experience))
        self.statdisplay.canvas.addstr(
            4,
            2,
            str(experience))

        gold = ('gold '
            + str(hero.gold))
        self.statdisplay.canvas.addstr(
            3,
            2,
            str(gold))

        time = ('time: '
            + str(self.time))
        self.statdisplay.canvas.addstr(
            2,
            20,
            str(time))
  
        self.statdisplay.canvas.noutrefresh()

        hero_y1 = max(hero.y - hero.view_radius - 2, board.first_y)
        hero_y2 = min(hero.y + hero.view_radius + 2, board.last_y)
        hero_x1 = max(hero.x - hero.view_radius - 2, board.first_x)
        hero_x2 = min(hero.x + hero.view_radius + 2, board.last_x)

        # TODO: modify this to reduce work when zoomed in
        #if board.camera_zoom == 5:
        if 1 <= board.camera_zoom <= 2:

            camera_y1 = int(board.camera_center_y
                - (board.dimensions['max_y'] - board.dimensions['beg_y']) / 2)
            camera_y2 = int(camera_y1 + board.dimensions['max_y'])
            camera_x1 = int(board.camera_center_x
                - (board.dimensions['max_x'] - board.dimensions['beg_x']) / 2)
            camera_x2 = int(camera_x1 + board.dimensions['max_x'])

        else:

            camera_y1 = board.camera_corner[0]
            camera_y2 = board.camera_corner[0] + board.dimensions['max_y']
            camera_x1 = board.camera_corner[1]
            camera_x2 = board.camera_corner[1] + board.dimensions['max_x']

        #y1 = min(hero_y1, camera_y1)
        y1 = max(hero_y1, camera_y1)
        #y2 = max(hero_y2, camera_y2)
        y2 = min(hero_y2, camera_y2)
        #x1 = min(hero_x1, camera_x1)
        x1 = max(hero_x1, camera_x1)
        #x2 = max(hero_x2, camera_x2)
        x2 = min(hero_x2, camera_x2)

        #y1 = max(y1, board.camera_corner[0])
        #y2 = min(y2, board.

        #if board.camera_zoom == 0:

            #y1 = int(board.camera_center_y
            #    - (board.dimensions['max_y'] - board.dimensions['beg_y']) / 2)
            #y2 = int(y1 + board.dimensions['max_y'])
            #x1 = int(board.camera_center_x
            #    - (board.dimensions['max_x'] - board.dimensions['beg_x']) / 2)
            #x2 = int(x1 + board.dimensions['max_x'])


        #self.logger.critical('y1, y2, x1, x2 = <%s>, <%s>, <%s>, <%s>',
        #    str(y1), str(y2), str(x1), str(x2))

        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                if not x & 1:
                    continue 
                board.drawSpace(y, x)
                #game.logger.critical('space at <%s>,<%s>',
                #    str(y), str(x)) 

        #for space in board.spaces.values():
        #    board.drawSpace(space.y, space.x)

        # prepare to update the board canvas at its current size/position
        board.canvas.noutrefresh(
            board.camera_corner[0],
            board.camera_corner[1],
            board.dimensions['beg_y'],
            board.dimensions['beg_x'],
            board.dimensions['max_y'],
            board.dimensions['max_x'])

        game.gamelog.frame.noutrefresh(
            0 + self.gamelog.position,
            0,
            self.gamelog.dimensions['beg_y'],
            self.gamelog.dimensions['beg_x'],
            self.gamelog.dimensions['max_y'],
            self.gamelog.dimensions['max_x'])

        #game.menu.content.noutrefresh()

        self.curses.panel.update_panels()

        self.curses.doupdate()

        user_input = board.canvas.getch()

        self.logger.critical("user_input is <%s>",
            str(user_input))

        # stop the game if the user presses "ENTER"
        if user_input == 10:
            #game.playing = False
            game.toggleZoom()

        # if the user presses 'g'
        elif user_input == 103:
            game.logger.critical('TEST20')
            hero.pickUp()

        # if the user presses 'm'
        elif user_input == 109:
            self.browseMenu('inventory')

        #TODO: fix this to use "hero.move"
        elif (user_input == curses.KEY_UP           # if input is up arrow
            or user_input == 119):                  # or input is 'w'
            hero.move(-1, 0)                 # move up

        elif user_input == 101:                     # if input is 'e'
            hero.move(-1, 1)                 # move up-right

        elif (user_input == curses.KEY_RIGHT        # if input is right arrow
            or user_input == 100):                  # or input is 'd'
            hero.move(0, 1)                  # move right

        elif user_input == 99:                      # if input is 'c'
            hero.move(1, 1)                  # move down-right

        elif (user_input == curses.KEY_DOWN         # if input is down arrow
            or user_input == 120):                  # or input is 'x'
            hero.move(1, 0)                  # move down

        elif user_input == 122:                     # if input is 'z'
            hero.move(1, -1)                 # move down-left

        elif (user_input == curses.KEY_LEFT         # if input is left arrow
            or user_input == 97):                   # or input is 'a'
            #hero.actor.player.move(0, -1)           # move left
            hero.move(0, -1)                 # move left

        elif user_input == 113:                     # if input is 'q'
            #hero.actor.player.move(-1, -1)          # move up-left
            hero.move(-1, -1)                # move up-left

        self.curses.flushinp()


    def initColors(self):
        """ Returns a color dictionary: 
            
                Used for simple color assignment.
                Requires color pairs to already by initialized.
         """

        self.logger.info('initializing colors . . .')

        # initialize the color dictionary
        colors = {

            # white foreground, black background
            'white'         :   self.curses.color_pair(0),

            # yellow foreground, black background
            'yellow'        :   self.curses.color_pair(1),

            # blue foreground, black background
            'blue'          :   self.curses.color_pair(2),

            # green foreground, black background
            'green'         :   self.curses.color_pair(3),

            # black foreground, white background
            'black_white'   :   self.curses.color_pair(4),

            # red foreground, black background
            'red'           :   self.curses.color_pair(5),

            # black foreground, green background
            'black_green'   :   self.curses.color_pair(6),

            # black foreground, yellow background
            'black_yellow'  :   self.curses.color_pair(7),

            # black foreground, blue background,
            'black_blue'    :   self.curses.color_pair(8),
        
            # black foreground, red background
            'black_red'     :   self.curses.color_pair(9),

            # magenta foreground, black background
            'magenta'       :   self.curses.color_pair(10),
    
            # red foreground, white background
            'red_white'     :   self.curses.color_pair(11),

            # a cyan foreground, black background
            'cyan'          :   self.curses.color_pair(12)

            }

        self.logger.debug('colors type = <%s>, length = <%s>',
            str(type(colors)), str(len(colors)))

        # if logger is in DEBUG mode
        if self.logger.getEffectiveLevel() == 10:
            for name, pair in colors.items():
            
                self.logger.debug('color name = <%s>, pair = <%s>',
                    str(name), str(pair))

        # return the colors dictionary object
        return dict(colors)


    def toggleZoom(self):
        if board.camera_zoom == 2:
            board.camera_zoom = 0
        elif board.camera_zoom == 0:
            board.camera_zoom = 1
        elif board.camera_zoom == 1:
            board.camera_zoom = 2

        board.camera_center_y = hero.y
        board.camera_center_x = hero.x

        for space in board.spaces.values():
            board.drawSpace(space.y, space.x)


    def initLoopCount(self,
        initial_value=int(0)):
        """
        Initializes the loop counter:

            Used for tracking how many loops have occurred in game.

            initial_value   =   The value which the $loop_counter integer
                                will initialize at.
        """ 

        # logging
        self.logger.info('initializing game loop counter . . .')

        loop_counter = int(initial_value)

        # logging
        self.logger.debug('$loop_counter = <%s>', str(loop_counter))

        # return the initialized integer
        return(int(loop_counter))
    

    def browseMenu(self,
        kind):
        menu_open = True

        #self.doMenu('inventory')

        if kind == 'inventory':

            position = 2

            while menu_open:

            #self.doMenu('inventory')

                items = hero.inventory
                y = 4
                x = 3

                #self.menu.content.clear()
                self.menu.content.erase()
                self.menu.content.border()

                self.menu.content.addstr(
                    y - 2,
                    x - 1,
                    'Inventory',
                    curses.A_UNDERLINE)

            
    
                for item in items:

                    if item.equipped:
                        continue

                    game.logger.critical('item is <%s>_<%s>',
                        str(item.name), str(item.serial))

                    attr = curses.A_NORMAL

                    game.logger.critical('y is <%s>, position is <%s>',
                        str(y), str(position))

                    if y == position:

                        attr = curses.A_REVERSE

                    self.menu.content.addstr(y, x, item.name, attr)

                    y += 2

                self.menu.content.noutrefresh()

                self.curses.doupdate()

                user_input = self.menu.content.getch()

                self.logger.critical('user_input is <%s>', str(user_input))
 
                # if the user presses 'enter'
                if user_input == 10:
                    #menu_open = False
                    hero.equip(item)

                # if user presses 'backspace'
                elif user_input == 263:
                    menu_open = False

                elif user_input == curses.KEY_UP:
                   
                    if position > 4:

                        position -= 2

                elif user_input == curses.KEY_DOWN:
    
                    if position < (len(items) * 2 + 2):
                        
                        position += 2


    def initPlaying(self,
        playing = bool(False)):
        """
        Initializes the playing state of the game instance:

            Should typically be false, so that game can be started by a
            separate function call.

            playing     =   The default state that the game instance will
                            start with for $playing.
        """

        self.logger.info('initializing game $playing value . . .')
        self.logger.debug('$playing = <%s>', str(playing))

        # return the value of playing
        return(playing)     # returns the same value that was given \
                            #   primary motivation for function call is \
                            #   logging.


    def initSerial(self,
        initial_value=0):
        """
        Initializes the serial number used for uniquely identifying things:

            initial_value   =   This will be the starting value for serial
                                number. If no value is given, it will default
                                to 0.
        """
        
        # logging
        self.logger.info('initializing game serial')

        # serial counter used for uniquely identifying things
        serial = int(initial_value) # initialize at 0

        # logging
        self.logger.debug('new $serial = <%s>', str(serial))
        return int(serial)  # return serial as an integer


    #TODO: this should be toggle-able based on user input and/or
    #       host settings scan. Needs options menu?
    def initTerminalMode(self, on=True):
        """
        Returns the initial value for $terminal_mode:

            on  =   Determines which state to initialize $terminal_mode to.
                    If $on is true, $terminal_mode will be true. If $on is
                    not true, $terminal_mode will be false.
        """

        # logging
        self.logger.debug('initializing $terminal_mode . . .')
        self.logger.debug('$on = <%s>', str(on))

        # set terminal_mode
        if on:                          # if 'on' is True
            terminal_mode = bool(True)  # initialize term_mode as on (true)
        else:                           # otherwise
            terminal_mode = bool(False) # initialize it as off (false)
        
        # logging
        self.logger.debug('$terminal_mode = <%s>', str(terminal_mode))

        # return the $terminal_mode value to caller
        return(terminal_mode)

    
    def initThings(self):
        """
        Initializes the empty list object for the game to use.
        """
        
        # logging
        self.logger.info('initializing game list $things . . .')

        # create things as an empty list
        things = list([])

        # logging
        self.logger.debug('$things type = <%s>, length = <%s>',
            str(type(things)), str(len(things)))

        # return the newly created list
        return list(things)
   

    def createStuff(
        self,
        request,
        chance=100,
        fixed=False,
        quantity=1):

        for i in range(quantity):
            space = random.choice(board.spaces.values())
            
            self.createThing(space.y, space.x, request)


    #TODO: think I can rework this to something like:
    #       "if keyword argument is received, then
    #        try to make finalized thing.$keyword
    #        whatever the value of the $keyword is
    def createThing(
        self,
        y,
        x,
        request,
        check_bounds=True,
        keywords = None,
        #blocks=None,
        #char=None,
        #name=None,
        #actor_name=None,
        #actor_sex=None,
        #actor_species=None,
        fast=False
        ):

        if check_bounds:
            if not board.inBounds(y,x):
                self.logger.warn('attempted to create tile at illegal position')
                return

        if request == 'rat':
            thing = Rat()
    
        elif request == 'common squirrel':
            thing = CommonSquirrel()

        elif request == 'cottage boar':
            thing = CottageBoar()

        # if requesting a deprived
        elif request == 'deprived':
            pass

        elif request == 'garden snake':
            thing = GardenSnake()

        elif request == 'kris':
            thing = Kris()

        elif request == 'shade':
            pass

        elif request == 'bush':
            thing = Bush()

            game.logger.debug('TEST9: bush sidechar is <%s>', 
                str(thing.side_char))

        elif request == 'grass':
            thing = Grass()

        elif request == 'lava':
            thing = Lava()

        elif request == 'man hunter':
            thing = ManHunter()

        elif request == 'sand':
            thing = Sand()

        elif request == 'stone':
            thing = Stone()

        elif request == 'water':
            thing = Water()

        elif request == 'woodland rat':
            thing = WoodRat()

        thing.y = y
        thing.x = x

        #if thing.actor is not None:
        if isinstance(thing, Actor):

            self.logger.debug('created thing <%s>, a <%s> <%s>'
                + ' named <%s> at <%s>, <%s>',
                str(thing.name), str(thing.sex),
                str(request), str(thing.name), 
                str(thing.y), str(thing.x))

            #thing.actor.restoreAll()
            thing.restoreAll()

        if keywords:
            if not isinstance(keywords, dict):
                game.logger.warning('ignoring non-dict keywords argument')
            else:
                for key, value in keywords.items():
                    try:
                        setattr(thing, key, value)
                    except AttributeError:
                        game.logger.warning(
                            'unable to set <%s> value on <%s>_<%s>',
                            str(key), str(thing.name), str(thing.serial))

        game.logger.debug('y = <%s>', str(thing.y))
        game.logger.debug('x = <%s>', str(thing.x))
        game.logger.debug('blocks = <%s>', str(thing.blocks))
        game.logger.debug('char = <%s>', str(thing.char))
        game.logger.debug('color = <%s>', str(thing.color))
        game.logger.debug('name = <%s>', str(thing.name))
        if isinstance(thing, Actor):
            game.logger.debug('sex = <%s>', str(thing.sex))
            game.logger.debug('hp = <%s>', str(thing.hp))
            game.logger.debug('gold = <%s>', str(thing.gold))
            game.logger.debug('inventory = <%s>', str(thing.inventory))
            #game.logger.debug('player = <%s>', str(thing.player))
            game.logger.debug('corpse = <%s>', str(thing.corpse))

        coordinate = str(str(thing.y) + '_' + str(thing.x))

        # make sure only 1 terrain is on space at atime
        if isinstance(thing, Terrain):
            for terrain in board.spaces[coordinate].contents:
                if isinstance(terrain, Terrain):
                    board.spaces[coordinate].contents.remove(terrain)
                
        game.logger.debug('coordinate = <%s>, coordinate type = <%s>',
            str(coordinate), str(type(coordinate)))
        
        board.spaces[coordinate].contents.append(thing)

        game.logger.debug('space name = <%s>, space location = <%s>',
            str(board.spaces[coordinate].name), 
            str(board.spaces[coordinate].location))

        self.things.append(thing)

        if fast:
            board.quickDraw(thing)
        else:
            board.drawSpace(thing.y, thing.x)
        

    def initBoard(self):
        global board

        self.logger.debug('initializing board . . .')

        board = Board()

        self.logger.debug('first_y, last_y: <%s>, <%s> \n' +
            'first_x, last_x: <%s>, <%s>',
            str(board.first_y), str(board.last_y), 
            str(board.first_x), str(board.last_x))

        
    def initCurses(self, stdscr):
        """
        - initializes the curses module objects
        - should only be called once at startup
        - gives the stdscr object to game as stdscr
        - creates a base window #REMOVED FOR NOW/TESTING
        - creates a map pad
        """

        # log what is happening
        self.logger.info("initializing curses objects")

        # give the stdscr to the game object
        self.stdscr = stdscr
        # log what is happening
        self.logger.debug("stdscr(<%s>) given to game instance(<%s>)",
            str(stdscr), str(self))

        curses.start_color()

        #curses.init_pair(1, 3, 0)       # yellow on black
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        # blue on black
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        # green on black
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        # black on white
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)
        # red on black
        curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
        # black on green
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_GREEN)
        # black on yellow
        curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        # black on blue
        curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_BLUE)
        # black on red
        curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_RED)
        # magenta on black
        curses.init_pair(10, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        # red on white
        curses.init_pair(11, curses.COLOR_RED, curses.COLOR_WHITE)
        # cyan on black
        curses.init_pair(12, curses.COLOR_CYAN, curses.COLOR_BLACK)

        # hide the cursor
        curses.curs_set(0)

        #self.curses = curses
        return curses

        
    def initLogger( self,
                    logfile     =   '.adventure.log.txt',
                    #loglevel    =   logging.DEBUG
                    #loglevel    =   logging.INFO
                    loglevel    =   logging.WARNING
                    ):
        """
        initializes the logger object

        takes 3 parameters:

            - self
            - logfile:
                this is the path for the file that logger will log to
            - loglevel:
                this sets the default initial value for the logger program

        returns null; creates an object called logger and gives it to the
        game object.

        """

        # instantiate the logger object
        logger = logging.getLogger()

        # define a new handler and tell it where to log events
        hdlr = logging.FileHandler(logfile)

        # set the format for the hdlr object to use
        hdlr.setFormatter(logging.Formatter(
            #'%(asctime)s ' +        # time
            '%(levelname)s ' +      # level of message
            '%(lineno)s - ' +       # line number
            '%(funcName)s - ' +     # function name
            '%(message)s'           # the message itself
            ))

        # add the handler to the logger object
        logger.addHandler(hdlr)

        # tell the logger which level to run on
        logger.setLevel(loglevel)

        logger.info("- - - - - - - - - - " + "<" + str(__file__) + "> has been executed" + " - - - - - - - - - -")

        # return the logger object
        return logger

    def initOther(self):
        """
        initializes miscellaneous values that the game needs to start

        """
        self.logger.info("initializing 'other' game objects")

        # initialize game things list
        game.things = []
        # log it
        self.logger.debug("game.things initialized")

        # initialize the loop counter at 0
        self.loop_count = int(0)
        self.logger.debug("initializing game.loop_count to <%s>",
            str(self.loop_count))

        # tell the game that it is being played
        self.playing = True
        # log it
        self.logger.debug("game.playing initialized to <%s>",
            str(self.playing))

    def initHero(self, y, x):
        """
        initializes the player object
        """

        global hero

        #TODO: add check to make sure player doesn't already exist

        #player_component = Player()

        #hero = Human()
            #y = y,
            #x = x)
            #char = '@',
            #color = self.colors['white'],
            #species = species_component,
            #player = player_component)
        #hero.y = y
        #hero.x = x
        #hero.char = '@'
        #hero.color = self.colors['white']
        #hero.player.view_radius = 12

        #hero.player = player_component
        #hero.player.owner = hero
        #hero.player.view_radius = 12
        hero = Hero()
        hero.y = y
        hero.x = x

        #hero.side_char = '*'

        #hero.actor.restoreAll()
        hero.restoreAll()

        self.things.append(hero)
        location = str(str(y) + '_' + str(x))
        self.logger.debug('hero spawn location: <%s>',
            str(location))
        board.spaces[location].contents.append(hero)

        self.logger.critical('hero y,x is <%s>, <%s>', 
            str(hero.y), str(hero.x))

        board.drawSpace(
            hero.y,
            hero.x)


    def createMixedThings(self,
        specifications,
        beg_y = None,
        max_y = None,
        beg_x = None,
        max_x = None,
        chance = 100,
        fast = False):

        #TODO: can't these just be defaulted?
        if beg_y is None:
            beg_y = board.first_y
        if max_y is None:
            max_y = board.last_y
        if beg_x is None:
            beg_x = board.first_x
        if max_x is None:
            max_x = board.last_x

        for y in range(beg_y, max_y + 1):
            for x in range(beg_x, max_x + 1):
                if not x & 1:
                    continue    # skip this tile
                self.logger.debug('creating different things at <%s>,<%s>',
                    str(y), str(x))

                diceroll = random.randint(chance, 100)
                self.logger.debug('diceroll = <%s>',
                    str(diceroll))
                if chance >= diceroll:
                    chance_total = 0
                    chances = {}
                    for specification in specifications:
                        chances[specification] = (chance_total, 
                            specification[1] + chance_total)
                        chance_total += specification[1]
                       
                    diceroll = random.randint(0, chance_total)
                    for specification in specifications:
                        if chances[specification][0] <= diceroll <= chances[specification][1]:
                            self.createThing(y, x, specification[0], fast=fast) 
                        
    
    def createManyThings(self,
        specification,
        chances=999,
        fast=False):
        self.logger.info('doing createManyThings: <%s>', str(specification))

        spaces = board.spaces.values()

        try: 
            chance = chances[0]
        except TypeError:
            chance = chances
            
        if specification == 'connected bushes':
            for y in range(board.first_y, board.last_y + 1):
                self.logger.debug('working on row <%s>', str(y))
                for x in range(board.first_x, board.last_x + 1):

                    if not x & 1:
                        continue

                    diceroll = random.randint(1, chance)
                    self.logger.debug('diceroll = <%s>',
                        str(diceroll))
                    if diceroll <= 75:
                        self.logger.debug('generating connected bushes at' + 
                            '<%s>,<%s>', str(y), str(x))
                        self.createThing(y, x, 'bush', fast=fast)   # create a bush
                        try:
                            chance = chances[1]
                        except TypeError:
                            pass
                        diceroll = random.randint(1, chance)        # roll dice
                        while diceroll <= 48:
                            if diceroll <= 6:
                                y = y-1     # up
                                x = x-2     # left
                            elif 7 <= diceroll <= 12:
                                y = y-1     # up
                            elif 13 <= diceroll <= 18:
                                y = y-1     # up
                                x = x+2     # right
                            elif 19 <= diceroll <= 24:
                                x = x-2     # left
                            elif 25 <= diceroll <= 30:
                                x = x+2     # right
                            elif 31 <= diceroll <= 36:
                                y = y+1     # down
                                x = x-2     # left
                            elif 37 <= diceroll <= 42:                  
                                y = y+1     # down
                            elif 43 <= diceroll <= 48:
                                y = y+1  # down
                                x = x+2  # right
                            self.createThing(y, x, 'bush', fast=fast)
                            diceroll = random.randint(1, chance)
        
        elif specification == 'scattered rats':
            for space in spaces:
                #TODO: check for obstacles and return if found
                diceroll = random.randint(1, chance)
                if diceroll < 10:
                    #self.createThing(space.owner.y, space.owner.x, 'rat', fast=fast)
                    self.createThing(space.y, space.x, 'woodland rat', fast=fast)
        

        elif specification == 'scattered water':
            for space in spaces:
                diceroll = random.randint(1, chance)
                if diceroll < 50:
                    #self.createThing(space.owner.y, space.owner.x, 'water', fast=fast)
                    self.createThing(space.y, space.x, 'water', fast=fast)

        elif specification == 'water border':
            for space in spaces:
                #if ((board.first_y <= space.owner.y <= board.first_y + 5 or
                if ((board.first_y <= space.y <= board.first_y + 5 or
                    #board.last_y - 5 <= space.owner.y <= board.last_y) or
                    board.last_y - 5 <= space.y <= board.last_y) or
                    #(board.first_x <= space.owner.x <= board.first_x + 5 or
                    (board.first_x <= space.x <= board.first_x + 5 or
                    #board.last_x - 5 <= space.owner.x <= board.last_x)):
                    board.last_x - 5 <= space.x <= board.last_x)):
                    
                        #self.createThing(space.owner.y, space.owner.x, 'water', fast=fast)
                        self.createThing(space.y, space.x, 'water', fast=fast)

        elif specification == 'water diamonds':
            for y in range(board.first_y, board.last_y + 1):
                self.logger.debug('creating water diamond on row <%s>', str(y))
                for x in range(board.first_x, board.last_x + 1):
                    if not x & 1:
                        continue
                    diceroll = random.randint(1, chance)
                    if diceroll < 2:
                        self.createThing(y-2, x, 'water', fast=fast)
                        self.createThing(y-1, x-2, 'water', fast=fast)
                        self.createThing(y-1, x, 'water', fast=fast)
                        self.createThing(y-1, x+2, 'water', fast=fast)
                        self.createThing(y, x-4, 'water', fast=fast)
                        self.createThing(y, x-2, 'water', fast=fast)
                        self.createThing(y, x, 'water', fast=fast)
                        self.createThing(y, x+2, 'water', fast=fast)
                        self.createThing(y, x+4, 'water', fast=fast)
                        self.createThing(y+1, x-2, 'water', fast=fast)
                        self.createThing(y+1, x, 'water', fast=fast)
                        self.createThing(y+1, x+2, 'water', fast=fast)
                        self.createThing(y+2, x, 'water', fast=fast)


    def incrementLoop(self,
        incrementer=1):
        #TODO: improve this docstring
        """ increment the loop count """

        self.logger.debug('incrementing the loop count . . .')
        self.logger.debug('old $loop_count = <%s>', str(self.loop_count))
        self.logger.debug('$incrementer = <%s>', str(incrementer))

        self.loop_count += 1

        self.logger.info('now on loop #<%s>', str(self.loop_count))

                    
    def loadMap(self, fast=False):
        game.logger.info('loading map . . .')
        game.logger.debug('map screen is <%s>',
            str(board.canvas))
        
        #world_size = 100
        #world_square = True

        board.first_y = 0
        board.last_y = 100
        board.first_x = 0
        board.last_x = 200

        board.camera_center_y = int((board.last_y - board.first_y) / 2)
        board.camera_center_x = int((board.last_x - board.first_x) / 2)
        if not board.camera_center_x & 1:
            board.camera_center_x -= 1

        #world_x = world_size
        #if world_square:
        #    world_y = int(world_size / 2)
        #else:
        #    world_y = int(world_size)
        #self.logger.info(
        #    'making world - size: <%s>, square: <%s>, y: <%s>, x: <%s>',
        #    str(world_size), str(world_square), str(world_y), str(world_x))

        #board.canvas.resize(world_y * 3, world_x * 6)
        board.canvas.resize(board.last_y * 8, board.last_x * 14)
    
        game.logger.debug('TEST3: first_y is <%s>', str(board.first_y))

        for y in range(board.first_y, board.last_y + 1):
            self.logger.info('creating spaces on row <%s>', str(y))
            for x in range(board.first_x, board.last_x + 1):
                if not x & 1:   # check if even using bitwise
                    continue
                #space_component = Space()
                #thing = Thing(
                #    y,
                #    x,
                #    space=space_component)
                #self.logger.debug('created space with location string <%s>',
                #    str(thing.space.location))
                thing = Space()
                    #y,
                    #x)
                thing.y = y
                thing.x = x
                #board.spaces[str(thing.space.location)] = thing.space
                board.spaces[str(thing.location)] = thing

                game.logger.debug('TEST4: created space at <%s>,<%s>',
                    str(y), str(x))

        self.logger.debug('spaces length = <%s>',
            str(len(board.spaces)))

        for space in board.spaces.values():
            self.logger.debug('space location = <%s>',
                str(space.location))
   
        self.logger.debug('canvas beg_y: <%s>, beg_x: <%s>, max_y: <%s>,' + 
            'max_x: <%s>', 
            str(board.canvas.getbegyx()[0]), str(board.canvas.getbegyx()[1]), 
            str(board.canvas.getmaxyx()[0]), str(board.canvas.getmaxyx()[1]))

        self.initHero( 
            board.camera_center_y,
            board.camera_center_x)

        self.createMixedThings((('sand', 40), ('grass', 1000), ('stone', 10)), fast=True)
        self.createManyThings('scattered water', chances=1500, fast=True)
        
        self.createManyThings('connected bushes', chances=[8999, 750], fast=True)
        self.createManyThings('water diamonds', chances=1700, fast=True)
        self.createManyThings('water border', fast=True)
        self.createThing(24, 27, 'lava', fast=True)
        self.createManyThings('scattered rats', fast=True)
        #self.createThing(11, 11, 'shade', fast=True)
        self.createStuff('common squirrel', quantity=20)
        #self.createStuff('man hunter', quantity=40)
        self.createStuff('garden snake', quantity=20)
        self.createStuff('cottage boar', quantity=10)
        self.createStuff('kris', quantity=330)


    def togglePlaying(self,
        toggle=None):

        self.logger.debug('toggling $playing state . . .')
        self.logger.debug('$toggle = <%s>', str(toggle))        

        if toggle is None:
            self.playing = not self.playing

        elif type(toggle) is bool:
            self.playing = toggle

        else:
            self.logger.error('invalid $toggle option <%s>', str(toggle))

        self.logger.debug('game $playing = <%s>', str(self.playing))


    def splitString(self, string, length):
        #return (string[0+i:length+i] for i in range(0, len(string), length))
        #lines = textwrap.wrap(string, length, break_long_words=False)
        #return lines

        words = iter(string.split())
        lines, current = [], next(words)
        for word in words:
            if len(current) + 1 + len(word) > length:
                lines.append(current)
                current = word
            else:
                current += " " + word
        lines.append(current)
        return lines


    def writeMessage(self,
        message,
        highlights={},
        attribute=curses.A_NORMAL):
        #highlights=None):
        #color=None,
        #attr=curses.A_NORMAL):

        #if color is None:
        #    color = self.colors['white']
       

        printable_length = 28
        delimit = (str('     ') + ('-' * (printable_length - 10)) + ('     '))

        start_x = ((self.gamelog.dimensions['beg_x'] - 
            self.gamelog.dimensions['beg_x']) + 1)

        lines = list(self.splitString(message, printable_length))
        #lines.append(str(delimit))

        for line in lines:

            #words = line.split

            self.gamelog.position += 1

            if self.gamelog.position == self.gamelog.frame.getmaxyx()[0] - 44:
                self.gamelog.position = (
                    (self.gamelog.dimensions['beg_y'] 
                    - self.gamelog.dimensions['beg_y']) 
                    + 0
                    + self.gamelog.dimensions['max_y'])

            self.setGameLogBorders()

            #TODO: try this
            #words = next(line.split())

            x = start_x

            #words = line.split()
            words = iter(line.split())

            #current = next(words)
            #current = ''
            #current = words[0]

            for index, word in enumerate(words):

                game.logger.critical('TEST26, word is <%s>', str(word))

                #word = str(word + ' ')

                modifier = None
                

                for keyword, attr in highlights.items():
                    game.logger.critical(
                        'TEST30: keyword, attr: <%s>, <%s>',
                        str(keyword), str(attr))
                    if keyword in word:
                        game.logger.critical('TEST30!')

                        #self.gamelog.frame.addstr(
                        #    (self.gamelog.position
                        #    + self.gamelog.dimensions['max_y']
                        #    - self.gamelog.dimensions['beg_y']
                        #    - 1),
                        #    x,
                        #    str(word),
                        #    attr)

                        modifier = attr
                        game.logger.critical('TEST30?')
                        #x += len(word)

                        break

                #if word == 'player':
                if 'player' in word:

                    game.logger.critical('TEST25')

                    #current += ' ' + word

                    #self.gamelog.frame.addstr(
                        #(self.gamelog.position
                        #+ self.gamelog.dimensions['max_y']
                        #- self.gamelog.dimensions['beg_y']
                        #- 1),
                        #x,
                        #str(current),
                        #str(word),
                        #game.colors['red'])
                    #modifier = game.colors['red']
                    #modifier = game.colors['black_white']
                    modifier = game.colors['cyan']

                    #x += len(current)
                    #x += len(word)
                    #current = ''


                if modifier == None:
                    #for keyword in highlights:
                    #num_highlights = len(highlights)
                        #try:
                        #    game.logger.critical(
                        #        'TEST35: cur_word is <%s>, next_word is <%s>',
                        #        str(keyword), str(list(words)[index + 1]))
                        #except IndexError:
                        #    game.logger.critical('TEST35-1')
                            #break
                    #game.logger.critical('TEST35-2')
                    modifier = curses.A_NORMAL 

                #if modifier == None:
                #    modifier = curses.A_NORMAL

                if index > 0:
                    if modifier == prev_modifier:
                        space_attr = modifier
                    else:
                        space_attr = curses.A_NORMAL

                    self.gamelog.frame.addstr(
                        (self.gamelog.position
                            + self.gamelog.dimensions['max_y']
                            - self.gamelog.dimensions['beg_y']
                            - 1),
                        x,
                        str(' '),
                        space_attr |
                        attribute)

                    x += 1


                game.logger.critical('TEST35*')
                self.gamelog.frame.addstr(
                    (self.gamelog.position 
                        + self.gamelog.dimensions['max_y']  
                        - self.gamelog.dimensions['beg_y'] 
                        - 1),
                    x,
                    #str(message))
                #    str(current))
                    str(word),
                    modifier |
                    attribute)
                    #color |
                    #attr)
                
                x += len(word)

                prev_modifier = modifier
                
                                #x += len(word)

        self.gamelog.position += 1

        x = start_x

        if self.gamelog.position == self.gamelog.frame.getmaxyx()[0] - 44:
            self.gamelog.position = (
                (self.gamelog.dimensions['beg_y'] 
                - self.gamelog.dimensions['beg_y']) 
                + 0
                + self.gamelog.dimensions['max_y'])

        self.setGameLogBorders()



        self.gamelog.frame.addstr(
            (self.gamelog.position
                + self.gamelog.dimensions['max_y']
                - self.gamelog.dimensions['beg_y']
                - 1),
            x,
            str(delimit)) 



    def doMenu(self,
            kind):
        window = self.menu.content

        if kind == 'inventory':

            items = hero.inventory
            y = 2
            x = 1

            for item in items:

                game.logger.critical('item is <%s>_<%s>',
                    str(item.name), str(item.serial))

                window.addstr(y, x, item.name)

                y += 2 
    


    def initMenu(
        self):

        dimensions = {
            #'beg_y' :   3,
            'beg_y' :   3,
            #'beg_x' :   91,
            'beg_x' :   91,
            #'beg_x' : 121,
            'max_y' :   36,
            #'max_x' :   120,
            'max_x' :   121,
            #'max_x' :   149
            }

        #frame = curses.newpad(
        #    20000,
        #    #36) 
        #    30)

        content = curses.newwin(
            dimensions['max_y'] - dimensions['beg_y'],
            dimensions['max_x'] - dimensions['beg_x'],
            dimensions['beg_y'],
            dimensions['beg_x'])

        #gamelog = Window(
        menu = Window(
            content = content,
            #frame = frame,
            frame = None,
            stack = None,
            dimensions = dimensions)

        menu.content.border()
        menu.content.keypad(1)

        #gamelog.position = (dimensions['beg_y'] - dimensions['beg_y'])

        #self.gamelog = gamelog
        self.menu = menu

        #self.setGameLogBorders()




    

    def initGameLog(
        self):

        dimensions = {
            'beg_y' :   3,
            'beg_x' :   91,
            'max_y' :   35,
            'max_x' :   120,
            }

        frame = curses.newpad(
            20000,
            #36) 
            30)

        gamelog = Window(
            content = None,
            frame = frame,
            stack = None,
            dimensions = dimensions)

        gamelog.position = (dimensions['beg_y'] - dimensions['beg_y'])

        self.gamelog = gamelog

        self.setGameLogBorders()


    #def getContents(
    def getSpace(self,
        y,
        x,
        item='space'):

        coordinate = str(str(y) + '_' + str(x))

        game.logger.debug('coordinate y,x = <%s>,<%s>',
            str(y), str(x))

        game.logger.debug('coordinate (<%s>,<%s>) = <%s>', 
            str(y), str(x), str(coordinate))

        #return list(board.spaces[coordinate].contents)
        try:
            return board.spaces[coordinate]
        except KeyError:
            return False


    def initStatDisplay(self):

        statdisplay = StatDisplay(
            nlines=7,
            ncols=65,
            begin_y=1,
            begin_x=2
            )

        game.statdisplay = statdisplay 


    def gameOver(self):
        self.playing = False


    def setGameLogBorders(self):
        start_y = (self.gamelog.dimensions['beg_y'] - 
            self.gamelog.dimensions['beg_y'])
        start_x = (self.gamelog.dimensions['beg_x'] - 
            self.gamelog.dimensions['beg_x'])
        end_y = (self.gamelog.dimensions['max_y'] - 
            self.gamelog.dimensions['beg_y'])
        end_x = (self.gamelog.dimensions['max_x'] - 
            self.gamelog.dimensions['beg_x'])

        for y in range(
            start_y, end_y + 1 + self.gamelog.position):
            for x in range(
                start_x, end_x + 1):
                    game.logger.debug('creating gamelog border at <%s>, <%s>',
                        str(y), str(x))
                    if y == start_y + self.gamelog.position:
                        if x == start_x:
                            character = curses.ACS_ULCORNER
                        elif x == end_x:
                            game.logger.debug('upper right corner detected ' +
                                'at <%s>, <%s>', str(y), str(x))
                            character = curses.ACS_URCORNER
                        else:
                            character = curses.ACS_HLINE
                    elif y == end_y + self.gamelog.position:
                        game.logger.debug('working on bottom row (<%s>, <%s>',
                            str(y), str(x))
                        if x == start_x:
                            character = curses.ACS_LLCORNER
                        elif x == end_x:
                            character = curses.ACS_LRCORNER
                        else:
                            character = curses.ACS_HLINE
                    elif x == start_x or x == end_x:
                        character = curses.ACS_VLINE

                    elif y == end_y - 1 + self.gamelog.position:
                        character = ' '
   
                    else:
                        continue
                    if character == '@':
                        game.logger.debug('character = <%s>', str(character))
                    self.gamelog.frame.addch(y, x, character)



class Window:
    def __init__(
        self,
        content=None,
        frame=None,
        stack=None,
        dimensions=None):

        self.content = content
        self.frame = frame
        self.stack = stack
        self.dimensions = dimensions


class StatDisplay:
    def __init__(
        self,
        nlines=None,
        ncols=None,
        begin_y=None,
        begin_x=None):

        self.nlines = nlines
        if self.nlines is None:
            self.nlines = 3

        self.ncols = ncols
        if self.ncols is None:
            self.ncols = 6

        self.begin_y = begin_y
        if self.begin_y is None:
            self.begin_y = 1

        self.begin_x = begin_x
        if self.begin_x is None:
            self.begin_x = 2

        self.canvas = curses.newwin(
            self.nlines,        # nlines
            self.ncols,         # ncols
            self.begin_y,       # begin y
            self.begin_x)       # begin x

        # always start the canvas with a border
        self.canvas.border()


class Board:
    def __init__(
        self,
        canvas=None,
        dimensions=None,
        #tiles,
        spaces=None,     # TODO: can this be defaulted?
        camera_center_y=None,
        camera_center_x=None,
        camera_threshold=5,
        error_buffer=2):

        #self.camera_zoom = 0
        self.camera_zoom = 0

        self.first_y = 1
        self.last_y = 2
        self.first_x = 1
        self.last_x = 2

        if canvas is None:
            size_y = 25
            size_x = 50
            try:
                self.canvas = game.curses.newpad(
                    size_y + error_buffer, 
                    size_x + error_buffer)
            except:
                self.canvas = curses.newpad(
                    size_y + error_buffer, 
                    size_x + error_buffer)
        elif canvas is not None and error_buffer is not None:
            canvas.resize(
                canvas.getmaxyx()[0] + error_buffer,
                canvas.getmaxyx()[1] + error_buffer)
            
        self.canvas.keypad(1)        

        if dimensions is None:
            self.dimensions = {
                'beg_y' : 8,
                'beg_x' : 0,
                'max_y' : 35,
                'max_x' : 90
                }

        if spaces is None:
            self.spaces = {}
            
        #if camera_center_y is None:
            #self.camera_center_y = int(size_y / 2)
            #self.camera_center_y = 6
            #self.camera_center_y = int((self.last_y - self.first_y) / 2)

        #if camera_center_x is None:
            #camera_center_x = int(size_x / 2)
            #self.camera_center_x = int((self.last_x - self.first_x) / 2)
            #TODO this should only be necessary in terminal mode
            #if not self.camera_center_x & 1:
            #    self.camera_center_x -= 1
            #self.camera_center_x = camera_center_x
            #self.camera_center_x = 9

        # TODO: rename this - camera_follow?
        self.camera_threshold = camera_threshold

    #@property
    #def first_y(self):
    #    return self.canvas.getbegyx()[0] + 2

    #@property
    #def last_y(self):
        # ignore the last 'buffer' row
    #    return self.canvas.getmaxyx()[0] - 2

    #@property
    #def first_x(self):
    #    return self.canvas.getbegyx()[1] + 2

    #@property
    #def last_x(self):
        # have to leave last column unused, due to bug
        # with curses cursor wrapping, ref:
        # http://stackoverflow.com/questions/36387625/
    #    return self.canvas.getmaxyx()[1] - 2
    
    @property
    def camera_corner(self):
        """ calculates actual camera origin coordinate from camera center """
        camera_y = self.camera_center_y
        camera_x = self.camera_center_x
        if self.camera_zoom == 2:
            camera_y = int((self.camera_center_y * 5) + 1)
            camera_x = int((self.camera_center_x * 5) + (self.camera_center_x / 2))
            #camera_x = int((self.camera_center_x * 7) + (self.camera_center_x / 2))
            #camera_x = int((self.camera_center_x * 6) + (self.camera_center_x / 2))
            #camera_x = int(self.camera_center_x * 6)
        elif self.camera_zoom == 1:
            #camera_y = int(((self.camera_center_y + 1) * 3) - 1)
            camera_y = int((self.camera_center_y * 3) + 1)
            #camera_y = int(self.camera_center_y * 3)
            #camera_x = int(((self.camera_center_x + 1) * 3) - 1)
            camera_x = int((self.camera_center_x * 3) + (self.camera_center_x / 2))
            #camera_x = int((self.camera_center_x * 3) + 1)
        y = int(camera_y 
            - (self.dimensions['max_y'] - self.dimensions['beg_y']) / 2)

        x = int(camera_x
            - (self.dimensions['max_x'] - self.dimensions['beg_x']) / 2)

        return y,x
    
    def checkCamera(self, focus=None):
        if focus is None:
            try: focus = hero
            except: #TODO capture actual error
                return
        if abs(self.camera_center_y - focus.y) >= self.camera_threshold or \
            abs(self.camera_center_x - focus.x) >= self.camera_threshold:
            self.camera_center_y = focus.y
            self.camera_center_x = focus.x


    def inBounds(self,
        y,
        x,
        cheap=True):
        """ used to check if tile is in bounds """

        if cheap:
            if (self.first_y <= y <= self.last_y
                and self.first_x <= x <= self.last_x):
                return True
            else:
                return False

        else:
            if (board.canvas.getbegyx()[0] + 1 <= tile.y 
                <= board.canvas.getmaxyx()[0] - 1 and
                board.canvas.getbegyx()[1] + 1 <= tile.x
                <= board.canvas.getmaxyx()[1] - 1):
                return True
            else:
                return False

    
    def moveCamera(
        self,
        y_diff,
        x_diff,
        focus=None):

        camera_threshold = self.camera_threshold
        x_diff = x_diff * 2

        #if self.camera_zoom is 5:
        if 1 <= self.camera_zoom <= 2:
            camera_threshold = int(camera_threshold / 2)
    
        if focus is None:
            try: focus = hero
            except: return
        if abs(self.camera_center_y - focus.y) >= camera_threshold:
            self.camera_center_y += y_diff
        if abs(self.camera_center_x - focus.x) >= camera_threshold * 2:
            self.camera_center_x += x_diff

    
    def querySpace(
        self,
        y,
        x):
        """ check what things are in a given space """

        game.logger.debug('querying objects on space <%s>, <%s>',
            str(y), str(x))

        things = []
        location = str(str(y) + '_' + str(x))
        #try:
        for thing in board.spaces[location].contents:
            things.append(thing)
        #except KeyError:
        #    things = False    
        return things


    #TODO: consolidate into drawSpace()
    def quickDraw(
            self,
            target):
            
        color = target.color
        side_color = target.side_char_color

        
        if (abs(target.y - hero.y) > (hero.view_radius / 2) or
            abs(target.x - hero.x) > hero.view_radius):
                color = target.char_color_dark
                side_color = target.side_char_color_dark



        if self.camera_zoom == 2:
            y = int((target.y * 5) + 2)
            #x = int((target.x * 5) + (target.x / 2))
            #x = int((target.x * 7) + (target.x / 2))
            #x = int((target.x * 6) + (target.x / 2) + 1)
            x = int((target.x * 5) + (target.x / 2))
            #x = int(target.x * 6)
        
            #self.canvas.addch(
            #    y,
            #    x,
            #    target.char,
            #    (color |
            #    target.char_attr))

            #z2_u3l7_color = target.char_z2_u3l7_color
            #z2_u3l6_color = target.char_z2_u3l6_color
            #z2_u3l5_color = target.char_z2_u3l5_color
            #z2_u3l4_color = target.char_z2_u3l4_color
            #z2_u3l3_color = target.char_z2_u3l3_color
            #z2_u3l2_color = target.char_z2_u3l2_color
            #z2_u3l1_color = target.char_z2_u3l1_color
            #z2_u3_color = target.char_z2_u3_color
            #z2_u3r1_color = target.char_z2_u3r1_color
            #z2_u3r2_color = target.char_z2_u3r2_color
            #z2_u3r3_color = target.char_z2_u3r3_color
            #z2_u3r4_color = target.char_z2_u3r4_color
            #z2_u3r5_color = target.char_z2_u3r5_color
            #z2_u3r6_color = target.char_z2_u3r6_color
            #z2_u3r7_color = target.char_z2_u3r7_color
            z2_u2l7_color = target.char_z2_u2l7_color
            z2_u2l6_color = target.char_z2_u2l6_color
            z2_u2l5_color = target.char_z2_u2l5_color
            z2_u2l4_color = target.char_z2_u2l4_color
            z2_u2l3_color = target.char_z2_u2l3_color
            z2_u2l2_color = target.char_z2_u2l2_color
            z2_u2l1_color = target.char_z2_u2l1_color
            z2_u2_color = target.char_z2_u2_color
            z2_u2r1_color = target.char_z2_u2r1_color
            z2_u2r2_color = target.char_z2_u2r2_color
            z2_u2r3_color = target.char_z2_u2r3_color
            z2_u2r4_color = target.char_z2_u2r4_color
            z2_u2r5_color = target.char_z2_u2r5_color
            z2_u2r6_color = target.char_z2_u2r6_color
            z2_u2r7_color = target.char_z2_u2r7_color
            z2_u1l7_color = target.char_z2_u1l7_color
            z2_u1l6_color = target.char_z2_u1l6_color
            z2_u1l5_color = target.char_z2_u1l5_color
            z2_u1l4_color = target.char_z2_u1l4_color
            z2_u1l3_color = target.char_z2_u1l3_color
            z2_u1l2_color = target.char_z2_u1l2_color
            z2_u1l1_color = target.char_z2_u1l1_color
            z2_u1_color = target.char_z2_u1_color
            z2_u1r1_color = target.char_z2_u1r1_color
            z2_u1r2_color = target.char_z2_u1r2_color
            z2_u1r3_color = target.char_z2_u1r3_color
            z2_u1r4_color = target.char_z2_u1r4_color
            z2_u1r5_color = target.char_z2_u1r5_color
            z2_u1r6_color = target.char_z2_u1r6_color
            z2_u1r7_color = target.char_z2_u1r7_color
            z2_l7_color = target.char_z2_l7_color
            z2_l6_color = target.char_z2_l6_color
            z2_l5_color = target.char_z2_l5_color
            z2_l4_color = target.char_z2_l4_color
            z2_l3_color = target.char_z2_l3_color
            z2_l2_color = target.char_z2_l2_color
            z2_l1_color = target.char_z2_l1_color
            z2_center_color = target.char_z2_center_color
            z2_r1_color = target.char_z2_r1_color
            z2_r2_color = target.char_z2_r2_color
            z2_r3_color = target.char_z2_r3_color
            z2_r4_color = target.char_z2_r4_color
            z2_r5_color = target.char_z2_r5_color
            z2_r6_color = target.char_z2_r6_color
            z2_r7_color = target.char_z2_r7_color
            z2_d1l7_color = target.char_z2_d1l7_color
            z2_d1l6_color = target.char_z2_d1l6_color
            z2_d1l5_color = target.char_z2_d1l5_color
            z2_d1l4_color = target.char_z2_d1l4_color
            z2_d1l3_color = target.char_z2_d1l3_color
            z2_d1l2_color = target.char_z2_d1l2_color
            z2_d1l1_color = target.char_z2_d1l1_color
            z2_d1_color = target.char_z2_d1_color
            z2_d1r1_color = target.char_z2_d1r1_color
            z2_d1r2_color = target.char_z2_d1r2_color
            z2_d1r3_color = target.char_z2_d1r3_color
            z2_d1r4_color = target.char_z2_d1r4_color
            z2_d1r5_color = target.char_z2_d1r5_color
            z2_d1r6_color = target.char_z2_d1r6_color
            z2_d1r7_color = target.char_z2_d1r7_color
            z2_d2l7_color = target.char_z2_d2l7_color
            z2_d2l6_color = target.char_z2_d2l6_color
            z2_d2l5_color = target.char_z2_d2l5_color
            z2_d2l4_color = target.char_z2_d2l4_color
            z2_d2l3_color = target.char_z2_d2l3_color
            z2_d2l2_color = target.char_z2_d2l2_color
            z2_d2l1_color = target.char_z2_d2l1_color
            z2_d2_color = target.char_z2_d2_color
            z2_d2r1_color = target.char_z2_d2r1_color
            z2_d2r2_color = target.char_z2_d2r2_color
            z2_d2r3_color = target.char_z2_d2r3_color
            z2_d2r4_color = target.char_z2_d2r4_color
            z2_d2r5_color = target.char_z2_d2r5_color
            z2_d2r6_color = target.char_z2_d2r6_color
            z2_d2r7_color = target.char_z2_d2r7_color



            #z2_u3l7_attr = target.char_z2_u2l7_attr
            #z2_u3l6_attr = target.char_z2_u2l6_attr
            #z2_u3l5_attr = target.char_z2_u2l5_attr
            #z2_u3l4_attr = target.char_z2_u2l4_attr
            #z2_u3l3_attr = target.char_z2_u2l3_attr
            #z2_u3l2_attr = target.char_z2_u2l2_attr
            #z2_u3l1_attr = target.char_z2_u2l1_attr
            #z2_u3_attr = target.char_z2_u2_attr
            #z2_u3r1_attr = target.char_z2_u2r1_attr
            #z2_u3r2_attr = target.char_z2_u2r2_attr
            #z2_u3r3_attr = target.char_z2_u2r3_attr
            #z2_u3r4_attr = target.char_z2_u2r4_attr
            #z2_u3r5_attr = target.char_z2_u2r5_attr
            #z2_u3r6_attr = target.char_z2_u2r6_attr
            #z2_u3r7_attr = target.char_z2_u2r7_attr
            z2_u2l7_attr = target.char_z2_u2l7_attr
            z2_u2l6_attr = target.char_z2_u2l6_attr
            z2_u2l5_attr = target.char_z2_u2l5_attr
            z2_u2l4_attr = target.char_z2_u2l4_attr
            z2_u2l3_attr = target.char_z2_u2l3_attr
            z2_u2l2_attr = target.char_z2_u2l2_attr
            z2_u2l1_attr = target.char_z2_u2l1_attr
            z2_u2_attr = target.char_z2_u2_attr
            z2_u2r1_attr = target.char_z2_u2r1_attr
            z2_u2r2_attr = target.char_z2_u2r2_attr
            z2_u2r3_attr = target.char_z2_u2r3_attr
            z2_u2r4_attr = target.char_z2_u2r4_attr
            z2_u2r5_attr = target.char_z2_u2r5_attr
            z2_u2r6_attr = target.char_z2_u2r6_attr
            z2_u2r7_attr = target.char_z2_u2r7_attr
            z2_u1l7_attr = target.char_z2_u1l7_attr
            z2_u1l6_attr = target.char_z2_u1l6_attr
            z2_u1l5_attr = target.char_z2_u1l5_attr
            z2_u1l4_attr = target.char_z2_u1l4_attr
            z2_u1l3_attr = target.char_z2_u1l3_attr
            z2_u1l2_attr = target.char_z2_u1l2_attr
            z2_u1l1_attr = target.char_z2_u1l1_attr
            z2_u1_attr = target.char_z2_u1_attr
            z2_u1r1_attr = target.char_z2_u1r1_attr
            z2_u1r2_attr = target.char_z2_u1r2_attr
            z2_u1r3_attr = target.char_z2_u1r3_attr
            z2_u1r4_attr = target.char_z2_u1r4_attr
            z2_u1r5_attr = target.char_z2_u1r5_attr
            z2_u1r6_attr = target.char_z2_u1r6_attr
            z2_u1r7_attr = target.char_z2_u1r7_attr
            z2_l7_attr = target.char_z2_l7_attr
            z2_l6_attr = target.char_z2_l6_attr
            z2_l5_attr = target.char_z2_l5_attr
            z2_l4_attr = target.char_z2_l4_attr
            z2_l3_attr = target.char_z2_l3_attr
            z2_l2_attr = target.char_z2_l2_attr
            z2_l1_attr = target.char_z2_l1_attr
            z2_center_attr = target.char_z2_center_attr
            z2_r1_attr = target.char_z2_r1_attr
            z2_r2_attr = target.char_z2_r2_attr
            z2_r3_attr = target.char_z2_r3_attr
            z2_r4_attr = target.char_z2_r4_attr
            z2_r5_attr = target.char_z2_r5_attr
            z2_r6_attr = target.char_z2_r6_attr
            z2_r7_attr = target.char_z2_r7_attr
            z2_d1l7_attr = target.char_z2_d1l7_attr
            z2_d1l6_attr = target.char_z2_d1l6_attr
            z2_d1l5_attr = target.char_z2_d1l5_attr
            z2_d1l4_attr = target.char_z2_d1l4_attr
            z2_d1l3_attr = target.char_z2_d1l3_attr
            z2_d1l2_attr = target.char_z2_d1l2_attr
            z2_d1l1_attr = target.char_z2_d1l1_attr
            z2_d1_attr = target.char_z2_d1_attr
            z2_d1r1_attr = target.char_z2_d1r1_attr
            z2_d1r2_attr = target.char_z2_d1r2_attr
            z2_d1r3_attr = target.char_z2_d1r3_attr
            z2_d1r4_attr = target.char_z2_d1r4_attr
            z2_d1r5_attr = target.char_z2_d1r5_attr
            z2_d1r6_attr = target.char_z2_d1r6_attr
            z2_d1r7_attr = target.char_z2_d1r7_attr
            z2_d2l7_attr = target.char_z2_d2l7_attr 
            z2_d2l6_attr = target.char_z2_d2l6_attr 
            z2_d2l5_attr = target.char_z2_d2l5_attr 
            z2_d2l4_attr = target.char_z2_d2l4_attr 
            z2_d2l3_attr = target.char_z2_d2l3_attr 
            z2_d2l2_attr = target.char_z2_d2l2_attr 
            z2_d2l1_attr = target.char_z2_d2l1_attr 
            z2_d2_attr = target.char_z2_d2_attr 
            z2_d2r1_attr = target.char_z2_d2r1_attr 
            z2_d2r2_attr = target.char_z2_d2r2_attr 
            z2_d2r3_attr = target.char_z2_d2r3_attr 
            z2_d2r4_attr = target.char_z2_d2r4_attr 
            z2_d2r5_attr = target.char_z2_d2r5_attr 
            z2_d2r6_attr = target.char_z2_d2r6_attr 
            z2_d2r7_attr = target.char_z2_d2r7_attr 



            #self.canvas.addch(
            #    y-3,
            #    x-7,
            #    target.char_z2_u3l7,
            #    (z2_u3l7_color |
            #    z2_u3l7_attr)
            #    )
            #self.canvas.addch(
            #    y-3,
            #    x-6,
            #    target.char_z2_u3l6,
            #    (z2_u3l6_color |
            #    z2_u3l6_attr)
            #    )
            #self.canvas.addch(
            #    y-3,
            #    x-5,
            #    target.char_z2_u3l5,
            #    (z2_u3l5_color |
            #    z2_u3l5_attr)
            #    )
            #self.canvas.addch(
            #    y-3,
            #    x-4,
            #    target.char_z2_u3l4,
            #    (z2_u3l4_color |
            #    z2_u3l4_attr)
            #    )
            #self.canvas.addch(
            #    y-3,
            #    x-3,
            #    target.char_z2_u3l3,
            #    (z2_u3l3_color |
            #    z2_u3l3_attr)
            #    )
            #self.canvas.addch(
            #    y-3,
            #    x-2,
            #    target.char_z2_u3l2,
            #    (z2_u3l2_color |
            #    z2_u3l2_attr)
            #    )
            #self.canvas.addch(
            #    y-3,
            #    x-1,
            #    target.char_z2_u3l1,
            #    (z2_u3l1_color |
            #    z2_u3l1_attr)
            #    )
            #self.canvas.addch(
            #    y-3,
            #    x,
            #    target.char_z2_u3,
            #    (z2_u3_color |
            #    z2_u2_attr)
            #    )
            #self.canvas.addch(
            #    y-3,
            #    x+1,
            #    target.char_z2_u3r1,
            #    (z2_u3r1_color |
            #    z2_u3r1_attr)
            #    )
            #self.canvas.addch(
            #    y-3,
            #    x+2,
            #    target.char_z2_u3r2,
            #    (z2_u3r2_color |
            #    z2_u3r2_attr)
            #    )
            #self.canvas.addch(
            #    y-3,
            #    x+3,
            #    target.char_z2_u3r3,
            #    (z2_u3r3_color |
            #    z2_u3r3_attr)
            #    )
            #self.canvas.addch(
            #    y-3,
            #    x+4,
            #    target.char_z2_u3r4,
            #    (z2_u3r4_color |
            #    z2_u3r4_attr)
            #    )
            #self.canvas.addch(
            #    y-3,
            #    x+5,
            #    target.char_z2_u3r5,
            #    (z2_u3r5_color |
            #    z2_u3r5_attr)
            #    )
            #self.canvas.addch(
            #    y-3,
            #    x+6,
            #    target.char_z2_u3r6,
            #    (z2_u3r6_color |
            #    z2_u3r6_attr)
            #    )
            #self.canvas.addch(
            #    y-3,
            #    x+7,
            #    target.char_z2_u3r7,
            #    (z2_u3r7_color |
            #    z2_u3r7_attr)
            #    )



            #self.canvas.addch(
            #    y-2,
            #    x-7,
            #    target.char_z2_u2l7,
            #    (z2_u2l7_color |
            #    z2_u2l7_attr)
            #    )
            #self.canvas.addch(
            #    y-2,
            #    x-6,
            #    target.char_z2_u2l6,
            #    (z2_u2l6_color |
            #    z2_u2l6_attr)
            #    )
            self.canvas.addch(
                y-2,
                x-5,
                target.char_z2_u2l5,
                (z2_u2l5_color |
                z2_u2l5_attr)
                )
            self.canvas.addch(
                y-2,
                x-4,
                target.char_z2_u2l4,
                (z2_u2l4_color |
                z2_u2l4_attr)
                )
            self.canvas.addch(
                y-2,
                x-3,
                target.char_z2_u2l3,
                (z2_u2l3_color |
                z2_u2l3_attr)
                )
            self.canvas.addch(
                y-2,
                x-2,
                target.char_z2_u2l2,
                (z2_u2l2_color |
                z2_u2l2_attr)
                )
            self.canvas.addch(
                y-2,
                x-1,
                target.char_z2_u2l1,
                (z2_u2l1_color |
                z2_u2l1_attr)
                )
            self.canvas.addch(
                y-2,
                x,
                target.char_z2_u2,
                (z2_u2_color |
                z2_u2_attr)
                )
            self.canvas.addch(
                y-2,
                x+1,
                target.char_z2_u2r1,
                (z2_u2r1_color |
                z2_u2r1_attr)
                )
            self.canvas.addch(
                y-2,
                x+2,
                target.char_z2_u2r2,
                (z2_u2r2_color |
                z2_u2r2_attr)
                )
            self.canvas.addch(
                y-2,
                x+3,
                target.char_z2_u2r3,
                (z2_u2r3_color |
                z2_u2r3_attr)
                )
            self.canvas.addch(
                y-2,
                x+4,
                target.char_z2_u2r4,
                (z2_u2r4_color |
                z2_u2r4_attr)
                )
            self.canvas.addch(
                y-2,
                x+5,
                target.char_z2_u2r5,
                (z2_u2r5_color |
                z2_u2r5_attr)
                )
            #self.canvas.addch(
            #    y-2,
            #    x+6,
            #    target.char_z2_u2r6,
            #    (z2_u2r6_color |
            #    z2_u2r6_attr)
            #    )
            #self.canvas.addch(
            #    y-2,
            #    x+7,
            #    target.char_z2_u2r7,
            #    (z2_u2r7_color |
            #    z2_u2r7_attr)
            #    )
            #self.canvas.addch(
            #    y-1,
            #    x-7,
            #    target.char_z2_u1l7,
            #    (z2_u1l7_color |
            #    z2_u1l7_attr)
            #    )
            #self.canvas.addch(
            #    y-1,
            #    x-6,
            #    target.char_z2_u1l6,
            #    (z2_u1l6_color |
            #    z2_u1l6_attr)
            #    )
            self.canvas.addch(
                y-1,
                x-5,
                target.char_z2_u1l5,
                (z2_u1l5_color |
                z2_u1l5_attr)
                )
            self.canvas.addch(
                y-1,
                x-4,
                target.char_z2_u1l4,
                (z2_u1l4_color |
                z2_u1l4_attr)
                )
            self.canvas.addch(
                y-1,
                x-3,
                target.char_z2_u1l3,
                #target.side_char,
                #(target.side_char_color |
                (z2_u1l3_color |
                #target.side_char_attr)
                z2_u1l3_attr)
                )
            self.canvas.addch(
                y-1,
                x-2,
                target.char_z2_u1l2,
                #target.side_char,
                #(target.side_char_color |
                (z2_u1l2_color |
                #target.side_char_attr)
                z2_u1l2_attr)
                )
            self.canvas.addch(
                y-1,
                x-1,
                target.char_z2_u1l1,
                #target.side_char,
                #(target.side_char_color |
                (z2_u1l1_color |
                #target.side_char_attr)
                z2_u1l1_attr)
                )
            self.canvas.addch(
                y-1,
                x,
                target.char_z2_u1,
                #target.side_char,
                #(target.side_char_color |
                (z2_u1_color |
                #target.side_char_attr)
                z2_u1_attr)
                )
            self.canvas.addch(
                y - 1,
                x + 1,
                target.char_z2_u1r1,
                #target.side_char,
                #(target.side_char_color |
                (z2_u1r1_color |
                #target.side_char_attr)
                z2_u1r1_attr)
                )
            self.canvas.addch(
                y - 1,
                x + 2,
                target.char_z2_u1r2,
                #target.side_char,
                #(target.side_char_color |
                (z2_u1r2_color |
                #target.side_char_attr)
                z2_u1r2_attr)
                )
            self.canvas.addch(
                y - 1,
                x + 3,
                target.char_z2_u1r3,
                #target.side_char,
                #(target.side_char_color |
                (z2_u1r3_color |
                #target.side_char_attr)
                z2_u1r3_attr)
                )
            self.canvas.addch(
                y-1,
                x+4,
                target.char_z2_u1r4,
                (z2_u1r4_color |
                z2_u1r4_attr)
                )
            self.canvas.addch(
                y-1,
                x+5,
                target.char_z2_u1r5,
                (z2_u1r5_color |
                z2_u1r5_attr)
                )
            #self.canvas.addch(
            #    y-1,
            #    x+6,
            #    target.char_z2_u1r6,
            #    (z2_u1r6_color |
            #    z2_u1r6_attr)
            #    )
            #self.canvas.addch(
            #    y-1,
            #    x+7,
            #    target.char_z2_u1r7,
            #    (z2_u1r7_color |
            #    z2_u1r7_attr)
            #    )
            #self.canvas.addch(
            #    y,
            #    x-7,
            #    target.char_z2_l7,
            #    (z2_l7_color |
            #    z2_l7_attr)
            #    )
            #self.canvas.addch(
            #    y,
            #    x-6,
            #    target.char_z2_l6,
            #    (z2_l6_color |
            #    z2_l6_attr)
            #    )
            self.canvas.addch(
                y,
                x-5,
                target.char_z2_l5,
                (z2_l5_color |
                z2_l5_attr)
                )
            self.canvas.addch(
                y,
                x-4,
                target.char_z2_l4,
                (z2_l4_color |
                z2_l4_attr)
                )
            self.canvas.addch(
                y,
                x-3,
                target.char_z2_l3,
                (z2_l3_color |
                z2_l3_attr)
                )
            self.canvas.addch(
                y,
                x - 2,
                target.char_z2_l2,
                #target.side_char,
                #(target.side_char_color |
                (z2_l2_color |
                #target.side_char_attr)
                z2_l2_attr)
                )
            self.canvas.addch(
                y,
                x - 1,
                target.char_z2_l1,
                #target.side_char,
                #(target.side_char_color |
                (z2_l1_color |
                #target.side_char_attr)
                z2_l1_attr)
                )
            self.canvas.addch(
                y,
                x,
                #target.char,
                target.char_z2_center,
                #(target.side_char_color |
                (z2_center_color |
                #target.char_attr)
                z2_center_attr)
                )
            self.canvas.addch(
                y,
                x + 1,
                target.char_z2_r1,
                #target.side_char,
                #(target.side_char_color |
                (z2_r1_color |
                #target.side_char_attr)
                z2_r1_attr)
                )
            self.canvas.addch(
                y,
                x + 2,
                target.char_z2_r2,
                #target.side_char,
                #(target.side_char_color |
                (z2_r2_color |
                #target.side_char_attr)
                z2_r2_attr)
                )
            self.canvas.addch(
                y,
                x + 3,
                target.char_z2_r3,
                #target.side_char,
                #(target.side_char_color |
                (z2_r3_color |
                #target.side_char_attr)
                z2_r3_attr)
                )
            self.canvas.addch(
                y,
                x+4,
                target.char_z2_r4,
                (z2_r4_color |
                z2_r4_attr)
                )
            self.canvas.addch(
                y,
                x+5,
                target.char_z2_r5,
                (z2_r5_color |
                z2_r5_attr)
                )
            #self.canvas.addch(
            #    y,
            #    x+6,
            #    target.char_z2_r6,
            #    (z2_r6_color |
            #    z2_r6_attr)
            #    )
            #self.canvas.addch(
            #    y,
            #    x+7,
            #    target.char_z2_r7,
            #    (z2_r7_color |
            #    z2_r7_attr)
            #    )
            #self.canvas.addch(
            #    y+1,
            #    x-7,
            #    target.char_z2_d1l7,
            #    (z2_d1l7_color |
            #    z2_d1l7_attr)
            #    )
            #self.canvas.addch(
            #    y+1,
            #    x-6,
            #    target.char_z2_d1l6,
            #    (z2_d1l6_color |
            #    z2_d1l6_attr)
            #    )
            self.canvas.addch(
                y+1,
                x-5,
                target.char_z2_d1l5,
                (z2_d1l5_color |
                z2_d1l5_attr)
                )
            self.canvas.addch(
                y+1,
                x-4,
                target.char_z2_d1l4,
                (z2_d1l4_color |
                z2_d1l4_attr)
                )
            self.canvas.addch(
                y+1,
                x-3,
                target.char_z2_d1l3,
                (z2_d1l3_color |
                z2_d1l3_attr)
                )
            self.canvas.addch(
                y + 1,
                x - 2,
                target.char_z2_d1l2,
                #target.side_char,
                #(target.side_char_color |
                (z2_d1l2_color |
                #target.side_char_attr)
                z2_d1l2_attr)
                )
            self.canvas.addch(
                y + 1,
                x - 1,
                target.char_z2_d1l1,
                #target.side_char,
                #(target.side_char_color |
                (z2_d1l1_color |
                #target.side_char_attr)
                z2_d1l1_attr)
                )
            self.canvas.addch(
                y + 1,
                x,
                target.char_z2_d1,
                #target.side_char,
                #(target.side_char_color |
                (z2_d1_color |
                #target.side_char_attr)
                z2_d1_attr)
                )
            self.canvas.addch(
                y + 1,
                x + 1,
                target.char_z2_d1r1,
                #target.side_char,
                #(target.side_char_color |
                (z2_d1r1_color |
                #target.side_char_attr)
                z2_d1r1_attr)
                )
            self.canvas.addch(
                y + 1,
                x + 2,
                target.char_z2_d1r2,
                #target.side_char,
                #(target.side_char_color |
                (z2_d1r2_color |
                #target.side_char_attr)
                z2_d1r2_attr)
                )
            self.canvas.addch(
                y + 1,
                x + 3,
                target.char_z2_d1r3,
                #target.side_char,
                #(target.side_char_color |
                (z2_d1r3_color |
                #target.side_char_attr)
                z2_d1r3_attr)
                )
            self.canvas.addch(
                y+1,
                x+4,
                target.char_z2_d1r4,
                (z2_d1r4_color |
                z2_d1r4_attr)
                )
            self.canvas.addch(
                y+1,
                x+5,
                target.char_z2_d1r5,
                (z2_d1r5_color |
                z2_d1r5_attr)
                )
            #self.canvas.addch(
            #    y+1,
            #    x+6,
            #    target.char_z2_d1r6,
            #    (z2_d1r6_color |
            #    z2_d1r6_attr)
            #    )
            #self.canvas.addch(
            #    y+1,
            #    x+7,
            #    target.char_z2_d1r7,
            #    (z2_d1r7_color |
            #    z2_d1r7_attr)
            #    )
            #self.canvas.addch(
            #    y+2,
            #    x-7,
            #    target.char_z2_d2l7,
            #    (z2_d2l7_color |
            #    z2_d2l7_attr)
            #    )
            #self.canvas.addch(
            #    y+2,
            #    x-6,
            #    target.char_z2_d2l6,
            #    (z2_d2l6_color |
            #    z2_d2l6_attr)
            #    )
            self.canvas.addch(
                y+2,
                x-5,
                target.char_z2_d2l5,
                (z2_d2l5_color |
                z2_d2l5_attr)
                )
            self.canvas.addch(
                y+2,
                x-4,
                target.char_z2_d2l4,
                (z2_d2l4_color |
                z2_d2l4_attr)
                )
            self.canvas.addch(
                y+2,
                x-3,
                target.char_z2_d2l3,
                (z2_d2l3_color |
                z2_d2l3_attr)
                )
            self.canvas.addch(
                y+2,
                x-2,
                target.char_z2_d2l2,
                (z2_d2l2_color |
                z2_d2l2_attr)
                )
            self.canvas.addch(
                y+2,
                x-1,
                target.char_z2_d2l1,
                (z2_d2l1_color |
                z2_d2l1_attr)
                )
            self.canvas.addch(
                y+2,
                x,
                target.char_z2_d2,
                (z2_d2_color |
                z2_d2_attr)
                )
            self.canvas.addch(
                y+2,
                x+1,
                target.char_z2_d2r1,
                (z2_d2r1_color |
                z2_d2r1_attr)
                )
            self.canvas.addch(
                y+2,
                x+2,
                target.char_z2_d2r2,
                (z2_d2r2_color |
                z2_d2r2_attr)
                )
            self.canvas.addch(
                y+2,
                x+3,
                target.char_z2_d2r3,
                #target.side_char,
                #(target.side_char_color |
                (z2_d2r3_color |
                #target.side_char_attr)
                z2_d2r3_attr)
                )
            self.canvas.addch(
                y+2,
                x+4,
                target.char_z2_d2r4,
                (z2_d2r4_color |
                z2_d2r4_attr)
                )
            self.canvas.addch(
                y+2,
                x+5,
                target.char_z2_d2r5,
                (z2_d2r5_color |
                z2_d2r5_attr)
                )
            #self.canvas.addch(
            #    y+2,
            #    x+6,
            #    target.char_z2_d2r6,
            #    (z2_d2r6_color |
            #    z2_d2r6_attr)
            #    )
            #self.canvas.addch(
            #    y+2,
            #    x+7,
            #    target.char_z2_d2r7,
            #    (z2_d2r7_color |
            #    z2_d2r7_attr)
            #    )





        elif self.camera_zoom == 1:
            #y = int(((target.y + 1) * 3) - 1)
            y = int((target.y * 3) + 1)
            #y = int(target.y * 3)
            #x = int(((target.x + 1) * 3) - 1)
            x = int((target.x * 3) + (target.x / 2))
            #x = int((target.x * 3) + 10)
            #x = int((target.x * 3) + 1)
            #y = 10
            #x = 10

            #y = target.y * 2
            #x = target.x * 3

            #game.logger.warning('TEST2: y,x is <%s>,<%s>', str(y), str(x))



            z1_u1l3_color = target.char_z1_u1l3_color
            z1_u1l2_color = target.char_z1_u1l2_color
            z1_u1l1_color = target.char_z1_u1l1_color
            z1_u1_color = target.char_z1_u1_color
            z1_u1r1_color = target.char_z1_u1r1_color
            z1_u1r2_color = target.char_z1_u1r2_color
            z1_u1r3_color = target.char_z1_u1r3_color
            z1_l3_color = target.char_z1_l3_color
            z1_l2_color = target.char_z1_l2_color
            z1_l1_color = target.char_z1_l1_color
            z1_center_color = target.char_z1_center_color
            z1_r1_color = target.char_z1_r1_color
            z1_r2_color = target.char_z1_r2_color
            z1_r3_color = target.char_z1_r3_color
            z1_d1l3_color = target.char_z1_d1l3_color
            z1_d1l2_color = target.char_z1_d1l2_color
            z1_d1l1_color = target.char_z1_d1l1_color
            z1_d1_color = target.char_z1_d1_color
            z1_d1r1_color = target.char_z1_d1r1_color
            z1_d1r2_color = target.char_z1_d1r2_color
            z1_d1r3_color = target.char_z1_d1r3_color

            z1_u1l3_attr = target.char_z1_u1l3_attr
            z1_u1l2_attr = target.char_z1_u1l2_attr
            z1_u1l1_attr = target.char_z1_u1l1_attr
            z1_u1_attr = target.char_z1_u1_attr
            z1_u1r1_attr = target.char_z1_u1r1_attr
            z1_u1r2_attr = target.char_z1_u1r2_attr
            z1_u1r3_attr = target.char_z1_u1r3_attr
            z1_l3_attr = target.char_z1_l3_attr
            z1_l2_attr = target.char_z1_l2_attr
            z1_l1_attr = target.char_z1_l1_attr
            z1_center_attr = target.char_z1_center_attr
            z1_r1_attr = target.char_z1_r1_attr
            z1_r2_attr = target.char_z1_r2_attr
            z1_r3_attr = target.char_z1_r3_attr
            z1_d1l3_attr = target.char_z1_d1l3_attr
            z1_d1l2_attr = target.char_z1_d1l2_attr
            z1_d1l1_attr = target.char_z1_d1l1_attr
            z1_d1_attr = target.char_z1_d1_attr
            z1_d1r1_attr = target.char_z1_d1r1_attr
            z1_d1r2_attr = target.char_z1_d1r2_attr
            z1_d1r3_attr = target.char_z1_d1r3_attr




            self.canvas.addch(
                y-1,
                x-3,
                target.char_z1_u1l3,
                (z1_u1l3_color |
                z1_u1l3_attr)
                )
            self.canvas.addch(
                y-1,
                x-2,
                target.char_z1_u1l2,
                #target.side_char,
                #(target.side_char_color |
                (z1_u1l2_color |
                #target.side_char_attr)
                z1_u1l2_attr)
                )
            self.canvas.addch(
                y-1,
                x-1,
                target.char_z1_u1l1,
                #target.side_char,
                #(target.side_char_color |
                (z1_u1l1_color |
                #target.side_char_attr)
                z1_u1l1_attr)
                )
            self.canvas.addch(
                y-1,
                x,
                target.char_z1_u1,
                #target.side_char,
                #(target.side_char_color |
                (z1_u1_color |
                #target.side_char_attr)
                z1_u1_attr)
                )
            self.canvas.addch(
                y - 1,
                x + 1,
                target.char_z1_u1r1,
                #target.side_char,
                #(target.side_char_color |
                (z1_u1r1_color |
                #target.side_char_attr)
                z1_u1r1_attr)
                )
            self.canvas.addch(
                y - 1,
                x + 2,
                target.char_z1_u1r2,
                #target.side_char,
                #(target.side_char_color |
                (z1_u1r2_color |
                #target.side_char_attr)
                z1_u1r2_attr)
                )
            self.canvas.addch(
                y - 1,
                x + 3,
                target.char_z1_u1r3,
                #target.side_char,
                #(target.side_char_color |
                (z1_u1r3_color |
                #target.side_char_attr)
                z1_u1r3_attr)
                )
            self.canvas.addch(
                y,
                x-3,
                target.char_z1_l3,
                (z1_l3_color |
                z1_l3_attr)
                )
            self.canvas.addch(
                y,
                x - 2,
                target.char_z1_l2,
                #target.side_char,
                #(target.side_char_color |
                (z1_l2_color |
                #target.side_char_attr)
                z1_l2_attr)
                )
            self.canvas.addch(
                y,
                x - 1,
                target.char_z1_l1,
                #target.side_char,
                #(target.side_char_color |
                (z1_l1_color |
                #target.side_char_attr)
                z1_l1_attr)
                )
            self.canvas.addch(
                y,
                x,
                #target.char,
                target.char_z1_center,
                #(target.side_char_color |
                (z1_center_color |
                #target.char_attr)
                z1_center_attr)
                )
            self.canvas.addch(
                y,
                x + 1,
                target.char_z1_r1,
                #target.side_char,
                #(target.side_char_color |
                (z1_r1_color |
                #target.side_char_attr)
                z1_r1_attr)
                )
            self.canvas.addch(
                y,
                x + 2,
                target.char_z1_r2,
                #target.side_char,
                #(target.side_char_color |
                (z1_r2_color |
                #target.side_char_attr)
                z1_r2_attr)
                )
            self.canvas.addch(
                y,
                x + 3,
                target.char_z1_r3,
                #target.side_char,
                #(target.side_char_color |
                (z1_r3_color |
                #target.side_char_attr)
                z1_r3_attr)
                )
            self.canvas.addch(
                y+1,
                x-3,
                target.char_z1_d1l3,
                (z1_d1l3_color |
                z1_d1l3_attr)
                )
            self.canvas.addch(
                y + 1,
                x - 2,
                target.char_z1_d1l2,
                #target.side_char,
                #(target.side_char_color |
                (z1_d1l2_color |
                #target.side_char_attr)
                z1_d1l2_attr)
                )
            self.canvas.addch(
                y + 1,
                x - 1,
                target.char_z1_d1l1,
                #target.side_char,
                #(target.side_char_color |
                (z1_d1l1_color |
                #target.side_char_attr)
                z1_d1l1_attr)
                )
            self.canvas.addch(
                y + 1,
                x,
                target.char_z1_d1,
                #target.side_char,
                #(target.side_char_color |
                (z1_d1_color |
                #target.side_char_attr)
                z1_d1_attr)
                )
            self.canvas.addch(
                y + 1,
                x + 1,
                target.char_z1_d1r1,
                #target.side_char,
                #(target.side_char_color |
                (z1_d1r1_color |
                #target.side_char_attr)
                z1_d1r1_attr)
                )
            self.canvas.addch(
                y + 1,
                x + 2,
                target.char_z1_d1r2,
                #target.side_char,
                #(target.side_char_color |
                (z1_d1r2_color |
                #target.side_char_attr)
                z1_d1r2_attr)
                )
            self.canvas.addch(
                y + 1,
                x + 3,
                target.char_z1_d1r3,
                #target.side_char,
                #(target.side_char_color |
                (z1_d1r3_color |
                #target.side_char_attr)
                z1_d1r3_attr)
                )


        
        elif self.camera_zoom == 0:

            self.canvas.addch(
                target.y,
                target.x,
                target.char,
                #(target.color |
                (color |
                target.char_attr))
 
            if target.side_char is not None:
            #if isinstance(target, Terrain):
                game.logger.debug('TEST11: target is <%s>_<%s>',
                    str(target.name), str(target.serial))
                self.canvas.addch(
                target.y,
                target.x + 1,
                target.side_char,
                #(target.side_char_color |
                (side_color |
                target.side_char_attr)
                )


    def drawSpace(
        self,
        y,
        x,
        ):

        #things = self.querySpace(y, x)

        space = game.getSpace(y, x)
        if not space:
            game.logger.warning('tried to draw on an illegal space <%s>, <%s>',
                str(y), str(x))
            return

        things = space.contents

        #if not things:
        #    game.logger.warning('tried to draw on illegal space')
        #    return

        actors = []
        items = []
        terrains = []

        for thing in things:
            if isinstance(thing, Actor):
                actors.append(thing)

            elif isinstance(thing, Item):
                items.append(thing)

            elif isinstance(thing, Terrain):
                terrains.append(thing)

        if actors:
            priority = actors[0]
            for actor in actors:
                game.logger.debug('priority <%s> at <%s>, <%s>', 
                    str(actor.name), str(y), str(x))
        elif items:
            priority = items[0]
        elif terrains:
            priority = terrains[0]
        else:
            priority = things[0]

        game.logger.debug('draw priority is <%s>',
            str(priority.name))

        self.quickDraw(priority) 


class Thing(object):
    def __init__(self):
        #self,
        #y,
        #x):

        self.serial = game.getSerial()
        game.logger.debug('<%s>.serial = <%s>', str(self), str(self.serial))

        self.name = str('thing')
        game.logger.debug('<%s>_<%s>.name = <%s>', 
            str(self), str(self.serial), str(self.name))

        #self.y = y
        self.y = 10
        game.logger.debug('<%s>_<%s>.y = <%s>', 
            str(self.name), str(self.serial), str(self.y))

        #self.x = x
        self.x = 10
        game.logger.debug('<%s>_<%s>.x = <%s>', 
            str(self.name), str(self.serial), str(self.x))

        if isinstance(self, Actor):
            self.blocks = True
        else:
            self.blocks = False
        game.logger.debug('<%s>_<%s>.blocks = <%s>',
            str(self.name), str(self.serial), str(self.blocks))

        self.char = '?'

        #self.char_attr = curses.A_ALTCHARSET
        self.char_attr = curses.A_NORMAL
        #self.char_attr = curses.A_BLINK
        #self.char_attr = curses.A_REVERSE
        #self.char_attr = curses.A_STANDOUT
        #self.char_attr = curses.A_UNDERLINE
        #self.char_attr = curses.A_BOLD
        #self.char_attr = curses.A_DIM
        
        #TODO: capture error and turn this into a try
        # important to call curses directly here instead of game, during-
        #   certain times, especially startup, game may not exist
        self.color = game.curses.color_pair(0)   # will always be white/black
        
        self.side_char = ' '
        self.side_char_color = game.colors['white']
        self.side_char_attr = curses.A_NORMAL

        self.char_color_dark = game.colors['blue']
        self.side_char_color_dark = game.colors['blue']
        

        #self.char_z1_center = self.char


        #self.char_z2_u3l7 = ' '
        #self.char_z2_u3l7_color = self.color
        #self.char_z2_u3l7_attr = self.char_attr
        #self.char_z2_u3l6 = ' '
        #self.char_z2_u3l6_color = self.color
        #self.char_z2_u3l6_attr = self.char_attr
        #self.char_z2_u3l5 = ' '
        #self.char_z2_u3l5_color = self.color
        #self.char_z2_u3l5_attr = self.char_attr
        #self.char_z2_u3l4 = ' '
        #self.char_z2_u3l4_color = self.color
        #self.char_z2_u3l4_attr = self.char_attr
        #self.char_z2_u3l3 = ' '
        #self.char_z2_u3l3_color = self.color
        #self.char_z2_u3l3_attr = self.char_attr
        #self.char_z2_u3l2 = ' '
        #self.char_z2_u3l2_color = self.color
        #self.char_z2_u3l2_attr = self.char_attr
        #self.char_z2_u3l1 = ' '
        #self.char_z2_u3l1_color = self.color
        #self.char_z2_u3l1_attr = self.char_attr
        #self.char_z2_u3 = ' '
        #self.char_z2_u3_color = self.color
        #self.char_z2_u3_attr = self.char_attr
        #self.char_z2_u3r1 = ' ' 
        #self.char_z2_u3r1_color = self.color
        #self.char_z2_u3r1_attr = self.char_attr
        #self.char_z2_u3r2 = ' '
        #self.char_z2_u3r2_color = self.color
        #self.char_z2_u3r2_attr = self.char_attr
        #self.char_z2_u3r3 = ' '
        #self.char_z2_u3r3_color = self.color
        #self.char_z2_u3r3_attr = self.char_attr
        #self.char_z2_u3r4 = ' '          
        #self.char_z2_u3r4_color = self.color
        #self.char_z2_u3r4_attr = self.char_attr
        #self.char_z2_u3r5 = ' '          
        #self.char_z2_u3r5_color = self.color
        #self.char_z2_u3r5_attr = self.char_attr
        #self.char_z2_u3r6 = ' '          
        #self.char_z2_u3r6_color = self.color
        #self.char_z2_u3r6_attr = self.char_attr
        #self.char_z2_u3r7 = ' '          
        #self.char_z2_u3r7_color = self.color
        #self.char_z2_u3r7_attr = self.char_attr
        self.char_z2_u2l7 = ' '
        self.char_z2_u2l7_color = self.color
        self.char_z2_u2l7_attr = self.char_attr
        self.char_z2_u2l6 = ' '
        self.char_z2_u2l6_color = self.color
        self.char_z2_u2l6_attr = self.char_attr
        self.char_z2_u2l5 = ' '
        self.char_z2_u2l5_color = self.color
        self.char_z2_u2l5_attr = self.char_attr
        self.char_z2_u2l4 = ' '
        self.char_z2_u2l4_color = self.color
        self.char_z2_u2l4_attr = self.char_attr
        self.char_z2_u2l3 = ' '
        self.char_z2_u2l3_color = self.color
        self.char_z2_u2l3_attr = self.char_attr
        self.char_z2_u2l2 = ' '
        self.char_z2_u2l2_color = self.color
        self.char_z2_u2l2_attr = self.char_attr
        self.char_z2_u2l1 = ' '
        self.char_z2_u2l1_color = self.color
        self.char_z2_u2l1_attr = self.char_attr
        self.char_z2_u2 = ' '
        self.char_z2_u2_color = self.color
        self.char_z2_u2_attr = self.char_attr
        self.char_z2_u2r1 = ' ' 
        self.char_z2_u2r1_color = self.color
        self.char_z2_u2r1_attr = self.char_attr
        self.char_z2_u2r2 = ' '
        self.char_z2_u2r2_color = self.color
        self.char_z2_u2r2_attr = self.char_attr
        self.char_z2_u2r3 = ' '
        self.char_z2_u2r3_color = self.color
        self.char_z2_u2r3_attr = self.char_attr
        self.char_z2_u2r4 = ' '          
        self.char_z2_u2r4_color = self.color
        self.char_z2_u2r4_attr = self.char_attr
        self.char_z2_u2r5 = ' '          
        self.char_z2_u2r5_color = self.color
        self.char_z2_u2r5_attr = self.char_attr
        self.char_z2_u2r6 = ' '          
        self.char_z2_u2r6_color = self.color
        self.char_z2_u2r6_attr = self.char_attr
        self.char_z2_u2r7 = ' '          
        self.char_z2_u2r7_color = self.color
        self.char_z2_u2r7_attr = self.char_attr
        self.char_z2_u1l7 = ' '
        self.char_z2_u1l7_color = self.color
        self.char_z2_u1l7_attr = self.char_attr
        self.char_z2_u1l6 = ' '
        self.char_z2_u1l6_color = self.color
        self.char_z2_u1l6_attr = self.char_attr
        self.char_z2_u1l5 = ' '
        self.char_z2_u1l5_color = self.color
        self.char_z2_u1l5_attr = self.char_attr
        self.char_z2_u1l4 = ' '
        self.char_z2_u1l4_color = self.color
        self.char_z2_u1l4_attr = self.char_attr
        self.char_z2_u1l3 = ' '
        self.char_z2_u1l3_color = self.color
        self.char_z2_u1l3_attr = self.char_attr
        self.char_z2_u1l2 = ' '
        self.char_z2_u1l2_color = self.color
        self.char_z2_u1l2_attr = self.char_attr
        #self.char_z1_u1l2_color = game.colors['blue']
        self.char_z2_u1l1 = ' '
        self.char_z2_u1l1_color = self.color
        self.char_z2_u1l1_attr = self.char_attr
        self.char_z2_u1 = ' '
        self.char_z2_u1_color = self.color
        self.char_z2_u1_attr = self.char_attr
        self.char_z2_u1r1 = ' '
        self.char_z2_u1r1_color = self.color
        self.char_z2_u1r1_attr = self.char_attr
        self.char_z2_u1r2 = ' '
        self.char_z2_u1r2_color = self.color
        self.char_z2_u1r2_attr = self.char_attr
        self.char_z2_u1r3 = ' '
        self.char_z2_u1r3_color = self.color
        self.char_z2_u1r3_attr = self.char_attr
        self.char_z2_u1r4 = ' '         
        self.char_z2_u1r4_color = self.color
        self.char_z2_u1r4_attr = self.char_attr
        self.char_z2_u1r5 = ' '          
        self.char_z2_u1r5_color = self.color
        self.char_z2_u1r5_attr = self.char_attr
        self.char_z2_u1r6 = ' '          
        self.char_z2_u1r6_color = self.color
        self.char_z2_u1r6_attr = self.char_attr
        self.char_z2_u1r7 = ' '          
        self.char_z2_u1r7_color = self.color
        self.char_z2_u1r7_attr = self.char_attr
        self.char_z2_l7 = ' '
        self.char_z2_l7_color = self.color
        self.char_z2_l7_attr = self.char_attr
        self.char_z2_l6 = ' '
        self.char_z2_l6_color = self.color
        self.char_z2_l6_attr = self.char_attr
        self.char_z2_l5 = ' '
        self.char_z2_l5_color = self.color
        self.char_z2_l5_attr = self.char_attr
        self.char_z2_l4 = ' '
        self.char_z2_l4_color = self.color
        self.char_z2_l4_attr = self.char_attr
        self.char_z2_l3 = ' '
        self.char_z2_l3_color = self.color
        self.char_z2_l3_attr = self.char_attr
        self.char_z2_l2 = ' '
        self.char_z2_l2_color = self.color
        self.char_z2_l2_attr = self.char_attr
        self.char_z2_l1 = ' '
        self.char_z2_l1_color = self.color
        self.char_z2_l1_attr = self.char_attr
        self.char_z2_center = self.char
        self.char_z2_center_color = self.color
        self.char_z2_center_attr = self.char_attr
        self.char_z2_r1 = ' '
        self.char_z2_r1_color = self.color
        self.char_z2_r1_attr = self.char_attr
        self.char_z2_r2 = ' '
        self.char_z2_r2_color = self.color
        self.char_z2_r2_attr = self.char_attr
        self.char_z2_r3 = ' '
        self.char_z2_r3_color = self.color
        self.char_z2_r3_attr = self.char_attr
        self.char_z2_r4 = ' '         
        self.char_z2_r4_color = self.color
        self.char_z2_r4_attr = self.char_attr
        self.char_z2_r5 = ' '          
        self.char_z2_r5_color = self.color
        self.char_z2_r5_attr = self.char_attr
        self.char_z2_r6 = ' '          
        self.char_z2_r6_color = self.color
        self.char_z2_r6_attr = self.char_attr
        self.char_z2_r7 = ' '          
        self.char_z2_r7_color = self.color
        self.char_z2_r7_attr = self.char_attr
        self.char_z2_d1l7 = ' '
        self.char_z2_d1l7_color = self.color
        self.char_z2_d1l7_attr = self.char_attr
        self.char_z2_d1l6 = ' '
        self.char_z2_d1l6_color = self.color
        self.char_z2_d1l6_attr = self.char_attr
        self.char_z2_d1l5 = ' '
        self.char_z2_d1l5_color = self.color
        self.char_z2_d1l5_attr = self.char_attr
        self.char_z2_d1l4 = ' '
        self.char_z2_d1l4_color = self.color
        self.char_z2_d1l4_attr = self.char_attr
        self.char_z2_d1l3 = ' '
        self.char_z2_d1l3_color = self.color
        self.char_z2_d1l3_attr = self.char_attr
        self.char_z2_d1l2 = ' '
        self.char_z2_d1l2_color = self.color
        self.char_z2_d1l2_attr = self.char_attr
        self.char_z2_d1l1 = ' '
        self.char_z2_d1l1_color = self.color
        self.char_z2_d1l1_attr = self.char_attr
        self.char_z2_d1 = ' '
        self.char_z2_d1_color = self.color
        self.char_z2_d1_attr = self.char_attr
        self.char_z2_d1r1 = ' '
        self.char_z2_d1r1_color = self.color
        self.char_z2_d1r1_attr = self.char_attr
        self.char_z2_d1r2 = ' '
        self.char_z2_d1r2_color = self.color
        self.char_z2_d1r2_attr = self.char_attr
        self.char_z2_d1r3 = ' '
        self.char_z2_d1r3_color = self.color
        self.char_z2_d1r3_attr = self.char_attr
        self.char_z2_d1r4 = ' ' 
        self.char_z2_d1r4_color = self.color
        self.char_z2_d1r4_attr = self.char_attr
        self.char_z2_d1r5 = ' '          
        self.char_z2_d1r5_color = self.color
        self.char_z2_d1r5_attr = self.char_attr
        self.char_z2_d1r6 = ' '          
        self.char_z2_d1r6_color = self.color
        self.char_z2_d1r6_attr = self.char_attr
        self.char_z2_d1r7 = ' '          
        self.char_z2_d1r7_color = self.color
        self.char_z2_d1r7_attr = self.char_attr
        self.char_z2_d2l7 = ' '
        self.char_z2_d2l7_color = self.color
        self.char_z2_d2l7_attr = self.char_attr
        self.char_z2_d2l6 = ' '
        self.char_z2_d2l6_color = self.color
        self.char_z2_d2l6_attr = self.char_attr
        self.char_z2_d2l5 = ' '
        self.char_z2_d2l5_color = self.color
        self.char_z2_d2l5_attr = self.char_attr
        self.char_z2_d2l4 = ' '
        self.char_z2_d2l4_color = self.color
        self.char_z2_d2l4_attr = self.char_attr
        self.char_z2_d2l3 = ' '
        self.char_z2_d2l3_color = self.color
        self.char_z2_d2l3_attr = self.char_attr
        self.char_z2_d2l2 = ' '
        self.char_z2_d2l2_color = self.color
        self.char_z2_d2l2_attr = self.char_attr
        self.char_z2_d2l1 = ' '
        self.char_z2_d2l1_color = self.color
        self.char_z2_d2l1_attr = self.char_attr
        self.char_z2_d2 = ' '
        self.char_z2_d2_color = self.color
        self.char_z2_d2_attr = self.char_attr
        self.char_z2_d2r1 = ' '
        self.char_z2_d2r1_color = self.color
        self.char_z2_d2r1_attr = self.char_attr
        self.char_z2_d2r2 = ' '
        self.char_z2_d2r2_color = self.color
        self.char_z2_d2r2_attr = self.char_attr
        self.char_z2_d2r3 = ' '
        self.char_z2_d2r3_color = self.color
        self.char_z2_d2r3_attr = self.char_attr
        self.char_z2_d2r4 = ' '         
        self.char_z2_d2r4_color = self.color
        self.char_z2_d2r4_attr = self.char_attr
        self.char_z2_d2r5 = ' '          
        self.char_z2_d2r5_color = self.color
        self.char_z2_d2r5_attr = self.char_attr
        self.char_z2_d2r6 = ' '          
        self.char_z2_d2r6_color = self.color
        self.char_z2_d2r6_attr = self.char_attr
        self.char_z2_d2r7 = ' '          
        self.char_z2_d2r7_color = self.color
        self.char_z2_d2r7_attr = self.char_attr


        #self.char_z1_u1l1 = ' '
        #self.char_z1_u1l1_color = self.color
        #self.char_z1_u1l1_attr = self.char_attr
        #self.char_z1_u1 = ' '
        #self.char_z1_u1_color = self.color
        #self.char_z1_u1_attr = self.char_attr
        #self.char_z1_u1r1 = ' '
        #self.char_z1_u1r1_color = self.color
        #self.char_z1_u1r1_attr = self.char_attr
        #self.char_z1_l1 = ' '
        #self.char_z1_l1_color = self.color
        #self.char_z1_l1_attr = self.char_attr
        #self.char_z1_center = self.char
        #self.char_z1_center_color = self.color
        #self.char_z1_center_attr = self.char_attr
        #self.char_z1_r1 = ' '
        #self.char_z1_r1_color = self.color
        #self.char_z1_r1_attr = self.char_attr


        self.char_z1_u1l3 = ' '
        self.char_z1_u1l3_color = self.color
        self.char_z1_u1l3_attr = self.char_attr
        self.char_z1_u1l2 = ' '
        self.char_z1_u1l2_color = self.color
        self.char_z1_u1l2_attr = self.char_attr
        #self.char_z1_u1l2_color = game.colors['blue']
        self.char_z1_u1l1 = ' '
        self.char_z1_u1l1_color = self.color
        self.char_z1_u1l1_attr = self.char_attr
        self.char_z1_u1 = ' '
        self.char_z1_u1_color = self.color
        self.char_z1_u1_attr = self.char_attr
        self.char_z1_u1r1 = ' '
        self.char_z1_u1r1_color = self.color
        self.char_z1_u1r1_attr = self.char_attr
        self.char_z1_u1r2 = ' '
        self.char_z1_u1r2_color = self.color
        self.char_z1_u1r2_attr = self.char_attr
        self.char_z1_u1r3 = ' '
        self.char_z1_u1r3_color = self.color
        self.char_z1_u1r3_attr = self.char_attr
        self.char_z1_l3 = ' '
        self.char_z1_l3_color = self.color
        self.char_z1_l3_attr = self.char_attr
        self.char_z1_l2 = ' '
        self.char_z1_l2_color = self.color
        self.char_z1_l2_attr = self.char_attr
        self.char_z1_l1 = ' '
        self.char_z1_l1_color = self.color
        self.char_z1_l1_attr = self.char_attr
        self.char_z1_center = self.char
        self.char_z1_center_color = self.color
        self.char_z1_center_attr = self.char_attr
        self.char_z1_r1 = ' '
        self.char_z1_r1_color = self.color
        self.char_z1_r1_attr = self.char_attr
        self.char_z1_r2 = ' '
        self.char_z1_r2_color = self.color
        self.char_z1_r2_attr = self.char_attr
        self.char_z1_r3 = ' '
        self.char_z1_r3_color = self.color
        self.char_z1_r3_attr = self.char_attr
        self.char_z1_d1l3 = ' '
        self.char_z1_d1l3_color = self.color
        self.char_z1_d1l3_attr = self.char_attr
        self.char_z1_d1l2 = ' '
        self.char_z1_d1l2_color = self.color
        self.char_z1_d1l2_attr = self.char_attr
        self.char_z1_d1l1 = ' '
        self.char_z1_d1l1_color = self.color
        self.char_z1_d1l1_attr = self.char_attr
        self.char_z1_d1 = ' '
        self.char_z1_d1_color = self.color
        self.char_z1_d1_attr = self.char_attr
        self.char_z1_d1r1 = ' '
        self.char_z1_d1r1_color = self.color
        self.char_z1_d1r1_attr = self.char_attr
        self.char_z1_d1r2 = ' '
        self.char_z1_d1r2_color = self.color
        self.char_z1_d1r2_attr = self.char_attr
        self.char_z1_d1r3 = ' '
        self.char_z1_d1r3_color = self.color
        self.char_z1_d1r3_attr = self.char_attr


class Terrain(Thing):
    def __init__(self):
        #self,
        #y,
        #x):
        super(Terrain, self).__init__()
            #y=y,
            #x=x)

        #self.char_attr = curses.A_BOLD
        #self.char_attr = curses.A_DIM
        #self.char_attr = curses.A_BLINK

        #self.side_char = ' '
        #self.side_char_color = game.colors['white']
        #self.side_char_attr = curses.A_NORMAL

        self.name = 'terrain'

        self.damage = 0


    def doTick(self):
        pass


class Bush(Terrain):
    def __init__(self):
        super(Bush, self).__init__()

        self.blocks = True
        
        self.char = '#'

        self.color = game.colors['green']
        #self.color = game.colors['black_green']

        self.name = 'bush'

        #self.side_char = '$'

        self.side_char_color = self.color

        chars = ['#','#','#','#','#','#','#','#','#','#','#','#','#','#','#',
            '-','*','^','%','`']

        #self.char_z1_u1l2 = random.choice(chars) 
        self.char_z1_u1l2 = curses.ACS_ULCORNER
        #self.char_z1_u1l2_color = game.colors['green']
        #self.char_z1_u1l2_color = self.color
        self.char_z1_u1l2_color = game.colors['black_green']
        self.char_z1_u1l1 = random.choice(chars)
        #self.char_z1_u1l1_color = game.colors['green']
        #self.char_z1_u1l1_color = self.color
        self.char_z1_u1l1_color = game.colors['black_green']
        self.char_z1_u1 = random.choice(chars)
        #self.char_z1_u1_color = game.colors['green']
        #self.char_z1_u1_color = self.color
        self.char_z1_u1_color = game.colors['black_green']
        self.char_z1_u1r1 = random.choice(chars)
        #self.char_z1_u1r1_color = game.colors['green']
        #self.char_z1_u1r1_color = self.color
        self.char_z1_u1r1_color = game.colors['black_green']
        self.char_z1_u1r2 = random.choice(chars)
        #self.char_z1_u1r2_color = game.colors['green']
        #self.char_z1_u1r2_color = self.color
        self.char_z1_u1r2_color = game.colors['black_green']
        #self.char_z1_u1r3 = random.choice(chars)
        self.char_z1_u1r3 = curses.ACS_URCORNER
        #self.char_z1_u1r3_color = game.colors['green']
        #self.char_z1_u1r3_color = self.color
        self.char_z1_u1r3_color = game.colors['black_green']
        self.char_z1_l2 = random.choice(chars)
        #self.char_z1_l2_color = game.colors['green']
        #self.char_z1_l2_color = self.color
        self.char_z1_l2_color = game.colors['black_green']
        self.char_z1_l1 = random.choice(chars)
        #self.char_z1_l1_color = game.colors['green']
        #self.char_z1_l1_color = self.color
        self.char_z1_l1_color = game.colors['black_green']
        #self.char_z1_center = random.choice(chars)
        self.char_z1_center = 'b'
        #self.char_z1_center_color = game.colors['green']
        self.char_z1_center_color = self.color
        #self.char_z1_center_color = game.colors['black_green']
        self.char_z1_r1 = random.choice(chars)
        #self.char_z1_r1_color = game.colors['green']
        #self.char_z1_r1_color = self.color
        self.char_z1_r1_color = game.colors['black_green']
        self.char_z1_r2 = random.choice(chars)
        #self.char_z1_r2_color = game.colors['green']
        #self.char_z1_r2_color = self.color
        self.char_z1_r2_color = game.colors['black_green']
        self.char_z1_r3 = random.choice(chars)
        #self.char_z1_r3_color = game.colors['green']
        #self.char_z1_r3_color = self.color
        self.char_z1_r3_color = game.colors['black_green']
        #self.char_z1_d1l2 = random.choice(chars)
        self.char_z1_d1l2 = curses.ACS_LLCORNER
        #self.char_z1_d1l2_color = game.colors['green']
        #self.char_z1_d1l2_color = self.color
        self.char_z1_d1l2_color = game.colors['black_green']
        self.char_z1_d1l1 = random.choice(chars)
        #self.char_z1_d1l1_color = game.colors['green']
        #self.char_z1_d1l1_color = self.color
        self.char_z1_d1l1_color = game.colors['black_green']
        self.char_z1_d1 = random.choice(chars)
        #self.char_z1_d1_color = game.colors['green']
        #self.char_z1_d1_color = self.color
        self.char_z1_d1_color = game.colors['black_green']
        self.char_z1_d1r1 = random.choice(chars)
        #self.char_z1_d1r1_color = game.colors['green']
        #self.char_z1_d1r1_color = self.color
        self.char_z1_d1r1_color = game.colors['black_green']
        self.char_z1_d1r2 = random.choice(chars)
        #self.char_z1_d1r2_color = game.colors['green']
        #self.char_z1_d1r2_color = self.color
        self.char_z1_d1r2_color = game.colors['black_green']
        #self.char_z1_d1r3 = random.choice(chars)
        self.char_z1_d1r3 = curses.ACS_LRCORNER
        #self.char_z1_d1r3_color = game.colors['green']
        #self.char_z1_d1r3_color = self.color
        self.char_z1_d1r3_color = game.colors['black_green']


class Grass(Terrain):
    def __init__(self):
        super(Grass, self).__init__()

        self.blocks = False

        #self.char = ' '
        self.char = curses.ACS_CKBOARD
        #self.char = 'g'
        #self.char = '.'

        #self.color = game.colors['black_green']
        self.color = game.colors['green']

        self.name = 'grass'

        self.side_char = self.char
        self.side_char_color = self.color

        zoom_char = curses.ACS_CKBOARD

        #self.char_z1_u1l2 = curses.ACS_CKBOARD
        self.char_z1_u1l2 = zoom_char
        self.char_z1_u1l2_color = game.colors['green']
        #self.char_z1_u1l1 = curses.ACS_CKBOARD
        self.char_z1_u1l1 = zoom_char
        self.char_z1_u1l1_color = game.colors['green']
        #self.char_z1_u1 = curses.ACS_CKBOARD
        self.char_z1_u1 = zoom_char
        self.char_z1_u1_color = game.colors['green']
        #self.char_z1_u1r1 = curses.ACS_CKBOARD
        self.char_z1_u1r1 = zoom_char
        self.char_z1_u1r1_color = game.colors['green']
        #self.char_z1_u1r2 = curses.ACS_CKBOARD
        self.char_z1_u1r2 = zoom_char
        self.char_z1_u1r2_color = game.colors['green']
        #self.char_z1_u1r3 = curses.ACS_CKBOARD
        self.char_z1_u1r3 = zoom_char
        self.char_z1_u1r3_color = game.colors['green']
        #self.char_z1_l2 = curses.ACS_CKBOARD
        self.char_z1_l2 = zoom_char
        self.char_z1_l2_color = game.colors['green']
        #self.char_z1_l1 = curses.ACS_CKBOARD
        self.char_z1_l1 = zoom_char
        self.char_z1_l1_color = game.colors['green']
        #self.char_z1_center = curses.ACS_CKBOARD
        self.char_z1_center = zoom_char
        self.char_z1_center_color = game.colors['green']
        #self.char_z1_center = 'g'
        #self.char_z1_r1 = curses.ACS_CKBOARD
        self.char_z1_r1 = zoom_char
        self.char_z1_r1_color = game.colors['green']
        #self.char_z1_r2 = curses.ACS_CKBOARD
        self.char_z1_r2 = zoom_char
        self.char_z1_r2_color = game.colors['green']
        #self.char_z1_r3 = curses.ACS_CKBOARD
        self.char_z1_r3 = zoom_char
        self.char_z1_r3_color = game.colors['green']
        #self.char_z1_d1l2 = curses.ACS_CKBOARD
        self.char_z1_d1l2 = zoom_char
        self.char_z1_d1l2_color = game.colors['green']
        #self.char_z1_d1l1 = curses.ACS_CKBOARD
        self.char_z1_d1l1 = zoom_char
        self.char_z1_d1l1_color = game.colors['green']
        #self.char_z1_d1 = curses.ACS_CKBOARD
        self.char_z1_d1 = zoom_char
        self.char_z1_d1_color = game.colors['green']
        #self.char_z1_d1r1 = curses.ACS_CKBOARD
        self.char_z1_d1r1 = zoom_char
        self.char_z1_d1r1_color = game.colors['green']
        #self.char_z1_d1r2 = curses.ACS_CKBOARD
        self.char_z1_d1r2 = zoom_char
        self.char_z1_d1r2_color = game.colors['green']
        #self.char_z1_d1r3 = curses.ACS_CKBOARD
        self.char_z1_d1r3 = zoom_char
        self.char_z1_d1r3_color = game.colors['green']


        self.char_z2_u3l7 = curses.ACS_CKBOARD
        self.char_z2_u3l7_color = game.colors['green']
        self.char_z2_u3l6 = curses.ACS_CKBOARD
        self.char_z2_u3l6_color = game.colors['green']
        self.char_z2_u3l5 = curses.ACS_CKBOARD
        self.char_z2_u3l5_color = game.colors['green']
        self.char_z2_u3l4 = curses.ACS_CKBOARD
        self.char_z2_u3l4_color = game.colors['green']
        self.char_z2_u3l3 = curses.ACS_CKBOARD
        self.char_z2_u3l3_color = game.colors['green']
        self.char_z2_u3l2 = curses.ACS_CKBOARD
        self.char_z2_u3l2_color = game.colors['green']
        self.char_z2_u3l1 = curses.ACS_CKBOARD
        self.char_z2_u3l1_color = game.colors['green']
        self.char_z2_u3 = curses.ACS_CKBOARD
        self.char_z2_u3_color = game.colors['green']
        self.char_z2_u3r1 = curses.ACS_CKBOARD
        self.char_z2_u3r1_color = game.colors['green']
        self.char_z2_u3r2 = curses.ACS_CKBOARD
        self.char_z2_u3r2_color = game.colors['green']
        self.char_z2_u3r3 = curses.ACS_CKBOARD
        self.char_z2_u3r3_color = game.colors['green']
        self.char_z2_u3r4 = curses.ACS_CKBOARD
        self.char_z2_u3r4_color = game.colors['green']
        self.char_z2_u3r5 = curses.ACS_CKBOARD
        self.char_z2_u3r5_color = game.colors['green']
        self.char_z2_u3r6 = curses.ACS_CKBOARD
        self.char_z2_u3r6_color = game.colors['green']
        self.char_z2_u3r7 = curses.ACS_CKBOARD
        self.char_z2_u3r7_color = game.colors['green']
        self.char_z2_u2l7 = curses.ACS_CKBOARD
        self.char_z2_u2l7_color = game.colors['green']
        self.char_z2_u2l6 = curses.ACS_CKBOARD
        self.char_z2_u2l6_color = game.colors['green']
        self.char_z2_u2l5 = curses.ACS_CKBOARD
        self.char_z2_u2l5_color = game.colors['green']
        self.char_z2_u2l4 = curses.ACS_CKBOARD
        self.char_z2_u2l4_color = game.colors['green']
        self.char_z2_u2l3 = curses.ACS_CKBOARD
        self.char_z2_u2l3_color = game.colors['green']
        self.char_z2_u2l2 = curses.ACS_CKBOARD
        self.char_z2_u2l2_color = game.colors['green']
        self.char_z2_u2l1 = curses.ACS_CKBOARD
        self.char_z2_u2l1_color = game.colors['green']
        self.char_z2_u2 = curses.ACS_CKBOARD
        self.char_z2_u2_color = game.colors['green']
        self.char_z2_u2r1 = curses.ACS_CKBOARD
        self.char_z2_u2r1_color = game.colors['green']
        self.char_z2_u2r2 = curses.ACS_CKBOARD
        self.char_z2_u2r2_color = game.colors['green']
        self.char_z2_u2r3 = curses.ACS_CKBOARD
        self.char_z2_u2r3_color = game.colors['green']
        self.char_z2_u2r4 = curses.ACS_CKBOARD
        self.char_z2_u2r4_color = game.colors['green']
        self.char_z2_u2r5 = curses.ACS_CKBOARD
        self.char_z2_u2r5_color = game.colors['green']
        self.char_z2_u2r6 = curses.ACS_CKBOARD
        self.char_z2_u2r6_color = game.colors['green']
        self.char_z2_u2r7 = curses.ACS_CKBOARD
        self.char_z2_u2r7_color = game.colors['green']
        self.char_z2_u1l7 = curses.ACS_CKBOARD
        self.char_z2_u1l7_color = game.colors['green']
        self.char_z2_u1l6 = curses.ACS_CKBOARD
        self.char_z2_u1l6_color = game.colors['green']
        self.char_z2_u1l5 = curses.ACS_CKBOARD
        self.char_z2_u1l5_color = game.colors['green']
        self.char_z2_u1l4 = curses.ACS_CKBOARD
        self.char_z2_u1l4_color = game.colors['green']
        self.char_z2_u1l3 = curses.ACS_CKBOARD
        self.char_z2_u1l3_color = game.colors['green']
        self.char_z2_u1l2 = curses.ACS_CKBOARD
        self.char_z2_u1l2_color = game.colors['green']
        self.char_z2_u1l1 = curses.ACS_CKBOARD
        self.char_z2_u1l1_color = game.colors['green']
        self.char_z2_u1 = curses.ACS_CKBOARD
        self.char_z2_u1_color = game.colors['green']
        self.char_z2_u1r1 = curses.ACS_CKBOARD
        self.char_z2_u1r1_color = game.colors['green']
        self.char_z2_u1r2 = curses.ACS_CKBOARD
        self.char_z2_u1r2_color = game.colors['green']
        self.char_z2_u1r3 = curses.ACS_CKBOARD
        self.char_z2_u1r3_color = game.colors['green']
        self.char_z2_u1r4 = curses.ACS_CKBOARD
        self.char_z2_u1r4_color = game.colors['green']
        self.char_z2_u1r5 = curses.ACS_CKBOARD
        self.char_z2_u1r5_color = game.colors['green']
        self.char_z2_u1r6 = curses.ACS_CKBOARD
        self.char_z2_u1r6_color = game.colors['green']
        self.char_z2_u1r7 = curses.ACS_CKBOARD
        self.char_z2_u1r7_color = game.colors['green']
        self.char_z2_l7 = curses.ACS_CKBOARD
        self.char_z2_l7_color = game.colors['green']
        self.char_z2_l6 = curses.ACS_CKBOARD
        self.char_z2_l6_color = game.colors['green']
        self.char_z2_l5 = curses.ACS_CKBOARD
        self.char_z2_l5_color = game.colors['green']
        self.char_z2_l4 = curses.ACS_CKBOARD
        self.char_z2_l4_color = game.colors['green']
        self.char_z2_l3 = curses.ACS_CKBOARD
        self.char_z2_l3_color = game.colors['green']
        self.char_z2_l2 = curses.ACS_CKBOARD
        self.char_z2_l2_color = game.colors['green']
        self.char_z2_l1 = curses.ACS_CKBOARD
        self.char_z2_l1_color = game.colors['green']
        self.char_z2_center = curses.ACS_CKBOARD
        self.char_z2_center_color = game.colors['green']
        self.char_z2_r1 = curses.ACS_CKBOARD
        self.char_z2_r1_color = game.colors['green']
        self.char_z2_r2 = curses.ACS_CKBOARD
        self.char_z2_r2_color = game.colors['green']
        self.char_z2_r3 = curses.ACS_CKBOARD
        self.char_z2_r3_color = game.colors['green']
        self.char_z2_r4 = curses.ACS_CKBOARD
        self.char_z2_r4_color = game.colors['green']
        self.char_z2_r5 = curses.ACS_CKBOARD
        self.char_z2_r5_color = game.colors['green']
        self.char_z2_r6 = curses.ACS_CKBOARD
        self.char_z2_r6_color = game.colors['green']
        self.char_z2_r7 = curses.ACS_CKBOARD
        self.char_z2_r7_color = game.colors['green']
        self.char_z2_d1l7 = curses.ACS_CKBOARD
        self.char_z2_d1l7_color = game.colors['green']
        self.char_z2_d1l6 = curses.ACS_CKBOARD
        self.char_z2_d1l6_color = game.colors['green']
        self.char_z2_d1l5 = curses.ACS_CKBOARD
        self.char_z2_d1l5_color = game.colors['green']
        self.char_z2_d1l4 = curses.ACS_CKBOARD
        self.char_z2_d1l4_color = game.colors['green']
        self.char_z2_d1l3 = curses.ACS_CKBOARD
        self.char_z2_d1l3_color = game.colors['green']
        self.char_z2_d1l2 = curses.ACS_CKBOARD
        self.char_z2_d1l2_color = game.colors['green']
        self.char_z2_d1l1 = curses.ACS_CKBOARD
        self.char_z2_d1l1_color = game.colors['green']
        self.char_z2_d1 = curses.ACS_CKBOARD
        self.char_z2_d1_color = game.colors['green']
        self.char_z2_d1r1 = curses.ACS_CKBOARD
        self.char_z2_d1r1_color = game.colors['green']
        self.char_z2_d1r2 = curses.ACS_CKBOARD
        self.char_z2_d1r2_color = game.colors['green']
        self.char_z2_d1r3 = curses.ACS_CKBOARD
        self.char_z2_d1r3_color = game.colors['green']
        self.char_z2_d1r4 = curses.ACS_CKBOARD
        self.char_z2_d1r4_color = game.colors['green']
        self.char_z2_d1r5 = curses.ACS_CKBOARD
        self.char_z2_d1r5_color = game.colors['green']
        self.char_z2_d1r6 = curses.ACS_CKBOARD
        self.char_z2_d1r6_color = game.colors['green']
        self.char_z2_d1r7 = curses.ACS_CKBOARD
        self.char_z2_d1r7_color = game.colors['green']
        self.char_z2_d2l7 = curses.ACS_CKBOARD
        self.char_z2_d2l7_color = game.colors['green']
        self.char_z2_d2l6 = curses.ACS_CKBOARD
        self.char_z2_d2l6_color = game.colors['green']
        self.char_z2_d2l5 = curses.ACS_CKBOARD
        self.char_z2_d2l5_color = game.colors['green']
        self.char_z2_d2l4 = curses.ACS_CKBOARD
        self.char_z2_d2l4_color = game.colors['green']
        self.char_z2_d2l3 = curses.ACS_CKBOARD
        self.char_z2_d2l3_color = game.colors['green']
        self.char_z2_d2l2 = curses.ACS_CKBOARD
        self.char_z2_d2l2_color = game.colors['green']
        self.char_z2_d2l1 = curses.ACS_CKBOARD
        self.char_z2_d2l1_color = game.colors['green']
        self.char_z2_d2 = curses.ACS_CKBOARD
        self.char_z2_d2_color = game.colors['green']
        self.char_z2_d2r1 = curses.ACS_CKBOARD
        self.char_z2_d2r1_color = game.colors['green']
        self.char_z2_d2r2 = curses.ACS_CKBOARD
        self.char_z2_d2r2_color = game.colors['green']
        self.char_z2_d2r3 = curses.ACS_CKBOARD
        self.char_z2_d2r3_color = game.colors['green']
        self.char_z2_d2r4 = curses.ACS_CKBOARD
        self.char_z2_d2r4_color = game.colors['green']
        self.char_z2_d2r5 = curses.ACS_CKBOARD
        self.char_z2_d2r5_color = game.colors['green']
        self.char_z2_d2r6 = curses.ACS_CKBOARD
        self.char_z2_d2r6_color = game.colors['green']
        self.char_z2_d2r7 = curses.ACS_CKBOARD
        self.char_z2_d2r7_color = game.colors['green']



class Lava(Terrain):
    def __init__(self):
        #self,
        #y,
        #x):
        super(Lava, self).__init__()
            #y=y,
            #x=x)

        self.blocks = False

        self.char = ' '
        #self.char = curses.ACS_CKBOARD

        self.color = game.colors['black_red']
        #self.color = game.colors['red']

        self.name = 'lava'

        self.damage = int(1)

        self.side_char = self.char

        self.side_char_color = self.color

        self.side_char_attr = self.char_attr


    def doTick(self):
        game.logger.debug('TEST6')
        space = game.getSpace(
            y = self.y,
            x = self.x)

        for thing in space.contents:
            game.logger.debug('TEST6 thing is <%s>',
                str(thing.name))
            game.logger.debug('TEST6 self is <%s> with damage <%s>',
                str(self.name), str(self.damage))
            if isinstance(thing, Actor):
                if not thing.corpse:
                    thing.resolveDamage(self, self.damage)


class Sand(Terrain):
    def __init__(self):
        super(Sand, self).__init__()

        self.blocks = False

        #self.char = ' '
        self.char = curses.ACS_CKBOARD

        #self.color = game.colors['black_yellow']
        self.color = game.colors['yellow']

        self.name = 'sand'

        self.side_char = self.char
        
        self.side_char_color = self.color

        self.side_char_attr = self.char_attr

        #chars = [curses.ACS_CKBOARD, '~', '.', '-']
        chars = [curses.ACS_CKBOARD,curses.ACS_CKBOARD,curses.ACS_CKBOARD,
            curses.ACS_CKBOARD,curses.ACS_CKBOARD,curses.ACS_CKBOARD,
            curses.ACS_CKBOARD,curses.ACS_CKBOARD,curses.ACS_CKBOARD,
            '~']

        self.char_z1_u1l2 = random.choice(chars) 
        self.char_z1_u1l2_color = game.colors['yellow']
        self.char_z1_u1l1 = random.choice(chars)
        self.char_z1_u1l1_color = game.colors['yellow']
        self.char_z1_u1 = random.choice(chars)
        self.char_z1_u1_color = game.colors['yellow']
        self.char_z1_u1r1 = random.choice(chars)
        self.char_z1_u1r1_color = game.colors['yellow']
        self.char_z1_u1r2 = random.choice(chars)
        self.char_z1_u1r2_color = game.colors['yellow']
        self.char_z1_u1r3 = random.choice(chars)
        self.char_z1_u1r3_color = game.colors['yellow']
        self.char_z1_l2 = random.choice(chars)
        self.char_z1_l2_color = game.colors['yellow']
        self.char_z1_l1 = random.choice(chars)
        self.char_z1_l1_color = game.colors['yellow']
        self.char_z1_center = random.choice(chars)
        self.char_z1_center_color = game.colors['yellow']
        self.char_z1_r1 = random.choice(chars)
        self.char_z1_r1_color = game.colors['yellow']
        self.char_z1_r2 = random.choice(chars)
        self.char_z1_r2_color = game.colors['yellow']
        self.char_z1_r3 = random.choice(chars)
        self.char_z1_r3_color = game.colors['yellow']
        self.char_z1_d1l2 = random.choice(chars)
        self.char_z1_d1l2_color = game.colors['yellow']
        self.char_z1_d1l1 = random.choice(chars)
        self.char_z1_d1l1_color = game.colors['yellow']
        self.char_z1_d1 = random.choice(chars)
        self.char_z1_d1_color = game.colors['yellow']
        self.char_z1_d1r1 = random.choice(chars)
        self.char_z1_d1r1_color = game.colors['yellow']
        self.char_z1_d1r2 = random.choice(chars)
        self.char_z1_d1r2_color = game.colors['yellow']
        self.char_z1_d1r3 = random.choice(chars)
        self.char_z1_d1r3_color = game.colors['yellow']
        

class Stone(Terrain):
    def __init__(self):
        super(Stone, self).__init__()
       
        self.blocks = False

        #self.char = ' '
        self.char = curses.ACS_CKBOARD

        #self.color = game.colors['black_white']
        self.color = game.colors['white']

        self.name = 'stone'

        self.side_char = self.char

        self.side_char_color = self.color

        self.side_char_attr = self.char_attr


class Water(Terrain):
    def __init__(self):
        super(Water, self).__init__()

        self.blocks = True

        self.char = '~'
        #self.char = str(' ')
        #self.char = curses.ACS_CKBOARD
        #self.char = curses.ACS_DIAMOND

        #self.color = game.colors['blue']
        self.color = game.colors['black_blue']

        self.name = 'water'

        self.side_char = self.char
        self.side_char_color = self.color

        self.char_z1_u1l2 = '~'
        self.char_z1_u1l2_color = game.colors['blue']
        self.char_z1_u1l1 = '~'
        self.char_z1_u1l1_color = game.colors['blue']
        self.char_z1_u1 = '~'
        self.char_z1_u1_color = game.colors['blue']
        self.char_z1_u1r1 = '~'
        self.char_z1_u1r1_color = game.colors['blue']
        self.char_z1_u1r2 = '~'
        self.char_z1_u1r2_color = game.colors['blue']
        self.char_z1_u1r3 = '~'
        self.char_z1_u1r3_color = game.colors['blue']
        self.char_z1_l2 = '~'
        self.char_z1_l2_color = game.colors['blue']
        self.char_z1_l1 = '~'
        self.char_z1_l1_color = game.colors['blue']
        self.char_z1_center = '~'
        self.char_z1_center_color = game.colors['blue']
        self.char_z1_r1 = '~'
        self.char_z1_r1_color = game.colors['blue']
        self.char_z1_r2 = '~'
        self.char_z1_r2_color = game.colors['blue']
        self.char_z1_r3 = '~'
        self.char_z1_r3_color = game.colors['blue']
        self.char_z1_d1l2 = '~'
        self.char_z1_d1l2_color = game.colors['blue']
        self.char_z1_d1l1 = '~'
        self.char_z1_d1l1_color = game.colors['blue']
        self.char_z1_d1 = '~'
        self.char_z1_d1_color = game.colors['blue']
        self.char_z1_d1r1 = '~'
        self.char_z1_d1r1_color = game.colors['blue']
        self.char_z1_d1r2 = '~'
        self.char_z1_d1r2_color = game.colors['blue']
        self.char_z1_d1r3 = '~'
        self.char_z1_d1r3_color = game.colors['blue']

class Item(Thing):
    def __init__(
        self):
        super(Item, self).__init__()

        self.name = 'item'

        self.blocks = False

        self.char = 'i'
        self.color = game.colors['white']

        self.side_char = '?'
        self.side_char_color = self.color


class Equipment(Item):
    def __init__(
        self):
        super(Equipment, self).__init__()

        self.name = 'equipment'

        self.side_char = 'e'

        self.usable_slots = None

        self.equipped = False

#class Dagger(Item):
class Dagger(Equipment):
    def __init__(
        self):
        super(Dagger, self).__init__()

        self.name = 'dagger'

        self.char = 'i'
        self.color = game.colors['white']

        self.side_char = 'd'
        self.side_char_color = self.color

        self.usable_slots = [
            'hand'
            ]

        self.char_z1_u1l2 = curses.ACS_ULCORNER
        self.char_z1_u1r3 = curses.ACS_URCORNER
        self.char_z1_center = '-'
        self.char_z1_d1 = 'k'
        self.char_z1_d1l2 = curses.ACS_LLCORNER
        self.char_z1_d1r3 = curses.ACS_LRCORNER

        self.skill = 'dagger'


class Kris(Dagger):
    def __init__(
        self):
        super(Kris, self).__init__()
    
        self.name = 'kris'
        self.side_char = '-'
        self.damage = 5

        #self.equip_slots = [
        #    'hand'
        #    ]


#class Ring(Item):
#    def __init__(
#        self):

#        self.enchantment = enchantment
#        if self.enchantment is not None:
#            self.enchantment.owner = self


class Actor(Thing):
    def __init__(self):
        #self,
        #y,              # passed to super (Thing)
        #x):              # passed to super (Thing)
        super(Actor, self).__init__()
            #y=y,
            #x=x)

        # attributes
        #self.vitality = ((int(1), int(0)))
        #self.dexterity = ((int(1), int(0)))
        self.dexterity = 1
        self.strength = 1
        self.vitality = 1

        self.dexterity_exp = 0
        self.strength_exp = 0
        self.vitality_exp = 0

        # skills
        #self.unarmed = ((int(0), int(0)))
        self.unarmed = 0
        self.dagger = 0

        self.unarmed_exp = 0
        self.dagger_exp = 0

        #self.attributes = {
        #    'vitality'  :   ( int(1),    int(0) ),
        #    'dexterity' :   ( int(1),   int(0) )
        #    }

        self.experience = int(0)

        self.exp_reward = 1

        self.name = 'actor'
           
        self.sex = 'male'

        #self.skills = {
        #    'unarmed'   :   ( int(0),   int(0) )
        #    }

        self.gold = 0

        self.logic = Simpleton()
        self.logic.owner = self

        self.corpse = None

        #self.equip_slots = None

        #self.hand = None

        self.hand = HumanoidHand()

        self.equipped = []

        self.exp_modifier = float(1.0)

        self.hp = 1

        self.gold = 0

        #TODO: is this necessary?
        #self.player = None
        #game.logger.debug('<%s>_<%s> is player', 
        #    str(self.name), str(self.serial))
        #if self.player:
        #    self.player.owner = self

        self.inventory = [] # init inventory as emtpy list

        self.side_char = '_'
        #self.side_char_color = self.color
        #self.side_char_attr = self.char_attr

        #self.dex_modifier = int(1)
        #self.str_modifier = int(1)
        #self.vit_hp_modifier = int(1)
 

        #self.char_z1_u1l2 = curses.ACS_ULCORNER
        self.char_z1_u1l3 = curses.ACS_ULCORNER
        #self.char_z1_u1l2_color = game.colors['white']
        self.char_z1_u1l3_color = game.colors['white']
        #self.char_z1_u1l2_color = game.colors['blue']
        #self.char_z1_u1l1 = '.'
        #self.char_z1_u1 = '.'
        #self.char_z1_u1r1 = '.'
        #self.char_z1_u1r2 = '.'
        #self.char_z1_u1r3 = '.'
        self.char_z1_u1r3 = curses.ACS_URCORNER
        self.char_z1_u1r3_color = game.colors['white']
        #self.char_z1_l2 = '.'
        #self.char_z1_l1 = '.'
        #self.char_z1_r1 = '.'
        #self.char_z1_r2 = '.'
        #self.char_z1_r3 = '.'
        #self.char_z1_d1l2 = '.'
        #self.char_z1_d1l2 = curses.ACS_LLCORNER
        self.char_z1_d1l3 = curses.ACS_LLCORNER
        #self.char_z1_d1l2_color = game.colors['white']
        self.char_z1_d1l3_color = game.colors['white']
        #self.char_z1_d1l1 = '.'
        #self.char_z1_d1 = '.'
        #self.char_z1_d1r1 = '.'
        #self.char_z1_d1r2 = '.'
        #self.char_z1_d1r3 = '.'
        self.char_z1_d1r3 = curses.ACS_LRCORNER
        self.char_z1_d1r3_color = game.colors['white']


    @property
    def primary_weapon(self):
        return self.hand.equipped
    

    @property
    def max_hp(self):
        #return int(10)
        #max_hp = int(self.attributes['vitality'][0] * self.vit_hp_modifier)
        #max_hp = int(self.vitality[0] * self.vit_hp_modifier)
        max_hp = int(self.vitality * 5)
        return int(max_hp)


    def initSkills(self, attr_points, skill_points):
        #for point in attr_points:
        for point in range(attr_points):
        #for (attr_points):
            attribute = random.choice([
                'dexterity',
                'strength',
                'vitality'
                ])
            setattr(self, attribute, getattr(self, attribute) + 1)

        #for point in skill_points:
        for point in range(skill_points):
            skill = random.choice([
                'unarmed'
                ])
            setattr(self, skill, getattr(self, skill) + 1)


    def equip(self, item):

        #item_slots = []
        #equip_slots = []

        #if any(slot in self.equip_slots for slot in item.usable_slots):
        for item_slot in item.usable_slots:
            #item_slots.append(slot)
            #for equip_slot in self.equip_slots:
            if getattr(self, item_slot) is not None:
                if getattr(self, item_slot).can_equip:
                    setattr(getattr(self, item_slot), 'equipped', item)
                    item.equipped = True
                    self.equipped.append(item)
       

            #self.equipped.append(item) 
            #item.equipped = True


    def pickUp(self, target=None):
        space = game.getSpace(self.y, self.x)
        game.logger.critical('TEST22')

        item = None
        for thing in space.contents:
            game.logger.critical('testing <%s>_<%s> for pickup',
                str(thing.name), str(thing.serial))
            if target:
                game.logger.critical('TEST24')
                if thing.name == str(target):
                    item = thing
            elif isinstance(thing, Item):
            #elif isinstance(self, Kris):
                    game.logger.critical('TEST21')
                    item = thing
        
        if item:
            game.logger.critical('TEST23')
            self.inventory.append(item)
            space.contents.remove(item)


    def skillUp(self,
        skill,
        value=1):

        game.logger.critical('TEST35: skill <%s', str(skill))

        #skill = getattr(self, skill)[0]
        #skill = getattr(self, skill)

        skill_exp = str(skill + '_exp')
        
        #self.skills[skill][0] = int(self.skills[skill][0]) + value
        #self.skills[skill][0] = int(self.skills[skill][0]) + value
        #getattr(self, skill)[0] += value
        #skill[0] = skill + value
        #getattr(self, skill) = getattr(self,skill) + value
        setattr(self, skill_exp, getattr(self,skill_exp) + value)

        while getattr(self, skill_exp) >= 100:
            setattr(self, skill, getattr(self, skill) + 1)
            message = str(str(self.name) 
                + ' ' + str(skill) 
                + ' skill increased by ' + str(value) +
                #' to ' + str(self.skills[skill][0]))
                ' to ' + str(getattr(self, skill)))
            game.writeMessage(message)
            setattr(self, skill_exp, getattr(self, skill_exp) - 100)

        game.logger.critical('<%s>_<%s> <%s> is <%s> + <%s>/100',
            str(self.name), str(self.serial), str(skill),
            str(getattr(self, skill)), str(getattr(self, skill_exp)))

        

    #def newattack(self,
    #    target,
    #    damage


    def attack(self, 
        target,
        skill='unarmed'):

        #TODO: this should be tweaked, maybe my species values or weapons used

        if not isinstance(target, Actor):
            game.logger.warning('tried attacking non-Actor <%s>, <%s>',
                str(target.name), str(target.serial))

        if self.primary_weapon:
            game.logger.critical('TEST35: primary weapon is <%s>',
                str(self.primary_weapon))
            skill = self.primary_weapon.skill


        #TODO: these should be declared elsewhere
        hit_chance_constant = 100
        dodge_chance_constant = 100

        

        game.logger.critical('<%s>_<%s>\'s dexterity is <%s>', 
            str(self.name), str(self.serial), 
            str(self.dexterity))
        game.logger.critical('<%s>_<%s>\'s unarmed skill is <%s>',
            str(self.name), str(self.serial),
            #str(self.unarmed))  
            str(getattr(self, skill)))
        atk_accuracy = int((self.dexterity * 2) 
            #+ (self.unarmed * 2))
            + (getattr(self, skill) * 2))

        game.logger.critical('<%s>_<%s> attack accuracy is <%s>',
            str(self.name), str(self.serial), str(atk_accuracy))

        hit_value = int((atk_accuracy / (atk_accuracy + hit_chance_constant) * 100))

        game.logger.critical('<%s>_<%s> hit chance is <%s>',
            str(self.name), str(self.serial), str(hit_value))

        diceroll = random.randint(1, 100) #TODO: should this be 0-99?

        game.logger.critical('diceroll is <%s>', str(diceroll))

        # if the hit misses
        if hit_value < diceroll:

            message = str(self.name) + ' misses ' + str(target.name) + '!'
            highlights = {}
            self_name = self.name.split()
            target_name = target.name.split()
            for word in self_name:
                highlights[word] = game.colors['red']
                highlights[word] = game.colors['magenta']
            for word in target_name:
                #highlights[word] = game.colors['red']
                highlights[word] = game.colors['magenta']
            game.writeMessage(message, highlights)
            return

        # if the hit hits
        elif hit_value >= diceroll:

            #dodge_chance = int((target.attributes['dexterity'][0]
            #dodge_chance = int((target.dexterity[0]
            dodge_chance = int((target.dexterity
                #+ (target.skills['unarmed'][0] / 2)))
                #+ (target.unarmed[0] / 2)))
                #+ (target.unarmed / 2)))
                + (getattr(target, skill) / 2)))
            
            diceroll = random.randint(1, 100) #TODO: should this be 0-99?
        
            # if target dodges
            if dodge_chance >= diceroll:

                message = str(str(self.name) + ' dodges ' + str(target.name)
                    + '\'s attack!')
                highlights = {}
                self_name = self.name.split()
                target_name = target.name.split()
                for word in target_name:
                    #highlights[word] = game.colors['red']
                    highlights[word] = game.colors['magenta']
                for word in self_name:
                    #highlights[word] = game.colors['red']
                    highlights[word] = game.colors['magenta']
                #game.writeMessage(message, highlights)
                game.writeMessage(message, highlights)
                return

            # if target fails to dodge
            elif dodge_chance < diceroll:
            
                #self.skillUp('unarmed', 10)
                self.skillUp(skill, 10)


                #if isinstance(target, Hero):
                #    color = game.colors['red']
                #else:
                #    color = game.colors['magenta']
                message = str(self.name) + ' hits ' + str(target.name) + '!'
                game.writeMessage(message)
                    #color=game.colors['red'])
                    #color=color)
                
                #damage = 1
                damage = (self.strength)
                #self.strength += 1
                self.skillUp('strength', 1)

                #TODO: readd this functionality back in
                #elif ('incorpreal' in target.actor.traits or
                #    'incorpreal' in self.traits and
                #    not 'corporeal attack' in self.traits):
                #    damage = 0
                ##target.actor.receiveDamage(damage)
                #target.receiveDamage(damage)
                target.resolveDamage(self, damage)
                #target.actor.hp -= 1


    def resolveDamage(self, attacker, damage):
        if not isinstance(self, Actor):
            game.logger.debug('TEST7:!!!')
            return
        else:
            
            self.hp -= damage

            if self.hp <= 0:

                self.die(attacker)
    

    def die(self,
        killer=None):
        
        if killer is None:
            message = str(self.name) + ' dies!'
        #elif killer == hero:
        else:
            message = str(str(self.name)
                + ' killed by ' + str(killer.name))

            if isinstance(killer, Actor):

                killer.experience += self.exp_reward 

        game.writeMessage(message,
            #attribute = curses.A_BOLD)    
            attribute = curses.A_REVERSE)    
            #attribute = curses.A_ITALIC)    
            #attribute = curses.A_STANDOUT)    

        #if self.player:
        #    game.gameOver()

        if isinstance(self, Hero):
            game.gameOver()

        self.corpse = Corpse()
        self.takeOwnership(self.corpse)


    def changeGold(self, amount):
        if self.gold < 0:
            self.gold -= amount
        else:
            self.gold += amount


    def takeOwnership(self, target):
        target.owner = self


    def move(self,
        y_diff,
        x_diff):
        """
        generic move function
        """
        #TODO: rename or remove this once specific movement is in place
        #TODO: add blocking

        #if self.player:
        if isinstance(self, Hero):
            game.logger.debug('<%s> moving <%s> (y) and <%s> (x)',
                str(self.name), str(y_diff), str(x_diff))
            #game.logger.critical('player at <%s>,<%s> is moving',
            #    str(self.y), str(self.x))

        x_diff = x_diff * 2       
 
        old_y = self.y 
        old_x = self.x
        new_y = self.y + y_diff
        new_x = self.x + x_diff

        #TODO this needs work!
        blocked = False
        target = None
        for thing in game.things:
            if thing.y == new_y and thing.x == new_x:
                if thing.blocks:
                    blocked = True
                if isinstance(thing, Actor):
                    if thing.corpse:
                        thing.corpse.interact(self)
                    else:
                        target = thing

        if blocked:
            if target is not None:
                self.attack(target)
            #if self.player:
            if isinstance(self, Hero):
                game.logger.info('player movement blocked!')
            else:
                game.logger.debug('<%s> movement blocked!',
                    str(self.name))
        else:
            self.y = new_y
            self.x = new_x

            old_location = str(str(old_y) + '_' + str(old_x))
            new_location = str(str(new_y) + '_' + str(new_x))
            game.logger.debug('old_location: <%s>, new_location: <%s>',
                str(old_location), str(new_location))

            game.logger.debug('old_location contents type: <%s>',
                str(type(board.spaces[old_location].contents)))
            
            if game.logger.getEffectiveLevel() == 10:
                stuff = []
                for thing in board.spaces[old_location].contents:
                    game.logger.debug('thing.name = <%s>', str(thing.name))
                    stuff.append(thing.name)
                game.logger.debug('old_location old contents: ' +
                    ', '.join(stuff))
            
            board.spaces[old_location].contents.remove(self)
            
            if game.logger.getEffectiveLevel() == 10:
                for thing in board.spaces[old_location].contents:
                    stuff.append(thing.name)
                game.logger.debug('old_location new contents: <%s>',
                    ', '.join(stuff))

            if game.logger.getEffectiveLevel() == 10:
                for thing in board.spaces[new_location].contents:
                    stuff.append(thing.name)
                game.logger.debug('new_location old contents: <%s>',
                    ', '.join(stuff))

            board.spaces[new_location].contents.append(self)

            if game.logger.getEffectiveLevel() == 10:
                for thing in board.spaces[new_location].contents:
                    stuff.append(thing.name)
                game.logger.debug('new_location new contents: <%s>',
                ', '.join(stuff))
                        

            #board.drawSpace(old_y, old_x)
            #board.drawSpace(new_y, new_x)


    def applyDamage( 
        self,
        target,
        damage):
        #TODO: add docstring

        target.hp -= damage


    def restoreAll(self):
        self.hp = self.max_hp   


class Wildlife(object):
    def __init__(self):
        
        #self.color = game.colors['green']
        self.color = game.colors['red']
        self.char_attr = curses.A_BOLD

        self.char_z2_center_color = self.color


class Beast(Actor):
    def __init__(self):
        #self,
        #y,
        #x):
        super(Beast, self).__init__()
            #y=y,
            #x=x)

        #self.char_z1_u1l2_color = game.colors['red']
        self.char_z1_u1l3_color = game.colors['white']
        #self.char_z1_u1l2_color = game.colors['white']
        self.char_z1_u1l2_color = game.colors['red']
        self.char_z1_u1l1_color = game.colors['red']
        self.char_z1_u1_color = game.colors['red']
        self.char_z1_u1r1_color = game.colors['red']
        self.char_z1_u1r2_color = game.colors['red']
        #self.char_z1_u1r3_color = game.colors['red']
        self.char_z1_u1r3_color = game.colors['white']
        self.char_z1_l3_color = game.colors['red']
        self.char_z1_l2_color = game.colors['red']
        self.char_z1_l1_color = game.colors['red']
        self.char_z1_center_color = game.colors['red']
        self.char_z1_r1_color = game.colors['red']
        self.char_z1_r2_color = game.colors['red']
        self.char_z1_r3_color = game.colors['red']
        #self.char_z1_d1l2_color = game.colors['red']
        self.char_z1_d1l3_color = game.colors['white']
        #self.char_z1_d1l2_color = game.colors['white']
        self.char_z1_d1l2_color = game.colors['red']
        self.char_z1_d1l1_color = game.colors['red']
        self.char_z1_d1_color = game.colors['red']
        self.char_z1_d1r1_color = game.colors['red']
        self.char_z1_d1r2_color = game.colors['red']
        #self.char_z1_d1r3_color = game.colors['red']
        self.char_z1_d1r3_color = game.colors['white']

        pass


class HumanoidHand(object):
    def __init__(self):

        self.can_equip = True

        self.equipped = None


class Humanoid(Actor):
    def __init__(self):
        #self,
        #y,              # passed to super (Actor->Thing)
        #x):              # passed to super (Actor->Thing)
        super(Humanoid, self).__init__()
            #y=y,
            #x=x)


        #self.equip_slots = [
        #    'hand'
        #    ]

        self.hand = HumanoidHand()

        # human baselines
        #self.vitality = 10
        #self.dexterity = 10
        #self.strength = 10

        #self.unarmed = 0

 
    def attack(self, target):

        if not isinstance(target, Actor):
            return


        if not self.primary_weapon:

            damage = int(self.strength)
            
            accuracy_constant = 100
            accuracy = int((self.dexterity * 2) + (self.unarmed * 2))
            hit_chance = int((accuracy / (accuracy + accuracy_constant) * 100))

            dodge_chance = int((target.dexterity
                + (target.unarmed / 2)))

            # roll a dice between 1 and 100
            diceroll = random.randint(1, 100)

            # if the attack misses outright
            if hit_chance < diceroll:
                #TODO: switch this to format syntax
                #TODO: switch this toa function   
                message = str(self.name) + ' misses ' + str(target.name) + '!'
                highlights = {}
                target_name = target.name.split()
                for word in target_name:
                    #highlights[word] = (game.colors['red'])
                    highlights[word] = (game.colors['magenta'])
                game.writeMessage(message, highlights)
                return

            # if the attack would hit
            elif dodge_chance >= diceroll:

                #TODO: convert to string format
                #TODO: convert to function call
                message = str(str(self.name) + ' dodges ' + str(target.name)
                    + '\'s attack!')
                highlights = {
                    'dodges'    :   game.colors['yellow']
                    }
                target_name = target.name.split()
                for word in target_name:
                    #highlights[word] = game.colors['red']
                    highlights[word] = game.colors['magenta']
                #game.writeMessage(message, highlights)
                game.writeMessage(message, highlights)
                return


            else:



                message = str(self.name) + ' hits ' + str(target.name) + '!'
                highlights = {
                    'hits'      :   game.colors['red']
                    }
                target_name = target.name.split()
                for word in target_name:
                    highlights[word] = game.colors['magenta']
                game.writeMessage(message, highlights)


                target.resolveDamage(self, damage)

        


            
        


class Enemy:
    def __init__(self,
        ai=None):

        game.logger.debug('creating enemy class <%s>', str(self))

        self.ai = ai
        if self.ai is None:
            self.ai = SimpleEnemyAi()        
        self.ai.owner = self


class Logic(object):
    def __init__(self):

        pass

        def takeTurn(self):
            pass

class Simpleton(Logic):

    def __init__(self):

        super(Simpleton, self).__init__()

    def takeTurn(self):
        
        game.logger.info('<%s> taking turn . . .',
            str(self.owner.name))

        y = self.owner.y
        x = self.owner.x

        y_away = abs(hero.y - self.owner.y)
        x_away = int(abs((hero.x - self.owner.x) / 2))

        y_diff = 1
        x_diff = 1

        game.logger.debug('y_away = <%s>, x_away = <%s>', 
            str(y_away), str(x_away))

        if y_away <= 5 and x_away <= 5:
            if y_away > 0 or x_away > 0:
                if max(hero.y, y) == y:
                    y_diff = y_diff * -1
                if max(hero.x, x) == x:
                    x_diff = x_diff * -1

                game.logger.debug('<%s> has decided to move', 
                    str(self.owner.name))

                self.owner.move(y_diff, x_diff)




class Corpse:
    def __init__(self):

        pass

    def interact(self,
        interactor):

        interactor.changeGold(1)

        game.things.remove(self.owner)
        location = str(self.owner.y) + '_' + str(self.owner.x)
        board.spaces[location].contents.remove(self.owner)
        board.drawSpace(self.owner.y, self.owner.x)
        del self.owner
        


class SimpleEnemyAi:
    def __init__(self):

        pass

    def takeTurn(self):

        game.logger.info('<%s> taking turn . . .',
            str(self.owner.owner.name))

        y = self.owner.owner.y
        x = self.owner.owner.x

        y_away = abs(hero.y - self.owner.owner.y)
        x_away = int(abs((hero.x - self.owner.owner.x) / 2))

        y_diff = 1
        x_diff = 1

        game.logger.debug('y_away = <%s>, x_away = <%s>', 
            str(y_away), str(x_away))

        if y_away <= 5 and x_away <= 5:
            if y_away > 0 or x_away > 0:
                # if below
                if max(hero.y, y) == y:
                    # invert y
                    y_diff = y_diff * -1
                # if to the right
                if max(hero.x, x) == x:
                    # invert x
                    x_diff = x_diff * -1

                game.logger.debug('<%s> has decided to move', 
                    str(self.owner.owner.name))

                self.owner.owner.move(y_diff, x_diff)


class Space(Thing):
    def __init__(self):
        #self,
        #y,              # passed to super (Thing)
        #x):              # passed to super (Thing)
        super(Space, self).__init__()
            #y=y,
            #x=x)

        self.contents = []


    @property
    def location(self):
        location = str(str(self.y) + '_' + str(self.x))
        return location 


class Human(Humanoid):
    def __init__(self):
        #self,
        #y,              # passed to super (Actor->Thing)
        #x):              # passed to super (Actor->Thing)
        super(Human, self).__init__()
            #y=y,
            #x=x)

        self.name = 'human'

        self.sexes = ['male']

        self.acceptable_roles = [
            'deprived'
            ]

        self.ai = SimpleEnemyAi()

        self.logic = Simpleton()
        self.logic.owner = self

        self.ai.owner = self

        #self.dex_modifier = int(20)
        #self.str_modifier = int(15)
        #self.vit_hp_modifier = int(25)


class Snake(Wildlife, Beast):
    def __init__(self):
        super(Wildlife, self).__init__()
        super(Snake, self).__init__()

        self.char = 's'
        self.side_char = '~'
        self.sex = 'male'
        self.name = 'snake'

        self.side_char_color = self.color

        self.char_z2_center = 's'

        self.char_z1_u1l3 = curses.ACS_ULCORNER
        #self.char_z1_u1l2 = curses.ACS_ULCORNER
        self.char_z1_u1l2 = ' '
        self.char_z1_u1l1 = ' '
        self.char_z1_u1 = ' '
        self.char_z1_u1r1 = ' '
        self.char_z1_u1r2 = ' '
        self.char_z1_u1r3 = curses.ACS_URCORNER
        self.char_z1_l2 = ' '
        self.char_z1_l1 = '~'
        self.char_z1_r1 = '~'
        self.char_z1_center = '~'
        self.char_z1_r2 = ' '
        self.char_z1_r3 = ' '
        self.char_z1_d1l3 = curses.ACS_LLCORNER
        #self.char_z1_d1l2 = curses.ACS_LLCORNER
        self.char_z1_d1l2 = ' '
        self.char_z1_d1l1 = ' '
        self.char_z1_d1 = 's'
        self.char_z1_d1_color = game.colors['white']
        self.char_z1_d1r1 = ' '
        self.char_z1_d1r2 = ' '
        self.char_z1_d1r3 = curses.ACS_LRCORNER


class Squirrel(Wildlife, Beast):
    def __init__(self):
        super(Wildlife, self).__init__()
        super(Squirrel, self).__init__()

        self.char = 's'

        self.exp_reward = 6

        self.name = 'squirrel'

        self.sex = 'male'

        self.char_z1_l1 = curses.ACS_BULLET
        self.char_z1_center = '8'
        self.char_z1_r1 = curses.ACS_BULLET
        self.char_z1_d1 = 's'
        self.char_z1_d1_color = game.colors['white']

        #self.dex_modifier = 8
        #self.str_modifier = 2
        #self.vit_hp_modifier = 3

        #self.dexterity = 30
        #self.vitality = 1
        #self.strength = 1

        #self.unarmed = 10


class Boar(Wildlife, Beast):
    def __init__(self):
        super(Wildlife, self).__init__()
        super(Boar, self).__init__()

        self.char = 'b'
        
        self.name = 'boar'

        self.sex = 'male'

        self.side_char = '!'

        self.char_z1_l1 = '`'
        self.char_z1_center = 'M'
        self.char_z1_r1 = 'M'
        self.char_z1_r2 = '>'
        self.char_z1_d1 = 'b'
        self.char_z1_d1_color = game.colors['white']


class CottageBoar(Boar):
    def __init__(self):
        super(CottageBoar, self).__init__()

        self.dexterity = random.randint(2, 9)
        self.strength = random.randint(7, 11)
        self.vitality = random.randint(8, 13)

        self.side_char_color = game.colors['red']

        

class Rat(Wildlife, Beast):
    def __init__(self):
        #self,
        #y,              # passed to super (Actor->Thing)
        #x):              # passed to super (Actor->Thing)
        super(Wildlife, self).__init__()
        super(Rat, self).__init__()
            #y=y,
            #x=x)

        self.ai = SimpleEnemyAi()
        self.ai.owner = self

        self.char = 'r'
        self.char_z1_center = self.char

        self.exp_reward = 5

        self.logic = Simpleton()
        self.logic.owner = self

        self.name = 'rat'

        self.sex = 'male'

        #self.dex_modifier = int(4)
        #self.str_modifier = int(3)
        #self.vit_hp_modifier = int(4)


        #self.sexes = ['male']

        #self.acceptable_roles = [
        #    'deprived'
        #    ]

        # rat baselines
        #self.dexterity = 20
        #self.vitality = 2
        #self.strength = 1

        #self.unarmed = 10
        #self.initSkills(3, 3)

        self.side_char_color = self.color

        self.char_z2_center = self.char

        self.char_z1_u1l3 = curses.ACS_ULCORNER
        #self.char_z1_u1l2 = curses.ACS_ULCORNER
        self.char_z1_u1l2 = ' '
        self.char_z1_u1l1 = ' '
        self.char_z1_u1 = ' '
        self.char_z1_u1r1 = ' '
        self.char_z1_u1r2 = ' '
        self.char_z1_u1r3 = curses.ACS_URCORNER
        self.char_z1_l3 = ' '
        self.char_z1_l2 = ' '
        self.char_z1_l1 = '<'
        self.char_z1_center = 'o'
        self.char_z1_r1 = '-'
        self.char_z1_r2 = ' '
        self.char_z1_r3 = ' '
        self.char_z1_d1l3 = curses.ACS_LLCORNER
        #self.char_z1_d1l2 = curses.ACS_LLCORNER
        self.char_z1_d1l2 = ' '
        self.char_z1_d1l1 = ' '
        self.char_z1_d1 = 'r'
        self.char_z1_d1_color = game.colors['white']
        self.char_z1_d1r1 = ' '
        self.char_z1_d1r2 = ' '
        self.char_z1_d1r3 = curses.ACS_LRCORNER


class Hero(Human):
    def __init__(self):
        super(Hero, self).__init__()

        self.char = '@'

        self.name = 'player'

        self.experience = 0

        self.view_radius = 100

        self.dexterity = 10
        self.strength = 10
        self.vitality = 10



        self.char_z2_center = '@'




        self.char_z1_u1l3 = curses.ACS_ULCORNER
        #self.char_z1_u1l2 = curses.ACS_ULCORNER
        self.char_z1_u1l2 = ' '
        self.char_z1_u1l1 = ' '
        self.char_z1_u1 = 'n'
        self.char_z1_u1r1 = ' '
        self.char_z1_u1r2 = ' '
        self.char_z1_u1r3 = curses.ACS_URCORNER
        self.char_z1_l2 = ' '
        self.char_z1_l1 = '|'
        self.char_z1_center = '@'
        self.char_z1_r1 = '|'
        self.char_z1_r2 = ' '
        self.char_z1_r3 = ' '
        self.char_z1_d1l3 = curses.ACS_LLCORNER
        #self.char_z1_d1l2 = curses.ACS_ULCORNER
        self.char_z1_d1l2 = ' '
        self.char_z1_d1l1 = '/'
        self.char_z1_d1 = ' '
        self.char_z1_d1r1 = '\\'
        self.char_z1_d1r2 = ' '
        self.char_z1_d1r3 = curses.ACS_LRCORNER

    def move(
        self,
        y_diff,
        x_diff):
        """ custom move function for player """
        game.logger.debug('doing player move function')
        #self.move(y_diff, x_diff)
        super(Hero, self).move(y_diff, x_diff)
        board.moveCamera(y_diff, x_diff)

        self.traits = [
            'corporeal attack'
            ]


class GardenSnake(Snake):
    def __init__(self):
        super(GardenSnake, self).__init__()

        self.dexterity = random.randint(2, 8)
        self.strength = random.randint(1, 3)
        self.vitality = random.randint(4, 5)


class CommonSquirrel(Squirrel):
    def __init__(self):
        super(CommonSquirrel, self).__init__()

        self.dexterity = random.randint(4, 10)
        self.strength = random.randint(1, 2)
        self.vitality = random.randint(3,8)


class WoodRat(Rat):
    def __init__(self,
        keywords=None):
        super(WoodRat, self).__init__()

        self.name = 'woodland rat'

        dexterity = random.randint(3, 8)
        self.dexterity = dexterity

        strength = random.randint(1, 5)
        self.strength = strength

        vitality = random.randint(1, 5)
        self.vitality = vitality


class ManHunter(Human):
    def __init__(self):
        super(ManHunter, self).__init__()

        self.name = 'Man-hunter'

        self.char = 'h'

        self.color = game.colors['red']

        self.dexterity = random.randint(5, 18)
        self.strength = random.randint(8, 25)
        self.vitality = random.randint(5, 20)



class Shade(Actor):
    def __init__(self):
        #self,
        #y,              # passed to super (Actor->Thing)
        #x):              # passed to super (Actor->Thing)
        super(Shade, self).__init__()
            #y=y,
            #x=x)

        self.sexes = ['male']

        self.acceptable_roles = [
            'deprived'
            ]

        self.ai = SimpleEnemyAi()
        self.ai.owner = self

        self.logic = Simpleton()
        self.logic.owner = self


    @property
    def max_hp(self):
        return int(3)


# ============================================================= BOOTSTRAPPING ={


# this is what runs when the main module (this one) is executed
if __name__ == '__main__':

    # start everything else
    curses.wrapper(main)


# ============================================================ /BOOTSTRAPPING =}

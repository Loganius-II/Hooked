from ast import arg
from gettext import pgettext
from re import escape
from unittest import installHandler
from xml.etree.ElementTree import QName
import pygame
import sys
import sprites
import random
import mathmatics
from items import roll, Items, Inventory, random
from textwrap import wrap
import time
import sounds

# starting code
pygame.init()
SCREEN = pygame.display.set_mode((1000,500))
clock = pygame.time.Clock()
running = True
font = pygame.font.Font('Font/slkscr.ttf', 18)
ui_font = pygame.font.Font('Font/slkscr.ttf', 30)
footer_font = pygame.font.Font('Font/slkscr.ttf', 15)

VERSION = '0.1.5'

# roll the music
sounds.play_theme()

# home, game, etc. screens global switcher
current_screen = 'home'

# global colors
WHITE = (255,255,255)
OCEAN_BLUE = (68, 114, 222)
BROWN = (74, 53, 36)
YELLOW = (255, 251, 0)
RED = (250, 32, 32)
GRAY = (128, 133, 161)
GREEN = (0, 224, 60)
LIGHT_GREEN = (77, 255, 109)
BLUE = (77, 147, 255)

# game params
walkingx = False
walkingy = False
playerx = 150
playery = 80

shipx = 100
shipy = 100
ship_angle = 0
ship_marker = sprites.Sprite('Sprites/marker.png', 100, 100, 0.2)

# directions
facing_left = False
facing_up = False
facing_down = False
# player stats
dabloons = 100
health = 100
hunger = 1
thirst = 100
tiredness = 20
in_hand = None
inventory_cap = 5
inventory = Inventory(capacity=inventory_cap)
# PLAYER INVENTORY SPRITES
player_slot1 = sprites.Button_UI('', 100, 100,(0,0,0), 'Sprites/empty-slot.png' )
player_slot2 = sprites.Button_UI('', 100, 100,(0,0,0), 'Sprites/empty-slot.png' )
player_slot3 = sprites.Button_UI('', 100, 100,(0,0,0), 'Sprites/empty-slot.png' )
player_slot4 = sprites.Button_UI('', 100, 100,(0,0,0), 'Sprites/empty-slot.png' )
player_slot5 = sprites.Button_UI('', 100, 100,(0,0,0), 'Sprites/empty-slot.png' )

PLAYER_SLOT_DEFAULT_Y = 50

player_slot_coords = {
        1: {'currentx': 190, 'currenty': 50, 'defaultx': 190},
        2: {'currentx': 310,'currenty': 50, 'defaultx': 310},
        3: {'currentx': 430,'currenty': 50, 'defaultx': 430},
        4: {'currentx': 550,'currenty': 50, 'defaultx': 550},
        5: {'currentx': 670,'currenty': 50, 'defaultx': 670}
    }

active_slot_player = None
# CARGO INVENTORY SPRITES
cargo_slot1 = sprites.Button_UI('', 100, 100,(0,0,0), 'Sprites/empty-slot.png' )
cargo_slot2 = sprites.Button_UI('', 100, 100,(0,0,0), 'Sprites/empty-slot.png' )
cargo_slot3 = sprites.Button_UI('', 100, 100,(0,0,0), 'Sprites/empty-slot.png' )
cargo_slot4 = sprites.Button_UI('', 100, 100,(0,0,0), 'Sprites/empty-slot.png' )
cargo_slot5 = sprites.Button_UI('', 100, 100,(0,0,0), 'Sprites/empty-slot.png' )
# COORD DICT CARGO
CARGO_SLOT_DEFAULT_Y = 250

cargo_slot_coords = {
        1: {'currentx': 190, 'currenty': 250, 'defaultx': 190},
        2: {'currentx': 310,'currenty': 250, 'defaultx': 310},
        3: {'currentx': 430,'currenty': 250, 'defaultx': 430},
        4: {'currentx': 550,'currenty': 250, 'defaultx': 550},
        5: {'currentx': 670,'currenty': 250, 'defaultx': 670}
    }

active_slot_cargo = None

time_left_til_catch = 2
# controls the highest possible amount until you catch a fish next
time_til_catch_max = 10
hook_speed = 0

# for displaying catch
display_card = False

# declaring the item rolled as a global varialbe
item = None

# this is for checking when the clock ticks
clock_tick = False
# ship stats
next_dest = 0

# events
HUNGER_EVENT = pygame.USEREVENT + 1
THIRST_EVENT = pygame.USEREVENT + 2
TIREDNESS_EVENT = pygame.USEREVENT + 3

# generic clock that ticks every second
# there is probably a better way to do this built
# in pygame but there is no better alternative that
# ive seen
GENERIC_CLOCK_EVENT = pygame.USEREVENT + 4

pygame.time.set_timer(HUNGER_EVENT, random.randint(3000,30000))
pygame.time.set_timer(THIRST_EVENT, random.randint(1000,10000))
pygame.time.set_timer(TIREDNESS_EVENT, random.randint(1000,30000))
pygame.time.set_timer(GENERIC_CLOCK_EVENT, 1000)

# for when you catch fish these are ui variables
# draw the part you dont want cursor to enter
RED_SQUARE_X = 350
RED_SQUARE_Y = 210

# dementions of the scope of where the hook can move to
FISH_CURSOR_LEFTX = RED_SQUARE_X - 45
FISH_CURSOR_RIGHTX = RED_SQUARE_X + 290
fish_cursor_x = FISH_CURSOR_LEFTX
fish_cursor_direction = 'right'

# raft dimentnions
RAFT1_LEFT_X = 136
RAFT1_RIGHT_X = 345
RAFT1_TOP_Y= -26
RAFT1_BOTTOM_Y= 120

anchored = True
# fishing rod cast
rod_cast = False
# fishing bob coords
# to be set until rod cast
bobx = None
boby = None
# initialize at cast start
vx_bob = None   # horizontal velocity
vy_bob = None   # initial upward velocity
GRAVITY = 0.3

# mouse coords will be set when the
# mouse event happens
mousex = None
mousey = None
# box that detects collisions for interactable objects
anchor_interact_box = pygame.rect.Rect(0,0,40,40)

# may not need this if i integrate it into a player class
#player_interact_box = pygame.rect.Rect(playerx,playery,20,20)
PLAYER_INTERACT_BOX_OFFSETX = 20
PLAYER_INTERACT_BOX_OFFSETY = 130

# fishing string width constant
FISHING_LINE_WIDTH = 4

# on screen texts
top_left_dialogue_text_str = "Press F to interact"
top_left_dialogue_txt = font.render(top_left_dialogue_text_str, True, WHITE)


# animations
raft_idle_side = sprites.Sprite('Sprites/idle-no-sail.png', 163, 146,y=87)
raft_idle_front = sprites.Sprite('Sprites/idle-no-sail.png', 163, 146, y=312)
raft_moving_front = sprites.Sprite('Sprites/move-no-sail.png', 163, 146, y=312)
current_raft = raft_idle_front

player_walking = sprites.Player(
    'Sprites/player-walking.png', 23, 56, 4,
    PLAYER_INTERACT_BOX_OFFSETX=PLAYER_INTERACT_BOX_OFFSETX,
    PLAYER_INTERACT_BOX_OFFSETY=PLAYER_INTERACT_BOX_OFFSETY
    )
player_walking_up_diag = sprites.Player(
    'Sprites/player-walking-diag.png', 21, 47, 4,
    PLAYER_INTERACT_BOX_OFFSETX=PLAYER_INTERACT_BOX_OFFSETX,
    PLAYER_INTERACT_BOX_OFFSETY=PLAYER_INTERACT_BOX_OFFSETY
    )
current_player = player_walking

# UI sprites
wood_panel_UI = sprites.Sprite('Sprites/wood-ui-bar.png', 1000, 100, 1)
coin = sprites.Sprite('Sprites/coin.png', 375,375, 0.1)

catch_fish_wood_panel = sprites.Sprite('Sprites/wood-ui-bar.png', 400, 100, 1)
green_square_width = 0
catch_fish_cursor = sprites.Sprite('Sprites/hook.png', 100,100, 1.2)
catch_fish_cursor_x = 0

green_flag = sprites.Sprite('Sprites/green-flag.png', 100, 100, scale=0.4)
flag = False
flagx = 0
flagy = 0

# caught fish card UI
CARD_SCALE = 0.8
BACKGROUND_COMMON = sprites.Sprite('Sprites/common-item-card.png',300,300,CARD_SCALE)
BACKGROUND_UNCOMMON = sprites.Sprite('Sprites/uncommon-item-card.png',300,300,CARD_SCALE)
BACKGROUND_RARE = sprites.Sprite('Sprites/rare-item-card.png',300,300,CARD_SCALE)
BACKGROUND_LEGENDARY = sprites.Sprite('Sprites/legendary-item-card.png',300,300,CARD_SCALE)

EAT_BTN_WIDTH = 300
eat_btn = sprites.Sprite('Sprites/eat-btn.png', EAT_BTN_WIDTH, 50, scale=0.74)
#global eat_btn_rect
eat_btn_rect = eat_btn.frames[0].get_rect()

# on ship sprites and items/ APPLIANCES
items = Items()
basic_cargo = items.get_cargo('basic')
basic_cargo_cap = basic_cargo.get('cap')

basic_cargo_box = sprites.Sprite(basic_cargo['img'], 100,100, 0.8)
cargo_inventory = Inventory(capacity=basic_cargo_cap)
cargo_inventory.add_item({
      "name": "Wet Newspaper",
      "description": "Yesterday's news. Literally.",
      "img": "wet_newspaper.png",
      "edible": False,
      "flammable": True,
      "rarity": 'Common',
      'x': -5
    }, 1)
# this is for tracking if the cargo box is being viewed
open_cargo = False

anchor_up = sprites.Sprite('Sprites/anchored.png', 200,112, 0.45)
anchor_down = sprites.Sprite('Sprites/anchordown.png', 50, 28, 1.5)

anchor_rect = anchor_up.frames[0].get_rect()

# rusted cooker
rusted_cooker = sprites.Sprite('Sprites/cooker.png', 100, 100, 1)
rusted_cooker_cooking = sprites.Sprite('Sprites/cooker-cooking.png', 100,100,1)
current_cooker = rusted_cooker
cooker_rect = current_cooker.frames[0].get_rect()
cooker_open = False
cook_timer = 0

cooker_fuel_btn = sprites.Button_UI('Fuel', 100,100, (0,0,0), font_name='Font/slkscr.ttf')
cooker_food_btn = sprites.Button_UI('Food', 100,100, (227, 95, 146), font_name='Font/slkscr.ttf')

cooker_slots_defaulty = 200
cooker_fuel_coords = {'currentx':200,'currenty':cooker_slots_defaulty,'defaultx':200}
cooker_food_coords = {'currentx':400,'currenty':cooker_slots_defaulty,'defaultx':400}
# fuel or food
active_cooker_slot = None

cooker_fuel_inv = Inventory(1)
cooker_food_inv = Inventory(1)

# on ship sprite stats
current_cargo_box = basic_cargo_box
cargo_rect = current_cargo_box.frames[0].get_rect()
CARGO_BOX_COORDS = (330, 120)

# player sprites
fishing_pole = sprites.Sprite('Sprites/fishing-pole.png', 162, 162, 0.5)
fishing_bob = sprites.Sprite('Sprites/bob.png', 100,100, 0.2)
fishing_bob_water = sprites.Sprite('Sprites/bob-in-water.png', 100,100, 0.2)
current_bob = fishing_bob
fishing_line = pygame.rect.Rect(100, 100, 3, 100)
base_string = pygame.Surface((1, 4), pygame.SRCALPHA)
pygame.draw.rect(base_string, WHITE, base_string.get_rect())
open_inventory = False

# backpack fixed to back of player
# add a rect image that its wrapped in so
# you can hover over the pack with cursor and see items
player_pack = sprites.Sprite('Sprites/pack.png', 123, 122, 0.5)
player_pack_x = 0
player_pack_y = 0
player_pack_rect = player_pack.frames[0].get_rect()

# SFX VARS
reel_sfx = None

# functions

def noop():
    # place holder function
    return None

def error_evader(funct):
    # decorator for functions im done messing with the errors
    def wrapper(*args, **kwargs):
        try:
            funct(*args, **kwargs)
        except:
            pass
    return wrapper

def draw_player_slots():

    # get all slot coords
    SLOT1_X = player_slot_coords.get(1).get('currentx')
    SLOT2_X = player_slot_coords.get(2).get('currentx')
    SLOT3_X = player_slot_coords.get(3).get('currentx')
    SLOT4_X = player_slot_coords.get(4).get('currentx')
    SLOT5_X = player_slot_coords.get(5).get('currentx')

    SLOT1_Y = player_slot_coords.get(1).get('currenty')
    SLOT2_Y = player_slot_coords.get(2).get('currenty')
    SLOT3_Y = player_slot_coords.get(3).get('currenty')
    SLOT4_Y = player_slot_coords.get(4).get('currenty')
    SLOT5_Y = player_slot_coords.get(5).get('currenty')

    # Draws the player inventory slots when opened
    player_slot1.draw(SCREEN,SLOT1_X, SLOT1_Y)
    player_slot2.draw(SCREEN,SLOT2_X, SLOT2_Y)
    player_slot3.draw(SCREEN,SLOT3_X, SLOT3_Y)
    player_slot4.draw(SCREEN,SLOT4_X, SLOT4_Y)
    player_slot5.draw(SCREEN,SLOT5_X, SLOT5_Y)

def draw_cargo_slots():
    # draws the player inventory slots when opened

    # get all slot coords
    SLOT1_X = cargo_slot_coords.get(1).get('currentx')
    SLOT2_X = cargo_slot_coords.get(2).get('currentx')
    SLOT3_X = cargo_slot_coords.get(3).get('currentx')
    SLOT4_X = cargo_slot_coords.get(4).get('currentx')
    SLOT5_X = cargo_slot_coords.get(5).get('currentx')

    SLOT1_Y = cargo_slot_coords.get(1).get('currenty')
    SLOT2_Y = cargo_slot_coords.get(2).get('currenty')
    SLOT3_Y = cargo_slot_coords.get(3).get('currenty')
    SLOT4_Y = cargo_slot_coords.get(4).get('currenty')
    SLOT5_Y = cargo_slot_coords.get(5).get('currenty')

    # draw at the given coords
    cargo_slot1.draw(SCREEN,SLOT1_X, SLOT1_Y)
    cargo_slot2.draw(SCREEN,SLOT2_X, SLOT2_Y)
    cargo_slot3.draw(SCREEN,SLOT3_X, SLOT3_Y)
    cargo_slot4.draw(SCREEN,SLOT4_X, SLOT4_Y)
    cargo_slot5.draw(SCREEN,SLOT5_X, SLOT5_Y)



def display_inventory_slots(slot_type:str):
    # displays each slot
    # if it is empty then to the empty-slot.png else show the card
    # slot_type should be cargo, or player

    for i in range(5):
        i = i+1

        # setting the inventory object to set it to
        # i couldve done it a better way but im lazy
        if slot_type == 'player':
            rarity = inventory.items.get(i)
        elif slot_type == 'cargo':
            rarity = cargo_inventory.items.get(i)

        else:
            print('NOT A VALID SLOT TYPE')
            return

        if rarity:
            rarity = rarity.get('rarity')

            # RIGHT HERE
            # CHANGE INVENTORY BACKGROUND

            exec(f"{slot_type}_slot{i}.change_bg('Sprites/{rarity}-item-card.png')")


        else:
            exec(f"{slot_type}_slot{i}.change_bg('Sprites/empty-slot.png')")

    #exec(f'draw_{slot_type}_slots()')

def display_cooker_slots():
    # displays slots for cooker
    cooker_fuel_btn.draw(SCREEN, cooker_fuel_coords['currentx'],cooker_fuel_coords['currenty'])
    cooker_food_btn.draw(SCREEN, cooker_food_coords['currentx'], cooker_food_coords['currenty'])

def cooker_btn_held(slot_type: str):
    # between the food or fuel slot and
    # drags the slot

    global active_cooker_slot

    active_cooker_slot = slot_type

    x,y = pygame.mouse.get_pos()

    if slot_type == 'fuel' and not active_slot_player:
        cooker_fuel_coords['currentx'] = x - 50
        cooker_fuel_coords['currenty'] = y - 50

    elif slot_type == 'food' and not active_slot_player:
        cooker_food_coords['currentx'] = x - 50
        cooker_food_coords['currenty'] = y - 50

def draw_fishing_line(screen, point1, point2) -> None:
    # accepts 3 arguments
    # screen: the surface object to draw to
    # point1: on point of the string
    # point2: the second point that the string is connecting to
    # mathmatically calculates and draws the angle and length to
    # draw a line between two points

    STRING_WIDTH = 2

    #first calculate the angle
    angle = mathmatics.two_point_angle(point1, point2)

    # get a length of the string
    length = mathmatics.two_point_distance(point1, point2)

    string = pygame.transform.scale(base_string, (length+10, STRING_WIDTH))

    # rotate string
    string = pygame.transform.rotate(string, -angle)

    rect = string.get_rect()

    rect.center = ((point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2)

    screen.blit(string, rect)

def fishing_pole_in_hand_logic() -> None:
    # globalizing all variables
    # i hope this isnt looked down upon
    global offsetx_pole, facing_left, fishing_pole, playerx, playery, rod_cast, offsetx_bob, offsety_bob, tip_of_polex, bobx, boby, current_bob, vy

    # accepts no arguements
    # function purely for code organization
    # this runs most everything regarding the fishing pole
    # adjust based off of direction facing
    offsetx_pole = 40 if not facing_left else -40
    # draw fishing pole below player
    fishing_pole.draw(SCREEN, playerx+offsetx_pole, playery+60, facing_left)

    if not rod_cast:
        #fishing bob

        #set the offset
        offsety_bob = 65
        offsetx_bob = 110 if not facing_left else -50

        # set the coords
        bobx = playerx + offsetx_bob
        boby = playery + offsety_bob

    else:
        # calculate fishing line angle

        # point 1 will be the tip of the fishing pole
        tip_of_polex = 120 if not facing_left else -35
        point1 = (playerx+ tip_of_polex, playery+60)
        # point two is where the fishing bob is
        # applying a slight offset in the x
        point2 = (bobx+10, boby)

        #draw fishing line
        draw_fishing_line(SCREEN, point1, point2)


        #                              making sure is for the right of player
        if boby >= mousey and bobx >= mousex and mousex > playerx:
            current_bob = fishing_bob_water
            # animate
            current_bob.update()

        elif boby >= mousey and bobx <= mousex and mousex < playerx:
            current_bob = fishing_bob_water
            # animate
            current_bob.update()

        else:
            bobx += vx
            boby += vy

            # applying gravity
            vy += GRAVITY

    # draw the bob
    current_bob.draw(SCREEN, bobx, boby, facing_left)

def catch_fish_ui(green_square_width, speed) -> None:
    # accepts the argument that sets the green sqwuare width
    # and reel sfx so it can manipulate stopping it
    # displays and handles the mini game to
    # catch the fish
    # a black cursor will go back and forth and
    # the player must stop the cursor by clicking at
    # the right time to where it stops in the green
    # speed is how fast the hook goes back and forth

    global fish_cursor_direction, fish_cursor_x, green_square

    # add make the cursro bounce right and left
    if fish_cursor_direction == 'right':
        fish_cursor_x += speed
        if fish_cursor_x > FISH_CURSOR_RIGHTX:
            fish_cursor_direction = 'left'

    elif fish_cursor_direction == 'left':
        fish_cursor_x -= speed
        if fish_cursor_x < FISH_CURSOR_LEFTX:
            fish_cursor_direction = 'right'
    else:
        # fish caught
        pass

    # draw background visual
    catch_fish_wood_panel.draw(SCREEN, 340,200)

    red_square = pygame.Rect(RED_SQUARE_X, RED_SQUARE_Y, 380, 80)
    pygame.draw.rect(SCREEN, RED, red_square)

    # random green area
    halfway = (350 // 2) + 350
    halfway = halfway - (green_square_width // 2)
    green_square = pygame.Rect(halfway, 210, green_square_width, 80)
    pygame.draw.rect(SCREEN, GREEN, green_square)
    catch_fish_cursor.draw(SCREEN,fish_cursor_x,RED_SQUARE_Y-20)


def show_card(item: dict, x, y, scale = 0.8, new = False) -> sprites.Sprite:
    # the item and coordinates
    # show the card on the screen with the given information

    # new is if the card is new so it can play sound
    # reel sfx is the mixer sound object to controll it

    if new:
        sounds.badadadink()


    try:
        rarity = item['rarity']

    except:
        return False, False

    # display card
    if rarity == 'Common':
        card = BACKGROUND_COMMON

    if rarity == 'Uncommon':
        card = BACKGROUND_UNCOMMON

    if rarity == 'Rare':
        card = BACKGROUND_RARE

    if rarity == 'Legendary':
        card = BACKGROUND_LEGENDARY

    card.scale = scale
    card.frames = card.load_frames()
    if item.get('cooked'):
        # indicate its cooked by color tint change
        card.tint((232, 150, 144))
    card.draw(SCREEN, x, y)

    if scale < 0.8:
        pass
    else:
        name = item['name']
        description = item['description']

        # name of the fish text
        name_txt = font.render(name, True, (0,0,0))
        description = wrap(description, width=16)

        # wrapping the description
        for i, line in enumerate(description):
            description_txt = font.render(line, True, BROWN)
            SCREEN.blit(description_txt, (x+ 30, (y + 140) + 20* i))

        # color key for text for rarity
        rarity_color_key = {
            'Common': GREEN,
            'Uncommon': LIGHT_GREEN,
            'Rare': BLUE,
            'Legendary': (0,0,0)
            }

        # rarity display
        rarity_txt = footer_font.render(rarity, True, rarity_color_key[rarity])
        SCREEN.blit(rarity_txt, (x+ 25, y+ 80))
        # draw on screen
        SCREEN.blit(name_txt, (x+ 30, y+ 110))

        # display eat button
        if scale <= 0.8:
            #eat_btn_rect = eat_btn.frames[0].get_rect()

            eat_btn.draw(SCREEN, x+11.5, 333)

            # creating rectangle object for mouse collision
            # setting the coordinates of it
            eat_btn_rect.topleft = (x+11.5, 333)

        return card, eat_btn_rect

# button functions
def cargo_item_clicked(slot: int):
    # slot is the cargo slot number
    # what happends when a certain item is clicked

    # display player inventory on top
    # display cargo ivnentory
    # drag and drop items from player inventory to cargo inventory
    # swap places if already occupied
    # else just add to that inventory

    # finished with:
    #   - creating on_hold function for button ui class
    #   - updated inventory to dict
    global active_slot_player, active_slot_cargo
    if active_slot_cargo != slot and active_slot_cargo != None or active_slot_player:
        return

    active_slot_cargo = slot

    items = cargo_inventory.items

    # change x and y to cursor
    x, y = pygame.mouse.get_pos()
    # set current x and y to themouse position
    # apply offset
    # changing coords
    cargo_slot_coords[slot]['currentx'] = x - 50
    cargo_slot_coords[slot]['currenty'] = y - 50

    return

def player_item_clicked(slot:int):
    # this is what happens when you hold down the inventory slot for player inventory
    global active_slot_player, active_slot_cargo
    # dont proceed if another slot is being moved
    if active_slot_player != slot and active_slot_player != None or active_slot_cargo:
        return

    active_slot_player = slot
    items = cargo_inventory.items

    # change x and y to cursor
    x, y = pygame.mouse.get_pos()
    # set current x and y to themouse position
    # apply offset
    # changing coords
    player_slot_coords[slot]['currentx'] = x - 50
    player_slot_coords[slot]['currenty'] = y - 50

    '''
    if len(items) >= slot:
        # this means that this space is occupied

        # transfer item to inventory
        first_item = items[slot-1]
        cargo_inventory.remove_item(first_item)

        inventory.add_item(first_item)

        s = f'cargo_slot{slot}.change_bg(\'Sprites/empty-slot.png\')'


    else:
        try:
            # transfer item to cargo box
            first_item = inventory.items[slot-1]
            inventory.remove_item(first_item)
            cargo_inventory.add_item(first_item)

            rarity = first_item['rarity']

            s = f'cargo_slot{slot}.change_bg(\'Sprites/{rarity}-item-card.png\')'
        except:
            return

    print(s)
    exec(s)
    '''



#

def view_inventory_card(number_pressed: int) -> tuple[dict, bool]:
    # this modularizes showing a card when a number is pushed
    # and the inventory is open
    # returns the inventory item and true or false
    # to set the displaying card variable
    try:
        print(inventory.items)
        return inventory.items[number_pressed], True
    except:
        return False, False

def center_x(surface: pygame.Surface):
    # accepts the pygame surface
    # calculates center x coord for surface
    # returns the x

    return SCREEN.get_width() // 2 - surface.get_width() // 2

def draw_ship_marker():
    global next_dest, shipx, shipy, flagx, flagy, ship_angle, dabloons, game, current_screen
    # draws the ship makrer on map

    # getting pygame surface
    marker_surface = ship_marker.frames[0]

    # getting the angle to rotate the ship to
    #angle = mathmatics.two_point_angle((shipx+680, shipy+70), (flagx, flagy-40))

    marker = pygame.transform.rotate(marker_surface, ship_angle)

    marker_rect = marker_surface.get_rect(topleft=(shipx+680, shipy+70))
    map_rect = mapui.map_paper_sprite_surface.get_rect(topleft=(mapui.x, mapui.y))



    # get and change distance
    next_dest = int(mathmatics.two_point_distance((shipx+680, shipy+70), (flagx-5, flagy-20))) if next_dest else 0

    if not anchored:
        # go forward
        # based on angle
        shipx, shipy = mathmatics.calculate_new_xy((shipx, shipy), 0.05, -ship_angle-110)

        # check if running into island
        for island in mapui.island_sprite_list:
            if marker_rect.colliderect(island.rectangle):
                print('ISLAND')
                game = False
                current_screen = "island"

        if not map_rect.colliderect(marker_rect):
            # THE SIRENS GOT YOU
            # DONT SAIL BEYOND CHARTED WATERS
            SCREEN.fill((0,0,0))

            warning = ['Do not travel beyond ye chart\'d wat\'r', 'Ignore their inviting beck\'ns!', 'AaAaArRrRrGgG']

            screen_txt1 = ui_font.render('Aye, The Sirens Got You!', True, WHITE)
            screen_txt2 = font.render(random.choice(warning), True, WHITE)

            SCREEN.blit(screen_txt1, (center_x(screen_txt1), 100))
            SCREEN.blit(screen_txt2, (center_x(screen_txt2), 250))

            pygame.display.update()

            pygame.time.wait(2000)

            screen_txt3 = font.render('-25 Gold Dabloons', True, RED)

            dabloons = max(0, dabloons - 25)

            SCREEN.blit(screen_txt3, (center_x(screen_txt3), 300))

            pygame.display.update()

            pygame.time.wait(2000)

            # reset ship
            shipx = 100
            shipy = 100


    SCREEN.blit(marker, (shipx+680, shipy+70))

# TITLE SCREEN
def title_screen():
    # function for what happens in the title screen
    # font graphics for credits
    g = ui_font.render('Graphics by:', False, WHITE)
    graphic_cred1 = font.render('Logan McDermott', False, WHITE)
    graphic_cred2 = font.render('Sevarihk', False, WHITE)

    author_cred = ui_font.render('Game by:', False, WHITE)

    present_cred = ui_font.render('presents...', False, WHITE)

    # display graphics credits
    SCREEN.blit(g, (center_x(g), 150))
    SCREEN.blit(graphic_cred1, (center_x(graphic_cred1), 260))
    SCREEN.blit(graphic_cred2, (center_x(graphic_cred2), 290))

    pygame.display.flip()
    pygame.time.delay(2500)

    # game by
    SCREEN.fill((0,0,0))
    SCREEN.blit(author_cred, (center_x(author_cred), 150))
    SCREEN.blit(graphic_cred1, (center_x(graphic_cred1), 260))

    pygame.display.flip()
    pygame.time.delay(2500)

    # losoft presents...

    # create a logo sprite obj
    losoft_logo = sprites.Sprite('Sprites/logo.png', 100, 100, 2.5)
    losoft_center = center_x(losoft_logo.frames[0])

    SCREEN.fill((0,0,0))
    SCREEN.blit(present_cred, (center_x(present_cred), 300))
    losoft_logo.draw(SCREEN, losoft_center, 60)

    pygame.display.flip()
    pygame.time.delay(5000)


#title_screen()

# randomly generating map
print('loading map...')
t = time.time()
mapui = sprites.Map_UI(SCREEN)
mapui.generate_map()
mapui.resolve_island_overlap()
t = time.time() - t
print('loaded in', t, 'seconds')

# game loop
while running:
    if current_screen == 'game':
        game = True

        while game:
            global green_square
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    game = False

                elif event.type == HUNGER_EVENT:
                    hunger = max(0, hunger-1)
                    pygame.time.set_timer(HUNGER_EVENT, random.randint(1000,10000))

                    # if your deathly hungery then start tacking health
                    if not hunger:
                        health = max(0, health-1)

                elif event.type == THIRST_EVENT:
                    thirst = max(0, thirst - 1)
                    pygame.time.set_timer(THIRST_EVENT, random.randint(3000,30000))

                    if not thirst:
                        health = max(0, health-1)

                elif event.type == TIREDNESS_EVENT:
                    tiredness = max(0, tiredness-random.randint(1,3))
                    pygame.time.set_timer(TIREDNESS_EVENT, random.randint(1000,30000))

                    if not tiredness:
                        health = max(0, health-1.5)

                elif event.type == GENERIC_CLOCK_EVENT:
                    # when the clock ticks which means about a second passed
                    # add everything here that you want to encorporate the witht he clock

                    # set ticked global to true
                    clock_tick = True

                    # subtract from time until you catch the fish
                    if rod_cast and in_hand == 'fishing pole':
                        time_left_til_catch -= 1
                    else:
                        # reset the time and it changes every second
                        time_left_til_catch = random.randint(1, time_til_catch_max)

                    # making sure it isnt negative
                    time_left_til_catch = max(time_left_til_catch, 0)

                    # cook timer
                    cook_timer -= 1 if cook_timer else 0

                    if not cook_timer:
                        current_cooker = rusted_cooker


                elif event.type == pygame.KEYDOWN:
                    # pressing f to interact
                    if event.key == pygame.K_f and press_f:
                        if press_f == 'anchor':
                            # toggle between anchored and not anchored
                            if anchored:
                                anchored = False
                                current_raft = raft_moving_front
                            else:
                                anchored = True
                                current_raft = raft_idle_front

                        elif press_f == 'cargo':
                            # interacted with cargo box
                            open_cargo = True

                            # check for items in that slot and get rarity
                            items = cargo_inventory.items
                            rarity = None

                        elif press_f == 'cooker':
                            cooker_open = True


                    elif event.key == pygame.K_1:
                        # if the inventory isnt opened
                        if not open_inventory:
                            # toggle fishing pole in and out of hand
                            if in_hand == 'fishing pole':
                                in_hand = None
                                rod_cast = False
                                current_bob = fishing_bob

                            else:
                                in_hand = 'fishing pole'
                        else:
                            # otherwise view hte item
                            item, display_card = view_inventory_card(1)

                    elif event.key == pygame.K_2:
                        if open_inventory:
                            item, display_card = view_inventory_card(2)

                    elif event.key == pygame.K_3:
                        if open_inventory:
                            item, display_card = view_inventory_card(3)

                    elif event.key == pygame.K_4:
                        if open_inventory:
                            item, display_card = view_inventory_card(4)

                    elif event.key == pygame.K_5:
                        if open_inventory:
                            item, display_card = view_inventory_card(5)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mousex, mousey = event.pos

                    if press_f != 'cargo' and open_cargo:
                        open_cargo = False

                    if press_f != 'cooker' and cooker_open:
                        cooker_open = False

                    if display_card:
                        display_card = False

                        if eat_btn_rect.collidepoint(mouse_pos):
                            try:
                                inventory.remove_item(item)
                            except:
                                # in this case just ignore because it was eaten in hand rather than from pack
                                pass

                            edible = item.get('edible')
                            hunger_increase = item.get('hunger_increase')

                            if edible:
                                hunger += hunger_increase
                                hunger = min(hunger, 100)

                            else:
                                health -= 10

                    elif in_hand == 'fishing pole':
                        # toggle rod cast
                        if not rod_cast and not display_card and not cooker_open and not open_cargo:
                            # now checking to see if it is trying to be cast behind the playesr
                            # which is a no no
                            if facing_left and mousex > playerx or not facing_left and mousex < playerx:
                                top_left_dialogue_text_str = 'CAN\'T CAST ROD BEHIND YOU'
                                top_left_dialogue_txt = font.render(top_left_dialogue_text_str, True, RED)

                                # click
                                sounds.click()
                            else:
                                # set the speed of the mini game to catch the fish
                                hook_speed = random.randint(4,10)
                                rod_cast = True
                                # initialize at cast start
                                vx = (mousex - playerx) / 45 # horizontal velocity
                                vy = -2 # initial upward velocity

                                # WHOOOSHHHH
                                sounds.whoosh()

                        else:
                            if time_left_til_catch == 0 and rod_cast:
                                # try to see if you caught the fish

                                right_of_green_square_x = green_square.x + green_square.width

                                # check if the range is within green square and apply an offsetx
                                caught = mathmatics.coordinate_range_x(green_square.x, right_of_green_square_x, fish_cursor_x+50)

                                if caught:
                                    # display the card and roll
                                    item = roll()
                                    display_card = True

                                    item['x'] = -5

                                    add_failed = inventory.add_item(item, len(inventory.items_list) +1)

                                    # if it returns true then it wasnt added
                                    print(inventory.items)
                                    if add_failed:
                                        top_left_dialogue_text_str = "INVENTORY FULL"
                                        top_left_dialogue_txt = font.render(top_left_dialogue_text_str, True, RED)
                                        sounds.error()



                                else:
                                    try:
                                        reel_sfx.stop()
                                        reel_sfx = None
                                    except:
                                        pass

                                # reset greensquare width so it can be set again
                                green_square_width = None

                            rod_cast = False
                            current_bob = fishing_bob

                elif event.type == pygame.MOUSEBUTTONUP:
                    if open_cargo or cooker_open:
                        # check if colliding with another slot
                        # and swap or move to

                        # make lists to iterate over
                        cargo_slot_list = [cargo_slot1,cargo_slot2,cargo_slot3,cargo_slot4,cargo_slot5]
                        player_slot_list = [player_slot1,player_slot2,player_slot3,player_slot4,player_slot5]

                        # ignore this crazy nest :|
                        for i, player_slot in enumerate(player_slot_list):
                            if not cooker_open:
                                for j, cargo_slot in enumerate(cargo_slot_list):
                                    if cargo_slot.rect.colliderect(player_slot):
                                        print(f'player slot {i+1} interacted with cargo slot {j+1}')
                                        if player_slot.rect.collidepoint(mouse_pos):
                                            if player_slot.rect.collidepoint(mouse_pos) and cargo_slot.rect.collidepoint(mouse_pos):
                                                # if both are touching

                                                # attempt transfer to the empty slot
                                                if inventory.items[i+1] and not cargo_inventory.items[j+1]:
                                                    cargo_inventory.transfer_item(inventory, i+1, j+1)
                                                    print(i, j)

                                                elif not inventory.items[i+1] and cargo_inventory.items[j+1]:
                                                    inventory.transfer_item(cargo_inventory, j+1, i+1)
                                                    print(2)
                                                    print(i, j)

                                                else:
                                                    # just swap
                                                    print(3)
                                                    inventory.transfer_item(cargo_inventory, j+1, i+1)
                                            else:
                                                cargo_inventory.transfer_item(inventory, i+1, j+1)
                                                print('transfering to cargo')
                                        else:
                                            inventory.transfer_item(cargo_inventory, j+1, i+1)
                                            print('transfering to inventory')
                                        break

                            # for cooker
                            elif not cook_timer:
                                if cooker_food_btn.rect.colliderect(player_slot):
                                    if player_slot.rect.collidepoint(mouse_pos):
                                        cooker_food_inv.transfer_item(inventory, i+1, 1)
                                    else:
                                        inventory.transfer_item(cooker_food_inv, 1, i+1)

                                elif cooker_fuel_btn.rect.colliderect(player_slot):
                                    if player_slot.rect.collidepoint(mouse_pos):
                                        cooker_fuel_inv.transfer_item(inventory, i+1, 1)
                                    else:
                                        inventory.transfer_item(cooker_fuel_inv, 1, i+1)

                                # logic for now cooking the food
                                food = cooker_food_inv.items[1]
                                fuel = cooker_fuel_inv.items[1]

                                if food and fuel:
                                    # THEN LET EM COOOOOOK
                                    if fuel.get('flammable'):
                                        cooker_fuel_inv.remove_item(fuel)

                                        # set timer to 30 secs
                                        cook_timer = 30

                                        cooker_food_inv.items[1]['hunger_increase'] += 20
                                        cooker_food_inv.items[1]['cooked'] = True

                                        current_cooker = rusted_cooker_cooking




                        # resetting the coords of the food and fuel of cooker
                        cooker_fuel_coords['currentx'] = cooker_fuel_coords['defaultx']
                        cooker_fuel_coords['currenty'] =  cooker_slots_defaulty

                        cooker_food_coords['currentx'] = cooker_food_coords['defaultx']
                        cooker_food_coords['currenty'] =  cooker_slots_defaulty


                        # reset the coords of inventory items
                        # if the inventory is open

                        active_slot_player = None
                        active_slot_cargo = None

                        for i in range(1, 6):
                            # reset x
                            defaultx = cargo_slot_coords.get(i).get('defaultx')
                            cargo_slot_coords[i]['currentx'] = defaultx

                            defaultx = player_slot_coords.get(i).get('defaultx')
                            player_slot_coords[i]['currentx'] = defaultx

                            # reset y
                            cargo_slot_coords[i]['currenty'] = CARGO_SLOT_DEFAULT_Y

                            player_slot_coords[i]['currenty'] = PLAYER_SLOT_DEFAULT_Y

                    elif mapui.map_paper_sprite_surface.get_rect(topleft=(mapui.x, mapui.y)).collidepoint(mouse_pos):
                        if mouse_pos == (flagx, flagy):
                            flag = False

                        else:
                            flag = True
                            flagx = mouse_pos[0]
                            flagy = mouse_pos[1]

                            next_dest = int(mathmatics.two_point_distance((shipx+680, shipy+70), (flagx, flagy-40)))

                keys_pressed = pygame.key.get_pressed()

                if keys_pressed[pygame.K_d]:
                    if anchored:
                        walkingx = True
                        facing_left = False

                    else:
                        # for controling ship
                        ship_angle -= 2.3



                elif keys_pressed[pygame.K_a]:
                    if anchored:
                        walkingx = True
                        facing_left = True

                    else:
                        # for controlling the ship
                        ship_angle += 2.3

                else:
                    walkingx = False

                if keys_pressed[pygame.K_w]:
                    facing_up = True
                    walkingy = True



                elif keys_pressed[pygame.K_s]:
                    facing_down = True
                    walkingy = True

                else:
                    walkingy = False
                    facing_up = False
                    facing_down = False


            #player_interact_box = pygame.rect.Rect(playerx + PLAYER_INTERACT_BOX_OFFSETX,playery + PLAYER_INTERACT_BOX_OFFSETY,10,20)

            # update player first
            current_player.update()

            if walkingx and not walkingy:
                current_player = player_walking
                # checking X boundaries and logic for just left and right turns
                if facing_left and playerx >= RAFT1_LEFT_X:
                    playerx -= 2
                elif not facing_left and playerx <= RAFT1_RIGHT_X:
                    playerx += 2

            elif walkingy and not walkingx:
                current_player = player_walking

                # checking Y boundaries and logic for just up and down turns
                if facing_up and playery >= RAFT1_TOP_Y:
                    playery -= 2
                elif facing_down and playery <= RAFT1_BOTTOM_Y:
                    playery += 2

            elif walkingx and walkingy and playerx >= RAFT1_LEFT_X and playerx <= RAFT1_RIGHT_X and playery <= RAFT1_BOTTOM_Y and playery >= RAFT1_TOP_Y:
                # down diagonal directions first
                # they wont have any change in animation
                if facing_left and facing_down:
                    current_player = player_walking
                    playerx -= 1
                    playery +=1

                elif not facing_left and facing_down:
                    current_player = player_walking
                    playerx += 1
                    playery += 1

                # for up and diagonal
                elif facing_left and facing_up:
                    current_player = player_walking_up_diag
                    playerx -= 1
                    playery -= 1

                elif not facing_left and facing_up:
                    current_player = player_walking_up_diag
                    playerx += 1
                    playery -= 1


            else:
                # make him idle
                current_player.current_frame = 0

            # mouse positino
            mouse_pos = pygame.mouse.get_pos()

            # fill background blue
            SCREEN.fill(OCEAN_BLUE)

            # game code rendering

            # draw interact collision
            #pygame.draw.rect(SCREEN, , player_interact_box, 100)

            # draw the raft
            current_raft.draw(SCREEN, 100,100)
            current_raft.update()

            # draw rusted cooker
            current_cooker.draw(SCREEN, 230, 100)
            current_cooker.update()

            # and things on the raft
            # update anchor collisions coords
            anchor_rect.topleft = (160,140)

            current_cargo_box.draw(SCREEN, CARGO_BOX_COORDS[0], CARGO_BOX_COORDS[1])
            cargo_rect.topleft = (CARGO_BOX_COORDS[0] - 10, CARGO_BOX_COORDS[1])

            cooker_rect.topleft =  (230, 100)

            if anchored:
                anchor_down.draw(SCREEN, 160, 140)

                # check if player is colliding
                # selecting the first frame since that is a pygame surface
                anchor_collided = pygame.Rect.colliderect(current_player.player_interact_box, anchor_rect)

                cargo_collided = pygame.Rect.colliderect(current_player.player_interact_box, cargo_rect)

                cooker_collided = pygame.Rect.colliderect(current_player.player_interact_box, cooker_rect)

                if anchor_collided or cargo_collided or cooker_collided:
                    # press f to interact dialogu
                    if anchor_collided:
                        press_f = 'anchor'
                    elif cargo_collided:
                        press_f = 'cargo'
                    elif cooker_collided:
                        press_f = 'cooker'

                    top_left_dialogue_text_str = 'Press F to interact'
                    top_left_dialogue_txt = font.render(top_left_dialogue_text_str, True, WHITE)
                    # update dialogue if not the priority dialogue
                    '''if top_left_dialogue_text_str != 'Press F to interact' and top_left_dialogue_text_str != 'CAN\'T CAST ROD BEHIND YOU':
                        top_left_dialogue_txt = font.render('Press F to interact', True, WHITE)'''

                else:
                    press_f = None
            else:
                anchor_up.draw(SCREEN, 160,140)
                # check if player is colliding
                # selecting the first frame since that is a pygame surface
                anchor_collided = pygame.Rect.colliderect(current_player.player_interact_box, anchor_rect)

                if anchor_collided:
                    # press f to interact dialogue
                    press_f = 'anchor'
                    #SCREEN.blit(pressf_txt, (0,0))
                    top_left_dialogue_text_str = 'Press F to interact'
                    top_left_dialogue_txt = font.render(top_left_dialogue_text_str, True, WHITE)

                else:
                    press_f = None

            if in_hand == 'fishing pole' and anchored:
                # display and logic for the fishing pole
                fishing_pole_in_hand_logic()
            else:
                in_hand = None

            # check for collisions for mouse on pack
            # displaying the cards


            if player_pack_rect.collidepoint(mouse_pos):
                # make the inventory go out and back in
                # fix to make space
                for card in inventory.items:
                    if type(inventory.items.get(card)) != str:

                        endx = (playerx - (card*25)) -5
                        endy = playery+90

                        card_info = inventory.items.get(card)



                        if card_info.get('x') + playerx > endx:
                            card_info['x'] -= 1
                        # drawing under pack
                        # making the inventory cards viewable
                        show_card(card_info, playerx + card_info.get('x'), endy, 0.1)

                        open_inventory = True

            else:
                endy = playery+90
                for card in inventory.items:
                    card = inventory.items.get(card)
                    if type(card) == str:
                        break
                    if card['x'] + playerx < playerx+5:
                        card['x'] += 1
                        show_card(card, playerx + card['x'], endy, 0.1)

                # resetting it
                open_inventory = False


            # backpack under player
            player_pack_x = playerx + 7 if not facing_left else playerx + 27
            player_pack_y = playery + 80
            player_pack.draw(SCREEN, player_pack_x, player_pack_y, facing_left)
            player_pack_rect.topleft = (player_pack_x, player_pack_y)

            # draw the player
            current_player.draw(SCREEN, playerx, playery, facing_left)

            # DRAW UI
            wood_panel_UI.draw(SCREEN, 0, 400)
            coins_txt = ui_font.render(f'{dabloons}', True, YELLOW)
            next_dest_txt = ui_font.render(f'NEXT DEST. {next_dest} NM', True, BROWN)
            health_txt = ui_font.render(f'HEALTH {health}%', True, RED)
            hunger_txt = ui_font.render(f'HUNGER {hunger}%', True, BROWN)
            thirst_txt = ui_font.render(f'THIRST {thirst}%', True, OCEAN_BLUE)
            tiredness_txt = ui_font.render(f'TIREDNESS {tiredness}%', True, GRAY)
            mapui.draw()

            draw_ship_marker()

            if flag:
                green_flag.draw(SCREEN, flagx, flagy-40)
                green_flag.update()

            SCREEN.blit(coins_txt, (870, 10))
            SCREEN.blit(next_dest_txt, (20,455))
            SCREEN.blit(health_txt, (400,410))
            SCREEN.blit(hunger_txt, (400,455))
            SCREEN.blit(thirst_txt, (700,410))
            SCREEN.blit(tiredness_txt, (700,455))
            coin.draw(SCREEN, 950, 5)

            if open_cargo:
                #clicked = btn.rect.collidepoint(mouse_pos)
                #cargo_slot1.on_click(events, cargo_item_clicked, (1,))

                # DISPLAY INVENTORY HERE
                display_inventory_slots('player')
                display_inventory_slots('cargo')

                # when each slot is being held down

                # for the cargo slots
                # iterate over each
                for i in range(1, 6):
                    # execute for each variable to define the onhold function
                    exec(f'cargo_slot{i}.on_hold(pygame.mouse.get_pressed(), mouse_pos, cargo_item_clicked, args=({i},))')
                    exec(f'player_slot{i}.on_hold(pygame.mouse.get_pressed(), mouse_pos, player_item_clicked, args=({i},))')

                draw_player_slots()
                draw_cargo_slots()

            if cooker_open:
                # open the cooker UI
                # slot for adding fish and slot for adding boot or newspaper
                # display inventory slots as well
                # dragging and dropping
                # 60 sec cook time

                # display inventory
                display_inventory_slots('player')

                display_cooker_slots()
                cooker_fuel_btn.on_hold(pygame.mouse.get_pressed(), mouse_pos, cooker_btn_held, args=('fuel',))
                cooker_food_btn.on_hold(pygame.mouse.get_pressed(), mouse_pos, cooker_btn_held, args=('food',))

                for i in range(1,6):
                    exec(f'player_slot{i}.on_hold(pygame.mouse.get_pressed(), mouse_pos, player_item_clicked, args=({i},))')

                draw_player_slots()



            # display top left corner dialogue
            SCREEN.blit(top_left_dialogue_txt, (0,0))
            # reset display for reoccurring updated texts
            if top_left_dialogue_text_str == 'Press F to interact':
                top_left_dialogue_text_str = ''
                top_left_dialogue_txt = font.render(top_left_dialogue_text_str, True, WHITE)

            # CATCHING FISH UI
            if time_left_til_catch == 0 and rod_cast:
                # show the challenge to get the fish
                if not green_square_width:
                    green_square_width = random.randint(10,100)

                if not reel_sfx:
                    reel_sfx = sounds.reel()

                catch_fish_ui(green_square_width, hook_speed)

            # displaying the caught fish card
            if display_card:
                # if it dont return false
                try:
                    reel_sfx.stop()
                    reel_sfx = None
                except:
                    pass
                a, r = show_card(item, 350, 100)
                if a:
                    _, eat_btn_rect = show_card(item, 350, 100, new=True)

            # update display
            pygame.display.flip()

            # reset tick
            clock_tick = False

            clock.tick(60)

    elif current_screen == 'island':
        in_island = True

        while in_island:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    in_island = False
                    pygame.quit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        in_island = False
                        current_screen = "game"





    elif current_screen == 'home':
        home = True

        sounds.badadadink()

        reelit_logo = sprites.Sprite('Sprites/reelit.png', 100, 100, 3.5)

        # y offset
        y = 0
        # speed and direction
        dy= 0.5

        play = sprites.Button_UI('Play', 150, 50, OCEAN_BLUE, font_name='Font/slkscr.ttf', font_size=40)

        while home:
            # absolutely grotesquely clean way
            # to apply floating effect on logo
            y += dy
            dy *= -1 if not -10 < y < 15 else 1

            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    home = False

            SCREEN.fill(OCEAN_BLUE)

            # home screen drawing
            reelit_logo.draw(SCREEN, center_x(reelit_logo.frames[0]), 0 - y)

            # OPTIONS
            play.draw(SCREEN, 410, 300)

            # the opposite of play since it returns true when clicked
            home = not play.is_clicked(events, pygame.mouse.get_pos())

            if home:
                current_screen = 'game'

            # FOOTER
            footer1 = footer_font.render(f'© 2025 LoSoft Productions . All rights reserved. Version {VERSION}', False, WHITE)
            SCREEN.blit(footer1, (center_x(footer1), 480))

            # update display
            pygame.display.flip()

            # reset tick
            clock_tick = False

            clock.tick(60)


pygame.quit()
sys.exit()
import importlib
import pygame
import math
import numpy
import sounds

islands = [
    "Kali Cove",
    "Azurewind Isle",
    "Crescent Palm Island",
    "Whispering Reef",
    "Emerald Shoal",
    "Solara Key",
    "Moonpetal Isle",
    "Coralheart Island",
    "Driftwood Haven",
    "Sapphire Bay Isle",
    "Thornbloom Cay",
    "Starwake Atoll",
    "Golden Lantern Isle",
    "Stormcradle Island",
    "Pearlstrand Key",
    "Tidewhisper Isle",
    "Crystal Drum Island",
    "Emberfin Cay",
    "Seafarer's Rest",
    "Mistveil Island",
    "Sunspire Shoal",
    "Willowtide Isle",
    "Blue Ember Atoll",
    "Sandstone Harbor Island",
    "Silverpeak Cay",
    "Seraph Shore",
    "Humming Gull Isle",
    "Rosewater Island",
    "Brinecrest Key",
    "Duskveil Isle",
    "Hidden Lantern Atoll",
    "Opalreef Island",
    "Windpetal Cay",
    "Sunblossom Isle",
    "Cragwhisper Key",
    "Nightglow Island",
    "Seamist Haven",
    "Coralvine Isle",
    "Gleamwater Cay",
    "Skybreaker Island",
    "Mariners' Moon Key",
    "Sirenfall Isle",
    "Brightglass Shoal",
    "Willowfoam Island",
    "Firecrest Cay",
    "Eastwind Atoll",
    "Palmshadow Isle",
    "Driftglade Key",
    "Tidebound Island",
    "Howling Lantern Cay",
    "Sunsilk Isle",
    "Coralwhisper Haven",
    "Jadeflare Shoal",
    "Moonshadow Atoll",
    "Dappled Reef Island",
    "Brineflower Cay",
    "Nightreef Isle",
    "Sunmeadow Island",
    "Saltpetal Key",
    "Horizon Pearl Isle",
    "Sablewind Cay",
    "Frosttide Island",
    "Silverleaf Key",
    "Evermist Isle",
    "Blue Lantern Cay",
    "Brightshore Atoll",
    "Coralspire Island",
    "Lanternwake Key",
    "Starbloom Isle",
    "Saltwind Haven",
    "Firepetal Atoll",
    "Quiet Harbor Isle",
    "Tideglass Cay",
    "Whisperfall Island",
    "Honeybay Key",
    "Opalstrand Isle",
    "Reefdream Cay",
    "Suncrest Island",
    "Driftfire Key",
    "Windblossom Isle",
    "Mooncrown Cay",
    "Sapphire Lantern Island",
    "Gullsway Key",
    "Tideglen Isle",
    "Coralshade Cay",
    "Brinelight Atoll",
    "Dawntree Island",
    "Pearlwind Key",
    "Shadowglen Isle",
    "Saltspire Cay",
    "Emberwake Island",
    "Seacrown Key",
    "Whisperfoam Isle",
    "Deeprose Cay",
    "Stormbay Island",
    "Lilypad Key",
    "Bluewhisper Isle",
    "Goldenbloom Cay",
    "Driftshore Island",
    "Sunspring Key"
]


class Sprite:
    def __init__(self, sprite_sheet_path, frame_width, frame_height, scale=2, y=0):
        """
        Initializes a sprite with a sprite sheet.

        :param sprite_sheet_path: Path to the sprite sheet image.
        :param frame_width: Width of each frame in the sprite sheet.
        :param frame_height: Height of each frame in the sprite sheet.
        :param scale: Scale factor for the sprite frames.
        :param y: How far from the top your frame is
        """
        self.sprite_sheet = pygame.image.load(sprite_sheet_path)#.convert_alpha()
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.scale = scale
        self.y = y
        self.frames = self.load_frames()
        self.current_frame = 0
        self.animation_speed = 10  # Adjust speed of animation (higher is slower)
        self.counter = 0

        self.posx = 0
        self.posy = 0

        self.rectangle = self.frames[0].get_rect(topleft=(0, 0))

    def change_posx(self, newx):

        self.posx = newx

        self.rectangle.x = newx

    def change_posy(self, newy):

        self.posy = newy

        self.rectangle.y = newy


    def load_frames(self):
        """
        Extracts and scales all frames from the sprite sheet.
        """
        frames = []
        sheet_width = self.sprite_sheet.get_width()
        for frame in range(math.ceil(sheet_width / self.frame_width)):#range(0,5): #range(sheet_width // self.frame_width):
            img = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            img.blit(self.sprite_sheet, (0, 0), (frame * self.frame_width, self.y, self.frame_width, self.frame_height))
            img = pygame.transform.scale(img, (self.frame_width * self.scale, self.frame_height * self.scale))
            frames.append(img)
        return frames

    def update(self):
        """
        Updates the current frame for animation.
        """
        self.counter += 1
        if self.counter >= self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.counter = 0

    def draw(self, screen, x, y, invert_h=False, invert_v=False):
        frame = self.frames[self.current_frame]

        if invert_h or invert_v:
            frame = pygame.transform.flip(frame, invert_h, invert_v)

        # get the sprite rect at (x, y)
        sprite_rect = frame.get_rect(topleft=(x, y))

        # center your rectangle on the sprite
        self.rectangle.center = sprite_rect.center

        screen.blit(frame, sprite_rect)


    def pg_surface(self) -> pygame.surface:
        # accepts no arguments
        # returns the pygame surface for the current frame
        return self.frames[self.current_frame]

    def tint(self, tint_color):
        # tint the image

        for i, frame in enumerate(self.frames):
            tinted = frame.copy()
            tint = pygame.Surface(frame.get_size()).convert_alpha()
            tint.fill(tint_color)
            tinted.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            self.frames[i] = tinted


class Player:
    def __init__(self, sprite_sheet_path, frame_width, frame_height, scale=2, y=0, PLAYER_INTERACT_BOX_OFFSETX = 0, PLAYER_INTERACT_BOX_OFFSETY = 0):
        """
        Initializes a sprite with a sprite sheet.

        :param sprite_sheet_path: Path to the sprite sheet image.
        :param frame_width: Width of each frame in the sprite sheet.
        :param frame_height: Height of each frame in the sprite sheet.
        :param scale: Scale factor for the sprite frames.
        :param y: How far from the top your frame is
        """
        self.sprite_sheet = pygame.image.load(sprite_sheet_path)#.convert_alpha()
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.scale = scale
        self.y = y
        self.frames = self.load_frames()
        self.current_frame = 0
        self.animation_speed = 10  # Adjust speed of animation (higher is slower)
        self.counter = 0

        # player x and y unset
        # this is just setting the player interact box globally
        self.PLAYER_INTERACT_BOX_OFFSETX = PLAYER_INTERACT_BOX_OFFSETX
        self.PLAYER_INTERACT_BOX_OFFSETY = PLAYER_INTERACT_BOX_OFFSETY
        self.player_interact_box = pygame.rect.Rect(0 + PLAYER_INTERACT_BOX_OFFSETX, 0 + PLAYER_INTERACT_BOX_OFFSETY,10,20)

        # feet for collisions
        self.player_feet_box = pygame.rect.Rect(0, 100, 10,20)

    def load_frames(self):
        """
        Extracts and scales all frames from the sprite sheet.
        """
        frames = []
        sheet_width = self.sprite_sheet.get_width()
        for frame in range(math.ceil(sheet_width / self.frame_width)):#range(0,5): #range(sheet_width // self.frame_width):
            img = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            img.blit(self.sprite_sheet, (0, 0), (frame * self.frame_width, self.y, self.frame_width, self.frame_height))
            img = pygame.transform.scale(img, (self.frame_width * self.scale, self.frame_height * self.scale))
            frames.append(img)
        return frames

    def update(self):
        """
        Updates the current frame for animation.
        """
        self.counter += 1
        if self.counter >= self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.counter = 0

    def draw(self, screen, x, y, invert_h = False, invert_v = False):
        """
        Draws the current frame at the specified position.

        :param screen: The pygame screen surface.
        :param x: X-coordinate to draw the sprite.
        :param y: Y-coordinate to draw the sprite.
        :param invert_h: inverts horizontally if true
        :param invert_v: inverts vertically if true
        """

        # updating the interaction box
        self.player_interact_box = pygame.rect.Rect(x + self.PLAYER_INTERACT_BOX_OFFSETX, y + self.PLAYER_INTERACT_BOX_OFFSETY,10,20)

        self.player_feet_box = pygame.rect.Rect(x+30, y+170, 40, 10)
        #pygame.draw.rect(screen, (255,255,255), self.player_feet_box)

        frame = self.frames[self.current_frame]

        # if any are selected to be inverted then flip it
        if invert_h or invert_v:
            frame = pygame.transform.flip(self.frames[self.current_frame], invert_h, invert_v)

        screen.blit(frame, (x, y))


    def pg_surface(self) -> pygame.surface:
        # accepts no arguments
        # returns the pygame surface for the current frame
        return self.frames[self.current_frame]

import pygame

class Button_UI:
    def __init__(self, text: str, width: int | float, height: int | float, bg: tuple,
                 custom_img_path: str = None, font_name=None, font_size=24):
        # Initializes button and customizations
        self.text = text
        self.custom_img_path = custom_img_path
        self.width = width
        self.height = height
        self.bg = bg  # base color (if no custom image)

        # default colors
        self.WHITE = (255, 255, 255)
        self.GRAY = (180, 180, 180)
        self.DARKEN_FACTOR = 0.85  # how much darker when hovering

        # load font
        self.font = pygame.font.Font(font_name, font_size)

        # load image (if any)
        self.image = None
        if custom_img_path:
            self.image = pygame.image.load(custom_img_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

        # text surface
        self.text_surface = self.font.render(self.text, True, self.WHITE)

        # rect placeholder
        self.rect = pygame.Rect(0, 0, self.width, self.height)

        # state tracking
        self.hovered = False
        self.clicked = False
        self.prev_hovered = False
        self.prev_held = False

    def _darken_image(self, factor):
        """
        Darkens a Pygame Surface by directly manipulating its pixel data.
        factor: A float between 0 and 1, where 0 is black and 1 is original brightness.
        """
        if self.image:
            arr = pygame.surfarray.pixels3d(self.image)
            arr = (arr * factor).astype(numpy.uint8)
            pygame.surfarray.blit_array(self.image, arr)


    def draw(self, screen, x, y):
        """Draws the button at (x, y) and updates hover state."""
        self.rect.topleft = (x, y)

        mouse_pos = pygame.mouse.get_pos()

        self.hovered = self.rect.collidepoint(mouse_pos)

        if not self.prev_hovered and self.hovered:
            # keep the soudn effect from repeatedly playing
            sounds.menubum()

        self.prev_hovered = self.hovered


        # Draw base
        if self.image:
            # if custom image, draw that (maybe tint if hovered)
            img = self.image.copy()
            if self.hovered:

                # apply darken effect
                dark = pygame.Surface(img.get_size(), pygame.SRCALPHA)
                dark.fill((0, 0, 0, int(255 * (1 - self.DARKEN_FACTOR))))
                img.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
                #self._darken_image(0.1)
            screen.blit(img, self.rect.topleft)
        else:
            # simple colored rectangle
            color = self.on_hover() if self.hovered else self.bg
            pygame.draw.rect(screen, color, self.rect, border_radius=8)

        # Draw text centered
        text_rect = self.text_surface.get_rect(center=self.rect.center)
        screen.blit(self.text_surface, text_rect)

    def is_clicked(self, events, mouse_pos):
        """Checks if button was just clicked. Pass in pygame.event.get()."""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(mouse_pos):
                sounds.buttonclicked()
                return True
            return False

    def on_hover(self):
        """Return a darker version of the button’s base color."""
        r, g, b = self.bg
        return (int(r * self.DARKEN_FACTOR), int(g * self.DARKEN_FACTOR), int(b * self.DARKEN_FACTOR))

    def on_hold(self, mouse_buttons, mouse_pos, funct, args:tuple = None):
        """Checks if the button is being held down """

        if mouse_buttons[0] and self.rect.collidepoint(mouse_pos):
            if not self.prev_held:
                sounds.pop()
                self.prev_held = True

            if args:
                #      test(a,b,c)
                funct(*args)

            else:
                funct()
        else:
            self.prev_held = False

    def on_click(self, event_list, mouse_pos,funct, args: tuple = None):
        """Runs a custom function when button is clicked."""
        if self.is_clicked(event_list, mouse_pos):
            if args:
                #      test(a,b,c)
               funct(*args)

            else:
                funct()

            return True

        return False


    def change_bg(self, filepath):
        # changes the background to an img

        # load image (if any)
        self.image = pygame.image.load(filepath).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))


class Map_UI:
    def __init__(self, screen):
        # this is for managing the map look and parameters
        # to anything map related

        self.random = importlib.import_module('random')

        # setting up all of the vars
        self.x = 750
        self.y = 150
        self.width = 100
        self.height = 100

        self.screen = screen

        self.ISLANDS_RANGE = (2,3) # tuple ranging least (incl) to highest (nonincl) amount of islands possible

        self.bg_path = 'Sprites/map-paper.png'
        self.map_paper_sprite = Sprite(self.bg_path, self.width, self.height, 2.5)
        self.map_paper_sprite_surface = self.map_paper_sprite.frames[0]

    def generate_map(self):
        # this is for generating all randomized parameters

        low = self.ISLANDS_RANGE[0]
        high = self.ISLANDS_RANGE[1]

        # generates how many islands will be in the world
        self.island_amount = self.random.randint(low, high)
        print(self.island_amount)

        self.island_sprite_list = []

        self.island_name_list = []

        for _ in range(self.island_amount):
            # generating random island
            island_num = self.random.randint(1, 9)
            island_sprite = Sprite(f'Sprites/islands/island{island_num}.png', 100, 100, 0.8)

            # gen. random position for each island
            # making giving a 10 px  padding

            #x = self.random.randint(20,90)
            #y = self.random.randint(20, 180)

            # NEW WAY
            # spawn all islands on top of eachother
            # than randomly spread them out until
            # no collisions exist
            x = 100
            y = 100

            island_sprite.change_posx(x)
            island_sprite.change_posy(y)

            # adding to island list
            self.island_sprite_list.append(island_sprite)
            self.island_name_list.append(self.random.choice(islands))

            island_sprite.rectangle.inflate_ip(-40, -40)


    def resolve_island_overlap(self):
        # this will fix coordinates of overlapping islands
        for i, island in enumerate(self.island_sprite_list):
            island_rect = island.frames[0].get_rect(topleft=(island.posx, island.posy))

            for j, island2 in enumerate(self.island_sprite_list):
                # dont compare same islands
                if i == j:
                    continue

                island2_rect = island2.frames[0].get_rect(topleft=(island2.posx, island2.posy))

                # if they are colliding
                if island_rect.colliderect(island2_rect):
                    while True:

                        if not island_rect.colliderect(island2_rect):
                            island2.change_posx(x)
                            island2.change_posy(y)

                            # re check so there was no new overlapping
                            # islands
                            self.resolve_island_overlap()
                            break
                        x = self.random.randint(20,90)
                        y = self.random.randint(20, 180)
                        island2_rect.topleft = (x, y)


    def draw(self):
        # draws the map and since the location
        # on the screen shouldnt change there is a global x and y
        ui_font = pygame.font.Font('Font/slkscr.ttf', 10)
        self.map_paper_sprite.draw(self.screen, self.x, self.y)

        for i, island in enumerate(self.island_sprite_list):


            island.draw(self.screen, island.posx + self.x, island.posy + self.y-30)

            island_txt = ui_font.render(self.island_name_list[i], True, (255,255,255))

            self.screen.blit(island_txt, (island.posx + self.x, island.posy + self.y))

            #pygame.draw.rect(self.screen, (0,0,0), island.rectangle)

'''
Sprites are 128x128px for each frame
'''
pygame.init()

def get_img(sheet, frame, width = 128, height = 128, scale = 2) -> pygame.Surface:
    img = pygame.Surface((width, height), pygame.SRCALPHA)
    img.blit(sheet, (0,0), (frame*width, 0, width, height))
    img = pygame.transform.scale(img, (width * scale, height * scale))
    return img

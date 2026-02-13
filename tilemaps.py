import sprites

# sprites and sprite map

gravel_sprite = sprites.Sprite('Sprites/newgrass.png', 128, 128, 1 )
gravel_sprite_bg = sprites.Sprite('Sprites/newgrass.png', 128, 128, 9 )

# island sprites
dirt_sprite = sprites.Sprite('Sprites/dirt.png', 147, 77, 1 )
house = sprites.Sprite('Sprites/house.png', 200, 200, 1)
fish = sprites.Sprite('Sprites/fish.png', 128, 72, 1)
oak_tree = sprites.Sprite('Sprites/oaktree.png', 178, 150, 1)
inn = sprites.Sprite('Sprites/inn.png', 128, 158, 1)
villa = sprites.Sprite('Sprites/villa.png', 231, 190, 1)
tavern = sprites.Sprite('Sprites/tavern.png', 231, 190, 1)
thatched = sprites.Sprite('Sprites/thatched.png', 128, 190, 1)
chapel = sprites.Sprite('Sprites/chapel.png', 128, 197, 1)
clock = sprites.Sprite('Sprites/clock.png', 128, 243, 1)

tiles = [gravel_sprite, house, fish, oak_tree, inn, villa, tavern, thatched, chapel, clock]

# tile maps
town1 = [
            [1,1,1,1,1,1,4,1,1],
            [2,10,2,1,1,1,1,4,1],
            [1,1,1,1,1,6,4,1,1],
            [1,1,1,1,1,1,4,1,1],
            [8,1,2,1,4,1,4,4,1],
            [1,1,1,1,1,4,4,1,1],
            [1,1,1,3,1,4,1,1,1],
            [1,1,1,1,4,1,4,1,1],
            [1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1],


        ]

town1_invert_h = [
    [0,0, 0,0,0,0,0,0,0],
    [1,0, 0,0,0,0,0,0,0],
    [0,0, 1,0,0,1,0,0,0],
    [0,0, 0,0,0,0,0,0,0],
    [0,0, 1,0,0,0,0,0,0],
    [0,0, 0,0,0,0,0,0,0],
    [0,0, 0,0,0,0,0,0,0],
    [0,0, 0,0,0,0,0,0,0],
    [0,0, 0,0,0,0,0,0,0],
    [0,0, 0,0,0,0,0,0,0],
    [0,0, 0,0,0,0,0,0,0],
    [0,0, 0,0,0,0,0,0,0],
    [0,0, 0,0,0,0,0,0,0],
    [0,0, 0,0,0,0,0,0,0],
    [0,0, 0,0,0,0,0,0,0],
]

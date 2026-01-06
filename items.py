from pydoc import classname
import random
import json
import importlib

COMMON_CHANCE = 55
UNCOMMON_CHANCE = 80
RARE_CHANCE = 97
LEGENDARY_CHANCE = 101

with open('fishables.json', 'r') as f:
    fishables = json.load(f)

class Items:
    # just a class for organizing buyable items
    def __init__(self):
        with open('items.json', 'r') as f:
            # loading in all of the items you can purchase and upgrade
            # and own
            self.items = json.load(f)


    def get_cargo(self, name = None) -> dict:
        # returns a dict of the cargo
        # or a certain type of cargo

        if not name:
            return self.items['cargo_boxes']

        return self.items['cargo_boxes'].get(name)


def roll() -> dict:
    # this rolls to pick depending on a certain percent chance
    # very simple and im still trying to figure out a more
    # mathmatical approach
    # roll
    roll_num = random.randint(1,100)
    #print(roll_num)
    if roll_num < COMMON_CHANCE:
        # select a common at random
        item =  random.choice(fishables['Common'])
        item['rarity'] = 'Common'

    elif roll_num < UNCOMMON_CHANCE:
        # select random uncommon
        item = random.choice(fishables['Uncommon'])
        item['rarity'] = 'Uncommon'

    elif roll_num < RARE_CHANCE:
        # select a rare
        item = random.choice(fishables['Rare'])
        item['rarity'] = 'Rare'

    elif roll_num < LEGENDARY_CHANCE:
        # select legendary
        # ~2% chance

        # roll again
        roll_num = random.randint(1,100)
        #print('Second roll:', roll_num)
        # if the roll is an uncommon the second time
        # then it will be a legendary
        if roll_num > UNCOMMON_CHANCE:
            item = random.choice(fishables['Legendary'])
            item['rarity'] = 'Legendary'

        # its otherwise a common
        else:
            item = random.choice(fishables['Common'])
            item['rarity'] = 'Common'

    return item

class Inventory:
    def __init__(self, capacity: int):
        # creates empty inventory
        # returns snothing
        self.items = {}
        self.items_list = []
        for i in range(capacity):
            self.items[i+1] = ''

        self.capacity = capacity

    def add_item(self, item: dict, slot:int) -> bool:
        """
        Adds item to the inventory
        returns a boolean of whether or not it was successful
        True if not successful

        :param item: dictionary of the item
        :param slot: item slot
        """

        # will fail if slot is occupied as well
        if len(self.items_list) == self.capacity or self.items[slot]:
            # capacity already met
            return True

        self.items[slot] = item
        self.items_list.append(item)

        return False

    def remove_item(self, item: dict) -> bool:
        # removes the item from inventory

        for t in self.items:
            if self.items.get(t) == item:
                self.items[t] = ''
                self.items_list.remove(item)
                # shift items down a slot
                for t in self.items:
                    if not self.items[t]:
                        try:
                            # trigger item in front to go back a slot
                            self.items[t] = self.items[t+1]
                            self.items[t+1] = ''

                        except:
                            break

                return False

        return False

    def transfer_items(self, inventory) -> None:
        #shouldve been called transfer_inventory_items
        # inherets all items from the inventory passed through
        # over writes anything if its already in this inventory

        self.items = inventory.items

    def transfer_item(self, inventory, index_from, index_to) -> None:
        # shouldve been called transfer_item!s!
        # inherets specific index of item from the inventory
        # either adding or swapping
        # index_from: the index to inheret
        # index_to: where to insert in this inventory

        if self.items.get(index_to) and inventory.items.get(index_from):
            # both slots occupied; swap

            # item in self inventory
            s_item = self.items.get(index_to)

            # incoming item
            i_item = inventory.items.get(index_from)

            # delete the items in both inventories and lists
            self.items[index_to] = ""
            self.items_list.remove(s_item)
            inventory.items_list.append(s_item)
            inventory.items[index_from] = ""
            inventory.items_list.remove(i_item)
            self.items_list.append(i_item)
            # initiate swap
            self.items[index_to] = i_item
            inventory.items[index_from] = s_item

        elif inventory.items.get(index_from):
            # transfer

            # incoming item
            i_item = inventory.items.get(index_from)

            # other item
            #s_item = self.items.get(index_to)

            # delete it
            inventory.items[index_from] = ""
            inventory.items_list.remove(i_item)
            self.items_list.append(i_item)

            # transfer to new isnventory
            self.items[index_to] = i_item

        else:
            # this is in the case that you dragged an empty
            # slot to an occupied space or emtpy space
            # in which case nothing will happen
            pass

'''# restore the random module's functions in case random.seed was overwritten earlier
importlib.reload(random)

max_attempts = 100000000
seed = 10000000
found = False

while seed < max_attempts:
    random.seed(seed)
    result1 = roll()
    result2 = roll()
    result3 = roll()
    result4 = roll()
    result5 = roll()
    result6 = roll()
    result7 = roll()
    result8 = roll()
    result9 = roll()
    result10 = roll()

    if result1.get('rarity') == 'Legendary' and result2.get('rarity') == 'Legendary' and result3.get('rarity') == 'Legendary' and result4.get('rarity') == 'Legendary' and result5.get('rarity') == 'Legendary' and result6.get('rarity') == 'Legendary' and result7.get('rarity') == 'Legendary' and result8.get('rarity') == 'Legendary' and result9.get('rarity') == 'Legendary' and result10.get('rarity') == 'Legendary':
        print('Legendary found  in first 10 rolls with seed', seed)
        found = True

    seed += 1

if not found:
    print('Legendary not found in', max_attempts, 'attempts')'''


#Legendary found  in first 3 rolls with seed 2042157
#Legendary found  in first 3 rolls with seed 2133653
#Legendary found  in first 3 rolls with seed 3096434
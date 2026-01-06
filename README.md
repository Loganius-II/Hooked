# ⚓ Reel It! (Pygame)

A 2D survival / fishing game built with **Python** and **Pygame**. The game focuses on inventory management, fishing mechanics, cooking, and exploration while surviving hunger, thirst, and tiredness on a small raft.

This README gives a **high-level overview** of the project structure and explains what each main file does without going too deep into implementation details.

---

## 📁 Project Structure

```
main.py
items.py
sprites.py
mathmatics.py
Sprites/
├─islands/
├─...png
├─...
Font/
├─slkscr.ttf
MusicAndFX/
requirements.txt
todo.txt
items.json
fishables.json
```

---

## 🧠 main.py

**Main game entry point and core game loop**.

This file:

* Initializes **Pygame**, the window, fonts, colors, and global game state
* Handles the **main game loop** and event processing
* Manages player movement, animations, and interactions
* Controls game systems such as:

  * Fishing mechanics (casting, bob physics, catch minigame)
  * Inventory UI (player inventory, cargo inventory, drag & drop)
  * Cooking system (fuel + food → cooked item)
  * Survival stats (health, hunger, thirst, tiredness)
* Draws all UI elements (HUD, inventory cards, dialogue text)
* Coordinates interactions between all other modules

In short: **this is where everything comes together**.

---

## 🎒 items.py

**Item definitions, loot rolling, and inventory logic**.

This file contains:

### `Items` class

* Loads item and cargo data from `items.json`
* Provides access to cargo box definitions

### `roll()` function

* Handles random loot rolls when fishing
* Uses rarity thresholds:

  * Common
  * Uncommon
  * Rare
  * Legendary
* Pulls fish/item data from `fishables.json`

### `Inventory` class

* Manages inventory slots and capacity
* Supports:

  * Adding items
  * Removing items
  * Transferring items between inventories
  * Swapping items between slots

This module keeps **game logic clean** by separating item rules from gameplay code.

---

## 🎨 sprites.py

**Rendering, animation, UI components, and map generation**.

This is a large utility file responsible for visuals and UI behavior.

### `Sprite` class

* Handles sprite sheets and frame-based animation
* Supports scaling, flipping, tinting, and frame updates

### `Player` class

* Specialized animated sprite for the player
* Manages interaction hitboxes and collision areas

### `Button_UI` class

* Reusable UI button system
* Supports:

  * Custom images or colored buttons
  * Hover effects
  * Click and hold detection
  * Drag-and-drop style interactions

### `Map_UI` class

* Generates a small randomized world map
* Randomly places islands
* Resolves island overlap
* Displays island sprites and names

This file is essentially the **visual backbone** of the game.

---

## 📐 mathmatics.py

**Small math utility functions used throughout the game**.

Includes:

* `two_point_angle()` – Calculates the angle between two points (used for fishing line rotation)
* `two_point_distance()` – Calculates distance between two points
* `coordinate_range_x()` – Checks if an X coordinate falls within a given range

These helpers keep math logic isolated and reusable.

---

## 🎮 Key Features

* Fishing with physics-based casting
* Timing-based catch minigame
* Item rarity system
* Player & cargo inventories
* Drag-and-drop inventory UI
* Cooking system with fuel + food
* Survival mechanics (hunger, thirst, tiredness)
* Animated sprites and UI
* Procedurally generated map preview

---

## ▶️ Running the Game

Make sure you have Python and Pygame installed:

```bash
(python3 -m) pip install -r requirements.txt
```

Then run:

```bash
python main.py
```

---

## 🛠 Notes

* The project is **work-in-progress** and intentionally experimental
* Some systems favor flexibility over strict structure
* Global state is used heavily for rapid iteration

---

## ✨ Credits

* Game & Programming: **Logan McDermott**
* Graphics: **Logan McDermott**, **Sevarihk**

---

Feel free to expand this README as systems stabilize or the project grows 🚀

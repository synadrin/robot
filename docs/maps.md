# Maps

All maps are made in [Tiled](http://www.mapeditor.org/).

## Layers

All characters (`player`, `npc`, `enemy`) are drawn on the third
layer from the bottom.
The bottom two layers are always behind characters.

## Objects

Objects represent characters, walls, and triggers in the map.
Generally, these are just rectangles in Tiled, with certain
properties.

### Properties

* `Name` - The name of the object. This usually matches a resource filename.
* `Type` - The type of object. See below for accepted types.
* Custom Properties - These are specific to certain types.
    * `entrance_name`
    * `map_name`
    * `message_text`
    * `on_enter`
    * `on_exit`
    * `on_interact`
    * `target_x`
    * `target_y`

### Object Types

* `wall` - An area which cannot be walked through.

    Additional properties: none

* `npc` - An NPC (non-player character).

    Additional properties:

    * `Name` - Used to load the resource file: `data/c_NAME.json`
    * `on_interact` - Action to perform when the player interacts
      with the NPC.
    * `target_x` - The X value of the NPC's path destination on the
      map grid.
    * `target_y` - The Y value of the NPC's path destination on the
      map grid.

* `enemy` - An Enemy.

    Additional properties:

    * `Name` - Used to load the resource file: `data/c_NAME.json`
    * `on_interact` - Action to perform when the player interacts
      with the NPC.
    * `target_x` - The X value of the NPC's path destination on the
      map grid.
    * `target_y` - The Y value of the NPC's path destination on the
      map grid.

* `trigger` - A trigger: something with which the player can
  interact.

    Additional properties:

    * `on_enter` - Performs the named `action` when the player steps
      into this space (**not implemented**).
    * `on_exit` - Performs the named `action` when the player steps
      out of this space (**not implemented**).
    * `on_interact` - Performs the named `action` when the player
      faces the object and presses the interaction key.

* `entrance` - Defines a location where a player can start when this
  map is loaded.

    * Special: Name: `player_start` - Default starting spot.

### Actions

* `dialogue` - TODO
* `message` - Displays the contents of `message_text` custom property.
* `load_map` - Loads the map given in `map_name` and places the
  player at the `entrance` named `entrance_name`.

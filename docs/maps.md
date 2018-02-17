# Maps

All maps are made in [Tiled](http://www.mapeditor.org/).

## Layers

All characters (`player`, `npc`, `enemy`) are drawn on the third
layer from the bottom.
The bottom two layers are always behind characters.

## Objects

### Properties

* `Name`
* `Type`
* Custom Properties:
    * `entrance_name`
    * `map_name`
    * `message_text`
    * `on_enter`
    * `on_exit`
    * `on_interact`

### Types

* `wall`
* `npc`
* `enemy`
* `trigger`
    * `on_enter` - TODO: not implemented
    * `on_exit` - TODO: not implemented
    * `on_interact`
* `entrance`
    * Special: Name: `player_start`

### Actions

* `message` - Displays the contents of `message_text` custom property.
* `load_map` - Loads the map given in `map_name` and places the
  player at the `entrance` named `entrance_name`.

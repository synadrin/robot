# Maps

All maps are made in [Tiled](http://www.mapeditor.org/).

## Layers

All characters (`player`, `npc`, `enemy`) are drawn on the third
layer from the bottom.
The bottom two layers are always behind characters.

## Objects

### Properties

`Name`
`Type`
Custom Properties

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

* `message`
* `load_map` - TODO: not implemented

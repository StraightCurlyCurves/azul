# Changelog

## [1.1.0] - 2024-03-28
### Added
- Introduced a new optional parameter, `show_bag_tiles`, to both the constructor of the `PlayAzul` class and the `print_state` method of the `Azul` class. This parameter allows users to control whether the bag tiles should be displayed with their respective color and color ID or just as grey 'X's, since in a 'real' game it is not possible to see the content of the bag. The parameter is set to False by default.

### Removed
- Removed the variables `self.__show_bots_move` and `self.__save_history` from the `PlayAzul` class, as they remain constant during a game and are unnecessary for game reset.

### Fixed
- Corrected the import statement in `azul.py`. Previously, `GameState` was mistakenly imported from `history`. It is now correctly imported from `game_state`.

## [1.0.0] - 2024-03-27
### Added
- Initial release
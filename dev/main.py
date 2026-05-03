#! python3
"""
Entry point. Initializes GameState, prompts game selection, and runs the
main game loop. Replaces the module-level code at the bottom of games.py.
"""

from state import GameState
from worlds import load_world
from engine import (
    locale, look_around, examine_item,
    take_item, drop_item, use_item,
    show_help, show_inventory, show_intro,
    toggle_verbose, get_move, short_move, valid_move,
    select_game,
)
from combat import creature_follow, remove_creature_fatigue, player_wellness, creature_attack
from save_load import save_game, load_saved_game


def main():
    print('Welcome to TextGames!')
    print('')

    state = GameState()
    game_choice = select_game()
    state.load_world(game_choice)
    world_module = load_world(game_choice)

    print('')
    show_intro(state)
    state.last_move = ''

    while state.room != state.exit_room:
        remove_creature_fatigue(state.room, state)

        if state.player_hp <= 0:
            print('Thanks for playing!')
            print('')
            input('Press ENTER to continue... ')
            break

        if not state.locale_visited:
            locale(state.room, state, world_module)
            state.locale_visited = True

        # Player may die from a room special (e.g. bad air in world 3)
        if state.player_hp <= 0:
            print('\nThanks for playing!')
            print('')
            input('Press ENTER to continue... ')
            break

        move = get_move(state)
        state.move = move

        if not move:
            pass
        elif move in ('?', 'help'):
            show_help(state)
        elif move in ('l', 'look'):
            look_around(state.room, state)
        elif move in ('x', 'examine'):
            examine_item(state.room, state)
        elif move in ('v', 'verbose'):
            toggle_verbose(state)
        elif move == 'save':
            save_game(state)
        elif move == 'load':
            if load_saved_game(state):
                world_module = load_world(state.game_choice)
                locale(state.room, state, world_module)
        elif move == 'use':
            use_item(state.room, state, world_module)
        elif move == 'take':
            take_item(state.room, state)
            creature_attack(state.room, state)
        elif move == 'drop':
            drop_item(state.room, state)
            creature_attack(state.room, state)
        elif move in ('i', 'inv', 'inventory'):
            show_inventory(state)
        elif move in ('h', 'health'):
            player_wellness(state)
            state.last_move = move
        elif move == 'quit':
            print('Are you sure you want to quit?')
            confirm = input()
            if confirm.lower() in ('y', 'yes'):
                print('Thanks for playing!')
                print('')
                input('Press ENTER to continue... ')
                break
            else:
                print('Okay, back to it.')
        else:
            direction = short_move(move)
            if valid_move(state.room, direction, state):
                new_room = state.world[state.room]['exits'][direction]
                creature_follow(state.room, new_room, state)
                state.room = new_room
                state.locale_visited = False
            else:
                if move not in ('r', 'repeat'):
                    print("You can't go that way.")
            state.last_move = move

        print('')

    if state.room == state.exit_room:
        print(state.outro_text)
        print('')
        input('Press ENTER to continue... ')


if __name__ == '__main__':
    main()

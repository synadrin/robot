import pygame
import pyscope

from constants import *
from functions import *
import scene_manager
import menu_scene
import text_scene
import game_scene
import character


class game_engine(object):
    """ This class is a basic game.

    This class will load data, create a pyscroll group, a hero object.
    It also reads input and moves the Hero around the map.
    Finally, it uses a pyscroll group to render the map and Hero.
    """

    def __init__(self, screen):
        # true while running
        self.running = False

        # Main drawing area
        self.screen = screen

        self.scene_manager = scene_manager.scene_manager()
        start_menu = menu_scene.menu_scene(scene_manager,
            START_MENU_IMAGE, START_MENU_RECT)
        start_menu.append("New Game", True, self.new_game)
        start_menu.append("Load Game", False, None)
        start_menu.append("Credits", True, self.show_credits)
        start_menu.append("Quit", True,
            lambda: pygame.event.post(pygame.event.Event(pygame.QUIT)))

        self.scene_manager.append(start_menu)

        self.hero = None

    def new_game(self):
        self.hero = character.player(HERO_NAME)
        self.scene_manager.append(game_scene.game_scene(
            self.scene_manager,
            self
        ))
        # New game_scene with default settings

    def load_game(self, save_name):
        # Load character data from saved game
        pass

    def show_credits(self):
        credits = []
        with open(get_resource_name(CREDITS_FILE)) as f:
            credits = f.readlines()
        credits = [line.strip() for line in credits]
        message_box = (0, 0.5, 1, 0.5)
        self.scene_manager.append(
            text_scene.text_scene(
                self.scene_manager,
                credits,
                message_box
            )
        )

    def handle_input(self):
        """ Handle pygame input events
        """
        poll = pygame.event.poll
        filtered_events = []

        # Convert events to custom R_ buttons
        event = poll()
        while event:
            if event.type == pygame.QUIT:
                self.running = False
                break

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    break
                elif event.key in keyboard_map:
                    filtered_events.append(
                        pygame.event.Event(R_INPUT_EVENT,
                            button=keyboard_map[event.key])
                    )

            elif event.type == pygame.JOYBUTTONDOWN:
                # TODO: Parse joystick input
                pass

            event = poll()

        # Create dict of which R_ buttons are pressed
        pressed_keys = pygame.key.get_pressed()
        filtered_pressed_keys = {}
        for key, button in keyboard_map.items():
            if button in filtered_pressed_keys:
                if not filtered_pressed_keys[button]:
                    filtered_pressed_keys[button] = pressed_keys[key]
            else:
                filtered_pressed_keys[button] = pressed_keys[key]

        current_scene = self.scene_manager.current_scene
        if self.running and current_scene:
            current_scene.handle_input(
                filtered_events, filtered_pressed_keys
            )

    def run(self):
        """ Run the game loop
        """
        clock = pygame.time.Clock()
        self.running = True

        from collections import deque
        times = deque(maxlen=30)

        try:
            while self.running:
                dt = clock.tick(TARGET_FPS) / 1000.
                times.append(clock.get_fps())

                self.handle_input()
                self.scene_manager.update(dt)
                self.scene_manager.draw(self.screen)
                pygame.display.flip()

        except KeyboardInterrupt:
            self.running = False


def main():
    pygame.init()
    pygame.font.init()
    scope = pyscope.pyscope()
    pygame.display.set_caption(DISPLAY_NAME + ' v' + GAME_VERSION)

    try:
        game = game_engine(scope.screen)
        game.run()
    except:
        pygame.quit()
        raise


if __name__ == "__main__":
    main()

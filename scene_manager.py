# Scene class components:
# .manager
# .pause()
# .resume()
# .handle_input(events, pressed_keys)
# .update(dt)
# .draw(surface)


class scene_manager(object):
    def __init__(self):
        # Stack of scenes
        self._scenes = []

    @property
    def current_scene(self):
        if self._scenes:
            return self._scenes[-1]
        else:
            return None

    def append(self, value):
        self._scenes.append(value)

    def pop(self):
        return self._scenes.pop()

    def change(self, value):
        self.pop()
        self.append(value)

    def draw_all(self, surface):
        for scene in reversed(self._scenes):
            scene.draw(surface)

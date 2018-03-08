# Scene class components:
# ._manager
# .finished
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

    def update(self, dt):
        cleanup_complete = False
        while not cleanup_complete:
            if self.current_scene and not self.current_scene.finished:
                self.current_scene.update(dt)
                cleanup_complete = True
            elif self.current_scene and self.current_scene.finished:
                self.pop()
            else:
                cleanup_complete = True

    def draw(self, surface):
        # Draw all scenes (from bottom to top)
        surface.fill((0, 0, 0))
        for scene in self._scenes:
            scene.draw(surface)

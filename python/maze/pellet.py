from utils import FPS, LARGE_PELLET_RADIUS, SMALL_PELLET_RADIUS


# Power pellets blink on/off over this many frames
blink_frames = FPS // 2


class Pellet:

    def __init__(self, x: float, y: float, is_power_pellet: bool):
        # Center of pellet
        self.x, self.y = x, y

        # Ghosts become "scared" when PacMan eats a power pellet
        self.is_power_pellet = is_power_pellet

        # Power pellets are larger and blink on/off
        self.blink_frame_counter = 0

        self.radius = LARGE_PELLET_RADIUS if is_power_pellet else SMALL_PELLET_RADIUS

    @property
    def visible(self) -> bool:
        """Power pellets are hidden for part of each blink."""
        return not self.is_power_pellet \
            or self.blink_frame_counter <= blink_frames // 2

    def update(self):
        if self.is_power_pellet:
            self.blink_frame_counter += 1
            self.blink_frame_counter %= blink_frames

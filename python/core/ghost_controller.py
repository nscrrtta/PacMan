from utils import GhostState, FPS
from entities import Ghost


class GhostController:
    """
    Controls the state of every ghost (scatter/chase).
    Also updates each ghost's scared_timer.
    """

    def __init__(self, ghosts: list[Ghost]):
        self.ghosts = ghosts

    def new_level(self):
        # Seconds remaining in scatter mode
        self.scatter_timer = 0

        # Seconds remaining in chase mode
        self.chase_timer = 0

        # How many scatter modes remaining
        # for this level.
        #
        # After 4 scatter modes, ghosts
        # are in chase mode indefinitely
        self.scatter_count = 4

        self._update_ghost_states(GhostState.SCATTER)

        self._start_scatter_timer()

    def update(self):
        if self.scatter_timer:
            self.scatter_timer -= 1
            if self.scatter_timer == 0:
                self.scatter_count -= 1
                self._start_chase_timer()

        elif self.chase_timer:
            self.chase_timer -= 1
            if self.chase_timer == 0 \
            and self.scatter_count > 0:
                self._start_scatter_timer()

        for ghost in self.ghosts:
            if ghost.is_scared():
                ghost.scared_timer -= 1
                if ghost.scared_timer == 0:
                    ghost.revive()

    def _start_scatter_timer(self):
        """
        Start 7 or 5 second timer, depending on
        how many scatter modes have occurred.
        """
        seconds = 7 if self.scatter_count > 2 else 5
        self.scatter_timer = seconds * FPS
        self._update_ghost_states(GhostState.SCATTER)

    def _start_chase_timer(self):
        """
        Start 20 second timer.
        """
        self.chase_timer = 20 * FPS
        self._update_ghost_states(GhostState.CHASE)

    def _update_ghost_states(self, state: GhostState):
        for ghost in self.ghosts:
            ghost.state = state

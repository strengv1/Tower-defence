
"""
Kuvastaa yhtä ruutua, ja vastaa siitä, millainen ruutu on kyseessä.
Funktioiden toiminta on selitettävissä niiden nimillä
"""
class Block():
    def __init__(self, is_path=False, is_checkpoint=False, is_spawn=False, is_goal=False, is_grass=False):

        self.is_path = is_path
        self.is_checkPoint = is_checkpoint
        self.is_spawn = is_spawn
        self.is_goal = is_goal
        self.is_grass = is_grass
        self.x = 0
        self.y = 0
        self.center = (0, 0)



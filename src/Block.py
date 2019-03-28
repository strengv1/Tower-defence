
"""
Kuvastaa yhtä ruutua, ja vastaa siitä, millainen ruutu on kyseessä.
Funktioiden toiminta on selitettävissä niiden nimillä
"""
class Block():
    def __init__(self, is_path=False, is_checkpoint=False, is_spawn=False):

        self.is_path = is_path
        self.is_checkPoint = is_checkpoint
        self.is_spawn = is_spawn
        self.tower = None
        self.x = 0
        self.y = 0
        self.center = (0,0)


    def get_tower(self):
        return self.tower

    def set_tower(self, tower):
        if self.tower == None:
            self.tower = tower
            return 1
        else:
            return -1

    def remove_tower(self):
        self.tower = None





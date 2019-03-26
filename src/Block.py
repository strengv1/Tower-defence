

class Block():
    def __init__(self, is_path=False, is_checkpoint=False):

        self.is_path = is_path
        self.is_checkPoint = is_checkpoint
        self.tower = None

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


    def is_path(self):
        if self.is_path:
            return True
        else:
            return False

    def is_checkPoint(self):
        if self.is_checkPoint:
            return True
        else:
            return False


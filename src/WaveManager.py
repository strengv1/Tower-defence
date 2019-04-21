from src import Enemy


class WaveManager():

    def __init__(self):

        self.enemies = []
        self.active = False
        self.wave = 0
        self.timer = 0
        self.enemyCount = 0
        self.spawned = 0

    def next_wave(self):
        if not self.active:
            if self.wave <= 3:
                self.enemyCount = 7 + 3*self.wave
            elif self.wave > 3 and self.wave < 5:
                self.enemyCount = 7 + 5*self.wave
            elif self.wave >= 5:
                self.enemyCount = 7 + 5*self.wave
            self.active = True
            self.wave += 1
        else:
            print("wait for the wave to end")


    def update(self):
        if self.spawned >= self.enemyCount:
            self.active = False
            self.spawned = 0
        if self.active and self.timer > 15:
            self.timer = 0
            self.spawned += 1
            return True
        else:
            self.timer += 1
            return False


from configparser import ConfigParser

class Player():

    def __init__(self):
        parser = ConfigParser()
        parser.read("config.ini")

        self.health = parser.getint("game", "starting_hp")
        self.money = parser.getint("game", "starting_money")

    def am_i_alive(self):
        if self.health > 0:
            return True
        else:
            return False

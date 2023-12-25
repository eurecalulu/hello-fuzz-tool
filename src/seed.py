
class Seed:
    def __init__(self, name, percent, cover_path, error):
        self.name = name
        self.percent = percent
        self.cover_path = cover_path
        self.error = error
        self.power = self.cal_power()

    def cal_power(self):
        return 10
    
    def set_power(self, power):
        self.power = power

    def get_name(self):
        return self.name
    
    def get_percent(self):
        return self.percent
    
    def get_power(self):
        return self.power

    def __str__(self) -> str:
        return f'seed: {self.name}, power: {self.power}, percent: {self.percent}, cover_path: {self.cover_path}, error: {self.error}'

    

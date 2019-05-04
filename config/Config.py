from BaseConfig import BaseConfig

class Config(BaseConfig):

    def __init__(self, filename):
        super().__init__(filename)
        self._para = {}

    def parse(self):
        f = open(self._profile)
        line = f.readline()
        while line:
            tmp = line.split(' = ')
            self._para[tmp[0]] = tmp[1].rstrip()

            line = f.readline()
    
    def __call__(self):
        self.parse()
            
if __name__ == '__main__':
    instance = Config('./config.txt')
    instance()
    print(instance._para)
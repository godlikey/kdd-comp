from config.Config import Config
from preprocess.Preprocess import Preprocess


config = Config('./config/config.txt')
config()
print(config.para)

preprocess = Preprocess(config.para['path'])
preprocess.train_queries = config.para['train_queries']
preprocess.train_plans = config.para['train_plans']
preprocess.train_clicks = config.para['train_clicks']
preprocess.test_queries = config.para['test_queries']
preprocess.test_plans = config.para['test_plans']
preprocess.user_info = config.para['profiles']


preprocess.run()

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


import pandas as pd
import numpy as np
import xgboost as xgb
import os
from sklearn.metrics import roc_curve,auc,roc_auc_score
from sklearn.model_selection import train_test_split


data = pd.read_csv('train_preprocess.csv.csv')
data=data.sort_values(by='gmt_occur')
zhezhi@alpha-trion:~/velocity_test$ clear
zhezhi@alpha-trion:~/velocity_test$ cat rong360_model_0105.py
import pandas as pd
import numpy as np
import xgboost as xgb
import os
from sklearn.metrics import roc_curve,auc,roc_auc_score
from sklearn.model_selection import train_test_split


data = pd.read_csv('rong360_train_data_0105.csv')
data=data.sort_values(by='gmt_occur')

data2 = data.copy()

y = data['target_flag'].copy()
del data['id']
del data['gmt_occur']
del data['target_flag']
x = data.copy()



cnt = int(len(data) * 0.7)
train_x = x.iloc[:cnt]
test_x = x.iloc[cnt:]

train_y = y.iloc[:cnt]
test_y = y.iloc[cnt:]

data2 = data2.iloc[cnt:]

tra_x,val_x,tra_y,val_y = train_test_split(train_x,train_y,test_size=0.3,random_state=1)



train = xgb.DMatrix(tra_x,label=tra_y,missing=-1)
val = xgb.DMatrix(val_x,label=val_y,missing=-1)

iteration=130
early_stopping=200

params={
        'objective':'binary:logistic'
        ,'booster':'gbtree'
        ,'max_depth':5
        ,'lambda':20
        ,'subsample':0.6
        ,'scale_pos_weight':9
        ,'colsample_bytree':0.6
        ,'min_child_weight':20
        ,'silent':1
        ,'eta':0.05
        ,'seed':1
        ,'nthread':7
        ,'eval_metric':'auc'
}

plst = list(params.items())

watchlist = [(train, 'train'),(val, 'val')]

clf = xgb.train(plst, train, iteration, watchlist,early_stopping_rounds=early_stopping)
best_iteration = clf.best_ntree_limit

y_pre_val = clf.predict(xgb.DMatrix(val_x,missing=-1),ntree_limit = best_iteration)
y_pre_test = clf.predict(xgb.DMatrix(test_x,missing=-1),ntree_limit = best_iteration)


from scipy.stats import ks_2samp
get_ks = lambda y_pred,y_true: ks_2samp(y_pred[y_true==1], y_pred[y_true!=1]).statistic
print('val ks : ',get_ks(y_pre_val,val_y))
print('test ks : ',get_ks(y_pre_test,test_y))
print('test auc : ',roc_auc_score(test_y,y_pre_test))

#data2['score'] = y_pre_test
#data2.to_csv('rong360_test_score.csv')



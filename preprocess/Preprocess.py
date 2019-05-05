from .BasePreprocess import BasePreprocess
from .DataFiles import DataFiles
import pandas as pd
import os
import datetime

class Preprocess(BasePreprocess,DataFiles):

    def __init__(self, path):
        super().__init__(path)
        self._init()


    def parseQueries(self):
        train_queries = pd.read_csv(os.path.join(self.path,self.train_queries))

        ####################################################reg_hour####################################################
        train_queries['reg_hour'] = train_queries.req_time.apply(lambda x : x[11:13])
        train_queries['reg_hour'] = train_queries.reg_hour.apply(lambda x : 0 if x == '00' else int(x.lstrip('0')))
        

        ####################################################reg_week####################################################
        train_queries['reg_week'] = train_queries.req_time.apply(lambda x : datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').weekday())


        ####################################################return####################################################
        return train_queries[['sid','pid','reg_hour','reg_week']]


    def calPlanDetail(self,x):
        dist_list = []
        price_list = []
        eta_list = []
        rank_list = []

        x = x.lstrip('[').rstrip(']').split('}, {')
        for item in x:
            item = item.split(':')
            tmp = ''.join(list(filter(str.isdigit,item[1])))
            dist_list.append(-1 if tmp == '' else int(tmp))

            tmp = ''.join(list(filter(str.isdigit,item[2])))
            price_list.append(-1 if tmp == '' else int(tmp))

            tmp = ''.join(list(filter(str.isdigit,item[3])))
            eta_list.append(-1 if tmp == '' else int(tmp))

            rank_list.append(int(''.join(list(filter(str.isdigit,item[4])))))

        tmp_list = [item for item in dist_list if item != -1]
        if len(tmp_list) != 0:
            avg_value = int(sum(tmp_list) / len(tmp_list))
            dist_list = [item if item != -1 else avg_value for item in dist_list]

        tmp_list = [item for item in price_list if item != -1]
        if len(tmp_list) != 0:
            avg_value = int(sum(tmp_list) / len(tmp_list))
            price_list = [item if item != -1 else avg_value for item in price_list]

        tmp_list = [item for item in eta_list if item != -1]
        if len(tmp_list) != 0:
            avg_value = int(sum(tmp_list) / len(tmp_list))
            eta_list = [item if item != -1 else avg_value for item in eta_list]


        max_dist = max(dist_list)
        max_price = max(price_list)
        max_eta = max(eta_list)

        min_dist = min(dist_list)
        min_price = min(price_list)
        min_eta = min(eta_list)

        m1_pos = rank_list.index(1) if 1 in rank_list else -1
        m2_pos = rank_list.index(2) if 2 in rank_list else -1
        m3_pos = rank_list.index(3) if 3 in rank_list else -1
        m4_pos = rank_list.index(4) if 4 in rank_list else -1
        m5_pos = rank_list.index(5) if 5 in rank_list else -1
        m6_pos = rank_list.index(6) if 6 in rank_list else -1
        m7_pos = rank_list.index(7) if 7 in rank_list else -1
        m8_pos = rank_list.index(8) if 8 in rank_list else -1
        m9_pos = rank_list.index(9) if 9 in rank_list else -1
        m10_pos = rank_list.index(10) if 10 in rank_list else -1
        m11_pos = rank_list.index(11) if 11 in rank_list else -1

        return ','.join([str(max_dist),str(max_price),str(max_eta),str(min_dist),str(min_price),str(min_eta),
                str(m1_pos),str(m2_pos),str(m3_pos),str(m4_pos),str(m5_pos),str(m6_pos),str(m7_pos),str(m8_pos),
                str(m9_pos),str(m10_pos),str(m11_pos)])






    def parsePlans(self):
        train_plans = pd.read_csv(os.path.join(self.path,self.train_plans))
        train_plans['plan_detail'] = train_plans.plans.apply(self.calPlanDetail)

        train_plans['max_dist'] = train_plans.plan_detail.apply(lambda x:x.split(',')[0])
        train_plans['max_price'] =  train_plans.plan_detail.apply(lambda x:x.split(',')[1])
        train_plans['max_eta'] =  train_plans.plan_detail.apply(lambda x:x.split(',')[2])

        train_plans['min_dist'] =  train_plans.plan_detail.apply(lambda x:x.split(',')[3])
        train_plans['min_price'] =  train_plans.plan_detail.apply(lambda x:x.split(',')[4])
        train_plans['min_eta'] =  train_plans.plan_detail.apply(lambda x:x.split(',')[5])

        train_plans['m1_pos'] =  train_plans.plan_detail.apply(lambda x:x.split(',')[6])
        train_plans['m2_pos'] =  train_plans.plan_detail.apply(lambda x:x.split(',')[7])
        train_plans['m3_pos'] =  train_plans.plan_detail.apply(lambda x:x.split(',')[8])
        train_plans['m4_pos'] =  train_plans.plan_detail.apply(lambda x:x.split(',')[9])
        train_plans['m5_pos'] =  train_plans.plan_detail.apply(lambda x:x.split(',')[10])
        train_plans['m6_pos'] =  train_plans.plan_detail.apply(lambda x:x.split(',')[11])
        train_plans['m7_pos'] =  train_plans.plan_detail.apply(lambda x:x.split(',')[12])
        train_plans['m8_pos'] =  train_plans.plan_detail.apply(lambda x:x.split(',')[13])
        train_plans['m9_pos'] =  train_plans.plan_detail.apply(lambda x:x.split(',')[14])
        train_plans['m10_pos'] =  train_plans.plan_detail.apply(lambda x:x.split(',')[15])
        train_plans['m11_pos'] =  train_plans.plan_detail.apply(lambda x:x.split(',')[16])


        
        return train_plans[['sid','max_dist','max_price','max_eta','min_dist','min_price','min_eta','m1_pos',
        'm2_pos','m3_pos','m4_pos','m5_pos','m6_pos','m7_pos','m8_pos','m9_pos','m10_pos','m11_pos']]

    
    def parseClicks(self):
        pass


    def run(self):
        train_queries = self.parseQueries()
        train_plans = self.parsePlans()
        train_clicks = pd.read_csv(os.path.join(self.path,self.train_clicks))
        train_clicks = train_clicks[['sid','click_mode']]
        train_clicks['click_mode'] = train_clicks.click_mode.astype(int)
        user_info = pd.read_csv(os.path.join(self.path,self.user_info))
        tmp = pd.merge(train_queries, user_info, how='left', on=['pid'])
        tmp = pd.merge(tmp, train_plans, how='inner', on='sid')
        data = pd.merge(tmp, train_clicks, how='left', on='sid')

        data.click_mode.fillna(0,inplace=True)
        del data['pid']
        data.fillna(-1,inplace=True)
        data.to_csv('train_preprocess.csv',index=False)




if __name__ == '__main__':
    instance = Preprocess('../data')


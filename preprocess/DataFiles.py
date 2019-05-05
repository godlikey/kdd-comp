class DataFiles:
    def __init__(self):
        pass

    def _init(self):
        self._train_queries = None
        self._train_plans = None
        self._train_clicks = None

        self._test_queries = None
        self._test_plans = None

        self._user_info = None

    @property
    def train_queries(self):
        return self._train_queries

    @train_queries.setter
    def train_queries(self,value):
        self._train_queries = value

    @property
    def train_plans(self):
        return self._train_plans

    @train_plans.setter
    def train_plans(self,value):
        self._train_plans = value

    @property
    def train_clicks(self):
        return self._train_clicks

    @train_clicks.setter
    def train_clicks(self,value):
        self._train_clicks = value

    @property
    def test_queries(self):
        return self._test_queries

    @test_queries.setter
    def test_queries(self,value):
        self._test_queries = value


    @property
    def test_plans(self):
        return self._test_plans

    @test_plans.setter
    def test_plans(self,value):
        self._test_plans = value


    @property
    def user_info(self):
        return self._user_info

    @user_info.setter
    def user_info(self,value):
        self._user_info = value

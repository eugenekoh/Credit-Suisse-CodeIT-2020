import logging
from flask import request, jsonify
from codeitsuisse import app
from io import StringIO

import pandas as pd
import lightgbm as lgb

logger = logging.getLogger(__name__)


@app.route('/pre-tick', methods=['POST'])
def evaluate_pre_tick():
    data = request.data
    logger.info(f"data: {data}")
    s = str(data,'utf-8')
    data = StringIO(s) 
    df = pd.read_csv(data)
    model = train(df)
    X = df[-1:][['Open','High','Low','Volume']].values
    Y = predict(model, X)[0]
    logger.info(f"prediction:{Y}")
    return jsonify(Y)


def train(df):
    train = df[:1600]
    val = df[1600:]
    x_train = train[['Open','High','Low','Volume']]
    y_train = train.Close.values
    x_val = val[['Open','High','Low','Volume']]
    y_val = val.Close.values
    lgb_params = {'boosting_type': 'gbdt',
        'objective': 'regression',       
        'metric': ['rmse'],             
        'learning_rate': 0.05,           
        'num_leaves': 2**7,            
        'min_data_in_leaf': 8,      
        'n_estimators': 100,            
        'early_stopping_rounds': 30,     
        'verbose': 1,}
    train_set = lgb.Dataset(x_train, y_train)
    val_set = lgb.Dataset(x_val, y_val)
    lgb_model = lgb.train(lgb_params, train_set, num_boost_round = 200, valid_sets = [train_set, val_set], verbose_eval = 100)
    logger.info("=== TRAINING DONE ====")
    return lgb_model

def predict(model, features):
    logger.info(f"predictors: {features}")
    logger.info("=== PREDICTING ===")
    return model.predict(features)
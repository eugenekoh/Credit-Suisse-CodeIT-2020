import logging
from flask import request, jsonify
from codeitsuisse import app
from io import StringIO
import json 
import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge, Lasso
from sklearn.metrics import mean_squared_error as mse


logger = logging.getLogger(__name__)


@app.route('/pre-tick', methods=['POST'])
def evaluate_pre_tick():
    data = request.data
    logger.info(f"data: {data}")
    s=str(data,'utf-8')
    data = StringIO(s) 
    df=pd.read_csv(data)
    ridge_Y = ridge(df)
    lasso_Y = lasso(df)
    Y = (ridge_Y + lasso_Y) / 2
    # test = df[-8:]
    # x_test = test[['Open','High','Low','Volume']].values
    # Y = predict(model, x_test)
    # print(Y)
    return json.dumps(Y)


# def train(df):
#     train = df[:1600]
#     val = df[1600:]
#     x_train = np.array(train[['Open','High','Low','Volume']])
#     print(x_train.shape)
#     y_train = train.Close.values
#     x_val = np.array(val[['Open','High','Low','Volume']])
#     y_val = val.Close.values
#     params = {
#         'boosting_type': 'gbdt',
#         'objective': 'regression',
#         'metric': 'rmsle',
#         'max_depth': 6, 
#         'learning_rate': 0.1,
#         'verbose': 0, 
#         'early_stopping_round': 20}
#     train_set = lgb.Dataset(x_train, y_train)
#     val_set = lgb.Dataset(x_val, y_val)
#     lgb_model = lgb.train(params, train_set, num_boost_round = 200, valid_sets = [train_set, val_set], verbose_eval = 100)
#     logger.info("=== TRAINING DONE ====")

#     Y = lgb_model.predict(x_val)
#     return Y

# def predict(model, features):
#     logger.info(f"predictors: {features}")
#     Y = model.predict(np.array([features,]))
#     return Y

def rmse(y_true,y_pred):
    return np.sqrt(mse(y_true,y_pred))

def ridge(df):
    train = df[:1600]
    val = df[1600:]
    x_train = train[['Open','High','Low','Volume']]
    y_train = train.Close.values
    x_val = val[['Open','High','Low','Volume']]
    y_val = val.Close.values

    best_ridge_model = None
    best_ridge_score = float('inf')
    for a in range(1,51):
        ridge_model = Ridge(alpha=a/10).fit(x_train,y_train)
        val_pred_ridge = ridge_model.predict(x_val)
        val_score_ridge = rmse(val_pred_ridge,y_val)
        if val_score_ridge < best_ridge_score:
            best_ridge_score = val_score_ridge
            best_ridge_model = ridge_model

    Y_pred = best_ridge_model.predict(x_val)
    return Y_pred[-1]

def lasso(df):
    train = df[:1600]
    val = df[1600:]
    x_train = train[['Open','High','Low','Volume']]
    y_train = train.Close.values
    x_val = val[['Open','High','Low','Volume']]
    y_val = val.Close.values

    best_lasso_model = None
    best_lasso_score = float('inf')
    for a in range(1,51):
        lasso_model = Lasso(alpha=a/10).fit(x_train,y_train)
        val_pred_lasso = lasso_model.predict(x_val)
        val_score_lasso = rmse(val_pred_lasso,y_val)
        if val_score_lasso < best_lasso_score:
            best_lasso_score = val_score_lasso
            best_lasso_model = lasso_model
    
    Y_pred = best_lasso_model.predict(x_val)
    return Y_pred[-1]

#


# def deep_train(df):
#     train = df[:6]
#     val = df[6:]
#     x_train = train[['Open','High','Low','Volume']]
#     y_train = train.Close.values
#     x_val = val[['Open','High','Low','Volume']]
#     y_val = val.Close.values

#     num_epochs = 100
#     batch_size = 8
#     num_nodes = 32
#     num_layers = 3
#     dropout = 0.2
#     loss_fn = rmse
#     optimizer = 'adam'

#     mlp_model = Sequential()
#     mlp_model.add(Dense(num_nodes, input_dim=x_train.shape[1], activation='relu'))
#     mlp_model.add(Dropout(dropout))
#     for i in range(num_layers-1):
#         mlp_model.add(Dense(num_nodes, activation='relu'))
#         mlp_model.add(Dropout(dropout))
#     es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=10)
#     mlp_model.compile(loss=loss_fn, optimizer=optimizer, metrics=['accuracy'])
#     mlp_model.fit(x_train, y_train,batch_size=batch_size,epochs=num_epochs,validation_data=(x_val, y_val),callbacks=[es],verbose=1)
#     return mlp_model
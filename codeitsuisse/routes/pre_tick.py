import logging
from flask import request, jsonify
from codeitsuisse import app
import io
# from keras.models import Sequential, Model
# from keras.layers import Dense, Embedding, LSTM, Dropout, Input, concatenate
import pandas as pd

logger = logging.getLogger(__name__)


@app.route('/pre-tick', methods=['POST'])
def evaluate_pre_tick():
    data = request.data
    logger.info(f"data: {data}")
    result = {}
    df = pd.read_csv(io.StringIO(data.decode('utf-8')))
    train(df)
    return jsonify(result)


def train(df):
    print(df.cols)
    return 
# def predict()
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class Transformer(BaseEstimator, TransformerMixin):
    def __init__(self, quantitative_variables, categorical_variables):
        self.quantitative_variables = quantitative_variables
        self.categorical_variables = categorical_variables
        self.encoder = OneHotEncoder()
        self.scaler = MinMaxScaler()

    def fit(self, X, y = None):
        self.encoder.fit(X[self.categorical_variables])
        self.scaler.fit(X[self.quantitative_variables])
        return self 

    def transform(self, X, y = None):
      X_categorical = pd.DataFrame(data = self.encoder.transform(X[self.categorical_variables]).toarray(),
                                  columns = self.encoder.get_feature_names(self.categorical_variables))
      
      X_quantitative = pd.DataFrame(data = self.scaler.transform(X[self.quantitative_variables]),
                                  columns = self.quantitative_variables)
      
      X = pd.concat([X_quantitative, X_categorical], axis = 1)

      return X
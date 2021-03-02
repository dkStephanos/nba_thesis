import pandas as pd
import statistics as stats
from sklearn import metrics, preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split

class SklearnClf:
    def __init__(self):
        self.min_max_scaler = preprocessing.MinMaxScaler()

    def get_model(self):
        return self.clf

    def set_data(self, df, target_col):
        self.X = df.drop(columns=[target_col])
        self.y = df[target_col]

    def get_data(self):
        return [self.X, self.y]

    def fit_and_predict(self, X_train, X_test, y_train):      
        X_train = self.min_max_scaler.fit_transform(X_train)
        X_test = self.min_max_scaler.fit_transform(X_test)
        
        self.clf.fit(X_train, y_train)
        self.predictions = self.clf.predict(X_test)

    def split_test_data(self, test_size, is_fixed=False):
        if(is_fixed):    #Use the same seed when generating test and training sets
            X_train, X_test, Y_train, Y_test = train_test_split(self.X, self.y, shuffle = True, random_state = 42, test_size = test_size)
        else:           #Use a completely random set of test and training data
            X_train, X_test, Y_train, Y_test = train_test_split(self.X, self.y, shuffle = True, test_size = test_size)

        return X_train, X_test, Y_train, Y_test

    def run_genetic_optimization_on_model(self,generations=100,pop_size=200,mutation_rate=0.1,display_rate=20,init_crossover_strategy='multipoint',rand_selection=False):
        pass  

    def get_confusion_matrix(self, y_test):
        return confusion_matrix(y_test, self.predictions)

    def get_classification_report(self, y_test):
        return classification_report(y_test, self.predictions)
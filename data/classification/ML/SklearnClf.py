import numpy as np
from sklearn import metrics, preprocessing
from sklearn.metrics import confusion_matrix, classification_report, f1_score
from sklearn.model_selection import train_test_split
from .GeneticOptimizer import GeneticOptimizer

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

    def get_avg_metrics_for_n_iterations(self, n_iterations, test_size, is_fixed=False):
        
        precision = 0
        recall = 0
        f1_score = 0
        support = 0
        confusion_matrix = np.zeros((2,2))


        for i in range(0,n_iterations):
            X_train, X_test, y_train, y_test = self.split_test_data(test_size, is_fixed)
            self.fit_and_predict(X_train, X_test, y_train)
            confusion_matrix += self.get_confusion_matrix(y_test)
            clf_report = self.get_classification_report(y_test).split("\n")[-2].split("      ")
            precision += float(clf_report[1])
            recall += float(clf_report[2])
            f1_score += float(clf_report[3])
            support += float(clf_report[4])

        precision = precision/n_iterations
        recall = recall/n_iterations
        f1_score = f1_score/n_iterations
        support = support/n_iterations
        confusion_matrix = confusion_matrix/n_iterations

        return [round(precision,3), round(recall,3), round(f1_score, 3), round(support, 3), confusion_matrix]

    def run_genetic_optimization_on_model(self,params_to_optimize,num_generations=20,pop_size=25,mutation_rate=0.85,display_rate=1,rand_selection=False,plot_dir='static/data/test/'):
        gen_optimizer = GeneticOptimizer(params_to_optimize,num_generations, pop_size, mutation_rate, display_rate, rand_selection)
        gen_optimizer.set_model(self)
        gen_optimizer.run_ga()
        gen_optimizer.plot_ga(plot_dir)

    def run_genetic_optimization_on_features(self,num_generations=20,pop_size=25,mutation_rate=0.25,display_rate=2,rand_selection=False,plot_dir='static/data/test/'):
        gen_optimizer = GeneticOptimizer({},num_generations, pop_size, mutation_rate, display_rate, rand_selection)
        gen_optimizer.set_model(self)
        gen_optimizer.run_ga_features()
        gen_optimizer.plot_ga(plot_dir)

    def get_confusion_matrix(self, y_test):
        return confusion_matrix(y_test, self.predictions)

    def get_classification_report(self, y_test):
        return classification_report(y_test, self.predictions)

    def get_f1_score(self, y_test):
        return f1_score(y_test, self.predictions)
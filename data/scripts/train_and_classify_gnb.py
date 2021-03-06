import pandas as pd

from data.classification.utilities.EncodingUtil import EncodingUtil
from data.classification.utilities.ConstantsUtil import ConstantsUtil
from data.classification.ML.GaussianNB import GaussianNB

from data.models import CandidateFeatureVector


def run():
    candidates = CandidateFeatureVector.objects.all().values()
    candidates_df = pd.DataFrame(candidates)
    candidates_df.set_index('id', inplace=True)
    candidates_df.drop(columns=['candidate_id'], inplace=True)

    candidates_df = EncodingUtil.basic_label_encode_cols(candidates_df, ConstantsUtil.BASIC_ENCODE_COLS)
    candidates_df = EncodingUtil.sort_position_cols_and_encode(candidates_df, ConstantsUtil.STRING_TUPLE_ENCODE_COLS)

    gnb = GaussianNB()
    gnb.set_data(candidates_df, 'classification')
    X_train, X_test, y_train, y_test = gnb.split_test_data(.3, True)

    gnb.get_roc_curve(X_train, X_test, y_train, y_test)

    gnb.fit_and_predict(X_train, X_test, y_train)
    print(gnb.get_confusion_matrix(y_test))
    print(gnb.get_classification_report(y_test))

    gnb.get_learning_curve()

    print(gnb.get_avg_metrics_for_n_iterations(10, .3, True))
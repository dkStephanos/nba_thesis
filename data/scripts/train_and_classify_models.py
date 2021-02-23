import pandas as pd

from data.classification.utilities.EncodingUtil import EncodingUtil

from data.models import CandidateFeatureVector


def run():
    candidates = CandidateFeatureVector.objects.all().values()
    candidates_df = pd.DataFrame(candidates)
    candidates_df.set_index('id', inplace=True)
    candidates_df.drop(columns=['candidate_id'], inplace=True)

    candidates_df = EncodingUtil.basic_label_encode_cols(candidates_df, ['cutter_archetype', 'screener_archetype'])
    candidates_df = EncodingUtil.sort_position_cols_and_encode(candidates_df, ['cutter_loc_on_pass'])

    print(candidates_df['cutter_loc_on_pass'])
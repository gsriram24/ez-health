import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
import os
import flask
from flask import request, jsonify, render_template, current_app

app = flask.Flask(__name__)

# Mode determines the flag
# 0 = Train
# 1 = Test
# 2 = Single Predict


def preprocess_and_cleanup(df, mode=0):

    # Age Column Cleanup
    if mode == 2:
        mean_age = 32
    else:
        mean_age = np.mean(df['Age'][(df['Age'] >= 10) & (df['Age'] <= 100)].values)
    df['Age'] = np.where((df['Age'] >= 18) & (df['Age'] <= 100), df['Age'], mean_age)

    # Cleanup Gender Column
    df['Gender'] = df['Gender'].str.strip()
    male_strings = ['Male', 'male', 'M', 'm', 'Man', "man", "male-ish",
                    "mal", 'Make', "maile", "msle", "mail", "malr", "make",
                    "male (cis)",  "cis man",  "Cis Male", "cis male"]
    df['gender_male'] = df['Gender'].isin(male_strings).astype(int)
    female_strings = ['Female', 'female', 'F', 'f', 'Woman', "woman",
                      "femake", "femail",
                      "cis female", "cis-female/femme", "female (cis)"
                      ]
    df['gender_female'] = df['Gender'].isin(female_strings).astype(int)
    df['gender_other'] = np.where((df['gender_male'] == 0) & (df['gender_female'] == 0), 1, 0)

    # Replace all no/dont know/yes with numeric values
    mcq_columns = []
    mcq_columns.extend(['self_employed', 'family_history', 'remote_work', 'tech_company', 'benefits',
                        'care_options', 'wellness_program', 'seek_help', 'anonymity', 'mental_health_consequence',
                        'phys_health_consequence', 'coworkers', 'supervisor', 'mental_health_interview',
                        'phys_health_interview', 'mental_vs_physical', 'obs_consequence'])
    if mode == 0:
        mcq_columns.append('treatment')
    for col in mcq_columns:
        df[col] = df[col].map({'Yes': 1,
                               'Maybe': 0.5,  'Some of them': 0.5, 'Not sure': 0.5, 'Don\'t know': 0.5,
                               'No': 0})

    # Convert Other Columns to Numeric
    # df['work_interfere'] = df['work_interfere'].map({'Often': 1, 'Sometimes': 2/3, 'Rarely': 1/3, 'Never': 0})

    # df['leave'] = df['leave'].map({'Very easy': 1, 'Somewhat easy': 3/4, 'Don\'t know ': 0.5,
    #                               'Somewhat difficult': 1/4, 'Very difficult': 0})

    # Drop Rubish Columns
    df = df.drop(['s.no', 'Timestamp', 'Gender', 'comments', 'Country', 'state'], axis=1)

    # Final Step
    if mode != 2:
        df = df.fillna(df.median())
    df = pd.get_dummies(df)
    df = df.reindex(columns=(sorted(df.columns)))

    return df


# Model Training
full_train_df = pd.read_csv('./data/devengers_train.csv')
full_test_df = pd.read_csv('./data/devengers_test.csv')
train_df = preprocess_and_cleanup(full_train_df, 0)
test_df = preprocess_and_cleanup(full_test_df, 1)

train_df, test_df = train_df.align(test_df, join='outer', axis=1, fill_value=0)
train_df = train_df.reindex(columns=(sorted(list([a for a in train_df.columns if a != 'treatment'])) + ['treatment']))

data_x, data_y = train_df.iloc[:, :-1], train_df.iloc[:, -1]
best_classifier = AdaBoostClassifier(learning_rate=0.01333521432163324, n_estimators=500)
best_classifier.fit(data_x, data_y)


@app.route('/api/v1/predict', methods=['POST'])
def predict_y():
    global train_df

    pandas_dict = {}
    for key in request.json:
        pandas_dict[key] = [request.json[key]]

    pred_df = pd.DataFrame(pandas_dict)
    pred_df = preprocess_and_cleanup(pred_df, 2)

    train_df, pred_df = train_df.align(pred_df, join='left', axis=1, fill_value=0)
    pred_df = pred_df.reindex(columns=(sorted(pred_df.columns)))
    pred_df = pred_df.drop(['treatment'], axis=1)

    print(pred_df.loc[0])
    y_pred = best_classifier.predict_proba(pred_df)
    y_pred = y_pred[:, 1][0]

    if y_pred <= 0.5:
        return jsonify({'treatment': False})
    else:
        return jsonify({'treatment': True})


@app.route('/')
def hello():
    return current_app.send_static_file('index.html')


if __name__ == '__main__':

    app.run(port=80)

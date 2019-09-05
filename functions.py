#functions to be used in the data preparation process

import pandas as pd
import numpy as np
import sklearn.metrics as metric

def market_columns(df):
    """Function that maps multiple entries in a column into individual columns
    and assings a score of 1 or 0 if the entry is question is within a given row.
    """
    categories = []
    for category in list(df['Market Category'].unique()):
        categories += category.split(',')

    unique = set(categories)
    for col in unique:
        df[col] = df['Market Category'].apply(lambda x: 1 if col in x.split(',') else 0)
    df.drop('Market Category', axis=1, inplace=True)
    return df

def get_metrics_by_class(labels, preds, score_type='macro'):
    
    """
    Return a dataframe of metrics for each class in test data(labels) against the predictions(preds)
    Classes are dataframe index, metrics are columns
    Metrics included are: precision, recall, accuracy and f1_score
    Last row is the the metric for overall model, class_param species the averaging method
    class_param inputs, 'micro', 'macro', 'weighted', 'samples', default is micro
    refer to sklearn.metrics for additional information for more information
    """
    
    metric_dict = {}
    
    for label in set(list(labels)):
        
        #calculate metrics for each class
        pre_score = ((labels==label) & (preds==label)).sum()/((preds==label)).sum()
        rec_score = ((labels==label) & (preds==label)).sum()/((labels==label)).sum()
        
        
        acc_score = (((labels==preds) & (labels==label)).sum()+
                     ((labels!=label) & (preds!=label) & (labels==label)).sum())/(labels==label).sum()
        
        
        f1_score = 2*(pre_score*rec_score)/(pre_score+rec_score)
        
        metric_dict[label] = {'Precision': pre_score,
                              'Recall': rec_score,
                              'Accuracy': acc_score,
                              'F1_Score': f1_score}
        
    metric_dict['M'] = {'Precision': metric.precision_score(labels, preds, average=class_param),
                        'Recall': metric.recall_score(labels, preds, average=class_param),
                        'Accuracy': metric.accuracy_score(labels, preds),
                        'F1_Score': metric.f1_score(labels, preds, average=class_param)}
        
    return pd.DataFrame.from_dict(metric_dict).transpose()

def optimize_k_knn(X_train, y_train, X_test, y_test, min_k=3, max_k=10, score='micro'):
    """
    Find best k neighbor number for KNN model based on scores on testing data
    Score is based on f1_score, for options refer to sklearn.metrics
    """
    k_f1 = []
    
    for k in range(min_k, max_k+1):
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X_train, y_train)
        y_hat_test = knn.predict(X_test)
        
        k_f1.append((k, metric.f1_score(y_test, y_hat_test, average=score)))
        
    k_f1.sort(key=lambda f1: f1[1], reverse=True)
    
    return k_f1[0]
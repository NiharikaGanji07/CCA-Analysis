# gensim modules
from gensim.models import Doc2Vec

import glob

# numpy
import numpy
import pandas as pd

# classifier
from sklearn.linear_model import LogisticRegression

# globals
from globals import DIM_SIZE
from globals import MODEL_FILE
from globals import META_FILE
from globals import log
from globals import sys
from globals import pickle
from globals import transform
from globals import update_progress

import pandas as pd

def infer():

    model = None
    exDict = None
    try:
        #log.info('Loading model file...')
        model = Doc2Vec.load(MODEL_FILE)
    except:
        log.error('Error loading '+MODEL_FILE+'. Try running train.py')
        sys.exit()
    try:
        #log.info('Loading meta file...')
        exDict = pickle.load(open(META_FILE, 'rb'))
    except:
        log.error('Error loading '+META_FILE+'. Try running train.py')
        sys.exit()

    #log.info('Preparing training data...')
    neg_size = exDict["neg_size"]
    pos_size = exDict["pos_size"]
    neu_size = exDict["neg_size"]
    tot_size = neg_size + pos_size + neu_size
    #log.info('Sample Size:' + str(tot_size) + ' -ve:' + str(neg_size) + ' +ve:' + str(pos_size) + ' neu: ' + str(neu_size))

    # initialize the arrays    
    docvecs = numpy.zeros((tot_size, DIM_SIZE))
    labels = numpy.zeros(tot_size)

    for count in range(neg_size):
        docvecs[count] = model.docvecs['NEG_' + str(count)]
        labels[count] = 0

    for count in range(pos_size):
        docvecs[neg_size + count] = model.docvecs['POS_' + str(count)]
        labels[neg_size + count] = 1

    for count in range(neu_size):
        docvecs[neu_size + count] = model.docvecs['NEG_' + str(count)]
        labels[neu_size + count] = 2

    #log.info('Fitting classifier...')
    clf = LogisticRegression()
    clf.fit(docvecs, labels)

    # Checking inference with one sample
    files = 'Sentiment.csv'
    df = pd.read_csv(filename)
    data = fd['Title']
    for titles in data:
        pred_sam = titles
        log.info('Predicting on: %s' % pred_sam)
        pred_lbl = clf.predict_proba(model.infer_vector(pred_sam).reshape(1, -1))
        percent_neg = str('%.2f' % (pred_lbl[0,0]*100))
        percent_pos = str('%.2f' % (pred_lbl[0,1]*100))
        log.info(pred_lbl)
        log.info(clf.classes_)
        if percent_neg > percent_pos: log.info('Sentiment: Negative ' + percent_neg + '%\n')
        else: log.info('Sentiment: Positive ' + percent_pos + '%\n')
if __name__ == "__main__": infer()

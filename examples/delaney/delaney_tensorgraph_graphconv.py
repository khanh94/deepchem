"""
Script that trains graphconv models on delaney dataset.
"""
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

import numpy as np
np.random.seed(123)
import tensorflow as tf
tf.set_random_seed(123)
import deepchem as dc

from sklearn.metrics import r2_score

# Load Delaney dataset
delaney_tasks, delaney_datasets, transformers = dc.molnet.load_lipo(
    featurizer='GraphConv', split='scaffold')
train_dataset, valid_dataset, test_dataset = delaney_datasets

# Fit models
metric = dc.metrics.Metric(dc.metrics.pearson_r2_score, np.mean)

n_atom_feat = 75
n_pair_feat = 14
# Batch size of models
batch_size = 48
n_feat = 128

model = dc.models.GraphConvTensorGraph(
    len(delaney_tasks),
    batch_size=batch_size,
    learning_rate=1e-3,
    use_queue=False,
    mode='regression')

for i in xrange(0, 50):
  model.fit(train_dataset, nb_epoch=1)
  valid_scores = model.evaluate(valid_dataset, [metric], transformers)
  mu, sigma = model.bayesian_predict(valid_dataset.X, transformers)
  y = valid_dataset.y
  #print(y.shape)
  #print(mu.shape)
  print(r2_score(y, mu))

  tmp = sigma
  amax = np.amax(tmp.reshape(-1, 1))
  amin = np.amin(tmp.reshape(-1, 1))
  print('max uncrt [%.4f] min uncrt [%.4f]' % (amin, amax))

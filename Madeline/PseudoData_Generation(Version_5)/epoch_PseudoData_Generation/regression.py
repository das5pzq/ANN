import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf # Version 2.9.1
from tensorflow import keras
from tensorflow.keras import layers
np.set_printoptions(precision=3, suppress=True)

column_names = ['count','Set','index','k','QQ','x_b','t','phi_x','F','sigmaF','F1','F2','ReH_true','ReE_true','ReHTilde_true','c0_true','Formalism']

dataset = [25, 50, 75, 100, 125, 150, 175, 200]
fig, axs = plt.subplots(8, figsize=(3, 20))
# fig.subplots_adjust(hspace=0)
# fig.tight_layout()

# fig = plt.figure()
# gs = fig.add_gridspec(10, hspace=0)
# axs = gs.subplots(sharex=True, sharey=True)

for (data,itr) in zip(dataset, range(len(dataset))):
    raw_dataset = pd.read_csv('BKM10_pseudodata_generation2.csv', skiprows=1, names=column_names,
                              na_values='?', comment='\t',
                              sep=',', skipinitialspace=True)
    del raw_dataset['count']
    del raw_dataset['Formalism']
    dataset = raw_dataset.copy()

    train_dataset = dataset.sample(frac=0.8, random_state=0)
    test_dataset = dataset.drop(train_dataset.index)

    train_features = train_dataset.copy()
    test_features = test_dataset.copy()

    train_labels = train_features.pop('F')
    test_labels = test_features.pop('F')


    # Normalization

    normalizer = tf.keras.layers.Normalization(axis=-1) # Normalization layer
    normalizer.adapt(np.array(train_features)) # Fit the state of the preprocessing later to the data


    # DNN with Multiple Inputs

    def build_and_compile_model(norm):
      model = keras.Sequential([
          norm,
          layers.Dense(64, activation='relu'),
          layers.Dense(64, activation='relu'),
          layers.Dense(1)
      ])

      model.compile(loss='mean_absolute_error',
                    optimizer=tf.keras.optimizers.Adam(0.001))
      return model

    dnn_model = build_and_compile_model(normalizer)

    history = dnn_model.fit(
        train_features,
        train_labels,
        validation_split=0.2,
        verbose=0, epochs=data)
    
    test_results = {}
    test_results['dnn_model'] = dnn_model.evaluate(test_features, test_labels, verbose=0)
    pd.DataFrame(test_results, index=['Mean absolute error [F]']).T
    axs[itr].set_xlim([0, data])
    axs[itr].set_ylim([0, 0.22])
    axs[itr].plot(history.history['loss'], label='loss')
    axs[itr].plot(history.history['val_loss'], label='val_loss')
#     axs[itr].legend(loc="upper right")
#     axs[itr].text(0.0, 1.0, 'smear err ='+str(data), fontsize='medium', verticalalignment='top')
#     axs[itr].text(0.5, 0.5,'smear err ='+str(data), ha='center')

#     axs[itr].text(53, 0.075, 'MAE='+str(test_results['dnn_model']),verticalalignment='bottom', horizontalalignment='left',color='green', fontsize=10)
    axs[itr].text((data*0.55), 0.075, 'MAE='+str('%s' % float('%.4g' % test_results['dnn_model'])),verticalalignment='bottom', horizontalalignment='left',color='green', fontsize=10)
    
    axs[itr].text((data*0.55), 0.1, 'epoch='+str(data),verticalalignment='bottom', horizontalalignment='left',color='green', fontsize=10)
    axs[itr].set_xlabel('Epoch')
    axs[itr].set_ylabel('Error [F]')

# axs[0].plot(history.history['loss'], label='loss')
# axs[0].plot(history.history['val_loss'], label='val_loss')
axs[0].set_title('Varied epoch')
axs[0].legend(loc="upper right")
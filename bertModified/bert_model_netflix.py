#!wget 'https://raw.githubusercontent.com/SarthakV7/covid_dashboard/master/data/country_to_iso.csv'

import numpy as np
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import warnings

warnings.filterwarnings('ignore')
sns.set()

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
        
df = pd.read_csv('sample_data/netflix_titles.csv')

#Author Zihan Luo, First check
df["rating"].value_counts()

#Author Zihan Luo, pre-processing
rating_filter = df["rating"].isin(["TV-MA", "TV-14", "TV-PG", "R", "PG-13", "TV-Y"])
df = df[rating_filter]

df.head()

#iso = pd.read_csv('country_to_iso.csv')[['Country','Alpha-3 code']]
#df_map = pd.DataFrame()
#x = np.hstack([np.array(i.split(',')) for i in df.country.dropna()])
#unique, counts = np.unique(x, return_counts=True)        
#df_map['Country'] = unique
#df_map['count'] = counts
#df_map = df_map.merge(iso, how='left', on='Country').dropna()
#df_map['Alpha-3 code'] = df_map['Alpha-3 code'].apply(lambda x:x[2:-1])

#fig = go.Figure(data=go.Choropleth(locations=df_map['Alpha-3 code'],
#                                   z=df_map['count'].astype(float),
#                                   colorscale='viridis',
#                                   text=df_map['Country'],
#                                   marker_line_color='black',
#                                   colorbar_title = 'number of shows'))

#"#" fig.update_geos(projection_type="orthographic")
                
#fig.show()

#fig = px.pie(df_map.sort_values('count', ascending=False).iloc[:20], values='count', 
#            names='Country', title='Shows available in different countries (top 20)')
#fig.show()

fig = px.histogram(df, x='type')
fig.show()

fig = px.histogram(df, x='release_year')
fig.show()

fig = px.histogram([int(i.split(', ')[1]) for i in df.date_added.dropna()], orientation='h', labels={'value':'year'})
fig.show()

df.sort_values('release_year')[['title', 'type', 'country', 'director', 'cast', 'release_year']].dropna().head(10)

#Author Zihan Luo, Secondary check
df.sort_values('release_year')[['title', 'type', 'country', 'director', 'cast', 'release_year']].dropna().head(10)
df["type"].value_counts()

fig = px.funnel(df.rating.value_counts(), labels={'index':'rating type'})
fig.show()

grp = df.groupby('type')
movie = grp.get_group('Movie')
movie['duration'] = [int(i.split(' ')[0]) for i in movie.duration.dropna()]
fig = px.histogram(movie, x='duration', nbins=60, labels={'duration':'duration (in mins)'})
fig.show()

movie = grp.get_group('Movie')
movie['duration'] = [int(i.split(' ')[0]) for i in movie.duration.dropna()]
fig = px.violin(movie, x='duration', box=True, points="all", labels={'duration':'duration (in mins)'})
fig.show()

#longest movie
fig = px.bar(movie.sort_values('duration')[['title', 'duration']].iloc[:20], x='title', y='duration',
             labels={'index':'Director', 'value':'movie count'})
fig.show()

movie.sort_values('duration')[['title', 'director', 'country', 'rating', 'duration', 'description']].iloc[:3]

fig = px.bar(movie.sort_values('duration')[['title', 'duration']].iloc[-20:], x='title', y='duration',
             labels={'title':'Movie name'})
fig.show()

movie.sort_values('duration')[['title', 'director', 'country', 'rating', 'duration', 'description']].iloc[-3:]

tv_series = grp.get_group('TV Show')
tv_series['duration'] = [int(i.split(' ')[0]) for i in tv_series.duration]
fig = px.histogram(tv_series, x='duration', nbins=20, labels={'duration':'number of seasons'})
fig.show()

dd = df[df['type']=='TV Show'][['title', 'duration']]
dd['duration'] = [int(i.split(' ')[0]) for i in dd.duration]
fig = px.bar(dd.sort_values('duration', ascending=False).iloc[:25], x='title', y='duration',
             labels={'title':'TV series name', 'duration':'number of seasons'})
fig.show()

dd = pd.DataFrame()
dd['director'] = [f'{i} ({j})' for i,j in df[['director', 'country']].dropna().values]
fig = px.bar(dd.director.value_counts()[:20], labels={'index':'Director', 'value':'movie count'})
fig.show()

dd = pd.DataFrame()
dd['cast'] = np.hstack([np.array(i.split(',')) for i in df.cast.dropna()])
fig = px.bar(dd.cast.value_counts()[:25], labels={'index':'cast', 'value':'movie count'})
fig.show()

dd = pd.DataFrame()
dd['listed_in'] = np.hstack([np.array(i.split(', ')) for i in df.listed_in.dropna()])
fig = px.bar(dd.listed_in.value_counts(), labels={'index':'genre', 'value':'movie count'}, orientation='h')
fig.show()

text = ' '.join(df.description.dropna().values)
wordcloud = WordCloud(background_color = 'black').generate(text)
plt.figure(figsize=(15, 6))
plt.imshow(wordcloud)
plt.axis('off')
plt.show()

text = ' '.join(df.title.dropna().values)
wordcloud = WordCloud(background_color = 'black').generate(text)
plt.figure(figsize=(15, 6))
plt.imshow(wordcloud)
plt.axis('off')
plt.show()

#Author Zihan Luo, create output label.
df = df.dropna()
labels_type_rating = np.hstack((df.type.dropna(), df.rating.dropna()))
arr_labels_type_rating = df["type"] + ', ' + df["rating"]
unique = np.unique(labels_type_rating)
def generate_label(x):
    genres = x.split(', ')
    label = np.zeros(shape=unique.shape)
    for i in genres:
        for j in range(len(unique)):
            if unique[j]==i:
                label[j]=1
    return label.astype(int)

#Author Zihan Luo, double check ndarr 'genres' correctly output 
#genres = ([np.array(i.split(', ')) for i in arr_labels_type_rating])
#genres[:]

#what were the output for genres in original code.
#genres = ([np.array(i.split(', ')) for i in df.listed_in.dropna()])
#genres[:]

#Author Zihan Luo, check the new combined array.
arr_labels_type_rating.head()
unique.view()

#Author Zihan Luo, input type & rating to the ylabel corpus 'data['label']'.
from tqdm.notebook import tqdm
data = pd.DataFrame()
data['text'] = df.dropna()['description']
data['title'] = df.dropna()['title']
data['label'] = [generate_label(x) for x in tqdm(arr_labels_type_rating.dropna())]
data[['text', 'label']].head()

#function for creating output labels from show genre (the feature 'listed_in' in the dataset)
#labels = np.hstack([np.array(i.split(', ')) for i in df.listed_in.dropna()])
#unique = np.unique(labels)
#def generate_label(x):
#    genres = x.split(', ')
#    label = np.zeros(shape=unique.shape)
#    for i in genres:
#        for j in range(len(unique)):
#            if unique[j]==i:
#                label[j]=1
#    return label.astype(int)

#from tqdm.notebook import tqdm
#data = pd.DataFrame()
#data['text'] = df.dropna()['description']
#data['title'] = df.dropna()['title']
#data['label'] = [generate_label(x) for x in tqdm(df.dropna()['listed_in'])]
#data[['text', 'label']].head()

def get_wordlen(x): 
    return len(x.split())

data['len'] = data.text.apply(get_wordlen)
data['len'].plot(kind='hist')
plt.title('histogram of show description word length')
plt.xlabel('word length')
plt.show()
for i in np.arange(0.9,1,0.01):
    p = data.len.quantile(i)
    print(f'word length at {int(i*100)} percentile:',p)

#Author Zihan Luo, Timestamp and starter
import time

Start_time_stamp = time.time()
print("Timestamp:", Start_time_stamp)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(data[['text', 'title']], data['label'], test_size=0.3, random_state=33)
X_val, X_test, y_val, y_test = train_test_split(X_test, y_test, test_size=0.5, random_state=33)

y_train.shape, y_val.shape, y_test.shape

!pip install bert-tensorflow

!pip install transformers

# importing necessary libraries
import tensorflow_hub as hub
import tensorflow as tf
from tensorflow.keras import Model
from transformers import BertTokenizer, TFBertModel
from tensorflow.keras.layers import Dense, GlobalAveragePooling1D, Input
tf.get_logger().setLevel('ERROR')

tf.keras.backend.clear_session()
max_seq_length = 31
input_word_ids = tf.keras.layers.Input(shape=(max_seq_length,), dtype=tf.int32, name="input_word_ids" )
input_mask = tf.keras.layers.Input(shape=(max_seq_length,), dtype=tf.int32, name="input_mask")
segment_ids = tf.keras.layers.Input(shape=(max_seq_length,), dtype=tf.int32, name="segment_ids")
bert_layer = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/1", trainable=False, name='BERT')
pooled_output, sequence_output = bert_layer([input_word_ids, input_mask, segment_ids])
bert_model = Model(inputs=[input_word_ids, input_mask, segment_ids], outputs=sequence_output)

bert_model.summary(), bert_model.output, bert_model.input

tf.keras.utils.plot_model(bert_model, show_shapes=False, show_dtype=False,
                          show_layer_names=True, rankdir='TB', 
                          expand_nested=False, dpi=96)

from bert import tokenization
vocab_file = bert_layer.resolved_object.vocab_file.asset_path.numpy() 
do_lower_case = bert_layer.resolved_object.do_lower_case.numpy()
tokenizer = tokenization.FullTokenizer(vocab_file, do_lower_case)

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def text_to_tokens(x):
    t = np.asarray(tokenizer.tokenize(x))
    if len(t)>max_seq_length-2:
        t = t[:max_seq_length-2]
    padding = np.asarray(['[PAD]']*(max_seq_length-t.shape[0]-2))
    pre, post = np.asarray(['[CLS]']), np.asarray(['[SEP]'])
    final = np.concatenate((pre,t,post,padding))
    ids = np.asarray(tokenizer.convert_tokens_to_ids(final))
    mask = (ids != 0)*1
    segment = np.zeros_like(ids)
    return ids, mask, segment

from tqdm.notebook import tqdm
# initializing lists to collect the generated tokens, masks and segments. 
X_train_tokens, X_val_tokens, X_test_tokens = [], [], []
X_train_mask, X_val_mask, X_test_mask = [], [], []
X_train_segment, X_val_segment, X_test_segment = [], [], []
# Generating and storing tokens, masks, segments values for X_train texts
for i,x in tqdm(enumerate(X_train.text.values)): 
    t,m,s = text_to_tokens(x) 
    X_train_tokens.append(t) 
    X_train_mask.append(m) 
    X_train_segment.append(s)
    
# Generating and storing tokens, masks, segments values for X_val texts
for i,x in tqdm(enumerate(X_val.text.values)): 
    t,m,s = text_to_tokens(x) 
    X_val_tokens.append(t) 
    X_val_mask.append(m) 
    X_val_segment.append(s)
    
# Generating and storing tokens, masks, segments values for X_test texts
for i,x in tqdm(enumerate(X_test.text.values)): 
    t,m,s = text_to_tokens(x) 
    X_test_tokens.append(t) 
    X_test_mask.append(m) 
    X_test_segment.append(s)

# converting the tokens lists to array type
X_train_tokens = np.row_stack(X_train_tokens) 
X_val_tokens = np.row_stack(X_val_tokens) 
X_test_tokens = np.row_stack(X_test_tokens)
# converting the masks lists to array type
X_train_mask = np.row_stack(X_train_mask) 
X_val_mask = np.row_stack(X_val_mask) 
X_test_mask = np.row_stack(X_test_mask)
# converting the segment lists to array type
X_train_segment = np.row_stack(X_train_segment) 
X_val_segment = np.row_stack(X_val_segment) 
X_test_segment = np.row_stack(X_test_segment)

X_train_pooled_output = bert_model.predict([X_train_tokens, X_train_mask, X_train_segment])
X_val_pooled_output = bert_model.predict([X_val_tokens, X_val_mask, X_val_segment])
X_test_pooled_output = bert_model.predict([X_test_tokens, X_test_mask, X_test_segment])

#origin output (3365, 31, 768)
X_train_pooled_output.shape

tf.keras.backend.clear_session()

input_layer = Input((None, 768))
gpa = GlobalAveragePooling1D()(input_layer)
# x = Dense(units=64, activation='elu')(gpa)
# x = Dense(units=64, activation='elu')(x)
#Author Zihan Luo, changed dense unit to 8, as number of type and rating is 8, original code: output_layer = Dense(units=42, activation='sigmoid')(gpa)
output_layer = Dense(units=8, activation='sigmoid')(gpa)

mlp = Model(input_layer, output_layer)
mlp.summary()

tf.keras.utils.plot_model(mlp, show_shapes=False, show_dtype=False,
                          show_layer_names=True, rankdir='TB', 
                          expand_nested=False, dpi=96)

from sklearn.metrics import accuracy_score
def get_accuracy(y, y_pred):
    acc = []
    for i,j in zip(y, y_pred):
        acc.append(accuracy_score(i,j))
    return np.mean(acc)

def accuracy(y, y_pred):
    return tf.py_function(get_accuracy, (y, tf.cast((y_pred>0.5), tf.float32)), tf.double)

from tensorflow.keras import optimizers
metrics = [accuracy]
mlp.compile(optimizer=optimizers.Adam(0.0001), loss='binary_crossentropy', metrics=metrics)

y_train_output = np.vstack(y_train.values)
y_test_output = np.vstack(y_test.values)
y_val_output = np.vstack(y_val.values)

history = mlp.fit(X_train_pooled_output, y_train_output, epochs=40, validation_data=(X_val_pooled_output, y_val_output))

#Author Zihan Luo, timestamp Ender
End_time_stamp = time.time()
print("Time duration:", (End_time_stamp - Start_time_stamp))

df_metric = pd.DataFrame()
df_metric['epoch'] = np.arange(len(history.history['loss']))
df_metric['loss'] = history.history['loss']
df_metric['val_loss'] = history.history['val_loss']
df_metric['accuracy'] = history.history['accuracy']
df_metric['val_accuracy'] = history.history['val_accuracy']

fig = px.line(df_metric, x="epoch", y=["accuracy", 'val_accuracy'])
fig.show()

fig = px.line(df_metric, x="epoch", y=["loss", 'val_loss'])
fig.show()

from sklearn.metrics import accuracy_score
y_pred = (mlp.predict(X_test_pooled_output)>0.5)*1
acc = [accuracy_score(i,j) for i,j in zip(y_pred, y_test)]
idx = np.argsort(acc)[::-1]
def show(i):
    print(f'movie: {X_test.title.values[i]}')
    print(f'description: {X_test.text.values[i]}')
    y_act_idx = unique[np.where(y_test_output[i]==1)]
    y_pred_idx = unique[np.where(y_pred[i]==1)]
    print(f'metric score: {acc[i]}')
    print(f'actual type & rating: {y_act_idx}')
    print(f'predicted type & rating: {y_pred_idx}')
    print('\n', '*'*50, '\n')
    
for i in idx[:10]:
    show(i)

from sklearn.metrics import accuracy_score
y_pred = (mlp.predict(X_test_pooled_output)>0.5)*1

fig = px.histogram(acc, nbins=20, labels={'value':'Accuracy score'})
fig.show()

#Author Zihan Luo, Accuracy score
history.history['accuracy'].pop()

#Author Zihan Luo
y_test_arr = y_test.to_numpy()
a, b, c, d, e, f, g, h = map(list, zip(*y_test_arr))
y_test_type = np.stack((a, b), axis=1)
y_test_rating = np.stack((c, d, e, f, g, h), axis=1)
a, b, c, d, e, f, g, h = map(list, zip(*y_pred))
y_pred_type = np.stack((a, b), axis=1)
y_pred_rating = np.stack((c, d, e, f, g, h), axis=1)

#Author Zihan Luo, Confusion matrix, UMCOMPLETE
from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels
print(confusion_matrix(y_test_type.argmax(axis=1), y_pred_type.argmax(axis=1)))
print(confusion_matrix(y_test_rating.argmax(axis=1), y_pred_rating.argmax(axis=1)))
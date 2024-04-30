import pandas as pd
import numpy as np
from corextopic import corextopic as ct
import topic_discovery as td
import warnings

# Ignore warnings to make things look prettier ... not good long term
warnings.filterwarnings('ignore')

"""
Design topics

Todo: Move to an excel format eventually

Design:

[
    'Topic Name',
    ['keywords', 'and ngrams'],
    ['hard assignment', 'words and phrases'],
    ['soft assignment', 'words and phrases']
]

"""

# Import the previously cleaned data to save some time
chatlogs = pd.read_csv('Data/data.csv')


# Assign topic choices here
topic_choices = [
    [
        'AccessCodes',
        ['access', 'code', 'multi', 'key'],
        [],
        []

    ],
    [
        'Frustration',
        ['speak with agent', 'annoyed', 'again', 'fuck', 'stupid'],
        [],
        []
    ]
]

# From the topic choices, convert to lists
column_choices = [x[0] for x in topic_choices]
anchors = [x[1] for x in topic_choices]
hard_anchors_all = [x[2] for x in topic_choices]
hard_anchors_other = [x[3] for x in topic_choices]

# Prepare the vectorizer
no_topics, vectorizer, tfidf, vocab = td.prepare_vectorizer(chatlogs, column_choices, ngram_range=[1, 3])

# Remove bad anchors
anchors = [[a for a in topic if a in vocab] for topic in anchors]

# Train the model
model = ct.Corex(n_hidden=no_topics, seed=100)
model = model.fit(
    tfidf,
    words=vocab,
    anchors=anchors,
    anchor_strength=10
)

for i, topic_ngrams in enumerate(model.get_topics(n_words=50)):
    topic_ngrams = [ngram[0] for ngram in topic_ngrams if ngram[1] > 0]
    print("\033[1mTopic #{}: {}".format(i + 1, "\033[0m, ".join(topic_ngrams)))
    print()

# Assign Topics to Chats
topic_df = pd.DataFrame(model.transform(tfidf), columns=[column_choices]).astype(float)
topic_df.index = chatlogs.index
chatlogs_slice = pd.concat([chatlogs[['BODY', 'STEMMED', 'BIGRAMS', 'TRIGRAMS', 'LEMMATIZED']].copy(), topic_df], axis=1)
chatlogs_slice.columns = ['BODY', 'STEMMED', 'BIGRAMS', 'TRIGRAMS', 'LEMMATIZED'] + column_choices
summary_df = chatlogs_slice.copy()

# Create ID column
conditions = []
for topic_choice in column_choices:
    conditions.append((summary_df[topic_choice] == 1))
summary_df['Identifier'] = np.select(conditions, column_choices, default='Other')
"""
# Reassign based on hard anchors
for topic in range(0, no_topics):
    for hard_anchor in hard_anchors_all[topic]:
        summary_df.loc[summary_df['STEMMED'].str.contains(hard_anchor), 'Identifier'] = column_choices[topic]
    for hard_anchor in hard_anchors_other[topic]:
        summary_df.loc[(summary_df['STEMMED'].str.contains(hard_anchor)) & (summary_df['Identifier'] == 'Other'),
                       'Identifier'] = column_choices[topic]
"""
# No junk allowed in visuals
visuals_df = summary_df.loc[summary_df['Identifier'] != 'Junk']

# Topic Distribution
vcs = summary_df.Identifier.value_counts()
vcs.index = ['\033[91m' + x + '\033[0m' if (x == 'Other') | (x == 'ML Topic')  # Makes things pretty
             else '\033[92m' + x + '\033[0m'
             for x in vcs.index]
print('\n\033[1mCurrent Values:\033[0m')
print(vcs)
print(sum(vcs))

# Export labelled chats
summary_df.to_csv('Data/labelled_data.csv', index=False)


# For each topic, return the most common keywords
num_most_common_tokens = 60
sample_size = 0

for choice in column_choices:
    slice_df, most_common_tokens = td.get_most_common_tokens(summary_df, choice, sample_size, num_most_common_tokens)

print(most_common_tokens)

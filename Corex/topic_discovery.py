import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from IPython.display import display
from collections import Counter
import re
import seaborn as sns
from operator import add
from sklearn.feature_extraction.text import TfidfVectorizer
from corextopic import corextopic as ct


###############
# CorEx Setup #
###############

# Performs the TF-IDF transformation from a provided matrix of counts
def prepare_vectorizer(chatlogs, column_choices, ngram_range):
    no_topics = len(column_choices)

    vectorizer = TfidfVectorizer(
        ngram_range=(ngram_range[0], ngram_range[1]),
        norm=None,
        binary=True,
        use_idf=False,
        sublinear_tf=False
    )

    vectorizer = vectorizer.fit(chatlogs['STEMMED'].values.astype('U'))
    tfidf = vectorizer.transform(chatlogs['STEMMED'].values.astype('U'))
    vocab = vectorizer.get_feature_names()

    return no_topics, vectorizer, tfidf, vocab


####################
# Topic Components #
####################

def get_most_common_tokens(df_input, choice, ss_choice=10, num_most_common_tokens=20):
    slice_df = df_input[['Identifier', 'BODY', 'LEMMATIZED']].copy()

    # If default, show other and ML topic together
    if choice.lower() == 'default':
        slice_df = slice_df.loc[(slice_df['Identifier'] == 'Other') | (slice_df['Identifier'] == 'ML Topic')]
    else:
        slice_df = slice_df.loc[slice_df['Identifier'] == choice].sort_values(by='Identifier')

    # Print most common tokens for topic
    # If there are 20 or less tokens, print in a single line
    # Otherwise, print over multiple lines, 20 values (max) each
    print('\033[1mMost Common Tokens in ' + choice + '\033[0m (Size ' + str(num_most_common_tokens) + ')')
    if num_most_common_tokens <= 20:
        most_common_tokens = pd.DataFrame(
            Counter(" ".join(slice_df['LEMMATIZED']).split()).most_common(num_most_common_tokens))
        mct_t = most_common_tokens.transpose()
        mct_t.columns = list(range(1, 21))
        mct_t.index = ['Word', 'Count']
        display(mct_t)
    else:
        most_common_tokens = pd.DataFrame(
            Counter(" ".join(slice_df['LEMMATIZED']).split()).most_common(num_most_common_tokens))
        for set_of_twenty in range(0, 1 + (num_most_common_tokens - 1) // 20):
            set_mct = most_common_tokens[set_of_twenty * 20:20 + set_of_twenty * 20]
            s_mct_t = set_mct.transpose()
            s_mct_t.columns = list(
                range(1 + set_of_twenty * 20, min(21 + set_of_twenty * 20, len(most_common_tokens) + 1)))
            s_mct_t.index = ['Word', 'Count']
            display(s_mct_t)

    # Print sample of topic
    print('\n\033[1mSample of ' + choice + '\033[0m (Size ' + str(ss_choice) + ')')
    display(slice_df.sample(ss_choice))

    return slice_df, most_common_tokens


##############################
# Composition Visualizations #
##############################

def plot_composition(visuals_df, no_topics, color_choice, legend_pos='upper left'):
    df_temp = pd.DataFrame(visuals_df['Identifier'].value_counts(normalize=True)).reset_index()
    df_temp.columns = ['x', 'y']
    colors = sns.color_palette(color_choice, no_topics + 1)

    # Bar Plot
    sns.set_theme(rc={'figure.figsize': (20, 7), 'axes.facecolor': 'white'})
    sns.barplot(x="x", y="y", data=df_temp, palette=colors)
    plt.xlabel('Topic', weight='bold').set_fontsize('18')
    plt.ylabel('Percent of Total', weight='bold').set_fontsize('18')
    plt.grid(False)
    plt.savefig('Plots/bar_plot_composition.png', transparent=True)
    plt.show()

    # Stacked Bar
    colors = sns.color_palette(color_choice, no_topics + 1)[::-1]
    ax = df_temp.set_index('x').transpose().plot(kind='bar', stacked=True, legend='reverse', width=0.25,
                                                 figsize=[10, 8],
                                                 color=colors)
    plt.legend(loc=legend_pos)

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], loc='upper left')

    plt.axis('off')
    plt.savefig('Plots/stacked_bar.png', transparent=True)
    plt.show()

    # Pie Chart No Numbers
    plt.subplots(figsize=[15, 9])
    ax = plt.pie(x=df_temp.y, labels=df_temp.x,
                 pctdistance=0.85, normalize=True,
                 colors=colors, textprops={'fontsize': 24},
                 )
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig('Plots/pie_composition.png', transparent=True)
    plt.show()

    # Pie Chart
    plt.subplots(figsize=[15, 9])
    _, _, autotexts = plt.pie(x=df_temp.y, labels=df_temp.x,
                              pctdistance=0.85, normalize=True,
                              colors=colors, autopct='%1.1f%%',
                              textprops={'fontsize': 24},
                              )
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_weight('bold')
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig('Plots/pie_labels_composition.png', transparent=True)
    plt.show()


#########################
# N-Gram Visualizations #
#########################

def list_wordcloud(visuals_df):
    """Plots a list wordcloud of relevant keywords"""

    for topic in list(visuals_df['Identifier'].unique()):
        for num_show in [True, False]:
            sliced_df = visuals_df.loc[visuals_df['Identifier'] == topic]
            most_common_tokens = pd.DataFrame(Counter(''.join(str(sliced_df['STEMMED'])).split()).most_common(20))

            most_common_tokens[2] = most_common_tokens[1] / max(most_common_tokens[1])

            fig, ax = plt.subplots(figsize=(6, 10))
            plt.ylim(0, len(most_common_tokens))
            plt.xticks([])
            plt.yticks([])
            plt.axis('off')
            plt.title('Topic: {}'.format(topic), fontsize=30, weight='bold')

            for i, (word, share) in enumerate(zip(most_common_tokens[0], most_common_tokens[2])):
                if num_show == True:
                    word = word + ' (' + str(most_common_tokens[1][i]) + ')'
                else:
                    word = word
                plt.text(0.3, len(most_common_tokens) - i - 1.0, word, fontsize=24 * share ** 0.15)

            plt.tight_layout()
            if num_show == False:
                plt.savefig('Plots/WC_' + topic + '.png', transparent=True)
                plt.close(fig)
            else:
                plt.savefig('Plots/WC_NUMS_' + topic + '.png', transparent=True)
            plt.show()

    return None


def get_makeup(ngrams, full_df):
    l = []

    for ngram in ngrams.index:
        ngram_val = ngram[0].replace(',', '').replace('(', '').replace(')', '')
        sliced_df = full_df.loc[full_df['STEMMED'].str.contains(ngram_val)][['Identifier']]
        vc_s_df = sliced_df.value_counts()
        l.append(vc_s_df)
    l_df = pd.DataFrame(l).fillna(0)

    return l_df


def ngram_distributions(visuals_df, column_choices, color_choice, bad_ngrams=[],
                        plotsize_x=25, plotsize_y=10, asc_or_desc=False, allow_title=True):

    # For all topics
    l_bigrams = ', '.join(str(visuals_df['BIGRAMS'].copy()))
    l_trigrams = ', '.join(str(visuals_df['TRIGRAMS'].copy()))
    l_both = l_bigrams + l_trigrams
    mcbt = pd.DataFrame([x[1:] for x in re.split('\), ', l_both)]).value_counts()[0:10 + len(bad_ngrams)]
    for word in list(column_choices):
        if word == 'Junk': column_choices.remove(word)

    # Create DF for plotting
    colors = sns.color_palette(color_choice, len(column_choices) + 1)
    x = get_makeup(mcbt, visuals_df)
    x.index = [str(x).replace('(', '').replace(')', '').upper() for x in mcbt.index]
    for bad_ngram in bad_ngrams:
        try:
            x = x.drop('\'' + bad_ngram + '\',')
        except:
            None
    l_sum = []
    for vals in x.iterrows():
        l_sum.append(sum(vals[1]))
    x['SUM'] = l_sum
    x2 = x.sort_values(x.columns[-1], ascending=asc_or_desc).drop('SUM', axis=1)

    # Plot all topics together in one chart
    ax = x2.plot(kind='barh', stacked=True, figsize=(plotsize_x, plotsize_y),
                 color=colors, rot=0, fontsize=15, legend='bottom right')
    if allow_title == True: plt.title('Most Common N-Grams', fontsize=30)
    plt.xlabel('Frequency', fontsize=18, labelpad=25)
    plt.ylabel('N-Gram', fontsize=18, labelpad=25)
    ax.grid(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.figure.savefig('Plots/Common Ngrams All Topics.png', transparent=True)
    plt.show()

    # For each individual topic
    for color_counter in range(0, len(column_choices)):
        topic_choice = column_choices[color_counter]
        slice_summary_df = visuals_df.loc[visuals_df['Identifier'] == topic_choice]

        l_bigrams = ', '.join(slice_summary_df['BIGRAMS'])
        l_trigrams = ', '.join(slice_summary_df['TRIGRAMS'])
        l_both = l_bigrams + l_trigrams
        mcbt = pd.DataFrame([x[1:] for x in re.split('\), ', l_both)]).value_counts()[0:10 + len(bad_ngrams)]

        colors = sns.color_palette(color_choice, len(column_choices))
        x = get_makeup(mcbt, slice_summary_df)
        x.index = [str(x).replace('(', '').replace(')', '').replace("'", "").upper()[:-1] for x in mcbt.index]

        # Sort values by column
        l_sum = []
        for vals in x.iterrows():
            l_sum.append(sum(vals[1]))
        x['SUM'] = l_sum
        x2 = x.sort_values(x.columns[-1], ascending=asc_or_desc).drop('SUM', axis=1)
        for bad_ngram in bad_ngrams:
            try:
                x2 = x2.drop(bad_ngram)
            except:
                None
        x2 = x2[0:10]
        x2 = x2 / max(x2.values)

        ax = x2.plot(kind='barh', figsize=(plotsize_x, plotsize_y), color=colors[color_counter], rot=0, fontsize=15,
                     legend='')
        if allow_title == True: plt.title(column_choices[color_counter], fontsize=30)
        ax.grid(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        plt.xlabel('Relative Frequency', fontsize=18, labelpad=25)
        plt.ylabel('N-Gram', fontsize=18, labelpad=25)
        print(column_choices[color_counter])
        ax.figure.savefig('Plots/Common Ngrams ' + column_choices[color_counter] + '.png', transparent=True)
        plt.show()

    return None


#########
# Other #
#########

def kill_plots():
    import os
    import glob

    files = glob.glob('Plots/*')
    for f in files:
        os.remove(f)

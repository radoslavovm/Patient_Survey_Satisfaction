import topic_discovery as td
import main

import pandas as pd


# Import the previously cleaned data to save some time
chatlogs = pd.read_csv('Data/data.csv').head(100)

print(chatlogs)
# Prepare the vectorizer
# no_topics, vectorizer, tfidf, vocab = td.prepare_vectorizer(chatlogs, column_choices, ngram_range=[1, 3])
td.get_most_common_tokens(main.summary_df, 'Frustration', ss_choice=10, num_most_common_tokens=20)
# td.plot_composition(main.visuals_df, 3, 'pastel')
# td.list_wordcloud(main.visuals_df)
#df = main.visuals_df.dropna()
#td.ngram_distributions(df, main.column_choices, 'pastel')

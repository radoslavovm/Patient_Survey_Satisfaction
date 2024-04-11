# Patient_Survey_Satisfaction
How do we get the most out of survey responses? 

Using [TextBlob](https://textblob.readthedocs.io/en/dev/quickstart.html#sentiment-analysis) to provide a polarity score for every text comment a patient leaves. 

TextBlob.py 
    Functions involved in taking in a Patient Satisfaction Survey table, and creating a new table with the Survey ID and the polarity of each sentence.

Clustering.py
    This is for clustering similar sentences together. Purpose it to be able to see the distribution of topics in the survey comments and see what the most common category of complaints are. 

Connection.py 
    Here we establish a connection to the database. 
    I am having issues with establishing a connection using my credentials because the username includes a domain seperated by a \

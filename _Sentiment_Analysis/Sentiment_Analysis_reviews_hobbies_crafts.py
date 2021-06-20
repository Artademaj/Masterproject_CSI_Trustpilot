### Check current working directory and import packages###
import os
wd = os.getcwd() 
print(wd)

import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd
from pandas import DataFrame
import numpy as np
import string
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.tokenize import WhitespaceTokenizer
from nltk.stem import WordNetLemmatizer
from collections import Counter
from fuzzywuzzy import fuzz
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from afinn import Afinn
afinn = Afinn(language='en')
import warnings
warnings.filterwarnings("ignore")


### Create postgres connection, read in tables and clean data
engine = create_engine('postgresql://localhost/')

# Read table reviews_food_beverages_tobacco from Database
review_data = pd.read_sql_table(
    "reviews_hobbies_crafts",
    con=engine
)
# Change column name
review_data.columns.values[0] = "company_review"
# Remove empty review text
review_data.dropna(subset=['review_text'], inplace=True)
# Clip any spaces of the cells
review_data.columns = review_data.columns.to_series().apply(lambda x: x.strip())
# Set column as numeric
review_data["total_reviews"] = review_data["total_reviews"].str.replace(",","").astype(float)
review_data['total_reviews'] = pd.to_numeric(review_data['total_reviews'])
review_data['general_rating'] = pd.to_numeric(review_data['general_rating'])
review_data['review_rating'] = pd.to_numeric(review_data['review_rating'])
# print amount total reviews
print(review_data[review_data.columns[0]].count())
# print company amount
count_companies = review_data[['company_review']]
count_companies = count_companies.drop_duplicates(subset=None, keep="first", inplace=False)
print(count_companies[count_companies.columns[0]].count())

# Read table companies_list from Database
companies_list = pd.read_sql_table(
    "list_companies",
    con=engine
)
# Change column name
companies_list.columns.values[1] = "company_market"
# Clip any spaces of the cells
companies_list.columns = companies_list.columns.to_series().apply(lambda x: x.strip())
# Check companies list nan to know which stock price to use for comparison
# companies_list.isna().sum()
# Select only useful columns
market_companies = companies_list[['company_market', 'subsidiaries', 'price']]

# Read table sustainability_words from Database
sustainability_words = pd.read_sql_table(
    "sustainability_words",
    con=engine
)


### Sampled review data for test purposes to speed up computations.
#review_data = review_data.sample(frac = 0.01, replace = False, random_state=42)

### Data manupilation for FuzzyWuzzy
### Combine df with reviews and df with financial information
### FuzzyWuzzy required, since some company names are not in the same format in both dataframes

### Data manupilation review df for FuzzyWuzzy
# Extract specific characteristics from company name for fuzzy matching
review_data['first_10_letters'] = review_data['company_review'].str[:10]
review_data['last_20_letters'] = review_data['company_review'].str[-20:]

### Data manupilation market_companies df for FuzzyWuzzy
### Create new column, where company and subsidiary are seperated
# Create new column 'all_names' where first company name and if available subsidiaries are visible
market_companies['all_names'] = market_companies['company_market'].str.cat(market_companies['subsidiaries'],sep=", ")
market_companies.all_names.fillna(market_companies.company_market, inplace=True)
# Define index
market_companies.set_index('company_market')
# Dplit the strings (all company names) into lists
market_companies['all_names'] = market_companies['all_names'].str.split(', ')
# Explode the lists
market_companies = market_companies.explode('all_names').reset_index(drop=True)
# Extract specific characteristics from company name for FuzzyWuzzy
market_companies['first_10_letters'] = market_companies['all_names'].str[:10]
market_companies['last_20_letters'] = market_companies['all_names'].str[-20:]
# Drop duplicates, if the company name was also listet under the column 'subsidiaries'
market_companies.drop_duplicates(subset='all_names', keep="last")


### String Matching with FuzzyWuzzy
# Casting the first 10 letters and last 20 letters column of both df into lists
match_2_10 = list(market_companies.first_10_letters.unique())
match_1_10 = list(review_data.first_10_letters.unique())
match_2_15 = list(market_companies.last_20_letters.unique())
match_1_15 = list(review_data.last_20_letters.unique())
# Defining a function to return the match and similarity score of the fuzz.ratio() scorer. 
# The function will take in a term(name), list of terms(list_names), and a minimum similarity score(min_score) to return the match.
def match_names(name, list_names, min_score=0):
    #-1 we dont get any matches
    max_score = -1
    #returning empty name for no match
    max_name = ""
    #iternating over all names in the other
    for x in list_names:
        #finding fuzzy match score
        score = fuzz.ratio(name, x)
        #checking if we are above our threshold and have a better score
        if (score>min_score)& (score>max_score):
            max_name=x
            max_score=score
    return (max_name, max_score)
# For loop to create a list of tuples of the first 10 letters of a company name with the first value being the name 
# from the second dataframe (name to replace) and the second value from the first dataframe (string replacing the name value). 
# Then, casting the list of tuples as a dictionary. 
names= []
for x in match_1_10:
    match = match_names(x, match_2_10, 90)
    if match[1] >=90:
        name = ('(' + str(x), str(match[0]) +')')
        names.append(name)
name_dict_first = dict(names)
# For loop to create a list of tuples of the last 20 letters of a company name
names_2= []
for x in match_1_15:
    match = match_names(x, match_2_15, 90)
    if match[1] >=90:
        name_2 = ('(' + str(x), str(match[0]) +')')
        names_2.append(name_2)
name_dict_last = dict(names_2)
# Change the name_dict lists into a df, to merge afterwards the review and financial df
# Check which lists are empty and use only matched last / first letters
if (names != []) and (names_2 != []):
    print('usual code')
    first_10_letters_items = name_dict_first.items()
    first_10_letters_list = list(first_10_letters_items)
    first_10_letters_df = pd.DataFrame(first_10_letters_list)
    first_10_letters_df.columns = ['review_company_abbrev', 'exchange_company_abbrev']
    first_10_letters_df['review_company_abbrev'] = first_10_letters_df['review_company_abbrev'].str[1:] 
    first_10_letters_df['exchange_company_abbrev'] = first_10_letters_df['exchange_company_abbrev'].str[:-1] 
    last_20_letters_items = name_dict_last.items()
    last_20_letters_list = list(last_20_letters_items)
    last_20_letters_df = pd.DataFrame(last_20_letters_list)
    last_20_letters_df.columns = ['review_company_abbrev', 'exchange_company_abbrev']
    last_20_letters_df['review_company_abbrev'] = last_20_letters_df['review_company_abbrev'].str[1:] 
    last_20_letters_df['exchange_company_abbrev'] = last_20_letters_df['exchange_company_abbrev'].str[:-1] 
    # Some companies are listet in both FuzzyWuzzy outcomes. 
    # For this reason merge first the FuzzyWuzzy outcomes df's with review df seperated, and append the new df's 
    first_10_letters_reviews = pd.merge(first_10_letters_df, review_data, left_on = 'review_company_abbrev', right_on = 'first_10_letters', how = 'inner')
    last_20_letters_reviews = pd.merge(last_20_letters_df, review_data, left_on = 'review_company_abbrev', right_on = 'last_20_letters', how = 'inner')
    Merged_fuzzy_reviews = first_10_letters_reviews.append(last_20_letters_reviews, ignore_index=True)
    # The new df Merged_fuzzy_reviews could have duplicates
    # For this reason compare review text and delete duplicates
    out = []
    seen = set()
    for c in Merged_fuzzy_reviews['review_text']:
        words = c.split()
        out.append(' '.join([w for w in words if w not in seen]))
        seen.update(words)
    Merged_fuzzy_reviews['Final_review_text'] = out
    Merged_fuzzy_reviews = Merged_fuzzy_reviews[Merged_fuzzy_reviews.Final_review_text != '']
    # Finally merge FuzzyWuzzy outcomes with review df (Merged_fuzzy_reviews) and financial df (market_companies)
    bigdata1 = pd.merge(Merged_fuzzy_reviews, market_companies, on = 'first_10_letters', how = 'left')
    # Select only useful columns
    bigdata = bigdata1[['company_review', 'company_market', 'subsidiaries','all_names','category', 'total_reviews', 'general_rating', 'review_rating', 'review_text', 'price']]
elif (names != []) and (names_2 == []):
    print('only first letter')
    first_10_letters_items = name_dict_first.items()
    first_10_letters_list = list(first_10_letters_items)
    first_10_letters_df = pd.DataFrame(first_10_letters_list)
    first_10_letters_df.columns = ['review_company_abbrev', 'exchange_company_abbrev']
    first_10_letters_df['review_company_abbrev'] = first_10_letters_df['review_company_abbrev'].str[1:] 
    first_10_letters_df['exchange_company_abbrev'] = first_10_letters_df['exchange_company_abbrev'].str[:-1] 
    # Merge FuzzyWuzzy outcomes with review df seperated
    first_10_letters_reviews = pd.merge(first_10_letters_df, review_data, left_on = 'review_company_abbrev', right_on = 'first_10_letters', how = 'inner')
    # Finally merge FuzzyWuzzy outcomes with review df (Merged_fuzzy_reviews) and financial df (market_companies)
    bigdata1 = pd.merge(first_10_letters_reviews, market_companies, on = 'first_10_letters', how = 'inner')
    # Select only useful columns
    bigdata = bigdata1[['company_review', 'company_market', 'subsidiaries','all_names','category', 'total_reviews', 'general_rating', 'review_rating', 'review_text', 'price']]
elif (names == []) and (names_2 != []):
    print('only last letters')
    last_20_letters_items = name_dict_last.items()
    last_20_letters_list = list(last_20_letters_items)
    last_20_letters_df = pd.DataFrame(last_20_letters_list)
    last_20_letters_df.columns = ['review_company_abbrev', 'exchange_company_abbrev']
    last_20_letters_df['review_company_abbrev'] = last_20_letters_df['review_company_abbrev'].str[1:] 
    last_20_letters_df['exchange_company_abbrev'] = last_20_letters_df['exchange_company_abbrev'].str[:-1] 
    # Merge FuzzyWuzzy outcomes with review df seperated
    last_20_letters_reviews = pd.merge(last_20_letters_df, review_data, left_on = 'review_company_abbrev', right_on = 'last_20_letters', how = 'inner')
    # Finally merge FuzzyWuzzy outcomes with review df (Merged_fuzzy_reviews) and financial df (market_companies)
    bigdata1 = pd.merge(last_20_letters_reviews, market_companies, on = 'last_20_letters', how = 'inner')
    # Select only useful columns
    bigdata = bigdata1[['company_review', 'company_market', 'subsidiaries','all_names','category', 'total_reviews', 'general_rating', 'review_rating', 'review_text', 'price']]
# print amount total reviews after FuzzyWuzzy
print(bigdata[bigdata.columns[0]].count())
# print company amount after FuzzyWuzzy
count_companies_2 = bigdata[['company_review']]
count_companies_2 = count_companies_2.drop_duplicates(subset=None, keep="first", inplace=False)
print(count_companies_2[count_companies_2.columns[0]].count())
# print company amount from market list after FuzzyWuzzy
count_companies_3 = bigdata[['company_market']]
count_companies_3 = count_companies_3.drop_duplicates(subset=None, keep="first", inplace=False)
print(count_companies_3[count_companies_3.columns[0]].count())


### Sentiment Analysis
### Clean review_text
bigdata['review_text'].replace('', np.nan, inplace=True)
bigdata.dropna(subset=['review_text'], inplace=True)
bigdata['review_text']= bigdata['review_text'].astype(str)
# Remove special characters
spec_chars = ["!",'"',"#","%","&","'","(",")",
              "*","+",",","-",".","/",":",";","<",
              "=",">","?","@","[","\\","]","^","_",
              "`","{","|","}","~","–"]
for char in spec_chars:
    bigdata['review_text'] = bigdata['review_text'].str.replace(char, ' ')   
bigdata['review_text'] = bigdata['review_text'].str.split().str.join(" ")
# Clean text data
def clean_text(text):
    # lower text
    text = text.lower()
    # tokenize text and remove puncutation
    text = [word.strip(string.punctuation) for word in text.split(" ")]
    # remove words that contain numbers
    text = [word for word in text if not any(c.isdigit() for c in word)]
    # remove stop words
    stop = stopwords.words('english')
    text = [x for x in text if x not in stop]
    # remove empty tokens
    text = [t for t in text if len(t) > 0]
    # pos tag text
    pos_tags = pos_tag(text)
    # lemmatize text
    #text = [WordNetLemmatizer().lemmatize(t[0], get_wordnet_pos(t[1])) for t in pos_tags]
    # remove words with only one letter
    text = [t for t in text if len(t) > 1]
    # join all
    text = " ".join(text)
    return(text)
bigdata["review_clean"] = bigdata["review_text"].apply(lambda x: clean_text(x))
# Add sentiment anaylsis columns
sid = SentimentIntensityAnalyzer()
bigdata["sentiments"] = bigdata["review_clean"].apply(lambda x: sid.polarity_scores(x))
bigdata = pd.concat([bigdata.drop(['sentiments'], axis=1), bigdata['sentiments'].apply(pd.Series)], axis=1)
# To estimate Afinn sentiment score for reviews, the scorer is applied to the "review_text" column 
# and a new column is created
bigdata['afinn_score'] = bigdata['review_clean'].apply(afinn.score)
# With the raw Afinn scores, longer texts have higher scores simply because they contain more words. 
# To compensate for this, the scores are divided by the number of words in the text using the split method.
def word_count(text_string):
    '''Calculate the number of words in a string'''
    return len(text_string.split())
# To apply the function to the 'review_clean' column, a new word_count column is created. 
bigdata['word_count'] = bigdata['review_clean'].apply(word_count)
# Original score (afinn_score) is divided by word count to get afinn_adjusted. 
# This is not exactly a percentage variable, since word scores in Afinn can range from -5 to 5, 
# but it is a useful adjustment to control for variable comment length. 
# To make the results more readable, the adjustment is multiplied by 100.
bigdata['sentiment'] = bigdata['afinn_score'] / bigdata['word_count'] * 100


### Add sustainability dictionary 
# Extract the three dimensions in seperate lists
social_words_list = sustainability_words['social_sustainability'].values
environmental_words_list = sustainability_words['environmental_sustainability'].values
economic_words_list = sustainability_words['economic_sustainability'].values
# Class for count occurences for words
def count_occurences(text, word_list):
    '''Count occurences of words from a list in a text string.'''
    text_list = text_to_words(text)
    intersection = [w for w in text_list if w in word_list]
    return len(intersection)
def text_to_words(text):
    '''Transform a string to a list of words,
    removing all punctuation.'''
    text = text.lower()
    p = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    text = ''.join([ch for ch in text if ch not in p])
    return text.split()
# Add new column in review df where amount of sustainability words are summed 
bigdata['social_sustainability_words'] = bigdata['review_clean'].apply(count_occurences, args=(social_words_list, ))
bigdata['environmental_sustainability_words'] = bigdata['review_clean'].apply(count_occurences, args=(environmental_words_list, ))
bigdata['economic_sustainability_words'] = bigdata['review_clean'].apply(count_occurences, args=(economic_words_list, ))

# Label sustainable reviews
bigdata['Sustainability'] = np.where((bigdata['environmental_sustainability_words'] > ((bigdata['social_sustainability_words'])) & (bigdata['economic_sustainability_words'])) & 
                                     (bigdata['sentiment'] >= 0), 'Positive Environmental', 
                                np.where((bigdata['environmental_sustainability_words'] > ((bigdata['social_sustainability_words'])) & (bigdata['economic_sustainability_words'])) & 
                                         (bigdata['sentiment'] < 0), 'Negative Environmental', 
                                    np.where((bigdata['social_sustainability_words'] > ((bigdata['environmental_sustainability_words'])) & (bigdata['economic_sustainability_words'])) & 
                                             (bigdata['sentiment'] >= 0), 'Positive Social', 
                                        np.where((bigdata['social_sustainability_words'] > ((bigdata['environmental_sustainability_words'])) & (bigdata['economic_sustainability_words'])) & 
                                                 (bigdata['sentiment'] < 0), 'Negative Social', 
                                            np.where((bigdata['economic_sustainability_words'] > ((bigdata['environmental_sustainability_words'])) & (bigdata['social_sustainability_words'])) & 
                                                     (bigdata['sentiment'] >= 0), 'Positive Economic', 
                                                np.where((bigdata['economic_sustainability_words'] > ((bigdata['environmental_sustainability_words'])) & (bigdata['social_sustainability_words'])) & 
                                                         (bigdata['sentiment'] < 0), 'Negative Economic', 
                                                    'Non-Sustainable'                                 
                                    ))))))
#New dummy columns to groupby later on
bigdata.loc[bigdata['Sustainability'] == 'Positive Environmental', 'Positive Environmental'] = 1
bigdata.loc[bigdata['Sustainability'] == 'Negative Environmental', 'Negative Environmental'] = 1
bigdata.loc[bigdata['Sustainability'] == 'Positive Social', 'Positive Social'] = 1
bigdata.loc[bigdata['Sustainability'] == 'Negative Social', 'Negative Social'] = 1
bigdata.loc[bigdata['Sustainability'] == 'Positive Economic', 'Positive Economic'] = 1
bigdata.loc[bigdata['Sustainability'] == 'Negative Economic', 'Negative Economic'] = 1
#Number of sustainable reviews per company
SustReviews = bigdata.groupby('company_review').sum() #Get total number of sust tweets, for percentage use .mean()
SustReviews['Total Sustainability Reviews'] = (SustReviews['Positive Environmental'] + 
                                               SustReviews['Negative Environmental'] + 
                                               SustReviews['Positive Social'] + 
                                               SustReviews['Negative Social'] + 
                                               SustReviews['Positive Economic'] +                                              
                                               SustReviews['Negative Economic'])
#Merge datasets
Reviews = pd.merge(SustReviews, bigdata, on = 'company_review', how = 'inner')


### Calculate Sustainability Index
# Sustainability Index can be divided into social, economic and environmental
# Create classes for dividing the new calculated columns
def divide_cols(df_sub):
    df_sub['Positive Index'] = ((df_sub['Positive Environmental_x'] + df_sub['Positive Social_x'] + df_sub['Positive Economic_x']) / df_sub['Total Sustainability Reviews']) * 100
    return df_sub
def divide_two_cols(df_sub):
    df_sub['Sustainability Index'] = (df_sub['Total Sustainability Reviews'] / df_sub['total_reviews_x']) * 100
    return df_sub
def ratio_division_social(df_sub):
    df_sub['Social Index'] = ((df_sub['Positive Social_x'] + df_sub['Negative Social_x']) / df_sub['Total Sustainability Reviews']) * 100
    return df_sub
def ratio_division_environmental(df_sub):
    df_sub['Environmental Index'] = ((df_sub['Positive Environmental_x'] + df_sub['Negative Environmental_x']) / df_sub['Total Sustainability Reviews']) * 100
    return df_sub
def ratio_division_economic(df_sub):
    df_sub['Economic Index'] =  ((df_sub['Positive Economic_x'] + df_sub['Negative Economic_x']) / df_sub['Total Sustainability Reviews']) * 100
    return df_sub
# Apply the classes for calculating the different Index
Reviews = Reviews.groupby('company_review').apply(divide_cols)
Reviews = Reviews.groupby('company_review').apply(divide_two_cols)
Reviews = Reviews.groupby('company_review').apply(ratio_division_social)
Reviews = Reviews.groupby('company_review').apply(ratio_division_environmental)
Reviews = Reviews.groupby('company_review').apply(ratio_division_economic)


### Final df with the calculated Sust. Index
# Select only useful column
final_df = Reviews[['company_review', 
                  'company_market',
                  'subsidiaries',
                  'all_names',
                  'category',
                  'price',
                  'sentiment_x',
                  'total_reviews_x',
                  'Total Sustainability Reviews',
                  'Positive Index',
                  'Sustainability Index',
                  'Environmental Index',
                  'Social Index',
                  'Economic Index']]
# Rename column for merge
final_df.columns.values[6] = "sentiment"
final_df.columns.values[7] = "total_reviews"
# Delete duplicates
final_df = final_df.drop_duplicates(subset='company_review', keep="last")

### Calculate the Sust. Index for each parent company to be able compare with the stock price
# Check where the parent company is listet more then one 
find_duplicates = final_df[final_df['company_market'].duplicated(keep=False)]
# Calulate the new mean for all parent companies 
find_duplicates['Avg Sustainability Index'] = find_duplicates['Sustainability Index'].groupby(find_duplicates['company_market']).transform('mean')
find_duplicates['Avg Social Index'] = find_duplicates['Social Index'].groupby(find_duplicates['company_market']).transform('mean')
find_duplicates['Avg Environmental Index'] = find_duplicates['Environmental Index'].groupby(find_duplicates['company_market']).transform('mean')
find_duplicates['Avg Economic Index'] = find_duplicates['Economic Index'].groupby(find_duplicates['company_market']).transform('mean')
find_duplicates['Avg Sentiment'] = find_duplicates['sentiment'].groupby(find_duplicates['company_market']).transform('mean')
# Select only useful columns
find_duplicates = find_duplicates[['company_market', 'Avg Sustainability Index', 'Avg Social Index', 'Avg Environmental Index', 'Avg Economic Index', 'Avg Sentiment']]
# Merge with market df and delete duplicates
find_duplicates_final = pd.merge(find_duplicates, final_df, on = 'company_market', how = 'outer')
find_duplicates_final = find_duplicates_final.drop_duplicates(subset=None, keep="first", inplace=False)
# Combine Indexes of all companies (also not S&P) in the same columns and delete the old columns
find_duplicates_final['Avg Sustainability Index'].fillna(find_duplicates_final['Sustainability Index'], inplace=True)
find_duplicates_final['Avg Social Index'].fillna(find_duplicates_final['Social Index'], inplace=True)
find_duplicates_final['Avg Environmental Index'].fillna(find_duplicates_final['Environmental Index'], inplace=True)
find_duplicates_final['Avg Economic Index'].fillna(find_duplicates_final['Economic Index'], inplace=True)
find_duplicates_final['Avg Sentiment'].fillna(find_duplicates_final['sentiment'], inplace=True)
del find_duplicates_final['Sustainability Index']
del find_duplicates_final['Social Index']
del find_duplicates_final['Environmental Index']
del find_duplicates_final['Economic Index']
del find_duplicates_final['sentiment']
# Change column to numeric
find_duplicates_final['Avg Sustainability Index'] = pd.to_numeric(find_duplicates_final['Avg Sustainability Index'])
find_duplicates_final['price'] = pd.to_numeric(find_duplicates_final['price'])
find_duplicates_final['Avg Sentiment'] = pd.to_numeric(find_duplicates_final['Avg Sentiment'])
# Delete duplicates and select only useful columns
find_duplicates_final = find_duplicates_final.drop_duplicates(subset='company_market', keep="last")
find_duplicates_final = find_duplicates_final[['company_market', 'category','Avg Sustainability Index', 'Avg Social Index', 'Avg Environmental Index', 'Avg Economic Index', 'price', 'Avg Sentiment']]
# Round numers to 2 decimals
find_duplicates_final.round(2)
find_duplicates_final = find_duplicates_final.assign(category='hobbies_crafts')
# Save df into SQL database
final_reviews_hobbies_crafts = find_duplicates_final
final_reviews_hobbies_crafts.to_sql('final_reviews_hobbies_crafts', engine)
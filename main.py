import gzip
import json
import tweepy as tw
import pandas as df

from google_trans_new import google_translator

translator = google_translator()
with gzip.open('', 'r') as zipfile:
    twitter_data = json.loads(zipfile.read().decode('ascii'))


# print( json.dumps(twitter_data[516], indent=4, sort_keys=True))


def twitter_search(searched_topic):
    lead_users = []

    for i in twitter_data:
        try:
            hashtags = []
            for hashtag in i['entities']['hashtags']:
                hashtags.append(hashtag['text'])

            if searched_topic in i['text'] or searched_topic in hashtags:
                lead_users.append(
                    [i['user']['name'], i['user']['followers_count'], i['text'], i['user']['url'], i['retweet_count']])

        except Exception as e:
            print(e)
            pass

    return lead_users


def get_lead_user(list_of_twits):
    tweet_text = df.DataFrame(data=list_of_twits,
                              columns=['user', "followers_count", 'text', 'url', 'retweet_count'])
    sorted_list_by_followers = tweet_text.sort_values(by=['followers_count', 'retweet_count'], ascending=False)

    return sorted_list_by_followers.head(10)


def get_who_had_the_most_twits(list_of_twits):
    return df['user'].value_counts().head(15)


def translate_twits(list_of_twits):
    for index, row in list_of_twits.iterrows():

        if translator.detect(row['text'])[0] != 'en' or translator.detect(row['text'])[0] != 'de':
            temp = translator.translate(row['text'], lang_tgt='de')
            list_of_twits.at[index, 'text'] = temp

    return list_of_twits


df.set_option('display.max_columns', 6)
df.set_option("display.max_colwidth", None)

print(translate_twits(get_lead_user(twitter_search(input("what do you want to search ?\n")))))

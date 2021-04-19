import gzip
import json
import tweepy as tw
import pandas as pd

from google_trans_new import google_translator


translator=google_translator()
with gzip.open('', 'r') as zipfile:
    twitter_data = json.loads(zipfile.read().decode('ascii'))


def twitter_search(searched_topic, list_of_twitts):
    lead_users = []
    users={}
    for i in list_of_twitts:
        try:
            hashtags = []
            for hashtag in i['entities']['hashtags']:
                hashtags.append(hashtag['text'])

            if searched_topic in i['text'] or searched_topic in hashtags:

                '''translate the twits to English '''
                # translated_twit
                # if translator.detect(i['text'])[0] == 'en' or translator.detect(i['text'])[0] == 'de' :
                #     translated_twit = translator.translate(i['text'], lang_tgt='en')

                # list of Tuple (user name , number of followers , the text of the twit ,twit url , number of retweets

                lead_users.append(
                    [i['user']['name'], i['user']['followers_count'], i['text'], i['user']['url'], i['retweet_count']])

        except Exception as e:
            print(e)
            pass

    return lead_users


temp_list = twitter_search('3d  ', twitter_data)
pd.set_option('display.max_columns', 6)


def get_lead_user(list_of_twitts):
    # list_of_users.sort(key=lambda x: x[1], reverse=True)
    # # sort the list with number of follower and get the first half of the list
    # sorted_list_by_followers = [x for x in
    #                             sorted(temp_list, key=lambda x: x[1], reverse=True)[:int(len(list_of_users) / 2)]]
    # # sort the list with number of twits and get the first half of the list
    # sorted_list_by_retweets = [x for x in sorted(sorted_list_by_followers, key=lambda x: x[4], reverse=True)[
    #                                       :int(len(list_of_users) / 2)]]
    tweet_text = pd.DataFrame(data=list_of_twitts,
                              columns=['user', "followers_count", 'text', 'url', 'retweet_count'])
    sorted_list_by_followers = tweet_text.sort_values(by=['followers_count', 'retweet_count'], ascending=False)

    """return the top ten element of the list"""""
    return sorted_list_by_followers.head(10)


print((get_lead_user(temp_list)))


import gzip
import json




with gzip.open('hier the name of the file ', 'r') as zipfile:
    twitter_data = json.loads(zipfile.read().decode('ascii'))


def twitter_search(searched_topic, list_of_twitts):
    lead_users = []

    for i in list_of_twitts:
        try:
            if searched_topic in i['text']:
                # list of Tuple (user name , number of followers , the text of the twit ,twit url , number of retweets
                lead_users.append(( i['user']['name'] , i['user']['followers_count'] , i['text'] , i['user']['url'] , i['retweet_count']))
        except Exception as e:
            pass

    return lead_users

temp_list = twitter_search('3d ', twitter_data)


def get_lead_user(list_of_users):
    list_of_users.sort(key=lambda x: x[1], reverse=True)
    # sort the list with number of follower and get the first half of the list
    sorted_list_by_followers=[ x for x in sorted(temp_list, key=lambda x: x[1], reverse=True)[ :int(len(list_of_users) / 2)] ]
    # sort the list with number of twits and get the first half of the list
    sorted_list_by_retweets =[ x for x in sorted(sorted_list_by_followers, key=lambda x: x[4], reverse=True)[ :int(len(list_of_users) / 2)] ]

    # return the top ten element of the list
    return sorted_list_by_retweets[:10]

print('//////////////////////////////////////////////////////')
print(len(get_lead_user(temp_list)))

for i in get_lead_user(temp_list):
    print(i)
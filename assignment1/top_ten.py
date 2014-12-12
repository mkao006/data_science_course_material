import sys
import json

def read_twitter_file(tweets_json_file, what):
    file = open(tweets_json_file)
    tweets = []
    for line in file:
        tweet = json.loads(line, encoding = 'utf-8')
        if what in tweet:
            tweets.append(tweet[what])
    return tweets


def word_distribution(twitter_feeds, freq = False):
    """ Computes the word frequency of a twitter feeds, if freq is
        True, then the frequency is returned, otherwise the denstiy
        is returned"""
    all_words = []
    for tweet in twitter_feeds:
        all_words = all_words + tweet.split()
    all_words = [elements.strip() for elements in all_words if elements != '']
    word_total_number = len(all_words)
    word_freq = {}
    for word in all_words:
        if word not in word_freq:
            word_freq[word] = 1
        elif word in word_freq:
            word_freq[word] += 1
    if freq:
        return word_freq
    else:
        word_density = dict([(k , float(v)/word_total_number)\
                             for k, v in word_freq.items()])
        return word_density

def get_hashtags(tweet_entity):
    if 'hashtags' in tweet_entity:
        hashtag_line = tweet_entity['hashtags']
        if len(hashtag_line) > 0:
            hashtags = []
            for n in range(len(hashtag_line)):
                hashtags.append(hashtag_line[n]['text'])
                return hashtags
                
twitter_entities = read_twitter_file(sys.argv[1], 'entities')

hashtags = []    
for tweets in twitter_entities:
    tags = get_hashtags(tweets)
    if tags != None:
        hashtags.append(get_hashtags(tweets))

hashtag_freq = {}
for elements in hashtags:
    if elements[0] in hashtag_freq:
        hashtag_freq[elements[0]] += 1
    elif elements[0] not in hashtag_freq:
        hashtag_freq[elements[0]] = 1

top10 = sorted(hashtag_freq, key = hashtag_freq.get, reverse = True)[0:10]


top10_hashtag = {}
for tags in top10:
    top10_hashtag[tags] = hashtag_freq[tags]


for i in sorted(top10_hashtag, key = top10_hashtag.get, reverse = True):
    print i.encode('utf-8'), top10_hashtag[i]

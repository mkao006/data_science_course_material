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

if __name__ == '__main__':
    twitter_feeds = read_twitter_file(sys.argv[1], 'text')
    my_tweets_distribution = word_distribution(twitter_feeds)
    for k, v in my_tweets_distribution.items():
        print k.encode('utf-8'), str(v)

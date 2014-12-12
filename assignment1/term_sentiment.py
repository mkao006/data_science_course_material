import sys
import json

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    hw()
    lines(sent_file)
    lines(tweet_file)

def read_twitter_file(tweets_json_file, what):
    file = open(tweets_json_file)
    tweets = []
    for line in file:
        tweet = json.loads(line, encoding = 'utf-8')
        if what in tweet:
            tweets.append(tweet[what])
    return tweets

def all_words(tweets):
    all_words = []
    for tweet in tweets:
        words = tweet.split(' ')
        all_words = all_words + words
        all_words = [k.strip() for k in all_words if k != '']
    return list(set(all_words))


def read_sentiment_dict(file_name):
    """ This function reads the file and turns the score into a
        dictionary """
    file_con = open(file_name)
    scores = {}
    for line in file_con:
        term, score = line.split('\t')
        scores[term] = int(score)
    return scores
   
def n_gram(sentiment_dict):
    """ Finds the n gram of the words """
    n_gram = {}
    for keys in sentiment_dict:
        n_gram[keys] = len(keys.split(' '))
    return n_gram

def sentiment_score(tweet, sentiment_dict):
    """ Function to score the tweets based on a given dictionary """
    tweet = tweet.encode('utf-8')
    sentiment_score = 0
    ngrams = n_gram(sentiment_dict)
    maxgrams = max(ngrams.values())
    score = 0
    for current_gram in sorted(range(1, maxgrams + 1), reverse = True):
        words_in_current_gram = [k for k, v in ngrams.items()\
                                 if v == current_gram]
        for word in words_in_current_gram:
            if word in tweet:
                score += sentiment_dict[word]
                tweet = tweet.replace(word, '')
                # print word, sentiment_dict[word]
    return score
    
my_twitter_stream = read_twitter_file(sys.argv[2], 'text')
my_sentiment_dict = read_sentiment_dict(sys.argv[1])
my_words = all_words(my_twitter_stream)
new_sentiment_dict = {}
for word in my_words:
    if word in my_sentiment_dict:
        new_sentiment_dict[word] = my_sentiment_dict[word]
    else:
        new_sentiment_dict[word] = None

# print new_sentiment_dict
my_scored_tweets = {}
for tweet in my_twitter_stream:
    my_scored_tweets[tweet] = sentiment_score(tweet, my_sentiment_dict)

for word in [k for k, v in new_sentiment_dict.items() if v == None]:
    tmp_score = 0
    current_iter = 0
    for k, v in my_scored_tweets.items():
        if word in k:
            tmp_score += v
            current_iter += 1
    new_sentiment_dict[word] = float(tmp_score)/current_iter

for k,v  in new_sentiment_dict.items():
    print k.encode('utf-8'), str(v)

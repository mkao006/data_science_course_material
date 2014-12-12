import sys
import json

def lines(fp):
    print str(len(fp.readlines()))

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    hw()
    lines(sent_file)
    lines(tweet_file)

def read_sentiment_dict(file_con):
    """ This function reads the file and turns the score into a
        dictionary """
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
    return score

def read_twitter_file(tweets_json_file):
    """ This parses the twitter file into an json object"""
    file = open(tweets_json_file)
    tweets = {}
    for line in file:
        tweet = json.loads(line, encoding = 'utf-8')
        if 'text' in tweet:
            tweets[tweet['text']] = tweet['text']
    return tweets

    
def score_tweets(tweets_json_file, sentiment_dict):
    """ Function to score the tweets based on a given dictionary """
    scored_tweets = {}
    for line in tweets_json_file:
        tweet = json.loads(line, encoding = 'utf-8')
        if 'text' in tweet:
            score = sentiment_score(tweet['text'], sentiment_dict)
            scored_tweets[tweet['text']] = score
            print score
    return scored_tweets


if __name__ == '__main__':
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])    
    scored_tweets = score_tweets(tweet_file, read_sentiment_dict(sent_file))
    print 'maximum score is: ' + str(max(scored_tweets.values()))
    print 'minimum score is: ' + str(min(scored_tweets.values()))


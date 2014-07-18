from __future__ import division
import sys
import json


def get_sentiment_scores(filepath="AFINN-111.txt"):
    scores = {}
    with open(filepath, 'r') as sentiment_file:
        for line in sentiment_file:
            # The file is tab-delimited. "\t" means "tab character"
            term, score  = line.split("\t")
            scores[term] = int(score)  # Convert the score to an integer.
    return scores


def num_lines(fp):
    num_lines = len(fp.readlines())
    fp.seek(0)
    return num_lines


def analyze_sentiment(scores, tweet):
    """Calculate the sentiment of a tweet using a dictionary of known word
    sentiments.

    :param dict scores: The dictionary of known sentiment scores (word, score).
    :param dict tweet: The dict-encoded json data of the tweet to analyze.
    :rtype:  int
    :return: An integer rating of the sentiment, with higher being more
        positive, 0 being neutral, and negative numbers being negative sentiment
        scores.

    """
    return sum(scores.get(word, 0) for word in tweet['text'].split())


def filter_english_tweets(tweets):
    """Filter a list of dict-encoded json tweet data down to only those tweets
    which are english and have text.

    :param list tweets: The tweets to filter.
    :rtype:  list
    :return: The list of filtered tweets.

    """
    return [t for t in tweets if 'text' in t and t['lang'] == 'en']


def main():
    if len(sys.argv) < 3:
        print 'tweet_sentiment.py <sentiment-file> <tweet-file>'
        return 1

    sent_filepath = sys.argv[1]
    tweet_filepath = sys.argv[2]

    sentiment_scores = get_sentiment_scores(sent_filepath)
    with open(tweet_filepath, 'r') as tweets_file:
        for line in tweets_file:
            tweet = json.loads(line)
            if 'text' in tweet and tweet['lang'] == 'en':
                print analyze_sentiment(sentiment_scores, tweet)

    return 0


if __name__ == '__main__':
    main()

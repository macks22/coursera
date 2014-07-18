from __future__ import division
import sys
import json


def clean_word(word):
    return ''.join([c for c in word if c.isalnum()])


def keep_word(word):
    if not word:
        return False
    elif word.startswith('http'):
        return False
    elif word.isdigit():
        return False
    elif word[0].isdigit():
        return False
    else:
        return True


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


class TermCounter(object):
    """Compute TF.IDF ratings for each term in a corpus of sentences."""

    def __init__(self):
        self.term_counts = {}
        self.term_count = 0

    def process_words(self, words):
        for word in words:
            if word in self.term_counts:
                self.term_counts[word] += 1
            else:
                self.term_counts[word] = 0

            self.term_count += 1


    def tfidf(self):
        for word in self.term_counts:
            print '{} {}'.format(word.encode('utf-8'),
                self.term_counts[word] / self.term_count)


def words_from_tweet(tweet):
    words = [unicode(word.lower()) for word in tweet['text'].split()]
    cleaned_words = map(clean_word, words)
    return filter(keep_word, cleaned_words)


def main():
    if len(sys.argv) < 2:
        print 'tweet_sentiment.py <tweet-file>'
        return 1

    tweet_filepath = sys.argv[1]
    term_counter = TermCounter()

    json_from_string = json.loads
    with open(tweet_filepath, 'r') as tweets_file:
        for line in tweets_file:
            tweet = json_from_string(line)
            if 'text' not in tweet or tweet['lang'] != 'en':
                continue

            filtered_words = words_from_tweet(tweet)
            term_counter.process_words(filtered_words)

    term_counter.tfidf()

    return 0


if __name__ == '__main__':
    main()

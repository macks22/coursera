from __future__ import division
import sys
import json


STATES = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}


def get_sentiment_scores(filepath="AFINN-111.txt"):
    scores = {}
    with open(filepath, 'r') as sentiment_file:
        for line in sentiment_file:
            # The file is tab-delimited. "\t" means "tab character"
            term, score  = line.split("\t")
            scores[term] = int(score)  # Convert the score to an integer.
    return scores


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


def words_from_tweet(tweet):
    words = [unicode(word.lower()) for word in tweet['text'].split()]
    cleaned_words = map(clean_word, words)
    return filter(keep_word, cleaned_words)


def get_state_from_tweet(tweet):
    """Attempt to figure out which state a tweet was posted from.

    :param dict tweet: The dict-encoded json data for the tweet.
    :rtype:  str
    :return: The two letter abbreviation for the tweet or an empty string.

    """
    t = tweet
    place = t['place']
    if place is not None:
        full_name = place['full_name']
        for state in STATES:
            if state in full_name or STATES[state] in full_name:
                return state

    user_loc = t['user']['location']
    if user_loc is not None:
        for state in STATES:
            if state in user_loc or STATES[state] in user_loc:
                return state

    return ''


def main():
    if len(sys.argv) < 3:
        print 'tweet_sentiment.py <sentiment-file> <tweet-file>'
        return 1

    sent_filepath = sys.argv[1]
    tweet_filepath = sys.argv[2]

    state_sentiments = {}
    for state in STATES:
        state_sentiments[state] = 0

    scores = get_sentiment_scores(sent_filepath)
    with open(tweet_filepath, 'r') as tweets_file:
        for line in tweets_file:
            tweet = json.loads(line)
            if tweet.get('lang','') != 'en':
                continue

            state = get_state_from_tweet(tweet)
            if state:
                words = words_from_tweet(tweet)
                sentiment = sum(scores.get(word, 0) for word in words)
                state_sentiments[state] = sentiment

    print max(state_sentiments, key=lambda state: state_sentiments[state])

    return 0


if __name__ == '__main__':
    main()

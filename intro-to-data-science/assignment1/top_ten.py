from __future__ import division
from collections import defaultdict, Counter
import sys
import json


def main():
    if len(sys.argv) < 2:
        print 'top_ten.py <tweet-file>'
        return 1

    tweet_filepath = sys.argv[1]
    hash_tags = defaultdict(int)

    json_from_string = json.loads
    with open(tweet_filepath, 'r') as tweets_file:
        for line in tweets_file:
            tweet = json_from_string(line)
            if 'entities' not in tweet:
                continue

            for tag_data in tweet['entities']['hashtags']:
                tag = tag_data['text']
                hash_tags[tag] += 1

    tag_counter = Counter(hash_tags)
    for tag, freq in tag_counter.most_common(10):
        print '{} {}'.format(tag.encode('utf-8'), freq)

    return 0


if __name__ == '__main__':
    main()

import requests
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class vaderAnalysis():

    """
    A very obscure API-less and OAuth-less data scrape from X that extracts
    text bodies from Tweets given a username (handle). The vaderAnalyzeX method
    then uses VADER to output a percentage of positive, negative and neutral connotations
    based on 100 Tweets pulled from the account.
    """
    @staticmethod
    def vaderAnalyzeX(username) -> None:
        url = f"https://syndication.twitter.com/srv/timeline-profile/screen-name/{username}"

        r = requests.get(url)
        html = r.text

        start_str = '<script id="__NEXT_DATA__" type="application/json">'
        end_str = '</script></body></html>'

        start_index = html.index(start_str) + len(start_str)
        end_index = html.index(end_str, start_index)

        json_str = html[start_index: end_index]
        data = json.loads(json_str)

        tweets = data["props"]["pageProps"]["timeline"]["entries"]

        if(len(tweets) < 100):
            print("Sample size not large enough.")
            exit    

        positivetotal = 0
        negativetotal = 0
        neutraltotal = 0

        analyzer = SentimentIntensityAnalyzer()

        for i in range(min(100, len(tweets))):
            tweet = tweets[i]["content"]["tweet"]["full_text"]

            positivetotal += analyzer.polarity_scores(tweet)['pos']
            negativetotal += analyzer.polarity_scores(tweet)['neg']
            neutraltotal += analyzer.polarity_scores(tweet)['neu']
       
            """
            DEBUG: This will print all the tweets obtained for the analysis sample.
            print(f"Tweet {i+1}: {tweet}\n")
            """

        print(f"Percent positive: {positivetotal / 100 * 100:.2f}%")
        print(f"Percent negative: {negativetotal / 100 * 100:.2f}%")
        print(f"Percent neutral: {neutraltotal / 100 * 100:.2f}%")





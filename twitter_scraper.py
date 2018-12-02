from argparse import ArgumentParser
import os

def scrape(search_string, begin_date, end_date, limit):

    print("Scraping Twitter for tweets containing string <{}>".format(search_string))
    file_path = 'scrape_archive/' + search_string.replace(' ', '_') + '.csv'
    scrape_instructions = 'twitterscraper \"{}\" -bd {} -ed {} -c -l {} -o'.format(search_string, begin_date, end_date, limit)
    cmd = scrape_instructions + ' ' + file_path
    os.system(cmd)

def main():

    parser = ArgumentParser()
    parser.add_argument("--text", help="text string to scrape for", required=True)
    parser.add_argument("--bd", help="begin date for tweet search", default='2018-04-01')
    parser.add_argument("--ed", help="end date for tweet search", default='2018-10-31')
    parser.add_argument("--user", help="limit to tweets from specified user", default='empty')
    parser.add_argument("--limit", help="limit to tweets from specified user", default=50000)
    args = parser.parse_args()
    text = args.text
    begin_date = args.bd
    end_date = args.ed
    user = args.user
    limit = args.limit

    if user == 'empty':
        scrape(text, begin_date, end_date, limit)
    else:
        text_with_user = text + ' from:{}'.format(user)
        scrape(text_with_user, begin_date, end_date, limit)

if __name__ == '__main__':

    main()

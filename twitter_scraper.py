from argparse import ArgumentParser
import os

def scrape(search_string, begin_date, end_date):

    print("Scraping Twitter for tweets containing string <{}>".format(search_string))
    file_path = 'scrape_archive/' + search_string.replace(' ', '_') + '.csv'
    scrape_instructions = 'twitterscraper \"{}\" -bd {} -ed {} -c -o'.format(search_string, begin_date, end_date)
    cmd = scrape_instructions + ' ' + file_path
    os.system(cmd)

def main():

    parser = ArgumentParser()
    parser.add_argument("--text", help="text string to scrape for", required=True)
    parser.add_argument("--bd", help="begin date for tweet search", default='2018-01-01')
    parser.add_argument("--ed", help="end date for tweet search", default='2018-10-31')
    parser.add_argument("--user", help="limit to tweets from specified user", default='empty')
    args = parser.parse_args()
    text = args.text
    begin_date = args.bd
    end_date = args.ed
    user = args.user

    if user == 'empty':
        scrape(text, begin_date, end_date)
    else:
        text_with_user = text + ' from:{}'.format(user)
        scrape(text_with_user, begin_date, end_date)

if __name__ == '__main__':

    main()

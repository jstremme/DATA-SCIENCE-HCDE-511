from argparse import ArgumentParser
import os

parser = ArgumentParser()
parser.add_argument("--text", help="text string to scrape for", required=True)
parser.add_argument("--bd", help="begin date for tweet search", default='2018-10-01')
parser.add_argument("--ed", help="end date for tweet search", default='2018-10-31')
args = parser.parse_args()
search_string = args.text
begin_date = args.bd
end_date = args.ed

print("Scraping Twitter for tweets containing string <{}>".format(search_string))
file_path = 'archive/' + search_string.replace(' ', '_') + '.csv'
scrape_instructions = 'twitterscraper \"{}\" -bd {} -ed {} -c -o'.format(search_string, begin_date, end_date)
cmd = scrape_instructions + ' ' + file_path
os.system(cmd)

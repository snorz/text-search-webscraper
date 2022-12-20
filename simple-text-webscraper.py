#!/usr/bin/python3

# imports
import requests
from bs4 import BeautifulSoup
import re
import argparse
from Levenshtein import distance, jaro_winkler

# Parse input arguments 
arg_parser = argparse.ArgumentParser(description='Simple program to search for strings on specified websites')
arg_parser.add_argument('--url', '-u', type=str, help='Search one single url')
arg_parser.add_argument('--file', '-f', help='File containing multiple urls seperated by newline')
arg_parser.add_argument('--search', '-s', nargs='+', help='Search string or word', required=True)
arg_parser.add_argument('--header', '-he', help='Use this to specify what headers to use in the site access', action="store_true")
arg_parser.add_argument('--method', '-m', help='Specify what pattern matching option to use: 0-exact(default), 1-Levenhstein, 2-Jaro-Winkler', choices=range(0, 3),default=0, type=int)
arg_parser.add_argument('--lev', '-l', help='Input the Levenshtein distance to be used; default=3', type=int, default=3)
arg_parser.add_argument('--verbose', '-v', help='Set this option for extra output', action="store_true")
arg_parser.add_argument('--jwDist', '-j', help='Send the threshold for using Jaro-Winkler between 0.00 and 1, default=0.80', default=0.80, type=float)

args = arg_parser.parse_args()

###################################################
## Config variables
## List of urls
url_list = []
if args.url and not args.file:
    #if not args.f and args.u:
    url_list.append(args.url)

### read from file
elif args.file and not args.url:
    # write code for reading from file
    print("hello")
    try:
        with open(args.file) as f_obj:
            lines = f_obj.readlines()
    
        for line in lines:
            if line:
                url_list.append(line.rstrip())
    except:
        print("could not open the file.. Does it exist and have the correct path?") 
        quit()
    print(url_list)


elif args.file and args.url:
    print("It is for now not possible to use both single url and file with url's")
    print(".... Exiting....")
    quit()

if args.verbose:
    verbose = 1
else:
    verbose = None

## Search method args -> variables
# 1 == Levenshtein
lev_dist = args.lev

# 2 == jaro-winkler
#elif args.method == 2:
jw_dist = args.jwDist


## list of search strings
search_strings = []
# append all search strings to a list
[search_strings.append(item) for item in args.search]


# set headers/user-agent to test differences
if args.header:
    header = {'Accept-Language': 'ext/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0'}
else:
    header = {}

###################################################
## Functions

### Get data from page
def get_page(url):
    res = requests.get(url,headers=header) #headers=headers
    if res.status_code == 200:
        #res = requests.get(url, headers=headers)
        #lines = res.text.split('\n')
        # clean list of emtpy strings  
        #lines = ' '.join(lines).split()

        ## using beatiful soup
        # this method removes html code/tags and hopefully extracts the most important text
        # not extensivly tested, but can seem to be a viable option
        soup = BeautifulSoup(res.text, features="html.parser")
        temp_res = soup.text.split('\n')
        lines = list(filter(None, temp_res)) # clean data from emtpy values

        return lines 
    else:
        return False

### Use for exact search of words
def ret_exact(data, s_string):
    res = re.search(s_string, data, re.IGNORECASE)
    
    if res:
        #print(s_string)
        return ([s_string, res])
    else:
        return None
        
### Search with levenshtein
def ret_levenshtein(data, s_string):
    # works only for words for now
        # if multiple words split into list
    words = data.split(' ') 
        # for each word
    for word in words:
        lev_dist_res = distance(word, s_string)

        if lev_dist_res <= lev_dist:
            #print(word)
            return ([word, lev_dist_res])

### Search with jaro winkler
# the current implementation does only work with words
def ret_jaro_winkler(data, s_string):
    
    words = data.split(' ')
    for word in words: 
        ret = jaro_winkler(s_string, data)
        if ret >= jw_dist:
            #print(data)
            #print(ret)
            #print("")
            return ([data, ret])
    return None


### Input results from get-request and the search string
def search_text(data, search_strings, method):
    
    # Some pretty output before starting the search: if verbose?
    if verbose:
        print("The number of search words/strings to search for: " + str(len(search_strings)))
        print("Searching for the following words/strings: " + str(search_strings))
        print('\n')   

    # could switch the order, to stop searching through all the data for each search string, 
    #   could be more efficient?
    search_res = []
    for s_string in search_strings:
        if verbose:
            print("Searching for the word/string: " + s_string + '\n')
            print('...............................')

        for i in data:
            
            # if normal
            if method == 0:
                results = ret_exact(i, s_string)
                if results:
                    search_res.append(results)

            # if levenshtein
            if method == 1:
                results = ret_levenshtein(i, s_string)
                if results:
                    search_res.append(results)

            # if Jaro-winkler
            if method == 2:
                results = ret_jaro_winkler(i, s_string)
                if results:
                    search_res.append(results)

            else:
                #print("Some error occured?")
                results = None



    # Improve the results returned -> only words found and the number of hits?
    # check if the search string is found
    if len(search_res) != 0:
        return search_res


    else:
        return False

###################################################
## main program
all_results = []

for item in url_list:
    data = get_page(item)
    if data != False:
        results = search_text(data, search_strings, args.method)

        if results != False: # if res is found store to array
            #all_results.append([item, len(results)])
            all_results.append([item, results[0][0]])
            #print(results)
        else:
            print("Search string not found...")
            
    #else:
    #    print("no results from the url")


print(all_results)

print("\n")
print(".....Quitting.....")




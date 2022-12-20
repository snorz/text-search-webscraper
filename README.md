# Simple text websearch tool

- [Simple text websearch tool](#simple-text-websearch-tool)
  - [Intro](#intro)
  - [Requirements](#requirements)
  - [How to use](#how-to-use)
    - [List of url's](#list-of-urls)
    - [Multiple search words](#multiple-search-words)
    - [Pattern matching algorithms](#pattern-matching-algorithms)
    - [Headers](#headers)
    - [Experiment](#experiment)
  - [References/Assistance](#referencesassistance)


## Intro

This is a simple webscraper/search tool build in a school project and are used to search for words and strings in webpages. It is developed as a script that could be used through the terminal. It is quite specialized in it needs to be fed what URL's to search and what text to search for. The potential use case of such a tool could be in researching similar websites in order to discover uniqe strings that could be used to identify whether multiple sites are created by the same actor.    

The project is far from what can be called finished but it does contain some basic functionality to send request to webpages and search for specific strings. It can also change the user-agent used for making requests and use Levenshtein distance to even identify typos. 

## Requirements

pip install Levenshtein
pip install beautifulsoup4


## How to use
Below is a short summary of the functionality and how to use them.

Standard use of the program with a single url and search word:

``` bash
python3 simple-text-webscraper.py -u '<http://url>' -s 'search-word'
```

### List of url's
One of the options availbale in the script is to provide a list of url's to search at a time. By specifying the option '-f' for file instead of '-u' as the example shown above can the user provide a text file containing the url's to search through separated by newlines. The program will then serach through each url for the specified search words. Each url needs the prefix 'http://'.  

### Multiple search words
Another neat but simple feature is to search for multiple words in the same run. As for now it is only add new words or strings whitin '' quotes after the '-s' option as shown above. There are no limits to how many words can be used but it should be added an option to provide a list instead for manually adding it in the commandline. 

### Pattern matching algorithms
A tought behind the project was to utilize string distance measurements algorithms in order to broaden the use-cases for the program. As for now only Levenshtein and Jaro-Winkler are implemented but only Levenshtein works properly alongside the exact match option. Indicating more work is needed, it should also be easy to implement others depending on the needs.
To use levenshtein instead of exact match, the option '-m' for method can be used with with the number 1. For Jaro-Winkler specify the number 2, if the option is not used is 0 the default and exact matching will be used(not case-sensitive). 

There are two additional options that also could be used with the method tag. '-lev' and '-jwDist' that can be used to change the sensitivity of each algorithm. Levenshtein defaults to allowing 3 edits to be a match but this can be changed by using that option.

### Headers
Another somewhat important part of the program is the ability to change what user-agent is provided in the request to the website. By default is it something with "request.x.x.x" but with the option '--header' enabled it will change to a hardcoded value that indicates a firefox on Linux user agent. The value can be changed to match other user agents as needed.


### Experiment

Barrowed code from the official Apache2 Ubuntu page(linked below) and modified some places with additional words and strings. Various words are added in different locations and will the tool will be used to search for them, testing the different capabilities. The webpage is ran in a docker container and the image used can be accessed py pulling: 

To build and run the docker image containing the webpage locally the following commands can be used(only tested in a linux environment, docker needs to be installed beforehand):
```bash
// can be run directly by pulling from docker-hub like this:

// to build the docker image containing the webpage, needs to be in the "docker-files" dir to do this
sudo docker build -t <name> .

// ro tun the created image
sudo docker run -d -p 80:80 <name> 


// To connect to the container with terminal
sudo docker exec -it <container id> bash

// logs can be viewed /usr/local/apache2/logs/forensic.log
//  here is it possible to see the user agent from the requests 

```

The extended logging in Apache is done by enabling the module "Mod_log_forensic" to be able to view the user agent in each request. documentation is found here: https://httpd.apache.org/docs/current/mod/mod_log_forensic.html


https://gist.github.com/SunDi3yansyah/c8e7a935a9f6ee6873a2


## References/Assistance

How to use headers:
https://stackoverflow.com/questions/6260457/using-headers-with-the-python-requests-librarys-get-method

Discovering my header data for testing:
http://myhttpheader.com/



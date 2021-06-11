# CS172 - Final Project (Web Crawler using ElasticSearch)

## Team member 1 - Melanie Aguilar
## Team member 2 - Alexander DeVictoria
## Team member 3 - John Huh

##### Language used: Python

##### The domain.py file parses the desired URL 

##### The es.py file uses the ElasticSearch directory we created to index the files in the html folder

##### The general.py file is used to create queue.txt and crawled.txt files. Links that the program 
##### plans to crawl are listed in the queue file, and links that have already been crawled are listed 
##### in the crawled file

##### The link_finder.py file allows the crawler to find hyperlinks on the website we are crawling

##### The main.py file creates our threads and the folder with all the HTML files crawled

##### The spider.py file gets the program’s threads to crawl and gather links from the website.

##### For our final project, the team created a multithreaded web crawler. To run the code, enter the command “python3 main.py” into the terminal. The program welcomes the user and prompts them to enter a URL to crawl. Once a URL is entered, the program will ask the user to enter in the number of pages and the number of levels (hops) that they wish to crawl. Essentially, this will make it so the crawler does not hop too many hyperlinks away from the original link. Finally, since the web crawler utilizes multithreading, the program will ask the user to enter how many threads they would like to crawl through the website. Once all this information is entered, the program will place hyperlinks that it finds on the seed URL into a queue.txt file, and once a page in the queue list is crawled, the hyperlink will be removed from the queue and put on a list of links that have already been crawled (crawled.txt). The program will continue to crawl until it has reached the page limit or hops limit that the user entered. Then, the links stored into the crawled.txt file are stored in a folder of html files. Only after the crawler has completed can the program start indexing the html files.
##### By entering the command “python3 es.py” into the terminal, ElasticSearch indexes the html files while ignoring the HTML characters when searching through the file. From here, the user can choose from four options. By entering in 1, they can add in a new document to the index. All they have to do is enter in the page title of the document and the text from the document that they would like to add when prompted. If the user wants to get the results for all indexes, they will have to enter in 2.  This will return all the index results. By entering in 3, the user can search the index for a particular search word. When prompted, enter in the word you are searching for, and the program will return the index results that contain the entered word. The final option is  to exit the program, which can be done by entering in 0 to the terminal. To satisfy Part 3, the extension of our program is the use of multithreading. This allows  multiple threads to crawl through the desired website at the same time, all working to find hyperlinks to add to the queue.txt file

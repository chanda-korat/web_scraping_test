# web_scraping_test
A sample project for web scrapping using python, requests, beautifulsoup , pandas
There's apython script under /target folder , which would basically fetach data from: https://www.landwatch.com websites.
There is pagination upto 100+ pages.
Script would collect data up to 100 page and saved it to Excel file under /logs folder.

Script has been developed using python : 3.8.2

To run the file just run : python web_scraping_test/target/collect_data.py

Packages required to run this file: beautifulsoup4 , requests, pandas

  beautifulsoup4==4.9.0
  pandas==1.0.3
  requests==2.23.0

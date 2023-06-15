# South African Police Services  Locator
## Overview
Find and locate SAPS services in RSA.
The app scrapes data from official government websites such as [saps](https://www.saps.gov.za/contacts/index.php), including contact information, operating hours, and services offered.

## Features
* Scrape data from official government websites.
* Display information about SAPS services in RSA.
* Allow users to search for and locate SAPS services.
* Focus on a vitimization combat tool that can show the nearset police station.

## Technologies Used
* `Scrapy`: Python-based framework used for extracting data fromwebsites.
* `Python`: A programming language used for high level programing.
## Installation
To install the scraper, you will need to have Python 3.x installed on your computer. You can download Python from the [official website](https://www.python.org/downloads/).

It is recommended that you install the scraper in a virtual environment to avoid conflicts with other Python packages on your system. You can create a virtual environment using the venv module that comes with Python by running the following command in your terminal:

`python -m venv env`
This will create a new virtual environment in a folder named env in the current directory. To activate the virtual environment, run the following command:

* On macOS and Linux:
`source env/bin/activate`
* On Windows:
`.\env\Scripts\activate`
Once you have activated the virtual environment, you can install the required dependencies by running the following command:

`pip install -r requirements.txt` This will install Scrapy library as well as any other dependencies specified in the `requirements.txt` file.
## Usage
to use this scraper navigate into the project directory into the `*/saps/saps/` or `*/saps` folder and in your terminal run the following command:

`scrapy crawl contacts_spider`

Please note: if you have an okay internet connection, the spider should run for about 8 minutes tops, but the average time is 4 minutes. Once scraping it done you shuld see the following response printed in the terminal `Ke heditse ka go dirisa: contacts_spider` then `cd ../` to same leve as the first saps folder and run this command: `py refine_scraped_data.py`. You should be albe to acces the refined scraped data on the `refined_data.json`

## Contributing
Contributions are welcome! Please use open issue or submit a pull request if you would like to contribute.

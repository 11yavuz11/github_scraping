# GitHub Data Scraper Application

This application is designed to scrape data from GitHub using the GitHub API and store the data into MongoDB. It utilizes PyQt5 for the GUI to allow users to input their search parameters and view the results.

## Features

- Fetch data based on user-specified parameters using GitHub API.
- Store the fetched data in MongoDB.
- User-friendly GUI built with PyQt5.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- You have a modern Windows, Linux, or macOS machine.
- You have Python 3.6+ installed on your machine.
- You have MongoDB set up either locally or remotely and have the connection string available.

## Installation

To install the necessary libraries, follow these steps:

1. Clone the repository:
```bash
git clone https://your-repository-url.git](https://github.com/11yavuz11/github_scraping.git
```
```bash
cd your-repository-directory
```

2. Install the required packages:
```bash
python -m pip install -r requirements.txt
```

## Configuration

### MongoDB Connection

You need to enter your own mongodb url in the connection_string variable:

```bash
connection_string = 'MONGODB_CONNECTION_STRING'
```

## Running the Application

To run the application, navigate to the project directory and run:

```bash
python main.py
```
This command will start the application, and you will be able to interact with the GUI.

## Usage

After starting the application, follow these steps:

1. Enter your GitHub API token and your query in the respective fields.
2. Select the type of data you want to search for (e.g., repositories, users).
3. Click the 'Start' button to begin scraping.
4. Results will be displayed in the GUI, and data will be stored in your MongoDB database.

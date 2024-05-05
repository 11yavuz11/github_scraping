from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from window import Ui_MainWindow
from pymongo import MongoClient

import sys
import requests
import time

# MongoDB connection string
connection_string = 'mongodb+srv://github:github123...@cluster0.pebdohc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

# Function to create and display a warning message box
def error_window(message):
    # Create a message box with a warning icon and 'Ok' button
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Warning)
    msgBox.setWindowTitle("Warning")
    msgBox.setText(message)
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.button(QMessageBox.Ok).setText("Ok")
    # Display the message box and wait for user interaction
    msgBox.exec_()

# Function to handle the start button click
def start():
    # Retrieve GitHub API token and query from user input
    token = ui.token_lineEdit.text()
    query = ui.query_textEdit.toPlainText()
    filter_by_index = ui.filterby_comboBox.currentIndex()
    filter_by = ui.filterby_comboBox.itemText(filter_by_index).lower()

    # Check if token or query is missing and display appropriate warning
    if not token:
        error_window("GitHub token girilmedi. Lütfen token giriniz.")
    elif not query.strip():
        error_window("Sorgu boş olamaz. Lütfen bir sorgu giriniz.")
    else:
        # If inputs are valid, proceed to scrape data
        scraping_github(filter_by, query, token)

# Function to perform data scraping from GitHub API
def scraping_github(filter_by, query, token):
    # Headers for GitHub API request
    headers = {
        "Authorization": f"token {token}"
    }
    # Initial API request to get total count of results
    url_total_count = f"https://api.github.com/search/{filter_by}?q={query}"
    response = requests.get(url_total_count, headers=headers)

    # Check if initial request was successful
    if response.status_code != 200:
        error_message = f"GitHub API'ye erişimde bir hata oluştu. Hata kodu: {response.status_code}"
        ui.error_label.setText(error_message)
        return
    
    data = response.json()
    total_count = data.get("total_count", 0)

    # Calculate the number of pages to fetch based on total results
    if total_count == 0:
        ui.error_label.setText("Sonuç bulunamadı.")
        error_window("Sonuç bulunamadı.")
        return
    elif total_count > 1000:
        page = 34
    else:
        page = total_count // 30 + 1

    # Update UI to show scraping is in progress and begin fetching data page by page
    ui.error_label.setText("Scraping continue...")
    error_window("Scraping continue...")
    for page_num in range(1, page):
        url = f"https://api.github.com/search/{filter_by}?q={query}&page={page_num}"
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            error_message = f"GitHub API'ye erişimde bir hata oluştu. Hata kodu: {response.status_code}"
            ui.error_label.setText(error_message)
            return
        
        data = response.json()
        items = data.get("items", [])
        if not items:
            break
        # Process each item and save to MongoDB
        for item in items:
            parsed_data = parse_repository_data(item) if filter_by == 'repositories' else parse_users_data(item)
            save_to_mongodb(parsed_data)
        # Pause for a second between requests to respect API rate limits
        time.sleep(1)
    # Indicate scraping completion on UI and through message box
    ui.error_label.setText("Scraping completed")
    error_window("Scraping completed")
    

# Function to parse repository data from API response
def parse_repository_data(data):
    repository_info = {
        "db_name": "Repositories",
        "id": data["id"],
        "full_name": data["full_name"],
        "owner": {
            "login": data["owner"]["login"],
            "id": data["owner"]["id"],
            "avatar_url": data["owner"]["avatar_url"],
            "html_url": data["owner"]["html_url"]
        },
        "html_url": data["html_url"],
        "description": data["description"],
        "size": data["size"],
        "language": data["language"]
    }
    return repository_info

# Function to parse user data from API response
def parse_users_data(data):
    users_info = {
        "db_name": "Users",
        "login": data["login"],
        "id": data["id"],
        "html_url": data["html_url"],
        "type": data["type"],
        "score": data["score"]
    }
    return users_info

# Function to save parsed data to MongoDB
def save_to_mongodb(data):
    try:
        # Establish a connection to MongoDB
        client = MongoClient(connection_string)
        db_name = data.get("db_name")
        db = client[db_name]
        collection_name = db_name
        collection = db[collection_name]
        # Insert data into the collection
        collection.insert_one(data)
    except Exception as e:
        error_message = f"MongoDB'ye veri eklerken hata oluştu: {e}"
        ui.error_label.setText(error_message)
    finally:
        # Close the MongoDB connection
        client.close()

if __name__ == "__main__":
    # Initialize the application and main window
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    ui.start_pushButton_2.clicked.connect(start)
    window.show()
    # Start the application event loop
    sys.exit(app.exec_())

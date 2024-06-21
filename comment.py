from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

def load_comments(driver, target_comment_count):
    comments = []
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    scroll_attempts = 0
    
    while len(comments) < target_comment_count:
        # Scroll to the bottom of the page
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(2)  # Wait for new comments to load

        # Collect comments
        comment_elements = driver.find_elements(By.CSS_SELECTOR, 'ytd-comment-thread-renderer #content-text')
        comments = [element.text for element in comment_elements]

        # Check if we've reached the bottom of the page
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            scroll_attempts += 1
            if scroll_attempts >= 5:
                break  # Exit if no new comments are loaded after 5 scroll attempts
        else:
            last_height = new_height
            scroll_attempts = 0

    return comments[:target_comment_count]  # Return only the required number of comments

def save_comments(comments, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for comment in comments:
            file.write(comment + '\n')

def main():
    video_url = 'https://youtu.be/JyJd111Ym7U?si=fzYV0_stzX11vc_h'  # Replace with your YouTube video URL
    target_comment_count = 10000  # Number of comments to scrape
    filename = 'comments2.txt'  # Output file name

    # Set up Selenium WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # Load the YouTube video page
        driver.get(video_url)
        time.sleep(5)  # Allow the page to load

        # Load and scrape comments
        comments = load_comments(driver, target_comment_count)
        
        # Save comments to a file
        save_comments(comments, filename)
        print(f'Saved {len(comments)} comments to {filename}')
    
    finally:
        driver.quit()

if __name__ == '__main__':
    main()

from flask import Flask, request, jsonify
import undetected_chromedriver as uc
import time
import csv
from selenium.webdriver.common.by import By


app = Flask(__name__)

def scrapper(product_url):
    chromeOptions = uc.ChromeOptions()
    chromeOptions.headless = False

    driver = uc.Chrome(use_subprocess=True, options=chromeOptions)
    
    # Replace the Amazon link below with your login URL
    driver.get("https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0")
    
    ## 
    time.sleep(5) # Wait for a few seconds to ensure the page loads completely

    email = driver.find_element(By.ID, "ap_email")

    # Replace the xxx with your Amazon email
    email.send_keys("ninjasneural@gmail.com")

    driver.find_element(By.ID, "continue").click()

    time.sleep(10)

    password = driver.find_element(By.ID, "ap_password")


    # Replace the xxx with your Amazon password
    password.send_keys("AIDI@group7")

    driver.find_element(By.ID, "signInSubmit").click()

    time.sleep(10)
    
    # Navigate to the Amazon product page
    driver.get(product_url)
    
    time.sleep(10) # Wait for a few seconds to ensure the page loads completely

    # Locate and extract review elements
    review_elements = driver.find_elements(By.CSS_SELECTOR, '.a-section.review')
    
    reviews_list = []

    for review_element in review_elements:
        # Extract the author's name
        author_name = review_element.find_element(By.CLASS_NAME, 'a-profile-name').text

        # Extract review text
        review_text = review_element.find_element(By.CLASS_NAME, 'review-text').text

        # Extract review date
        review_date = review_element.find_element(By.CLASS_NAME, 'review-date').text

        # Print the extracted information
        print("Author: ", author_name)
        print("Review: ", review_text)
        print("Review Date: ", review_date)
        print("\n")

        # Append review information to the list
        review_info = {
            'Author': author_name,
            'Review': review_text,
            'Review Date': review_date
        }
        
        reviews_list.append(review_info)
    
    driver.close()
    
    return reviews_list


@app.route('/get_product_url', methods=['POST'])
def get_product_url():
    try:
        data = request.get_json()
        product_url = data.get('product_url')

        reviews = scrapper(product_url)
        
        return reviews
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

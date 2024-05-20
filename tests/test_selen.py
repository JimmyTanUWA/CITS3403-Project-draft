import multiprocessing
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from unittest import TestCase
from flask import url_for
from app import create_app, db
from app.config import TestConfig
from app.models import User

localHost = "http://localhost:5000"

class SeleniumTests(TestCase):
    def setUp(self):
        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.session.remove()
        db.drop_all()
        db.create_all()
        self.insert_dummy_data(db)

        self.server_thread = multiprocessing.Process(target=self.testApp.run)
        self.server_thread.start()

        options = webdriver.ChromeOptions()
        options.add_argument('--window-size=1920,1080')
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=options)

        time.sleep(1)  # Ensure the server has time to start
        self.driver.get(localHost)

    def tearDown(self):
        self.server_thread.terminate()
        self.driver.close()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def insert_dummy_data(self, db):

        user = User(username='matt', email='matt@example.com')
        user.set_password('123456')
        db.session.add(user)
        db.session.commit()

    def get_csrf_token(self):
        # Extract CSRF token from the current page
        csrf_token = self.driver.find_element(By.NAME, "csrf_token").get_attribute("value")
        return csrf_token

    def test_edit_profile(self):
        """
        This function tests editing the user profile
        """
        # Log in first
        self.driver.get(localHost + "/login")
        csrf_token = self.get_csrf_token()
        loginElement = self.driver.find_element(By.ID, "username")
        loginElement.send_keys("matt")
        loginElement = self.driver.find_element(By.ID, "password")
        loginElement.send_keys("123456")
        csrfElement = self.driver.find_element(By.NAME, "csrf_token")
        csrfElement.send_keys(csrf_token)
        submitElement = self.driver.find_element(By.ID, "submit")
        submitElement.click()

        self.assertEqual(self.driver.current_url, localHost + "/index")

        # Go to profile page
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        self.assertEqual(self.driver.current_url, localHost + "/profile")

        # Open the edit profile modal
        self.driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary").click()
        time.sleep(1)  # Wait for the modal to open

        # Edit the profile
        csrf_token = self.get_csrf_token()
        emailElement = self.driver.find_element(By.ID, "email")
        emailElement.clear()
        emailElement.send_keys("newemail@example.com")
        usernameElement = self.driver.find_element(By.ID, "username")
        usernameElement.clear()
        usernameElement.send_keys("newusername")
        passwordElement = self.driver.find_element(By.ID, "password")
        passwordElement.send_keys("newpassword")
        csrfElement = self.driver.find_element(By.NAME, "csrf_token")
        csrfElement.send_keys(csrf_token)

        submitElement = self.driver.find_element(By.CSS_SELECTOR, "#editProfileForm .btn.btn-primary")
        submitElement.click()

        # Ensure the modal closes and changes are saved
        time.sleep(1)  # Wait for the modal to close and the page to refresh
        self.assertEqual(self.driver.current_url, localHost + "/profile")
        self.assertIn("newusername", self.driver.page_source)
        self.assertIn("newemail@example.com", self.driver.page_source)

    # Other test cases...

if __name__ == "__main__":
    unittest.main()

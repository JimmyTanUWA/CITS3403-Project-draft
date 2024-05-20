import multiprocessing
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from flask import url_for
from app import create_app, db
from app.config import TestConfig
from app.models import User

localHost = "http://localhost:5000"

class SeleniumTests(unittest.TestCase):
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
        csrf_token = self.driver.find_element(By.NAME, "csrf_token").get_attribute("value")
        return csrf_token

    def test_signup(self):
        """
        This function tests user signup
        """
        self.driver.get(localHost + "/signup")
        csrf_token = self.get_csrf_token()

        self.driver.find_element(By.ID, "username").send_keys("newuser")
        self.driver.find_element(By.ID, "email").send_keys("newuser@example.com")
        self.driver.find_element(By.ID, "password").send_keys("Password123!")
        self.driver.find_element(By.ID, "confirm_password").send_keys("Password123!")
        self.driver.find_element(By.NAME, "csrf_token").send_keys(csrf_token)
        self.driver.find_element(By.ID, "submit").click()

        self.assertEqual(self.driver.current_url, localHost + "/login")

    def test_login(self):
        """
        This function tests user login
        """
        self.driver.get(localHost + "/login")
        csrf_token = self.get_csrf_token()

        self.driver.find_element(By.ID, "username").send_keys("matt")
        self.driver.find_element(By.ID, "password").send_keys("123456")
        self.driver.find_element(By.NAME, "csrf_token").send_keys(csrf_token)
        self.driver.find_element(By.ID, "submit").click()

        self.assertEqual(self.driver.current_url, localHost + "/index")

    def test_create_chat(self):
        """
        This function tests creating a new chat
        """
        self.test_login()  # Log in first

        self.driver.get(localHost + "/moviedetails/some_movie")
        self.driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary").click()
        time.sleep(1)  # Wait for the modal to open

        csrf_token = self.get_csrf_token()
        self.driver.find_element(By.NAME, "comment").send_keys("This is a test comment")
        self.driver.find_element(By.NAME, "csrf_token").send_keys(csrf_token)
        self.driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary").click()

        time.sleep(1)  # Wait for the page to refresh
        self.assertIn("This is a test comment", self.driver.page_source)

    def test_delete_chat(self):
        """
        This function tests deleting a chat
        """
        self.test_create_chat()  # Ensure there is a chat to delete

        self.driver.find_element(By.CSS_SELECTOR, "button.btn-danger").click()
        time.sleep(1)  # Wait for the page to refresh

        self.assertNotIn("This is a test comment", self.driver.page_source)

    def test_like_dislike_chat(self):
        """
        This function tests liking and disliking a chat
        """
        self.test_create_chat()  # Ensure there is a chat to like/dislike

        like_button = self.driver.find_element(By.CSS_SELECTOR, "button.btn-outline-success")
        dislike_button = self.driver.find_element(By.CSS_SELECTOR, "button.btn-outline-danger")

        like_button.click()
        time.sleep(1)  # Wait for the action to complete

        self.assertIn("btn-success", like_button.get_attribute("class"))

        dislike_button.click()
        time.sleep(1)  # Wait for the action to complete

        self.assertIn("btn-danger", dislike_button.get_attribute("class"))

    def test_search_movies(self):
        """
        This function tests searching for movies
        """
        self.driver.get(localHost + "/search?query=some_movie")
        time.sleep(1)  # Wait for the search results to load

        self.assertIn("some_movie", self.driver.page_source)

    def test_edit_profile(self):
        """
        This function tests editing the user profile
        """
        self.test_login()  # Log in first

        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        self.assertEqual(self.driver.current_url, localHost + "/profile")

        self.driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary").click()
        time.sleep(1)  # Wait for the modal to open

        csrf_token = self.get_csrf_token()
        self.driver.find_element(By.ID, "email").clear()
        self.driver.find_element(By.ID, "email").send_keys("newemail@example.com")
        self.driver.find_element(By.ID, "username").clear()
        self.driver.find_element(By.ID, "username").send_keys("newusername")
        self.driver.find_element(By.NAME, "csrf_token").send_keys(csrf_token)
        self.driver.find_element(By.CSS_SELECTOR, "#editProfileForm .btn.btn-primary").click()

        time.sleep(1)  # Wait for the page to refresh
        self.assertEqual(self.driver.current_url, localHost + "/profile")
        self.assertIn("newusername", self.driver.page_source)
        self.assertIn("newemail@example.com", self.driver.page_source)

    def test_change_password(self):
        """
        This function tests changing the user password
        """
        self.test_login()  # Log in first

        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        self.assertEqual(self.driver.current_url, localHost + "/profile")

        self.driver.find_element(By.ID, "changePwButton").click()
        time.sleep(1)  # Wait for the form to display

        csrf_token = self.get_csrf_token()
        self.driver.find_element(By.ID, "password").send_keys("newpassword")
        self.driver.find_element(By.ID, "confirm_password").send_keys("newpassword")
        self.driver.find_element(By.NAME, "csrf_token").send_keys(csrf_token)
        self.driver.find_element(By.CSS_SELECTOR, "#changePwForm .btn.btn-primary").click()

        time.sleep(1)  # Wait for the page to refresh
        self.assertEqual(self.driver.current_url, localHost + "/profile")

if __name__ == "__main__":
    unittest.main()

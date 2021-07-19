import unittest, sys

sys.path.append('../Twitch-Youtube-Stats') # imports python file from parent directory
from Web import app #imports flask app object

class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        self.app = app.test_client()

    ###############
    #### tests ####
    ###############

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/home', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_youtube_page(self):
        response = self.app.get('/youtube', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_twitch_page(self):
        response = self.app.get('/twitch', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_logout_page(self):
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_profile_page(self):
        response = self.app.get('/profile', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_about_page(self):
        response = self.app.get('/about', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        response = self.app.get('/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
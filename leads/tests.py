from django.test import TestCase
from django.shortcuts import reverse


# there are many test functions in TestCase class that can be used to test

# test if our view for landing page is working or not
class LandingPageTest(TestCase):

    # if we start our func with test then a single test will run
    # send a request to our landing page and see the response
    # if we get a 200 response then it means our view is working
    def test_get(self):
        response = self.client.get(reverse('landing_page'))
        # check if the response is 200 otherwise raise an error
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing_page.html')



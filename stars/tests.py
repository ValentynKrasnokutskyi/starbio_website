from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from stars.models import Stars


class GetPagesTestCase(TestCase):
    fixtures = ['stars_stars.json', 'stars_category.json', 'stars_spouse.json', 'stars_tagpost.json']

    def setUp(self):
        "Initialization before each test execution"

    def test_mainpage(self):  # Test for checking the main page
        path = reverse('home')  # Get the URL of the main page
        response = self.client.get(path)  # Get the server response for this URL
        self.assertEqual(response.status_code, HTTPStatus.OK)  # Check that the response code is HTTP 200 (OK)
        self.assertTemplateUsed(response, 'stars/index.html')  # Check that the correct template is used
        self.assertEqual(response.context_data['title'], 'Main page')  # Check that the context contains the correct title

    def test_redirect_addpage(self):  # Test for checking redirection when attempting to add a page
        path = reverse('add_page')  # Get the URL of the add page
        redirect_uri = reverse('users:login') + '?next=' + path  # Formulate the URL to redirect to the login page
        response = self.client.get(path)  # Get the server response for this URL
        self.assertEqual(response.status_code, HTTPStatus.FOUND)  # Check that redirection occurs
        self.assertRedirects(response, redirect_uri)  # Check that redirection occurs to the login page

    def test_data_mainpage(self):  # Test for checking data on the main page
        s = Stars.published.all().select_related('cat')  # Get a list of published stars with their categories
        path = reverse('home')  # Get the URL of the main page
        response = self.client.get(path)  # Get the server response for this URL
        self.assertQuerySetEqual(response.context_data['posts'], s[:3])  # Check that the correct data is displayed

    def test_paginate_mainpage(self):  # Test for checking pagination on the main page
        path = reverse('home')  # Get the URL of the main page
        page = 2  # Page number for the test
        paginate_by = 3  # Number of entries per page
        response = self.client.get(path + f'?page={page}')  # Get the server response for a specific page
        w = Stars.published.all().select_related('cat')  # Get all published stars with their categories
        # Check that the correct entries are displayed on this page
        self.assertQuerysetEqual(response.context_data['posts'], w[(page - 1) * paginate_by:page * paginate_by])

    def test_content_post(self):  # Test for checking the content of a single post page
        s = Stars.published.get(pk=1)  # Get a published star by primary key
        path = reverse('post', args=[s.slug])  # Get the URL of the page with this star
        response = self.client.get(path)  # Get the server response for this URL
        self.assertEqual(s.content, response.context_data['post'].content)  # Check that the post content is displayed correctly

    def tearDown(self):
        "Actions after each test execution"

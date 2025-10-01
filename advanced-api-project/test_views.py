# api/test_views.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Author, Book
import datetime

class BookAPITestCase(APITestCase):
    def setUp(self):
        # create user for authenticated actions
        self.user = User.objects.create_user(username='tester', password='password123')
        # create authors and sample books
        self.author1 = Author.objects.create(name='Author One')
        self.author2 = Author.objects.create(name='Author Two')

        current_year = datetime.date.today().year
        self.book1 = Book.objects.create(title='Alpha', publication_year=current_year - 1, author=self.author1)
        self.book2 = Book.objects.create(title='Beta', publication_year=current_year - 2, author=self.author2)

        self.client = APIClient()

    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # results might be paginated
        data = response.data.get('results', response.data)
        titles = [b['title'] for b in data]
        self.assertIn('Alpha', titles)
        self.assertIn('Beta', titles)

    def test_filter_by_author(self):
        url = reverse('book-list') + f'?author={self.author1.id}'
        response = self.client.get(url)
        data = response.data.get('results', response.data)
        self.assertTrue(all(item['author'] == self.author1.id for item in data))

    def test_search(self):
        url = reverse('book-list') + '?search=Alpha'
        response = self.client.get(url)
        data = response.data.get('results', response.data)
        self.assertTrue(any('Alpha' in item['title'] for item in data))

    def test_ordering(self):
        url = reverse('book-list') + '?ordering=publication_year'
        response = self.client.get(url)
        data = response.data.get('results', response.data)
        years = [item['publication_year'] for item in data]
        self.assertEqual(sorted(years), years)

    def test_create_book_requires_authentication(self):
        url = reverse('book-create')
        payload = {'title': 'Gamma', 'publication_year': 2000, 'author': self.author1.id}
        # unauthenticated attempt
        r = self.client.post(url, payload, format='json')
        self.assertIn(r.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        # authenticated attempt
        self.client.force_authenticate(user=self.user)
        r2 = self.client.post(url, payload, format='json')
        self.assertEqual(r2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.filter(title='Gamma').count(), 1)

    def test_publication_year_validation(self):
        url = reverse('book-create')
        bad_year = datetime.date.today().year + 1
        payload = {'title': 'FutureBook', 'publication_year': bad_year, 'author': self.author1.id}
        self.client.force_authenticate(user=self.user)
        r = self.client.post(url, payload, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', r.data)

    def test_update_and_delete_requires_auth(self):
        update_url = reverse('book-update', kwargs={'pk': self.book1.id})
        delete_url = reverse('book-delete', kwargs={'pk': self.book1.id})

        # unauthenticated update should fail
        r = self.client.patch(update_url, {'title': 'New Title'}, format='json')
        self.assertIn(r.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        # authenticated update
        self.client.force_authenticate(user=self.user)
        r2 = self.client.patch(update_url, {'title': 'New Title'}, format='json')
        self.assertEqual(r2.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'New Title')

        # delete
        r3 = self.client.delete(delete_url)
        self.assertEqual(r3.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book1.id).exists())

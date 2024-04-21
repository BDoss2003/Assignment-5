from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework import routers
from rest_framework.test import APIRequestFactory, APITestCase
from django.contrib.auth.models import User
import os
from django.conf import settings
import datetime
from .models import Bookmark, Snippet 
from .views import BookmarkViewSet, SnippetViewSet

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djbarky.settings')
settings.configure()

# Create your tests here.
# test plan


class BookmarkTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.bookmark = Bookmark.objects.create(
            id=1,
            title="Awesome Django",
            url="https://awesomedjango.org/",
            notes="Best place on the web for Django.",
        )
        # print(f"bookmark id: {self.bookmark.id}")

        # the simple router provides the name 'bookmark-list' for the URL pattern: https://www.django-rest-framework.org/api-guide/routers/#simplerouter
        self.list_url = reverse("barkyapi:bookmark-list")
        self.detail_url = reverse(
            "barkyapi:bookmark-detail", kwargs={"pk": self.bookmark.id}
        )

    # 1. create a bookmark
    def test_create_bookmark(self):
        """
        Ensure we can create a new bookmark object.
        """

        # the full record is required for the POST
        data = {
            "id": 99,
            "title": "Django REST framework",
            "url": "https://www.django-rest-framework.org/",
            "notes": "Best place on the web for Django REST framework.",
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(Bookmark.objects.count(), 2)
        self.assertEqual(Bookmark.objects.get(id=99).title, "Django REST framework")

    # 2. list bookmarks
    def test_list_bookmarks(self):
        """
        Ensure we can list all bookmark objects.
        """
        response = self.client.get(self.list_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["results"][0]["title"], self.bookmark.title)

    # 3. retrieve a bookmark
    def test_retrieve_bookmark(self):
        """
        Ensure we can retrieve a bookmark object.
        """
        response = self.client.get(self.detail_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["title"], self.bookmark.title)

    # 4. delete a bookmark
    def test_delete_bookmark(self):
        """
        Ensure we can delete a bookmark object.
        """
        response = self.client.delete(
            reverse("barkyapi:bookmark-detail", kwargs={"pk": self.bookmark.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Bookmark.objects.count(), 0)

    # 5. update a bookmark
    def test_update_bookmark(self):
        """
        Ensure we can update a bookmark object.
        """
        # the full record is required for the POST
        data = {
            "id": 99,
            "title": "Awesomer Django",
            "url": "https://awesomedjango.org/",
            "notes": "Best place on the web for Django just got better.",
        }
        response = self.client.put(
            reverse("barkyapi:bookmark-detail", kwargs={"pk": self.bookmark.id}),
            data,
            format="json",
        )
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["title"], "Awesomer Django")

#Snippets
class SnippetCreateTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpassword')
    
# 6. create a snippet
    def test_create_snippet(self):
        """
        Test creating a snippet via the API.
        """
        snippet_data = {
            'id': 100,
            'title': 'Test Snippet',
            'code': 'print("Create Snippet!")',
            'language': 'python',
            'style': 'friendly',
        }
        response = self.client.post('/snippets/', snippet_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check if the snippet is created in the database
        self.assertTrue(Snippet.objects.filter(title='Test Snippet').exists())



# 6. create a snippet
    def test_create_snippet(self):
        """
        Ensure we can create a snippet
        """
        snippet = Snippet.objects.get(id=100)
        self.assertEqual(snippet.title, 'Test Snippet')
        self.assertEqual(snippet.code, 'print("Snippet Success!")')
        self.assertEqual(snippet.language, 'python')
        self.assertEqual(snippet.style, 'friendly')
        self.assertEqual(snippet.owner.username, 'BaM')
        self.assertEqual(snippet.highlighted, '<pre><code class="python">print("<span class=\"kn\">Snippet</span>, <span class=\"n\">Created</span>!")\n</code></pre>')

# 7. retrieve a snippet
    def test_retrieve_snippet(self):
        """
        Test retrieving a single snippet via the API.
        """
        response = self.client.get(f'/snippets/{self.snippet.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Snippet')

# 8.  List snippets
    def test_delete_snippet(self):
        """
        Test deleting a snippet via the API.
        """
        response = self.client.delete(f'/snippets/{self.snippet.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Snippet.objects.filter(id=self.snippet.id).exists())    
    
# 9. List Snippets    
    def test_list_snippets(self):
        """
        Test listing all snippets via the API.
        """
        response = self.client.get('/snippets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Snippet')

# 10. Update Snippets
    def test_update_snippet(self):
        """
        Test updating a snippet via the API.
        """
        snippet_data = {
            'title': 'Updated Snippet',
            'code': 'print("Updated!")',
            'language': 'python',
            'style': 'friendly',
        }
        response = self.client.put(f'/snippets/{self.snippet.id}/', snippet_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Snippet')

class UserCRUDTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
# 11. create a user
    def test_create_user(self):
        """
        Test creating a user via the API.
        """
        user_data = {
            'username': 'newuser',
            'password': 'newpassword',
        }
        response = self.client.post('/users/', user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())
# 12. retrieve a user
    def test_retrieve_user(self):
        """
        Test retrieving a user via the API.
        """
        response = self.client.get(f'/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
# 13. delete a user
    def test_delete_user(self):
        """
        Test deleting a user via the API.
        """
        response = self.client.delete(f'/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())
# 14. list users
    def test_list_users(self):
        """
        Test listing all users via the API.
        """
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'testuser')
# 15. update a user
    def test_update_user(self):
        """
        Test updating a user via the API.
        """
        user_data = {
            'username': 'updateduser',
        }
        response = self.client.put(f'/users/{self.user.id}/', user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'updateduser')

class AdditionalAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
# 16. highlight a snippet
    def test_highlight_snippet(self):
        """
        Test highlighting a snippet via the API. (Test #16)
        """
        snippet_data = {
            'title': 'Test Snippet',
            'code': 'print("Highlighted Snippet!")',
            'language': 'python',
            'owner': self.user.id
        }
        response = self.client.post('/snippets/', snippet_data, format='json')
        snippet_id = response.data['id']
        response = self.client.get(f'/snippets/{snippet_id}/highlight/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
# 17. list bookmarks by user
    def test_list_bookmarks_by_user(self):
        """
        Test listing bookmarks by user via the API. (Test #17)
        """
        response = self.client.get(f'/bookmarks/?user={self.user.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
# 18. list snippets by user
    def test_list_snippets_by_user(self):
        """
        Test listing snippets by user via the API. (Test #18)
        """
        response = self.client.get(f'/snippets/?owner={self.user.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# 20. list bookmarks by date
def test_list_bookmarks_by_date(self):
        """
        Test listing bookmarks by date via the API. (Test #20)
        """
        # Add your test logic here
        response = self.client.get(f'/bookmarks/?date={datetime.datetime.now()}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# 21. list snippet by date
def test_list_bookmarks_by_date(self):
        """
        Test listing snippets by date via the API. (Test #20)
        """
        # Add your test logic here
        response = self.client.get(f'/snippets/?created={datetime.datetime.now()}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# 20. list bookmarks by title
def test_list_bookmarks_by_date(self):
        """
        Test listing bookmarks by date via the API. (Test #20)
        """
        # Add your test logic here
        response = self.client.get(f'/bookmarks/?ordering=title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# 21. list snippet by title
def test_list_bookmarks_by_date(self):
        """
        Test listing snippets by date via the API. (Test #20)
        """
        # Add your test logic here
        response = self.client.get(f'/snippets/?ordering=title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# 26. list bookmarks by url
# 27. list snippets by url

from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment

class CommentTests(TestCase):
    def setUp(self):
        self.u1 = User.objects.create_user('u1','u1@example.com','pass')
        self.u2 = User.objects.create_user('u2','u2@example.com','pass')
        self.post = Post.objects.create(title='T', content='C', author=self.u1, slug='t')

    def test_add_comment_requires_login(self):
        url = reverse('blog:comment-create', kwargs={'slug': self.post.slug})
        resp = self.client.post(url, {'content': 'hello'})
        self.assertNotEqual(resp.status_code, 200)  # should redirect to login

    def test_add_comment_creates(self):
        self.client.login(username='u2', password='pass')
        url = reverse('blog:comment-create', kwargs={'slug': self.post.slug})
        resp = self.client.post(url, {'content': 'hello'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(self.post.comments.filter(content='hello', author=self.u2).exists())

    def test_edit_comment_only_author(self):
        c = Comment.objects.create(post=self.post, author=self.u2, content='x')
        edit_url = reverse('blog:comment-edit', kwargs={'pk': c.pk})
        self.client.login(username='u1', password='pass')
        resp = self.client.post(edit_url, {'content':'y'})
        # not allowed - should not change
        c.refresh_from_db()
        self.assertEqual(c.content, 'x')

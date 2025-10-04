from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import  Comment , Post

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



from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post

class TagSearchTests(TestCase):
    def setUp(self):
        u = User.objects.create_user('u','u@example.com','pass')
        self.p1 = Post.objects.create(title='Foo', content='bar', author=u, slug='foo')
        self.p1.tags.add('news','django')
        self.p2 = Post.objects.create(title='Django tips', content='tips content', author=u, slug='django-tips')
        self.p2.tags.add('django')

    def test_tag_listing(self):
        resp = self.client.get(reverse('blog:tag-posts', kwargs={'tag':'django'}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Django tips')
        self.assertContains(resp, 'Foo')

    def test_search_title(self):
        resp = self.client.get(reverse('blog:search') + '?q=Foo')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Foo')

    def test_search_tag(self):
        resp = self.client.get(reverse('blog:search') + '?q=django')
        self.assertEqual(resp.status_code, 200)
        # both posts have django tag
        self.assertContains(resp, 'Foo')
        self.assertContains(resp, 'Django tips')

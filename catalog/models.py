from django.db import models
from django.urls import reverse  # To generate URLS by reversing URL patterns
from django.conf.global_settings import LANGUAGES
from django.contrib.auth.models import AbstractUser


# recommended to wrap user model : https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
class User(AbstractUser):
    pass


class Tag(models.Model):
    """Model representing a book tag (e.g. Science Fiction, Non Fiction)."""
    name = models.CharField(
        max_length=200,
        help_text="Enter a book tag (e.g. Science Fiction, French Poetry etc.)"
        )

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book", blank=True, null=True)
    isbn = models.CharField('ISBN', max_length=13,
                            unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>', blank=True, null=True)
    tag = models.ManyToManyField(Tag, help_text="Select a tag for this book", blank=True, null=True)
    # ManyToManyField used because a tag can contain many books and a Book can cover many tags.
    # Tag class has already been defined so we can specify the object above.
    language = models.CharField(
        max_length=10,
        choices=LANGUAGES,
        blank=True,
        null=True,
        default='en',
    )

    # book lending admin
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="borrower")
    LOAN_STATUS = (
        ('o', 'On loan'),
        ('a', 'Available'),
    )
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='a',
        help_text='Book availability')
    
    class Meta:
        ordering = ['title', 'author']

    def display_tag(self):
        """Creates a string for the Tag. This is required to display tag in Admin."""
        return ', '.join([tag.name for tag in self.tag.all()[:3]])

    display_tag.short_description = 'Tag'

    def get_absolute_url(self):
        """Returns the url to access a particular book instance."""
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.title

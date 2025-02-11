from django.shortcuts import render
from .models import Book, Tag
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin


def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    latest_books = Book.objects.order_by('-creation_date')[0:4]
    colours = ["mistyrose", "lemonchiffon", "#d0eed0", "aliceblue"]
    books = []
    for idx, book in enumerate(latest_books):
        books.append({
            'title': book.title,
            'author': book.author,
            'get_absolute_url': book.get_absolute_url(),
            'colour': colours[idx]
        })

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={'num_books': num_books,
                 'num_visits': num_visits, 'books': books},
    )


class BookListView(generic.ListView):
    """Generic class-based view for a list of books."""
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    """Generic class-based detail view for a book."""
    model = Book


# class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
#     """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""
#     model = BookInstance
#     permission_required = 'catalog.can_mark_returned'
#     template_name = 'catalog/bookinstance_list_borrowed_all.html'
#     paginate_by = 10

#     def get_queryset(self):
#         return BookInstance.objects.filter(status__exact='o').order_by('due_back')


# from django.shortcuts import get_object_or_404
# from django.http import HttpResponseRedirect
# from django.urls import reverse
# import datetime
# from django.contrib.auth.decorators import login_required, permission_required

# # from .forms import RenewBookForm
# from catalog.forms import RenewBookForm


# @login_required
# @permission_required('catalog.can_mark_returned', raise_exception=True)
# def renew_book_librarian(request, pk):
#     """View function for renewing a specific BookInstance by librarian."""
#     book_instance = get_object_or_404(BookInstance, pk=pk)

#     # If this is a POST request then process the Form data
#     if request.method == 'POST':

#         # Create a form instance and populate it with data from the request (binding):
#         form = RenewBookForm(request.POST)

#         # Check if the form is valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
#             book_instance.due_back = form.cleaned_data['renewal_date']
#             book_instance.save()

#             # redirect to a new URL:
#             return HttpResponseRedirect(reverse('all-borrowed'))

#     # If this is a GET (or any other method) create the default form
#     else:
#         proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
#         form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

#     context = {
#         'form': form,
#         'book_instance': book_instance,
#     }

#     return render(request, 'catalog/book_renew_librarian.html', context)


# Classes created for the forms challenge
class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'tag', 'language']
    permission_required = 'catalog.can_mark_returned'


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'tag', 'language']
    permission_required = 'catalog.can_mark_returned'


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.can_mark_returned'

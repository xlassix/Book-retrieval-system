from import_export import resources
from .models import Books

class BooksResource(resources.ModelResource):
    class Meta:
        model = Books
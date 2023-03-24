from django.shortcuts import render
from rest_framework.schemas.openapi import SchemaGenerator


def schema(request):
    """Этот код вам не пригодится, но и удалять его не стоит."""
    generator = SchemaGenerator(title='YaMDb API')
    getted_schema = generator.get_schema() or {
        'info': {'title': 'YaMDb API'}, 'paths': {}
    }
    schema = {
        'title': getted_schema['info']['title'],
        'endpoints': []
    }
    for path in getted_schema['paths']:
        for method in getted_schema['paths'][path].keys():
            schema['endpoints'].append({'path': path, 'method': method})

    return render(request, 'index.html', {'schema': schema})

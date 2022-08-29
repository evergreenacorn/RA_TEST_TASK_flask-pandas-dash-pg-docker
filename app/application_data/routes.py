from .views import index, upload_file, show_dashboard, filter_table, Output, Input

def configure_apis(app):
    
    app.add_url_rule(
        '/',
        'index',
        view_func=index
    )
    app.add_url_rule(
        '/import_csv/',
        'import-csv',
        methods=['GET', 'POST'],
        view_func=upload_file
    )

def configure_styles():
    return [
        {
            "href": "https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css",
            "rel": "stylesheet",
            "integrity": "sha384-gH2yIJqKdNHPEq0n4Mqa/HGKIhSkIHeL5AyhkYV8i59U5AR6csBvApHHNl/vI1Bx",
            "crossorigin": "anonymous"
        },
    ]

def configure_dashboard(app):
    show_dashboard(app)
    
def configure_dashboard_callbacks(app):
    filter_table(app)
        

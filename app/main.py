from application_data import create_server, create_app_from_server, db
from application_data.models.task_models import Event, EventType, Company, MediaSource, Platform
from application_data.routes import configure_apis, configure_dashboard, configure_styles, configure_dashboard_callbacks


server = create_server()
configure_apis(server)
app = create_app_from_server(server, stylesheets=configure_styles())
configure_dashboard(app)
configure_dashboard_callbacks(app)
app = app.server


@server.shell_context_processor
def make_shell_context():
    context_dict = {x.__name__: x for x in (Event, EventType, Company, MediaSource, Platform)}
    context_dict['db'] = db
    context_dict['app'] = server
    return context_dict


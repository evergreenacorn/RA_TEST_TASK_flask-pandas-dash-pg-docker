from flask import request, render_template, redirect, url_for, current_app, flash
from sqlalchemy import select, func
from werkzeug.utils import secure_filename
from .models import Event, EventType, Company, MediaSource, Platform
from .helpers import CsvImporter, DataframeImporter, render_dashboard_table, render_dashboard_filters
from application_data import db
from datetime import datetime
from dash import html, dcc
from dash.dependencies import Output, Input
import os


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']

def index():
    """Обработчик загрузки домашней страницы"""
    return render_template('index.html')

def _import_secondary_data_to_bd(secondary_table_data):
    db.create_all()
    secondary_tables = (EventType, Company, MediaSource, Platform)

    for _ in secondary_tables:
        data = list(secondary_table_data[_.__tablename__])
        exists_data = _.query.filter(_.name.in_(data))
        not_exists_data = list(set(data) - set(exists_data))

        values_to_insert = [_(name=val) for val in not_exists_data]
        try:
            db.session.add_all(values_to_insert)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return False
    return True

def _import_main_data_to_bd(df):
    try:
        date_format = "%Y-%m-%d %H:%M:%S"
        new_events = []
        for row in df.itertuples():
            row_data = tuple(row)
            new_event = Event(
                appsflyer_id=row_data[3],
                revenue=row_data[8],
                revenue_usd=row_data[9],
                install_time=datetime.strptime(row_data[1], date_format),
                event_time=datetime.strptime(row_data[2], date_format),
            )
            event_type = EventType.query.filter_by(name=row_data[7]).first()\
                if (row_data[7] is not None and str(row_data[7]) != 'nan') else None
            media_source = MediaSource.query.filter_by(name=row_data[4]).first()\
                if (row_data[4] is not None and str(row_data[4]) != 'nan') else None
            campaign = Company.query.filter_by(name=row_data[5]).first()\
                if (row_data[5] is not None and str(row_data[5]) != 'nan') else None
            platform = Platform.query.filter_by(name=row_data[6]).first()\
                if (row_data[6] is not None and str(row_data[6]) != 'nan') else None
            
            
            if event_type is not None:
                new_event.type_id = event_type.id
            if media_source is not None:
                new_event.mediasource_id = media_source.id
            if campaign is not None:
                new_event.company_id = campaign.id
            if platform is not None:
                new_event.platform_id = platform.id

            new_events.append(new_event)

        db.session.add_all(new_events)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return False

    return True

def upload_file():
    """Обработчик загрузки страницы импорта csv-файлов"""
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            csv_df = CsvImporter(file)
            
            models_map = {
                "media_source": MediaSource,
                "campaign": Company,
                "platform": Platform,
                "event_name": EventType,
            }
            main_model = Event
            
            df = DataframeImporter(
                csv_df.df,
                models_map=models_map,
                main_model=main_model
            )
            secondary_table_data = df.secondary_tables_data
            df = df.df
            
            imported_sec_data = _import_secondary_data_to_bd(secondary_table_data)
            imported_main_data = _import_main_data_to_bd(df)
            if imported_main_data:
                message="Файл успешно импортирован!"
            else:
                message="Не удалось импортировать файл!"
            flash(message)
            return redirect(url_for('index'))

    if request.method == 'GET':
        return render_template('import_csv.html')

def show_dashboard(app):
    """Обработчик загрузки страницы генерации отчетов"""
    data = None
    media_sources = None
    companies = None
    platforms = None
    with app.server.app_context():
        db.create_all()
        data = db.session.query(
            Company.name.label('company_name'),
            
            func.count(Event.type_id).label("installs_count"),
            func.sum(Event.revenue).label("total_revenue")
        ).join(
            EventType,
            MediaSource,
            Company,
            Platform
        ).filter(
            EventType.name == 'install'
        ).group_by(
            'company_name'
        ).all()
        
        media_sources = db.session.query(MediaSource).all()
        companies = db.session.query(Company).all()
        platforms = db.session.query(Platform).all()

    table = render_dashboard_table(data)
    
    filters_list = render_dashboard_filters(media_sources, companies, platforms)

    return html.Div(
        children=[
            # Navbar
            html.Nav(
                children=html.Div(
                    children=html.A(
                        children="Домой",
                        href="/",
                        className="navbar-brand"
                    ),
                    className="row"
                ),
                className="navbar navbar-dark bg-primary"
            ),
            
            # Filters
            html.Div(
                children=filters_list,
                className='row',
                id="dashboard-filters"
            ),

            # Table
            html.Div(
                html.Div(
                    children=table,
                    className='col-12', id="dashboard-table"
                ),
                className="row"
            ),

        ], 
        className='container-fluid'
    )


def filter_table(app):
    @app.callback(
            Output("dashboard-table", "children"),
        [
            Input("date-range", "start_date"),
            Input("date-range", "end_date"),
            Input("mediasource-filter", "value"),
            Input("company-filter", "value"),
            Input("platform-filter", "value"),
        ],
    )
    def table_callback(start_date, end_date, mediasource_value, company_value, platform_value):
        inp_date_fmt = '%Y-%m-%d'

        with app.server.app_context():
            db.create_all()
            data = db.session.query(
                Company.name.label('company_name'),
                func.count(Event.type_id).label("installs_count"),
                func.sum(Event.revenue).label("total_revenue")
            ).join(
                EventType,
                MediaSource,
                Company,
                Platform
            ).filter(
                EventType.name == 'install'
            )
            
            if all([start_date, end_date]):
                start_date = datetime.strptime(start_date, inp_date_fmt)
                end_date = datetime.strptime(end_date, inp_date_fmt)
                data = data.filter(Event.event_time >= start_date).\
                    filter(Event.event_time <= end_date)
            if mediasource_value and mediasource_value != '':
                data = data.filter(Event.mediasource_id == mediasource_value)
            if company_value and company_value != '':
                data = data.filter(Event.company_id == company_value)
            if platform_value and platform_value != '':
                data = data.filter(Event.platform_id == platform_value)
            
            data = data.group_by('company_name').all()
                        
        table = render_dashboard_table(data)
        return table  # , mediasource_value, company_value, platform_value

 
def reset_filters(app):
    @app.callback(
        Output("dashboard-filters", "children"),
        Input("reset-button", "n_clicks")
    )
    def reset_btn_callback(n_clicks):
        if n_clicks:
            if n_clicks >= 1:
                n_clicks = 0

                with app.server.app_context():
                    db.create_all()
                    media_sources = db.session.query(MediaSource).all()
                    companies = db.session.query(Company).all()
                    platforms = db.session.query(Platform).all()
                return render_dashboard_filters(media_sources, companies, platforms) 
        else:
            return render_dashboard_filters(None, None, None)

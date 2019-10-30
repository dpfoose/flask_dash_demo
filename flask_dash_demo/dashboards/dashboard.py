from dash import Dash
from dash.exceptions import PreventUpdate
from flask import url_for
from flask_login import current_user
from jinja2 import Template


def url_for_(endpoint, **values):
    try:
        return url_for(endpoint, **values)
    except RuntimeError:
        return ''


navbar_template = open('templates/navbar.html')
navbar_html = Template(navbar_template).render(url_for=url_for, current_user=current_user)


class Dashboard:
    name = 'Dashboard'
    prefix = '/dashboards/'
    description = 'You should overload description with the description of your dashboard.'
    id = 'dashboard'

    @staticmethod
    def create_dash_app(server):
        """
        :param server:
        :return:
        """
        raise NotImplementedError('')

    @staticmethod
    def check_clicks(n_clicks):
        if not n_clicks:
            raise PreventUpdate('Callback triggered without action!')

    @staticmethod
    def check_dropdown(value):
        if not value or None in value:
            raise PreventUpdate('Callback triggered without action!')


class MyDash(Dash):
    def interpolate_index(self, **kwargs):
        return f'''
        <!DOCTYPE html>
        <html>
            <head>
                <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
                <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.0/css/all.css" integrity="sha384-lZN37f5QGtY3VHgisS14W3ExzMWZxybE1SJSEsQp9S+oqd12jhcu+A56Ebc1zFSJ" crossorigin="anonymous">
                <title>{kwargs["title"]}</title>
            </head>
            <body>
                { navbar_html }
                {kwargs["app_entry"]}
                {kwargs["config"]}
                {kwargs["scripts"]}
                <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
                <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.bundle.min.js" integrity="sha384-zDnhMsjVZfS3hiP7oCBRmfjkQC4fzxVxFhBx8Hkz2aZX8gEvA/jsP3eXRCvzTofP" crossorigin="anonymous"></script>
                {kwargs["renderer"]}
            </body>
        </html>
        '''

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed


class CsvImporterForm(FlaskForm):
    file = FileField(
        "Загрузить csv-файл",
        validators=[
            FileRequired(),
            FileAllowed(['csv'], 'только csv файлы')
        ]
    )

# ---------- IMPORTS ---------- #

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

# ---------- FORMS ---------- #

class NewTaskForm(FlaskForm):
    list_id = SelectField("List", coerce=int, validators=[DataRequired()])
    title = StringField("Task", validators=[DataRequired()])
    notes = StringField("Notes")
    submit = SubmitField("Create Task")

class EditTaskForm(FlaskForm):
    list_id = SelectField("List", coerce=int, validators=[DataRequired()])
    title = StringField("Task", validators=[DataRequired()])
    notes = StringField("Notes")
    submit = SubmitField("Update Task")

class NewListForm(FlaskForm):
    title = StringField("List", validators=[DataRequired()])
    submit = SubmitField("Create List")
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField ,TextAreaField, IntegerField, DateField, SelectField, SubmitField,FloatField,DecimalField
from wtforms.validators import InputRequired, EqualTo, Email, Length


class AdminRegisterForm(FlaskForm):
	username = StringField("Username",validators=[InputRequired(),Length(max=100)])
	email = StringField("Email",validators=[InputRequired(),Email(),Length(max=100)])
	password = PasswordField("Password",validators=[InputRequired(),Length(min=6,max=100)])

class AdminLoginForm(FlaskForm):
	email = StringField("Email",validators=[InputRequired(),Email(),Length(max=100)])
	password = PasswordField("Password",validators=[InputRequired(),Length(min=6,max=100)])



############################################ Inventory ###########################################
class AddInventoryForm(FlaskForm):
	tahun = IntegerField("Tahun",validators=[InputRequired()])
	merk = StringField("Merk",validators=[InputRequired(),Length(max=200)])
	jenis = StringField("Jenis",validators=[InputRequired(),Length(max=200)])
	tipe = StringField("Tipe",validators=[InputRequired(),Length(max=200)])
	warna = StringField("Warna",validators=[InputRequired(),Length(max=200)])
	nopol = StringField("Nopol",validators=[InputRequired(),Length(max=200)])
	samsat = DateField("Samsat",format="%m/%d/%Y")
	asli = StringField("Asli/Mutasan",validators=[InputRequired()])
	beli = IntegerField("Harga Beli",validators=[InputRequired()])
	biaya = IntegerField("Biaya",validators=[InputRequired()])
	harga = IntegerField("Harga Bukaan",validators=[InputRequired()])

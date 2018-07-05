# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy 
from config import database, secret
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask_login import LoginManager , UserMixin, login_user, login_required, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
from flask_mail import Mail,Message 
from functools import wraps
from form import AdminRegisterForm,AdminLoginForm,AddInventoryForm



app = Flask(__name__) 
app.config["SQLALCHEMY_DATABASE_URI"] = database
app.config["SECRET_KEY"] = secret 
db = SQLAlchemy(app)
app.debug = True 


#################################################### Decorator ##############################################################################

#login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "Login"

#user loader
@login_manager.user_loader
def user_loader(user_id):
	return User.query.get(int(user_id))

#fungsi mail
app.config.from_pyfile("config.py") 
mail = Mail(app)
s = URLSafeTimedSerializer("secret")





class User(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(100))
	email = db.Column(db.String(200))	
	password = db.Column(db.String(500))	
	role = db.Column(db.String(100))	

	def is_active(self):
		return True

	def get_id(self):
		return self.id

	def is_authenticated(self):
		return self.authenticated

	def is_anonymous(self):
		return False


class Inventory(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	img = db.Column(db.String(200))
	tahun = db.Column(db.Integer())
	merk = db.Column(db.String(200))
	jenis = db.Column(db.String(200))
	tipe = db.Column(db.String(200))
	warna = db.Column(db.String(200))
	nopol = db.Column(db.String(200))
	samsat = db.Column(db.DateTime())
	asli = db.Column(db.String(200))
	beli = db.Column(db.BigInteger())
	biaya = db.Column(db.BigInteger())
	harga = db.Column(db.BigInteger())


class Invoice(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	nama = db.Column(db.String(200))
	alamat = db.Column(db.String(200))
	telp = db.Column(db.String(200))
	hp = db.Column(db.String(200))
	rangka = db.Column(db.String(200))
	mesin = db.Column(db.String(200))
	bpkb = db.Column(db.String(200))
	harga_jadi = db.Column(db.BigInteger())
	uang_muka = db.Column(db.BigInteger())
	sisa_1 = db.Column(db.BigInteger())
	susulan_1 = db.Column(db.DateTime())
	sisa_2 = db.Column(db.BigInteger())
	susulan_2 = db.Column(db.DateTime())
	sisa_3 = db.Column(db.BigInteger())



########################################################### Auth ###############################################
@app.route("/")
def Index():
	return redirect(url_for("AdminLogin"))

@app.route("/admin/register",methods=["GET","POST"])
def AdminRegister():
	form = AdminRegisterForm()
	if form.validate_on_submit():
		check = User.query.filter_by(email=form.email.data).all()
		if len(check) > 0 :
			flash("email sudah terdaftar","danger")
		else :
			hass = generate_password_hash(form.password.data,method="sha256")
			admin = User(username=form.username.data,email=form.email.data,password=hass,role="admin")
			db.session.add(admin)
			db.session.commit()
			return redirect(url_for("AdminDashboard"))
	return render_template("admin/auth/admin_register.html",form=form)			 		


@app.route("/admin/login",methods=["GET","POST"])
def AdminLogin():
	form = AdminLoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			if check_password_hash(user.password,form.password.data):
				login_user(user)
				return redirect(url_for("AdminDashboard"))
		flash("Invalid login","danger")
	return render_template("admin/auth/admin_login.html",form=form)			



################################################## Dashboard ###########################################
@app.route("/dashboard/admin",methods=["GET","POST"])
@login_required
def AdminDashboard():
	return render_template("admin/dashboard/dashboard.html")






################################################### Inventory ##########################################
@app.route("/dashboard/admin/inventory",methods=["GET","POST"])
@login_required
def AllInventory():
	inventorys = Inventory.query.all()
	form = AddInventoryForm()
	if form.validate_on_submit():
		inventory = Inventory(
			tahun=form.tahun.data,merk=form.merk.data,jenis=form.jenis.data,tipe=form.tipe.data,warna=form.warna.data,
			nopol=form.nopol.data,samsat=form.samsat.data,asli=form.asli.data,beli=form.beli.data,
			biaya=form.biaya.data,harga=form.harga.data)
		db.session.add(inventory)
		db.session.commit()
		flash("data berhasil di tambah","success")
		return redirect(url_for("AllInventory"))
	return render_template("admin/inventory/all.html",form=form,inventorys=inventorys) 	


@app.route("/dashboard/admin/inventory/<id>",methods=["GET","POST"])
@login_required
def InventoryId(id):
	inventory = Inventory.query.filter_by(id=id).first()
	form = AddInventoryForm()
	form.tahun.data = inventory.tahun
	form.merk.data = inventory.merk
	form.jenis.data = inventory.jenis
	form.tipe.data = inventory.tipe
	form.warna.data = inventory.warna
	form.nopol.data = inventory.nopol
	form.samsat.data = inventory.samsat
	form.asli.data = inventory.asli
	form.beli.data = inventory.beli
	form.biaya.data = inventory.biaya
	form.harga.data = inventory.harga
	if form.validate_on_submit():
		date = datetime.strptime(request.form["samsat"], '%m/%d/%Y').strftime('%Y-%m-%d')
		inventory.tahun = request.form["tahun"]
		inventory.merk = request.form["merk"]
		inventory.jenis = request.form["jenis"]
		inventory.tipe = request.form["tipe"]
		inventory.warna = request.form["warna"]
		inventory.nopol = request.form["nopol"]
		inventory.samsat = date
		inventory.asli = request.form["asli"]
		inventory.beli = request.form["beli"]
		inventory.biaya = request.form["biaya"]
		inventory.harga = request.form["harga"]
		db.session.commit()
		flash("data berhasil di update","success")
		return redirect(url_for("AllInventory"))
	return render_template("admin/inventory/id.html",inventory=inventory,form=form)


@app.route("/dashboard/admin/inventory/<id>/delete",methods=["GET","POST"])
@login_required
def DeleteInventory(id):
	inventory = Inventory.query.filter_by(id=id).first_or_404()
	db.session.delete(inventory)
	db.session.commit()
	flash("data berhasil di hapus","success")
	return redirect(url_for("AllInventory"))
















if __name__ == "__main__":
	app.run()

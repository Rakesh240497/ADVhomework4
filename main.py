from audioop import add
from logging import PlaceHolder
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, session, redirect,url_for
from flask_wtf import FlaskForm
from wtforms import (StringField,SubmitField,PasswordField, validators,TextAreaField)
from wtforms.validators import (DataRequired,EqualTo)

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir, 'data.sqlite') 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY'] = 'newsecrectkey'

db=SQLAlchemy (app)

class AddCompmany(FlaskForm):
    companyName = StringField(validators=[DataRequired()],render_kw={"placeholder":"Enter Company Name"})
    emaiId = StringField(validators=[DataRequired()],render_kw={"placeholder":"Enter Email Id"})
    phoneNumber = StringField(validators=[DataRequired()],render_kw={"placeholder":"Enter Phone Number"})
    address = TextAreaField(validators=[DataRequired()],render_kw={"placeholder":"Enter Company Name"})
    submit = SubmitField('Add Company')

class DeleteCompany(FlaskForm):
    deleteCompanyPhone = StringField(validators=[DataRequired()], render_kw={"placeholder":"Enter Phone Number of the Company" })
    submit = SubmitField('Delete')

class UpdateCompany(FlaskForm):
    ucompanyName = StringField(validators=[DataRequired()], render_kw={"placeholder": "Enter Name of the company you want to update"})
    companyName = StringField(validators=[DataRequired()], render_kw={"placeholder":"Enter Company Name"})
    emaiId = StringField(validators=[DataRequired()],render_kw={"placeholder":"Enter Email Id"})
    phoneNumber = StringField(validators=[DataRequired()],render_kw={"placeholder":"Enter Phone Number"})
    address = TextAreaField(validators=[DataRequired()],render_kw={"placeholder":"Enter Company Name"})
    submit = SubmitField('Update')
    

class Database(db.Model):
    tablename = 'companies'
    id = db.Column (db.Integer, primary_key = True)
    companyName = db.Column (db.Text)
    emaiId = db.Column (db.Text)
    phoneNumber = db.Column (db.Text)
    address = db.Column (db.Text)

    def __init__(self,companyName,emailId,phoneNumber,address):
        self.companyName=companyName
        self.emaiId=emailId
        self.phoneNumber=phoneNumber
        self.address=address 

@app.route('/add', methods=['GET','POST'])
def add():
    company = AddCompmany()
    if company.validate_on_submit():
        session['companyName'] = company.companyName.data
        session['emaiId'] = company.emaiId.data
        session['phoneNumber'] = company.phoneNumber.data
        session['address'] = company.address.data

        record = Database(companyName=company.companyName.data,emailId=company.emaiId.data,phoneNumber=company.phoneNumber.data,address=company.address.data)

        try:
            db.session.add(record)
            db.session.commit()
            records = Database.query.all()
            return render_template('display.html', form=records)
        except:
            return 'error occured while adding'
    return render_template('add.html', form=company)

@app.route('/', methods=['GET','POST'])
def display():
    records = Database.query.all()
    return render_template('display.html',form=records)

@app.route('/delete', methods=['GET','POST'])
def delete():
    record = DeleteCompany()
    if record.validate_on_submit():
        temp = Database.query.filter_by(phoneNumber=record.deleteCompanyPhone.data).first()
        try:
            db.session.delete(temp)
            db.session.commit()
            records = Database.query.all()
            return render_template('display.html',form=records)
        except:
            return 'error while deleting'
    return render_template('delete.html',form=record)
@app.route('/update',methods=['GET','POST'])
def update():
    record = UpdateCompany()
    if record.validate_on_submit():
        temp = Database.query.filter_by(companyName=record.ucompanyName.data).first()
        temp.companyName = record.companyName.data
        temp.emaiId  = record.emaiId.data
        temp.phoneNumber = record.phoneNumber.data
        temp.address = record.address.data
        try:
            db.session.add(temp)
            db.session.commit()
            records = Database.query.all()
            return render_template('display.html',form=records)
        except:
            return 'error occured while updating'
    return render_template('update.html',form=record)


if __name__ == '__main__':
    app.run(debug=True)
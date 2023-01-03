from flask import Flask, render_template, redirect, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, EmailField, SubmitField, RadioField, PasswordField
from wtforms.validators import Optional, DataRequired

class InfoPage(FlaskForm):
    email = EmailField(validators=[Optional()])
    check_email = BooleanField('Email me with news and Offers', validators=[Optional()])
    state = StringField(validators=[DataRequired()])
    first_name = StringField(validators=[Optional()])
    last_name = StringField(validators=[DataRequired()])
    address = StringField(validators=[DataRequired()])
    apartment = StringField(validators=[Optional()])
    postal_code = StringField(validators=[DataRequired()])
    city = StringField(validators=[DataRequired()])
    save_info = BooleanField(label='Save this information for next time', validators=[Optional()])
    submit = SubmitField('Continue to shipping')

class ShipPage(FlaskForm):
    submit = SubmitField('Continue to Payment')
    select_logistics = RadioField('Logistic options',choices=[('GIG Logistics', 'GIG Logistic'),('Agorfure Parcel', 'Agofure Parcel')], validators=[DataRequired()])
    

class PaymentPage(FlaskForm):
    card_number = StringField('card number', validators=[DataRequired()])
    name_of_card = StringField('Name of card', validators=[DataRequired()])
    expiring_date = StringField('Expiring Date', validators=[DataRequired()])
    security_code = PasswordField('security code', validators=[DataRequired()])
    submit = SubmitField('Paynow')
app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'

@app.route('/agricfresh/info', methods=['GET', 'POST'])
def info():
    form = InfoPage()
    if request.method == 'POST':
        if form.validate_on_submit():
            data = form.data
            user_data = list(data.keys())
            return redirect(url_for(email=data[user_data[0]], check_email=data[user_data[1]], state=data[user_data[2]], first_name=data[user_data[3]], last_name=data[user_data[4]], address= data[user_data[5]], apartment=data[user_data[6]], postal_code=data[user_data[7]], city=data[user_data[8]], save_info=data[user_data[9]] ,endpoint='shipping'), code=307,)
    elif request.method == 'GET':
        return render_template('info.html', form=form)


@app.route('/agricfresh/shipping', methods=['POST'])
def shipping():
    form = ShipPage()
    email = request.args.get('email')
    address = request.args.get('address')
    city = request.args.get('city')
    state = request.args.get('state')
    if form.validate_on_submit():
        data = form.data
        logistic_data = data['select_logistics']
        parameter ={
            'endpoint':'payment',
            'logistic':logistic_data,
            'email':email,
            'address':address,
            'city':city,
            'state':state
        }
        return redirect(url_for(**parameter), code=307)
    return render_template('ship.html', form=form, email=email, address=address, city=city, state=state)

@app.route('/agricfresh/payment', methods=['POST'])
def payment():
    form = PaymentPage()
    email = request.args.get('email')
    address = request.args.get('address')
    city = request.args.get('city')
    state = request.args.get('state')
    logistic = request.args.get('logistic')
    print(logistic)
    
    return render_template('pay.html', form=form, email=email, address=address, city=city, state=state, logistic=logistic)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
from os import abort

from flask import Flask, render_template, request, redirect
from models import db, FundModel

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')

    if request.method == 'POST':
        fund_id = request.form['fund_id']
        name = request.form['name']
        source = request.form['source']
        effective_date = request.form['effective_date']
        fund_type = request.form['fund_type']
        fund = FundModel(fund_id=fund_id, name=name, source=source, effective_date=effective_date,
                         fund_type=fund_type)
        db.session.add(fund)
        db.session.commit()
        return redirect('/')


@app.route('/')
def RetrieveList():
    funds = FundModel.query.all()
    return render_template('datalist.html', funds=funds)


@app.errorhandler(500)
def resource_not_found(e):
    return render_template('duplicateError.html')


@app.errorhandler(400)
def resource_not_found(e):
    return render_template('duplicateError.html')


@app.route('/<int:id>')
def RetrieveFunds(id):
    fund = FundModel.query.filter_by(fund_id=id).first()
    if fund:
        return render_template('data.html', fund=fund)
    return f"Fund with id = {id} Does not exist"


@app.route('/<int:id>/edit', methods=['GET', 'POST'])
def update(id):
    fund = FundModel.query.filter_by(fund_id=id).first()
    if request.method == 'POST':
        if fund:
            db.session.delete(fund)
            db.session.commit()
            fund_id = request.form.get('fund_id')
            name = request.form.get('name')
            source = request.form.get('source')
            if source is None:
                source = fund.source
            effective_date = request.form.get('effective_date')
            fund_type = request.form.get('fund_type')
            fund = FundModel(fund_id=fund_id, name=name, source=source, effective_date=effective_date,
                             fund_type=fund_type)
            print(fund)
            db.session.add(fund)
            db.session.commit()
            return redirect(f'/')

        return f"Fund with id = {id} Does not exist"

    return render_template('edit.html', fund=fund)


@app.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    fund = FundModel.query.filter_by(fund_id=id).first()
    if request.method == 'POST':
        if fund:
            db.session.delete(fund)
            db.session.commit()
            return redirect('/')
        abort(404)

    return render_template('delete.html')


app.run(host='localhost', port=5000)

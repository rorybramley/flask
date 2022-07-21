from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os
from flask_marshmallow import Marshmallow

app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(base_dir, 'kubrick.db')

db = SQLAlchemy(app)
ma = Marshmallow(app)

@app.route('/')
def root():
	return "Works on contingency? No, money down!"


@app.route('/consultant', methods = ['GET'])
def consultant():
	# grab cohort from the query string /consultant?cohort=DE17
	chrt = request.args.get('cohort')
	cohort_details = Cohort.query.filter_by(cohortname = chrt).first()
	result = cohort_schema.dump(cohort_details)
	return jsonify(result), 200

@app.route('/client')
def client():
	clt = request.args.get('client_industry')
	clientdetails = Client.query.filter_by(industry = clt).all()
	clt_result = client_schema.dump(clientdetails)
	return jsonify(clt_result), 200

# table in SQLite for client
# BP, Shell, HSBC,
# columns: id, name, industry, ehadoffice address
# build flask endpoint which return all clients by industry (many = True), query.all


class Cohort(db.Model):
	__tablename__ = 'cohort'
	id = Column(Integer, primary_key = True)
	cohortname = Column(String, unique = True)
	startdate = Column(String)
	specialism = Column(String)

class Client(db.Model):
	__tablename__ = 'client'
	id = Column(Integer, primary_key = True)
	name = Column(String, unique = True)
	industry = Column(String)
	headoffice = Column(String)



class ClientSchema(ma.Schema):
	class Meta():
		fields = ('id','name','industry','headoffice')


client_schema = ClientSchema(many = True)


class CohortSchema(ma.Schema):
	class Meta():
		fields = ('id', 'cohortname', 'startdate', 'specialism')

cohort_schema = CohortSchema()


if __name__ == '__main__':
	app.run()

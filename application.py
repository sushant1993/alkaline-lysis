from flask import Flask, render_template,request
import csv
from sklearn import linear_model
from scipy.optimize import curve_fit
import scipy
app = Flask(__name__)

def compute_coeffs():
	csv_file = open('dop_c2.csv','r')
	dim1 = []
	dim2 = []
	lines = csv_file.readlines()
	for line in lines:
		row = line.strip('\r\n').split(',')
		row = map(float,row)
		dim2.append(row[-1])
		row.pop(-1)
		dim1.append(row)
	clf = linear_model.Ridge(1)
	clf.fit(dim1,dim2)
	coeffs = clf.coef_
	return coeffs

def compute_yield(coeffs, inputs):
	plasmid_yield = 0
	for i in range(len(coeffs)):
		plasmid_yield += coeffs[i]*inputs[i]
	return plasmid_yield

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit',methods=['POST'])
def submit():
	if(request.method == "POST"):
		#return request.form.get('buff1',None)+" "+request.form.get('buff2',None)+" "+request.form.get('buff3',None)+" "+request.form.get('vte',None)+" "+request.form.get('voc',None)
		voc = request.form.get('voc',None)
		buff1 = request.form.get('buff1',None)
		buff2 = request.form.get('buff2',None)
		buff3 = request.form.get('buff3',None)
		vte = request.form.get('vte',None)
		input_data = [float(voc),float(buff1),float(buff2),float(buff3),float(vte)]
		print "***************************************"
		print "Input data is: "+str(input_data)
		print "***************************************"
		coeff = compute_coeffs().tolist()
		print "Coefficients: "+str(coeff)
		print "***************************************"
		plasmid_yield =  compute_yield(coeff,input_data)
		return "The predicted yield is : "+str(abs(plasmid_yield))
	else:
		return "Fail"

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask,redirect, url_for, request
from flask import Markup
from flask import Flask
from flask import render_template
app = Flask(__name__)
import parse

@app.route("/prism",methods = [ 'GET'])
def searchF():

	decisions = []

	"""
	if request.method == 'GET':
    		decisions = request.args.getlist('d')
		#print "Decisions received ",decisions
	#return str(decisions)
	#decisions = [1982,27,27,1982,97,27,74,48,135,3 ,110,3,1 ,9,12004]


	"""
	
	# testing correctly

	#b_rp, s_rp, b_ip,s_ip, tb, tbb, ts, tsb, bcinc, bbinc, scdec, sbdec,  kb, ks, offset
	
	if request.method == 'GET':
		decisions.append( int(request.args.get('brp')))
		decisions.append( int(request.args.get('srp')))
		decisions.append( int(request.args.get('bip')))
		decisions.append( int(request.args.get('sip')))
		decisions.append( int(request.args.get('tb')))
		decisions.append( int(request.args.get('tbb')))
		decisions.append( int(request.args.get('ts')))
		decisions.append( int(request.args.get('tsb')))
		decisions.append( int(request.args.get('bcinc')))
		decisions.append( int(request.args.get('bbinc')))
		decisions.append( int(request.args.get('scdec')))
		decisions.append( int(request.args.get('sbdec')))
		decisions.append( int(request.args.get('kb')))
		decisions.append( int(request.args.get('ks')))
		decisions.append( int(request.args.get('offset')))
	
	print decisions
        prism_path = "/home/ubuntu/prism-4.3.1-linux64/bin/prism"
	if decisions != []:
        	filename = parse.call_prism(prism_path,decisions)
	        evaluated_results =parse.Parse(filename).get_output()
		print filename,evaluated_results
	else: return str((0,0,0))
        if evaluated_results:
                return str(evaluated_results)
        else:
                return str((0,0,0))




if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5001)

from flask import Flask,redirect, url_for, request
from flask import Markup
from flask import Flask
from flask import render_template
app = Flask(__name__)
import parse

@app.route("/prism",methods = [ 'GET'])
def searchF():

	decisions = []
	if request.method == 'GET':
    		decisions = request.args.getlist('d')
		#print "Decisions received ",decisions
	#return str(decisions)
	#decisions = [1982,27,27,1982,97,27,74,48,135,3 ,110,3,1 ,9,12004]
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

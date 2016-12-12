from flask import Flask, render_template as render_template_raw, request
import os, json, time, pickle, base64
app = Flask(__name__)

def encodeObj(obj):
	d = pickle.dumps(obj)
	d = base64.b64encode(d)
	return d

def decodeObj(obj):
	d = base64.b64decode(obj)
	d = pickle.loads(d)
	return d

def safeStr(s):
	return str(s)

def render_template(template, *args, **kwargs):
	content = render_template_raw(template, *args, **kwargs)
	kwargs["RENDERBODYCONTENT"] = content
	return render_template_raw("resources/template.html", *args, **kwargs)

def get_projects():
	return os.listdir("projects/")

def create_project(name, desc):
	try:
		name = safeStr(name)
		desc = safeStr(desc)
		os.mkdir("projects/%s" % (name))
		projinfo = {"name":name, "desc":desc, "time":time.time(), "ip":request.remote_addr}
		data = encodeObj(projinfo)
		open("projects/%s/info.b64" % (name), "w+").write(data)
		return "SUCCESS"
	except Exception as e:
		return safeStr(e)

#Back end interface
@app.route("/get/projects", methods=["GET", "POST"])
def PAGE_get_projects():
	return json.dumps(get_projects())

@app.route("/action/create/project", methods=["GET", "POST"])
def PAGE_action_create_project():
	name = request.form["name"]
	desc = request.form["desc"]
	return create_project(name, desc)

#Front end (UI) interface
@app.route("/")
def PAGE_index():
	return render_template("index.html", hostname=HOST, port=PORT)

@app.route("/view/<proj>")
def PAGE_view(proj):
	return render_template("editor.html", hostname=HOST, port=PORT, file=proj)

HOST = "0.0.0.0"
PORT = 5000
app.run(HOST, port=PORT, debug=True)
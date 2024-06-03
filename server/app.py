from flask import Flask, render_template, jsonify
app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("map.html")

@app.route("/base-select-info")
def base_select_info():
    return jsonify([{"optgroupLabel": "someLabel", "optionValue": "someValue", "optionInnerHTML": "someInnerHTML"}, {"optgroupLabel": "someLabel2", "optionValue": "someValue2", "optionInnerHTML": "someInnerHTML2"}])

@app.route("/point-select-info")
def point_select_info():
    return jsonify([{"optgroupLabel": "someLabel", "optionValue": "someValue", "optionInnerHTML": "someInnerHTML"}, {"optgroupLabel": "someLabel2", "optionValue": "someValue2", "optionInnerHTML": "someInnerHTML2"}])

@app.route("/arrow-select-info")
def arrow_select_info():
    return jsonify([{"optgroupLabel": "someLabel", "optionValue": "someValue", "optionInnerHTML": "someInnerHTML"}, {"optgroupLabel": "someLabel2", "optionValue": "someValue2", "optionInnerHTML": "someInnerHTML2"}])


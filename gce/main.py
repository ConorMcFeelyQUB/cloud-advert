from flask import Flask, render_template, request
import mysql.connector as mysql
import os
app = Flask(__name__)

db = mysql.connect(
    host = "35.187.184.139",
    user = "root",
    passwd = "QUBccProject"
)

database_name = "cloudcomputingadverts.advert"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        error = False

        advert_content = request.form["advertContent"]
        advert_URL = request.form["advertURL"]
        advert_keywords = request.form["advertKeywords"].split(" ")[0]
        
        print(advert_keywords)
        print(len(advert_keywords))
        if(advert_content == None or len(advert_content) < 1 or advert_keywords == None or len(advert_keywords) < 1):
            error = True
            return render_template("advertResult.html", error = error, content = "", keywords = "", URL = "")

        #if url was provided keep it as is else just put in a # to make links nice in search section
        advert_URL = advert_URL if advert_URL else "#"

        cursor = db.cursor()
        sql = "INSERT INTO "+ database_name + " (keyword, advert, url) VALUES (%s, %s, %s)"
        values = (advert_keywords, advert_content, advert_URL)
        cursor.execute(sql, values)
        db.commit()
        
        return render_template("advertResult.html", error = error, content = advert_content, keywords = advert_keywords, URL = advert_URL)

    return render_template("index.html")


@app.route('/test')
def test():
    cursor = db.cursor()
    sql = "SELECT * FROM " + database_name +";"
    cursor.execute(sql)
    adverts = cursor.fetchall()

    return str(len(adverts))

@app.route('/new')
def new():
    osvar = os.environ.get("autostart")
    if osvar == None:
        return "Was none"
    else:
        return str(osvar)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)

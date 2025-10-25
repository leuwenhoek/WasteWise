from flask import Flask, render_template

app = Flask(__name__)

# Route for the Home page (existing)
@app.route("/")
def home():
    return render_template("home.html")

# Route for the Marketplace page
@app.route("/marketplace")
def marketplace():
    return render_template("marketplace.html")

# Route for the Complaint page
@app.route("/complain")
def complain():
    return render_template("complain.html")

# New route for the Educational Library page
@app.route("/library")
def library():
    # Renders the new library.html page
    return render_template("library.html")

if __name__ == "__main__":
    app.run(debug=True)
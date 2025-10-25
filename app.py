from flask import Flask, render_template

app = Flask(__name__)

# Route for the Home page (existing)
@app.route("/")
def home():
    return render_template("home.html")

# Route for the Marketplace page (from previous request)
@app.route("/marketplace")
def marketplace():
    return render_template("marketplace.html")

# New route for the Complaint page
@app.route("/complain")
def complain():
    # Renders the new complain.html page
    return render_template("complain.html")

if __name__ == "__main__":
    app.run(debug=True)
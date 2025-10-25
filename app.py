from flask import Flask, render_template

app = Flask(__name__)

# Route for the Home page (existing)
@app.route("/")
def home():
    return render_template("home.html")

# New route for the Marketplace page
@app.route("/marketplace")
def marketplace():
    # Renders the new marketplace.html page
    return render_template("marketplace.html")

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///translations.db'
db = SQLAlchemy(app)  # Initialize SQLAlchemy with the app

# Define the Quiz model
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    questions = db.relationship('Question', backref='quiz', lazy=True)

# Define the Question model
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_text = db.Column(db.String(255), nullable=False)
    options = db.Column(db.PickleType, nullable=False)
    answer = db.Column(db.String(100), nullable=False)

# Define the Translation model
class Translation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expression = db.Column(db.String(255), nullable=False, unique=True)
    english = db.Column(db.String(255))
    french = db.Column(db.String(255))
    spanish = db.Column(db.String(255))
    german = db.Column(db.String(255))
    italian = db.Column(db.String(255))
    chinese = db.Column(db.String(255))
    japanese = db.Column(db.String(255))
    arabic = db.Column(db.String(255))

# Create the tables in the database
with app.app_context():
    db.create_all()

# Populate the data if the table is empty
def populate_translations():
    sample_data = [
        {
            "expression": "hello",
            "english": "hello",
            "french": "bonjour",
            "spanish": "hola",
            "german": "hallo",
            "italian": "ciao",
            "chinese": "你好",
            "japanese": "こんにちは",
            "arabic": "مرحبا"
        },
        {
            "expression": "goodbye",
            "english": "goodbye",
            "french": "au revoir",
            "spanish": "adiós",
            "german": "auf wiedersehen",
            "italian": "addio",
            "chinese": "再见",
            "japanese": "さようなら",
            "arabic": "وداعا"
        }
    ]
    
    for data in sample_data:
        translation = Translation(
            expression=data["expression"],
            english=data["english"],
            french=data["french"],
            spanish=data["spanish"],
            german=data["german"],
            italian=data["italian"],
            chinese=data["chinese"],
            japanese=data["japanese"],
            arabic=data["arabic"]
        )
        db.session.add(translation)
    db.session.commit()
    print("Sample translations added to the database!")

# Check if the table is empty, then populate
with app.app_context():
    if Translation.query.count() == 0:
        populate_translations()

# Define the /translations endpoint
@app.route('/translations', methods=['GET'])
def get_all_translations():
    translations = Translation.query.all()
    return jsonify([{
        "expression": t.expression,
        "english": t.english,
        "french": t.french,
        "spanish": t.spanish,
        "german": t.german,
        "italian": t.italian,
        "chinese": t.chinese,
        "japanese": t.japanese,
        "arabic": t.arabic
    } for t in translations])

@app.route('/translation/<expression>', methods=['GET'])
def get_translation(expression):
    translation = Translation.query.filter_by(expression=expression).first()
    if translation:
        return jsonify({
            "expression": translation.expression,
            "english": translation.english,
            "french": translation.french,
            "spanish": translation.spanish,
            "german": translation.german,
            "italian": translation.italian,
            "chinese": translation.chinese,
            "japanese": translation.japanese,
            "arabic": translation.arabic
        })
    return jsonify({"error": "Expression not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request
import re

def grade_essay(essay):
    # Rubric-based grading using regex pattern matching
    purpose_focus_score = 1 if re.search(r'(?i)(thesis|main idea|focus)', essay) else 0
    evidence_elaboration_score = 1 if re.search(r'(?i)(for example|evidence|quote|supports)', essay) else 0
    conventions_score = 0 if re.search(r'[^a-zA-Z0-9.,;!?\s]', essay) else 1  # Basic check
    
    return {
        "Purpose, Focus, and Organization": purpose_focus_score,
        "Evidence and Elaboration": evidence_elaboration_score,
        "Conventions": conventions_score,
        "Total Score": purpose_focus_score + evidence_elaboration_score + conventions_score
    }

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/grade', methods=['POST'])
def grade():
    essay = request.form['essay']
    result = grade_essay(essay)
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)

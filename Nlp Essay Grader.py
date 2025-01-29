from flask import Flask, render_template, request
import re

def grade_essay(essay, prompt, passage):
    rubric = {
        "Purpose, Focus, and Organization": 0,
        "Evidence and Elaboration": 0,
        "Conventions": 0
    }
    
    # Basic grading criteria based on established rubric
    if len(essay) > 150 and essay.lower().count(prompt.lower().split()[0]) > 1:
        rubric["Purpose, Focus, and Organization"] = 4
    elif len(essay) > 100:
        rubric["Purpose, Focus, and Organization"] = 3
    else:
        rubric["Purpose, Focus, and Organization"] = 1
    
    if re.search(r'".*?"', essay) or any(word in essay.lower() for word in ["according", "states", "paragraph"]):
        rubric["Evidence and Elaboration"] = 4
    elif len(essay.split()) > 100:
        rubric["Evidence and Elaboration"] = 3
    else:
        rubric["Evidence and Elaboration"] = 1
    
    if re.search(r'[.?!]', essay) and len(re.findall(r'[,;]', essay)) > 2:
        rubric["Conventions"] = 2
    else:
        rubric["Conventions"] = 0
    
    total_score = sum(rubric.values())
    return rubric, total_score

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        essay = request.form['essay']
        prompt = request.form['prompt']
        passage = request.form['passage']
        rubric, total_score = grade_essay(essay, prompt, passage)
        return render_template('result.html', rubric=rubric, total_score=total_score, essay=essay, prompt=prompt, passage=passage)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

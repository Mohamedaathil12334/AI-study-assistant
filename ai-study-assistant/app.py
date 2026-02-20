import requests
import PyPDF2
from flask import Flask, render_template, request

app = Flask(__name__)


def extract_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content
    return text


def ask_ai(context, question, mode):

    if mode == "2":
        prompt = f"""
        Generate a clear 2-mark university exam answer.
        Question: {question}
        Context: {context}
        """
    elif mode == "16":
        prompt = f"""
        Generate a structured 16-mark university exam answer with headings.
        Question: {question}
        Context: {context}
        """
    else:
        prompt = f"""
        Explain in simple engineering student language.
        Question: {question}
        Context: {context}
        """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]


@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""

    if request.method == "POST":
        pdf = request.files["pdf"]
        question = request.form["question"]
        mode = request.form["mode"]

        if pdf and question:
            text = extract_text(pdf)
            answer = ask_ai(text[:8000], question, mode)

    return render_template("index.html", answer=answer)


if __name__ == "__main__":
    app.run(debug=True)

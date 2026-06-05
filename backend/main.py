from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(BASE_DIR, "..", "database.xlsx")


@app.route("/")
def home():
    return jsonify({
        "message": "AI Title Similarity Detection System"
    })


@app.route("/check", methods=["POST"])
def check_title():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No JSON data received"
            }), 400

        title = data.get("title", "").strip()

        print("Received Title:", title)

        if not title:
            return jsonify({
                "error": "Title is required"
            }), 400

        if not os.path.exists(EXCEL_PATH):
            return jsonify({
                "error": f"Database file not found: {EXCEL_PATH}"
            }), 500

        df = pd.read_excel(EXCEL_PATH)

        if "Project Title" not in df.columns:
            return jsonify({
                "error": "Column 'Project Title' not found in database.xlsx"
            }), 500

        existing_titles = df["Project Title"].dropna().astype(str).tolist()

        if len(existing_titles) == 0:
            return jsonify({
                "error": "No titles found in database"
            }), 500

        all_titles = existing_titles + [title]

        vectorizer = TfidfVectorizer()

        vectors = vectorizer.fit_transform(all_titles)

        similarity_scores = cosine_similarity(
            vectors[-1],
            vectors[:-1]
        )[0]

        best_index = similarity_scores.argmax()

        similarity = float(
            similarity_scores[best_index] * 100
        )

        matched_title = existing_titles[best_index]

        if similarity >= 70:
            status = "Rejected"

        elif similarity >= 40:
            status = "Needs Review"

        else:
            status = "Accepted"

            new_row = pd.DataFrame({
                "Project Title": [title]
            })

            df = pd.concat(
                [df, new_row],
                ignore_index=True
            )

            df.to_excel(
                EXCEL_PATH,
                index=False
            )

        return jsonify({

            "entered_title": title,

            "matched_title": matched_title,

            "similarity": round(
                similarity,
                2
            ),

            "status": status

        })

    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
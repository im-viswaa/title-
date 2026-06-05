from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
import traceback

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(BASE_DIR, "..", "database.xlsx")


@app.route("/")
def home():
    return jsonify({
        "message": "AI-Powered Project Title Validation System"
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

        if not title:
            return jsonify({
                "error": "Title is required"
            }), 400

        if not os.path.exists(EXCEL_PATH):
            return jsonify({
                "error": f"Database file not found: {EXCEL_PATH}"
            }), 500

        df = pd.read_excel(
            EXCEL_PATH,
            engine="openpyxl"
        )

        if "Project Title" not in df.columns:
            return jsonify({
                "error": "Column 'Project Title' not found in database.xlsx"
            }), 500

        existing_titles = (
            df["Project Title"]
            .dropna()
            .astype(str)
            .tolist()
        )

        if len(existing_titles) == 0:
            return jsonify({
                "error": "No titles found in database"
            }), 500

        all_titles = existing_titles + [title]

        # TF-IDF Similarity
        vectorizer = TfidfVectorizer()

        vectors = vectorizer.fit_transform(all_titles)

        similarity_scores = cosine_similarity(
            vectors[-1],
            vectors[:-1]
        )[0]

        results = []

        for existing_title, score in zip(
            existing_titles,
            similarity_scores
        ):
            results.append({
                "title": existing_title,
                "similarity": round(float(score * 100), 2)
            })

        results.sort(
            key=lambda x: x["similarity"],
            reverse=True
        )

        top_matches = results[:5]

        max_similarity = (
            top_matches[0]["similarity"]
            if top_matches else 0
        )

        matched_title = (
            top_matches[0]["title"]
            if top_matches else "No Match"
        )

        novelty_score = round(
            100 - max_similarity,
            2
        )

        if max_similarity >= 70:
            status = "Rejected"
            risk_level = "High"

        elif max_similarity >= 40:
            status = "Needs Review"
            risk_level = "Medium"

        else:
            status = "Accepted"
            risk_level = "Low"

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

        title_lower = title.lower()

        if any(
            keyword in title_lower
            for keyword in [
                "ai",
                "machine learning",
                "deep learning",
                "neural network"
            ]
        ):
            domain = "Artificial Intelligence"

        elif any(
            keyword in title_lower
            for keyword in [
                "web",
                "website",
                "portal"
            ]
        ):
            domain = "Web Development"

        elif any(
            keyword in title_lower
            for keyword in [
                "iot",
                "sensor",
                "arduino"
            ]
        ):
            domain = "Internet of Things"

        elif any(
            keyword in title_lower
            for keyword in [
                "cloud",
                "aws",
                "azure"
            ]
        ):
            domain = "Cloud Computing"

        elif any(
            keyword in title_lower
            for keyword in [
                "security",
                "cyber",
                "encryption"
            ]
        ):
            domain = "Cyber Security"

        else:
            domain = "General"

        suggestions = [
            f"Smart {title}",
            f"Advanced {title}",
            f"AI Powered {title}"
        ]

        return jsonify({

            "entered_title": title,
            "matched_title": matched_title,
            "similarity": round(max_similarity, 2),
            "novelty_score": novelty_score,
            "risk_level": risk_level,
            "domain": domain,
            "status": status,
            "top_matches": top_matches,
            "suggestions": suggestions

        })

    except Exception as e:

        traceback.print_exc()

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            10000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
    
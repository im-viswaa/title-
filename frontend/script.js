async function checkTitle() {

    const title = document.getElementById("title").value;

    if (title.trim() === "") {
        alert("Please enter a project title");
        return;
    }

    try {

        const response = await fetch(
            "https://title-gjvj.onrender.com/check",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    title: title
                })
            }
        );

        const data = await response.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        // Update Similarity Circle
        document.getElementById("scoreValue").innerText =
            data.similarity + "%";

        document.getElementById("progressBar").style.width =
            data.similarity + "%";

        let statusClass = "";

        if (data.status === "Rejected") {
            statusClass = "rejected";
        }
        else if (data.status === "Needs Review") {
            statusClass = "review";
        }
        else {
            statusClass = "accepted";
        }

        let riskClass = "";

        if (data.risk_level === "High") {
            riskClass = "rejected";
        }
        else if (data.risk_level === "Medium") {
            riskClass = "review";
        }
        else {
            riskClass = "accepted";
        }

        let topMatchesHTML = "";

        if (data.top_matches && data.top_matches.length > 0) {

            data.top_matches.forEach((item, index) => {

                topMatchesHTML += `
                    <tr>
                        <td>${index + 1}</td>
                        <td>${item.title}</td>
                        <td>${item.similarity}%</td>
                    </tr>
                `;

            });

        }
        else {

            topMatchesHTML = `
                <tr>
                    <td colspan="3">No similar titles found</td>
                </tr>
            `;

        }

        let suggestionsHTML = "";

        if (data.suggestions && data.suggestions.length > 0) {

            data.suggestions.forEach(item => {

                suggestionsHTML += `
                    <li>${item}</li>
                `;

            });

        }

        document.getElementById("result").innerHTML = `

            <div class="result-card">

                <h2>Analysis Result</h2>

                <p>
                    <strong>Entered Title:</strong><br>
                    ${data.entered_title}
                </p>

                <p>
                    <strong>Closest Match:</strong><br>
                    ${data.matched_title}
                </p>

                <p>
                    <strong>Similarity Score:</strong><br>
                    ${data.similarity}%
                </p>

                <p>
                    <strong>Novelty Score:</strong><br>
                    ${data.novelty_score}%
                </p>

                <p>
                    <strong>Domain:</strong><br>
                    <span class="domain-badge">
                        ${data.domain}
                    </span>
                </p>

                <p class="${riskClass}">
                    <strong>Risk Level:</strong>
                    ${data.risk_level}
                </p>

                <p class="${statusClass}">
                    <strong>Status:</strong>
                    ${data.status}
                </p>

            </div>

            <br>

            <div class="result-card">

                <h2>Top 5 Similar Titles</h2>

                <table>

                    <tr>
                        <th>Rank</th>
                        <th>Project Title</th>
                        <th>Similarity</th>
                    </tr>

                    ${topMatchesHTML}

                </table>

            </div>

            <br>

            <div class="result-card">

                <h2>AI Suggested Titles</h2>

                <ul>
                    ${suggestionsHTML}
                </ul>

            </div>

        `;

    }
    catch (error) {

        console.error("ERROR:", error);

        alert(
            "Backend connection failed. Please check if backend is running."
        );

    }
}
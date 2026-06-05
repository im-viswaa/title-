async function checkTitle() {

    const title = document.getElementById("title").value;

    if (title.trim() === "") {
        alert("Please enter a project title");
        return;
    }

    try {

        console.log("Sending request...");

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

        console.log("Response:", response);

        const data = await response.json();

        console.log("Data:", data);

        if (data.error) {
            alert(data.error);
            return;
        }

        if (document.getElementById("scoreValue")) {
            document.getElementById("scoreValue").innerText =
                data.similarity + "%";
        }

        if (document.getElementById("progressBar")) {
            document.getElementById("progressBar").style.width =
                data.similarity + "%";
        }

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

        document.getElementById("result").innerHTML = `
            <div class="result-card">

                <h3>Analysis Result</h3>

                <p>
                    <strong>Entered Title:</strong><br>
                    ${data.entered_title}
                </p>

                <p>
                    <strong>Closest Match:</strong><br>
                    ${data.matched_title}
                </p>

                <p>
                    <strong>Similarity:</strong><br>
                    ${data.similarity}%
                </p>

                <p class="${statusClass}">
                    <strong>Status:</strong>
                    ${data.status}
                </p>

            </div>
        `;

    } catch (error) {

        console.error("ERROR:", error);

        alert("Backend connection failed");

    }
}
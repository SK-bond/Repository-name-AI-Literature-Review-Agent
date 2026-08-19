const API_URL =
    "https://ai-literature-review-backend.onrender.com";


const topicInput =
    document.getElementById("topic");

const generateBtn =
    document.getElementById("generateBtn");

const loading =
    document.getElementById("loading");

const result =
    document.getElementById("result");

const errorBox =
    document.getElementById("error");

const reviewText =
    document.getElementById("reviewText");

const copyBtn =
    document.getElementById("copyBtn");


generateBtn.addEventListener(
    "click",
    generateReview
);


topicInput.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            generateReview();

        }

    }
);


async function generateReview() {

    const topic =
        topicInput.value.trim();


    if (!topic) {

        showError(
            "Please enter a research topic."
        );

        return;
    }


    loading.classList.remove("hidden");

    result.classList.add("hidden");

    errorBox.classList.add("hidden");

    generateBtn.disabled = true;

    generateBtn.innerText =
        "Generating...";


    try {

        const response =
            await fetch(
                `${API_URL}/review`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        topic: topic
                    })
                }
            );


        if (!response.ok) {

            throw new Error(
                `Server returned ${response.status}`
            );

        }


        const data =
            await response.json();


        reviewText.textContent =
            data.review;


        result.classList.remove(
            "hidden"
        );


        result.scrollIntoView({
            behavior: "smooth"
        });


    }

    catch (error) {

        console.error(error);

        showError(
            "Unable to generate the review. " +
            "Please try again."
        );

    }

    finally {

        loading.classList.add(
            "hidden"
        );

        generateBtn.disabled =
            false;

        generateBtn.innerText =
            "✨ Generate Review";
    }

}


function showError(message) {

    errorBox.textContent =
        message;

    errorBox.classList.remove(
        "hidden"
    );

}


copyBtn.addEventListener(
    "click",
    async function() {

        await navigator.clipboard.writeText(
            reviewText.textContent
        );

        copyBtn.innerText =
            "✓ Copied";

        setTimeout(
            () => {
                copyBtn.innerText =
                    "Copy Review";
            },
            2000
        );

    }
);
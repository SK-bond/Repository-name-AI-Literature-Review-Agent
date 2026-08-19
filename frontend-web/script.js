// =========================================================
// AI Literature Review Agent - Frontend
// =========================================================

// ---------------------------------------------------------
// Backend API
// ---------------------------------------------------------

const API_URL =
    "https://ai-literature-review-backend.onrender.com";


// ---------------------------------------------------------
// Get HTML Elements
// ---------------------------------------------------------

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


// =========================================================
// Generate Button
// =========================================================

generateBtn.addEventListener(
    "click",
    generateReview
);


// =========================================================
// Enter Key
// =========================================================

topicInput.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            generateReview();

        }

    }
);


// =========================================================
// Generate Literature Review
// =========================================================

async function generateReview() {

    const topic =
        topicInput.value.trim();


    // -----------------------------------------------------
    // Validate input
    // -----------------------------------------------------

    if (!topic) {

        showError(
            "Please enter a research topic."
        );

        return;
    }


    // -----------------------------------------------------
    // Show loading
    // -----------------------------------------------------

    loading.classList.remove(
        "hidden"
    );

    result.classList.add(
        "hidden"
    );

    errorBox.classList.add(
        "hidden"
    );

    generateBtn.disabled = true;

    generateBtn.innerText =
        "Generating...";


    try {

        // -------------------------------------------------
        // Send request to FastAPI backend
        // -------------------------------------------------

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


        // -------------------------------------------------
        // Check response
        // -------------------------------------------------

        if (!response.ok) {

            throw new Error(
                `Server returned ${response.status}`
            );

        }


        // -------------------------------------------------
        // Convert response to JSON
        // -------------------------------------------------

        const data =
            await response.json();


        // -------------------------------------------------
        // Convert Markdown to HTML
        // -------------------------------------------------

        let markdown =
            data.review;


        // -------------------------------------------------
        // Convert plain URLs into Markdown links
        // -------------------------------------------------

        markdown =
            convertUrlsToLinks(markdown);


        // -------------------------------------------------
        // Render Markdown
        // -------------------------------------------------

        const html =
            marked.parse(
                markdown,
                {
                    gfm: true,
                    breaks: true
                }
            );


        // -------------------------------------------------
        // Sanitize generated HTML
        // -------------------------------------------------

        reviewText.innerHTML =
            DOMPurify.sanitize(html);


        // -------------------------------------------------
        // Show result
        // -------------------------------------------------

        result.classList.remove(
            "hidden"
        );


        // -------------------------------------------------
        // Scroll to result
        // -------------------------------------------------

        result.scrollIntoView({
            behavior: "smooth"
        });

    }


    catch (error) {

        console.error(
            "Literature Review Error:",
            error
        );


        showError(
            "Unable to generate the review. " +
            "Please try again."
        );

    }


    finally {

        // -------------------------------------------------
        // Hide loading
        // -------------------------------------------------

        loading.classList.add(
            "hidden"
        );


        generateBtn.disabled =
            false;


        generateBtn.innerText =
            "✨ Generate Review";

    }

}


// =========================================================
// Convert Plain URLs to Clickable Markdown Links
// =========================================================

function convertUrlsToLinks(text) {

    const urlRegex =
        /(?<!["'=])(https?:\/\/[^\s<]+)/g;


    return text.replace(
        urlRegex,
        function(url) {

            // Remove punctuation from URL ending
            let cleanUrl = url;

            let punctuation = "";


            while (
                /[.,;:!?)]$/.test(cleanUrl)
            ) {

                punctuation =
                    cleanUrl.slice(-1) +
                    punctuation;

                cleanUrl =
                    cleanUrl.slice(0, -1);

            }


            return `[${cleanUrl}](${cleanUrl})${punctuation}`;

        }
    );

}


// =========================================================
// Show Error
// =========================================================

function showError(message) {

    errorBox.textContent =
        message;

    errorBox.classList.remove(
        "hidden"
    );

}


// =========================================================
// Copy Review
// =========================================================

copyBtn.addEventListener(
    "click",
    async function() {

        try {

            // Copy the visible text
            await navigator.clipboard.writeText(
                reviewText.innerText
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

        catch (error) {

            console.error(
                "Copy failed:",
                error
            );

        }

    }
);
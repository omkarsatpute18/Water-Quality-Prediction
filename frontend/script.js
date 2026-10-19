// ==========================================================
// Get HTML Elements
// ==========================================================

const predictionForm =
    document.getElementById("predictionForm");

const clearButton =
    document.getElementById("clearButton");

const loading =
    document.getElementById("loading");

const result =
    document.getElementById("result");

const errorBox =
    document.getElementById("error");

const predictionResult =
    document.getElementById("predictionResult");

const potableProbability =
    document.getElementById("potableProbability");

const notPotableProbability =
    document.getElementById("notPotableProbability");


// ==========================================================
// Form Submit
// ==========================================================

predictionForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();


        // Hide previous result/error

        result.classList.add("hidden");

        errorBox.classList.add("hidden");


        // Show loading

        loading.classList.remove("hidden");


        // ==================================================
        // Collect User Input
        // ==================================================

        const data = {

            ph: parseFloat(
                document.getElementById("ph").value
            ),

            Hardness: parseFloat(
                document.getElementById("Hardness").value
            ),

            Solids: parseFloat(
                document.getElementById("Solids").value
            ),

            Chloramines: parseFloat(
                document.getElementById("Chloramines").value
            ),

            Sulfate: parseFloat(
                document.getElementById("Sulfate").value
            ),

            Conductivity: parseFloat(
                document.getElementById("Conductivity").value
            ),

            Organic_carbon: parseFloat(
                document.getElementById("Organic_carbon").value
            ),

            Trihalomethanes: parseFloat(
                document.getElementById("Trihalomethanes").value
            ),

            Turbidity: parseFloat(
                document.getElementById("Turbidity").value
            )

        };


        try {


            // ==================================================
            // Send Request to Flask
            // ==================================================

            const response = await fetch(
                "/predict",
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body:
                        JSON.stringify(data)

                }
            );


            const responseData =
                await response.json();


            // ==================================================
            // Handle Error
            // ==================================================

            if (!response.ok) {

                throw new Error(
                    responseData.error ||
                    "Prediction failed"
                );

            }


            // ==================================================
            // Display Prediction
            // ==================================================

            predictionResult.textContent =
                responseData.prediction;


            potableProbability.textContent =
                responseData.potable_probability +
                "%";


            notPotableProbability.textContent =
                responseData.not_potable_probability +
                "%";


            // Remove previous result classes

            predictionResult.classList.remove(
                "potable",
                "not-potable"
            );


            // Add correct class

            if (
                responseData.prediction ===
                "Potable"
            ) {

                predictionResult.classList.add(
                    "potable"
                );

            } else {

                predictionResult.classList.add(
                    "not-potable"
                );

            }


            // Show result

            result.classList.remove(
                "hidden"
            );

        }


        catch (error) {

            console.error(error);


            errorBox.textContent =
                "Error: " +
                error.message;


            errorBox.classList.remove(
                "hidden"
            );

        }


        finally {

            loading.classList.add(
                "hidden"
            );

        }

    }
);


// ==========================================================
// Clear Button
// ==========================================================

clearButton.addEventListener(
    "click",
    function () {

        predictionForm.reset();

        result.classList.add(
            "hidden"
        );

        errorBox.classList.add(
            "hidden"
        );

    }
);
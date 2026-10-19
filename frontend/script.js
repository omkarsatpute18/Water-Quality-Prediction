const form = document.getElementById("predictionForm");

const clearBtn = document.getElementById("clearBtn");

const loading = document.getElementById("loading");

const result = document.getElementById("result");

const predictionText =
    document.getElementById("predictionText");

const notPotableProbability =
    document.getElementById("notPotableProbability");

const potableProbability =
    document.getElementById("potableProbability");

const resultMessage =
    document.getElementById("resultMessage");



/*
    Form Submit
*/

form.addEventListener("submit", async function(event) {

    event.preventDefault();


    // Get input values

    const data = {

        ph: Number(
            document.getElementById("ph").value
        ),

        hardness: Number(
            document.getElementById("hardness").value
        ),

        solids: Number(
            document.getElementById("solids").value
        ),

        chloramines: Number(
            document.getElementById("chloramines").value
        ),

        sulfate: Number(
            document.getElementById("sulfate").value
        ),

        conductivity: Number(
            document.getElementById("conductivity").value
        ),

        organic_carbon: Number(
            document.getElementById("organic_carbon").value
        ),

        trihalomethanes: Number(
            document.getElementById("trihalomethanes").value
        ),

        turbidity: Number(
            document.getElementById("turbidity").value
        )

    };


    // Show loading

    loading.classList.remove("hidden");

    result.classList.add("hidden");


    try {

        /*
            Send data to Python backend
        */

        const response = await fetch(
            "http://127.0.0.1:5000/predict",
            {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(data)

            }
        );


        const prediction =
            await response.json();


        if (!response.ok) {

            throw new Error(
                prediction.error ||
                "Prediction failed"
            );

        }


        /*
            Display prediction
        */

        if (prediction.prediction === 1) {

            predictionText.textContent =
                "✓ POTABLE";

            predictionText.style.color =
                "#16a34a";

            resultMessage.textContent =
                "The machine learning model predicts that this water sample is likely to be potable.";

        }

        else {

            predictionText.textContent =
                "✗ NOT POTABLE";

            predictionText.style.color =
                "#dc2626";

            resultMessage.textContent =
                "The machine learning model predicts that this water sample is likely to be not potable.";

        }


        /*
            Display probabilities
        */

        notPotableProbability.textContent =
            prediction.not_potable_probability.toFixed(2)
            + "%";


        potableProbability.textContent =
            prediction.potable_probability.toFixed(2)
            + "%";


        // Show result

        result.classList.remove("hidden");

    }


    catch (error) {

        console.error(error);

        predictionText.textContent =
            "Error";

        predictionText.style.color =
            "#dc2626";

        resultMessage.textContent =
            "Unable to connect to the prediction server. Please make sure the Python backend is running.";

        result.classList.remove("hidden");

    }


    finally {

        loading.classList.add("hidden");

    }

});



/*
    Clear Button
*/

clearBtn.addEventListener("click", function() {

    form.reset();

    result.classList.add("hidden");

});
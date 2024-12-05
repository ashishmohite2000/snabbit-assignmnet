document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("getPriceBtn").addEventListener("click", async function () {
        try {
            // Get the values from the form
            const sportName = document.getElementById("sport")?.value;
            const duration = parseInt(document.getElementById("duration")?.value, 10);
            const date = document.getElementById("date")?.value; // Date in YYYY-MM-DD format
            let time = document.getElementById("time")?.value; // Time in HH:MM format

            // Validate the inputs
            if (!sportName || !duration || !date || !time) {
                alert("Please fill in all fields.");
                return;
            }

            // Ensure the time is in HH:MM:SS format
            if (!time.includes(':')) {
                alert("Invalid time format.");
                return;
            }
            if (time.split(':').length === 2) {
                time += ":00"; // Add seconds if missing
            }

            // Prepare the URL for the API call
            const url = `http://localhost:8000/price/${sportName}?duration=${duration}&date=${date}&time=${time}`;

            // Make the GET request to the backend
            const response = await fetch(url);

            if (!response.ok) {
                throw new Error("Failed to fetch data from server.");
            }

            const data = await response.json();

            // Display the result
            const priceElement = document.getElementById("price");
            if (data.error) {
                priceElement.textContent = `Error: ${data.error}`;
            } else {
                priceElement.textContent = `Price: ₹${data.final_price}`;
            }
        } catch (error) {
            console.error("Error:", error);
            document.getElementById("price").textContent = "Error: Something went wrong.";
        }
    });
});

document.getElementById("submitBtn").addEventListener("click", async function(event) {
    event.preventDefault();

    // Count checked amenities
    const amenitiesChecked = document.querySelectorAll('input[name="amenities"]:checked');
    const amenitiesCount = amenitiesChecked.length;

    const bathroomsValue = document.getElementById("bathrooms").value;
    const property_ageValue = document.getElementById("property_age").value;
    const property_sizeValue = document.getElementById("property_size").value;
    const totalFloorValue = document.getElementById("totalFloor").value;
    const facingValue = document.getElementById("facing").value;
    const furnishingValue = document.getElementById("furnishing").value;
    const localityValue = document.getElementById("locality").value;
    const parkingValue = document.getElementById("parking").value;
    const waterSupplyValue = document.getElementById("waterSupply").value;
    const amenitiesValue = amenitiesCount; 

    let data = {
        "bathrooms": String(bathroomsValue),
        "property_age": String(property_ageValue),
        "property_size": String(property_sizeValue),
        "total_floor": String(totalFloorValue),
        "facing": String(facingValue),
        "furnishing": String(furnishingValue),
        "locality": String(localityValue),
        "parking": String(parkingValue),
        "water_supply": String(waterSupplyValue),
        "amenities": String(amenitiesValue)  // send only number of amenities
    };

    // ✅ Print the collected data
    console.log("Data to be sent to API:", data);

    // // If you also want to print amenities specifically
    // console.log("Selected amenities count:", amenitiesValue);
    // console.log("Selected amenities list:", [...amenitiesChecked].map(a => a.value));

    try {
        const response = await fetch("http://127.0.0.1:8000/predictprice", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error("Network response was not ok");
        }

        const result = await response.json();
        document.getElementById("result").textContent = "Predicted Price: ₹ " + result.prediction;
    } catch (error) {
        document.getElementById("result").innerText = "Error: " + error.message;
    }
});

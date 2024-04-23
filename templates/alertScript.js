const dangerEvents = [
  "Hazardous Weather Detected!",
  "Severe Storm Warning!",
  "Tornado Warning!",
  "Flash Flood Warning!",
  "Extreme Heat Alert!"
];

// safety tips for lower severity alerts
const safetyTips = [
  "Wear sun cream for UV protection.",
  "Wear a coat in cold weather.",
  "Ensure your bike tires are snow-proof in snowy conditions."
];

// randomly select a danger event or safety tip and display it
function displayAlert() {
  const alertElement = document.getElementById("alert");
  const alertMessage = document.getElementById("alertMessage");

  // Randomly select between a danger event and a safety tip
  const isDanger = Math.random() < 0.5;

  if (isDanger) {
    // Randomly select a danger event 
    const randomIndex = Math.floor(Math.random() * dangerEvents.length);
    const selectedEvent = dangerEvents[randomIndex];

    // Display the selected danger event in the alert message
    alertMessage.textContent = "⚠️ " + selectedEvent + " ⚠️";
    alertElement.classList.add("danger");
  } else {
    // Randomly select a safety tip 
    const randomIndex = Math.floor(Math.random() * safetyTips.length);
    const selectedTip = safetyTips[randomIndex];

    // Display the selected safety tip in the alert message
    alertMessage.textContent = selectedTip;
    alertElement.classList.add("warning");
  }
}


displayAlert();
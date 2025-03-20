async function sendMessage() {
    let userInput = document.getElementById("user-input").value.trim();
    if (userInput === "") return;

    let chatbox = document.getElementById("chatbox");
    chatbox.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;

    // Send message to chatbot API
    let response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userInput })
    });

    let data = await response.json();
    chatbox.innerHTML += `<p><strong>Chirpy:</strong> ${data.response}</p>`;

    // If the chatbot doesn't know the response, ask the user to teach it
    if (data.response.includes("I don't know how to respond")) {
        let userReply = prompt("How should Chirpy reply?");
        if (userReply) {
            // Save the new response to the chatbot
            await fetch("/learn", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_input: userInput, bot_reply: userReply })
            });

            chatbox.innerHTML += `<p><strong>Chirpy:</strong> Thanks! I've learned something new.</p>`;
        }
    }

    document.getElementById("user-input").value = ""; // Clear input field
}


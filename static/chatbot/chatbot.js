function toggleChat() {
    const chat = document.getElementById("wa-chat-container");
    chat.style.display = chat.style.display === "flex" ? "none" : "flex";
}

async function sendMessage() {
    const input = document.getElementById("wa-input");
    const message = input.value.trim();
    const chatBody = document.getElementById("wa-chat-body");

    if (!message) return;

    // Add User Message
    chatBody.innerHTML += `<div class="wa-user">${message}</div>`;
    chatBody.scrollTop = chatBody.scrollHeight;
    input.value = "";

    try {
        const response = await fetch("/chatbot-api/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        if (data.reply) {
            chatBody.innerHTML += `<div class="wa-bot">${data.reply}</div>`;
        } else {
            chatBody.innerHTML += `<div class="wa-bot">Sorry, something went wrong.</div>`;
        }

        chatBody.scrollTop = chatBody.scrollHeight;

    } catch (error) {
        chatBody.innerHTML += `<div class="wa-bot">Server error.</div>`;
    }
}
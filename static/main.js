console.log("main.js loaded");

// Elements
const chat = document.getElementById("chat");
const input = document.getElementById("msg");
const btn = document.querySelector("button");

// Helpers
function addMsg(role, text) {
  const div = document.createElement("div");
  div.className = "msg " + (role === "user" ? "user" : "ai");
  div.textContent = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

async function sendMsg() {
  const text = input.value.trim();
  if (!text) return;

  addMsg("user", text);
  input.value = "";

  try {
    const resp = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });

    const data = await resp.json();
    addMsg("assistant", data.reply);
  } catch (err) {
    console.error(err);
  }
}

// Events
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendMsg();
});
btn.addEventListener("click", sendMsg);

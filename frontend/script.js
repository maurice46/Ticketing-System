const API_BASE = "http://127.0.0.1:5000/api/tickets";

/* Load tickets on page load */
document.addEventListener("DOMContentLoaded", loadTickets);

async function loadTickets() {
    const res = await fetch(API_BASE);
    const tickets = await res.json();

    const list = document.getElementById("ticket-list");
    list.innerHTML = "";

    tickets.forEach(ticket => {
        const li = document.createElement("li");
        li.className = "ticket";

        li.innerHTML = `
            <span>${ticket.title}</span>
            <div>
                <button onclick="closeTicket(${ticket.id})">Close</button>
                <button onclick="deleteTicket(${ticket.id})">Delete</button>
            </div>
        `;

        list.appendChild(li);
    });
}


async function createTicket() {
    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;

    if (!title) {
        alert("Title required");
        return;
    }

    await fetch(API_BASE, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, description })
    });

    document.getElementById("title").value = "";
    document.getElementById("description").value = "";

    loadTickets();
}

async function closeTicket(id) {
    await fetch(`${API_BASE}/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: "closed" })
    });

    loadTickets();
}

async function deleteTicket(id) {
    await fetch(`${API_BASE}/${id}`, {
        method: "DELETE"
    });

    loadTickets();
}


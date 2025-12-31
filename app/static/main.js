async function submitExpense() {
    const text = document.getElementById("expenseText").value.trim();
    const statusDiv = document.getElementById("status");

    if (!text) {
        statusDiv.innerHTML = "<span class='error'>Please enter expense text</span>";
        return;
    }

    statusDiv.innerHTML = "⏳ Adding expense...";

    try {
        const response = await fetch("/expense/text", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Failed to add expense");
        }

        statusDiv.innerHTML = `
            <div class="success">
                ✅ Expense added successfully<br/>
                <pre>${JSON.stringify(data.parsed, null, 2)}</pre>
            </div>
        `;

        document.getElementById("expenseText").value = "";

    } catch (err) {
        statusDiv.innerHTML = `<span class='error'>❌ ${err.message}</span>`;
    }
}

// --------------------
// THEME TOGGLE
// --------------------
(function initTheme() {
    const html = document.documentElement;
    const toggleBtn = document.getElementById("theme-toggle");

    const storedTheme = localStorage.getItem("theme");
    const systemPrefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

    const initialTheme = storedTheme || (systemPrefersDark ? "dark" : "light");
    html.setAttribute("data-bs-theme", initialTheme);
    
    if (toggleBtn) {
        updateToggleIcon(initialTheme);

        toggleBtn.addEventListener("click", () => {
            const currentTheme = html.getAttribute("data-bs-theme");
            const newTheme = currentTheme === "dark" ? "light" : "dark";

            html.setAttribute("data-bs-theme", newTheme);
            localStorage.setItem("theme", newTheme);
            updateToggleIcon(newTheme);
        });
    }

    function updateToggleIcon(theme) {
        if (toggleBtn) {
            toggleBtn.textContent = theme === "dark" ? "☀️" : "🌙";
        }
    }
})();


// --------------------
// EXPENSE SUBMIT
// --------------------
async function submitExpense() {
    const textArea = document.getElementById("expenseText");
    const statusDiv = document.getElementById("status");
    const submitBtn = document.getElementById("submit-btn");

    const text = textArea.value.trim();

    if (!text) {
        showStatus("Please enter expense text", "danger");
        return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = "Adding...";

    try {
        const response = await fetch("/expense/text", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Failed to add expense");
        }

        showStatus(
            `Expense added successfully!<pre class="mt-2">${JSON.stringify(data.parsed, null, 2)}</pre>`,
            "success"
        );

        textArea.value = "";

    } catch (err) {
        showStatus(err.message, "danger");
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = "Add Expense";
    }
}

function showStatus(message, type) {
    const statusDiv = document.getElementById("status");
    statusDiv.className = `alert alert-${type}`;
    statusDiv.innerHTML = message;
}

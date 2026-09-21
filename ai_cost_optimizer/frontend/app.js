let networkChartInstance = null;

document.addEventListener("DOMContentLoaded", () => {
    fetchAnalytics();

    // Strategy Selector Logic
    const options = document.querySelectorAll('.strategy-option');
    options.forEach(opt => {
        opt.addEventListener('click', () => {
            options.forEach(o => o.classList.remove('active'));
            opt.classList.add('active');
            opt.querySelector('input').checked = true;
        });
    });

    // Enter to Send
    const input = document.getElementById('prompt-input');
    input.addEventListener('keypress', function (e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendPrompt();
        }
    });
});

async function fetchAnalytics() {
    try {
        const response = await fetch('/usage');
        if (!response.ok) {
            console.error("Database offline or unavailable");
            return;
        }

        const data = await response.json();

        // Ensure values are numbers before toFixed, or fall back to 0
        const cost = typeof data.total_estimated_cost === 'number' ? data.total_estimated_cost : 0;
        document.getElementById('val-cost').innerText = `$${cost.toFixed(6)}`;

        const saved = typeof data.total_cost_saved === 'number' ? data.total_cost_saved : 0;
        document.getElementById('val-saved').innerText = `$${saved.toFixed(6)}`;

        document.getElementById('val-tokens').innerText = data.total_tokens || 0;
        document.getElementById('val-req').innerText = data.total_requests || 0;
        document.getElementById('val-split').innerText = `${data.local_requests || 0} / ${data.cloud_requests || 0}`;
        document.getElementById('val-success').innerText = `${data.success_rate || 0}%`;

        const lat = typeof data.average_latency_ms === 'number' ? data.average_latency_ms : 0;
        document.getElementById('val-latency').innerText = `${lat.toFixed(1)}ms`;

        // Update Chart
        updateChart(data.local_requests || 0, data.cloud_requests || 0);

        // Fetch models
        const modelsRes = await fetch('/usage/models');
        if (modelsRes.ok) {
            const modelsData = await modelsRes.json();
            const list = document.getElementById('model-list');
            list.innerHTML = '';

            modelsData.data.forEach(item => {
                const li = document.createElement('li');
                li.className = 'model-item';
                li.innerHTML = `<div>${item.model} <br><small style="color:var(--text-dim)">${item.provider.toUpperCase()}</small></div> <span>${item.total_requests} reqs</span>`;
                list.appendChild(li);
            });
        }
    } catch (e) {
        console.error("Failed to fetch analytics:", e);
    }
}

async function sendPrompt() {
    const input = document.getElementById('prompt-input');
    const prompt = input.value.trim();
    if (!prompt) return;

    // Get Active Strategy
    const strategy = document.querySelector('input[name="strategy"]:checked').value;

    input.value = '';

    // Append User Message
    appendMessage(prompt, 'user');

    // Add Loading AI Bubble
    const aiMessage = document.createElement('div');
    aiMessage.className = 'chat-message ai loading';
    aiMessage.innerHTML = `
        <div class="avatar"><i class="fa-solid fa-microchip"></i></div>
        <div class="content">Computing runtime paths... executing via Inference Router.</div>
    `;
    const chatHistory = document.getElementById('chat-history');
    chatHistory.appendChild(aiMessage);
    chatHistory.scrollTop = chatHistory.scrollHeight;

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt, strategy })
        });

        const data = await response.json();

        aiMessage.classList.remove('loading');

        // Depending on network, colorize the metrics badge
        let colorClass = data.network === 'cloud' ? 'fa-cloud' : 'fa-network-wired';
        let costStyle = data.network === 'cloud' ? 'color: var(--accent-blue)' : 'color: var(--accent-green)';

        const costVal = typeof data.estimated_cost === 'number' ? data.estimated_cost : 0;
        const latencyVal = typeof data.latency_ms === 'number' ? data.latency_ms : 0;

        aiMessage.innerHTML = `
            <div class="avatar" style="background: ${data.network === 'cloud' ? 'var(--accent-blue)' : 'var(--accent-green)'}">
                <i class="fa-solid fa-robot"></i>
            </div>
            <div class="content">
                <div style="white-space: pre-wrap;">${data.response}</div>
                <div class="metrics-badge">
                    <span><i class="fa-solid ${colorClass}" style="${costStyle}"></i> ${data.network.toUpperCase()} (${data.model})</span>
                    <span><i class="fa-solid fa-clock"></i> ${latencyVal.toFixed(1)}ms</span>
                    <span><i class="fa-solid fa-coins"></i> $${costVal.toFixed(6)}</span>
                </div>
            </div>
        `;

        // Refresh dashboard asynchronously so user doesn't wait
        fetchAnalytics();

    } catch (e) {
        aiMessage.classList.remove('loading');
        aiMessage.classList.add('system');
        aiMessage.innerHTML = `
            <div class="avatar"><i class="fa-solid fa-triangle-exclamation"></i></div>
            <div class="content" style="color: #ef4444;">Network Error: Failed to contact AI Inference Engine. Make sure backend is active.</div>
        `;
    }

    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function appendMessage(text, role) {
    const msg = document.createElement('div');
    msg.className = `chat-message ${role}`;

    let icon = role === 'user' ? 'fa-user' : 'fa-robot';

    msg.innerHTML = `
        <div class="avatar"><i class="fa-solid ${icon}"></i></div>
        <div class="content">${text}</div>
    `;

    document.getElementById('chat-history').appendChild(msg);
}

// Chart.js rendering function
function updateChart(localCount, cloudCount) {
    const ctx = document.getElementById('networkChart').getContext('2d');

    if (networkChartInstance) {
        networkChartInstance.destroy(); // Clear old chart
    }

    networkChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['LAN (Local)', 'WAN (Cloud)'],
            datasets: [{
                data: [localCount, cloudCount],
                backgroundColor: ['#10b981', '#3b82f6'], // Green and Blue
                borderColor: 'transparent',
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'right',
                    labels: { color: '#94a3b8', font: { size: 10 } }
                }
            }
        }
    });
}

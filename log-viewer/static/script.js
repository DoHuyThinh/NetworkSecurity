let currentPage = 1;
let totalPages = 1;

function formatLogLine(line) {
  const timeRegex = /\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]/;
  const match = line.match(timeRegex);

  // Highlight Priority
  const priorityMatch = line.match(/\[Priority: (\d+)\]/);
  const priorityColor = {
    1: "text-danger",
    2: "text-warning",
    3: "text-success",
  };
  let prioritySpan = "";
  if (priorityMatch) {
    const prio = priorityMatch[1];
    prioritySpan = `<span class="${
      priorityColor[prio] || "text-muted"
    } fw-bold">[Priority: ${prio}]</span>`;
    line = line.replace(/\[Priority: \d+\]/, ""); // Remove from line
  }

  if (match) {
    const time = `<span class="text-info fw-semibold">[ ${match[1]} ]</span>`;
    const message = line.replace(match[0], "").trim();
    return `<div class="log-line animate-fade border-bottom border-secondary py-2">${time} ${message} ${prioritySpan}</div>`;
  }

  return `<div class="log-line animate-fade py-2 border-bottom border-secondary">${line}</div>`;
}

async function loadLogs(page = 1) {
  try {
    const res = await fetch(`/logs?page=${page}`);
    const data = await res.json();
    const logContent = document.getElementById("log-content");
    const indicator = document.getElementById("page-indicator");

    if (data.logs) {
      logContent.innerHTML = data.logs.map(formatLogLine).join("<br>");
      currentPage = data.current_page;
      totalPages = data.total_pages;
      indicator.innerText = `Page ${currentPage} of ${totalPages}`;
    }
  } catch (err) {
    console.error("Error loading logs:", err);
  }
}

async function fetchLatestLogs() {
  try {
    const res = await fetch("/latest");
    const data = await res.json();
    if (data.logs && currentPage === totalPages) {
      const logContent = document.getElementById("log-content");
      logContent.innerHTML += data.logs.map(formatLogLine).join("<br>");
    }
  } catch (err) {
    console.error("Error fetching latest logs:", err);
  }
}

document.getElementById("prev-btn").addEventListener("click", () => {
  if (currentPage > 1) loadLogs(currentPage - 1);
});

document.getElementById("next-btn").addEventListener("click", () => {
  if (currentPage < totalPages) loadLogs(currentPage + 1);
});

loadLogs(currentPage);
setInterval(fetchLatestLogs, 5000);

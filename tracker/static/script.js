const timerDisplay = document.getElementById('timer-display');
const totalTimeDisplay = document.getElementById('total-time');
const highscoreDisplay = document.getElementById('highscore-time');
const toggleBtn = document.getElementById('toggle-btn');
const historyBtn = document.getElementById('history-btn');
const historyAside = document.getElementById('history-aside');

let startTime = null;
let elapsedBeforePause = 0;
let intervalId = null;
let running = false;
let elapsed = 0;

// Format the highscore and total time displays
highscoreDisplay.textContent = formatTime(parseFloat(highscoreDisplay.textContent));
totalTimeDisplay.textContent = formatTime(parseFloat(totalTimeDisplay.textContent))

toggleBtn.addEventListener('click', () => {
  if (!running) {
    startTimer();
    toggleBtn.classList.add("stop")
  } else {
    stopTimer();
    toggleBtn.classList.remove("stop")
  }
  running = !running;
  toggleBtn.textContent = running ? "Stop" : "Start";
});

historyBtn.addEventListener('click', () => {
  historyAside.classList.toggle("hidden");
});

function startTimer() {
  elapsed = 0; // Reset elapsed time
  timerDisplay.textContent = formatTime(elapsed); // Reset display
  startTime = Date.now();
  intervalId = setInterval(() => {
    elapsed = Date.now() - startTime;
    timerDisplay.textContent = formatTime(elapsed);
  }, 10); // update every 10 ms for centiseconds
}

function stopTimer() {
  clearInterval(intervalId);
  submitElapsedTime(elapsed);
}

function formatTime(ms) {
  const totalCentiseconds = Math.floor(ms / 10);
  const centiseconds = totalCentiseconds % 100;
  const totalSeconds = Math.floor(ms / 1000);
  const seconds = totalSeconds % 60;
  const minutes = Math.floor(totalSeconds / 60) % 60;
  const hours = Math.floor(totalSeconds / 3600);
  const pad = (num, size = 2) => String(num).padStart(size, '0');
  return `${pad(hours)} : ${pad(minutes)} : ${pad(seconds)}.${pad(centiseconds)}`;
}

function submitElapsedTime(seconds) {
    fetch('/api/submit-time/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            // Add CSRF token here if CSRF protection is enabled
        },
        body: JSON.stringify({ elapsed: seconds })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
          totalTimeDisplay.textContent = formatTime(data.total);  
          highscoreDisplay.textContent = formatTime(data.highscore);
        } else {
          console.error("Server error:", data.message);
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}
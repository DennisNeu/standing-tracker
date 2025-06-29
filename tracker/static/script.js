const timerDisplay = document.getElementById('timer-display');
const toggleBtn = document.getElementById('toggle-btn');

let startTime = null;
let elapsedBeforePause = 0;
let intervalId = null;
let running = false;

toggleBtn.addEventListener('click', () => {
  if (!running) {
    startTimer();
  } else {
    stopTimer();
  }
  running = !running;
  toggleBtn.textContent = running ? "Stop" : "Start";
});

function startTimer() {
  startTime = Date.now() - elapsedBeforePause;
  intervalId = setInterval(() => {
    const elapsed = Date.now() - startTime;
    elapsedBeforePause = elapsed;
    timerDisplay.textContent = formatTime(elapsed);
  }, 10); // update every 10 ms for centiseconds
}

function stopTimer() {
  clearInterval(intervalId);
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
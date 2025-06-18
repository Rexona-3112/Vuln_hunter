// Boot messages
const bootLines = [
  "> [OK] Loading scanner modules...",
  "> [OK] Establishing secure shell...",
  "> [WARN] Untrusted SSL certificate ignored",
  "> [OK] Building payloads...",
  "> [OK] Launching terminal engine..."
];

// Print boot logs one at a time
function printBootLines(index = 0) {
  if (index >= bootLines.length) return;
  const log = document.getElementById("bootLog");
  const line = document.createElement("div");
  line.textContent = bootLines[index];
  log.appendChild(line);
  log.scrollTop = log.scrollHeight;
  setTimeout(() => printBootLines(index + 1), 700);
}

// Typewriter loading line
function typeWriter() {
  const text = "Booting Cyber Intelligence Terminal............";
  let i = 0;
  const speed = 90;
  function write() {
    if (i < text.length) {
      document.getElementById("typewriter").innerHTML += text.charAt(i);
      i++;
      setTimeout(write, speed);
    }
  }
  write();
}

// Countdown from 3 to GO!
function startCountdown() {
  const c = document.getElementById("countdown");
  const countdownValues = ["3", "2", "1", "GO!"];
  let index = 0;

  function nextTick() {
    if (index >= countdownValues.length) {
      document.getElementById("introScreen").style.transition = "all 0.8s ease";
      document.getElementById("introScreen").style.opacity = 0;
      setTimeout(() => {
        document.getElementById("introScreen").style.display = "none";
        c.classList.remove("launch-blast");
      }, 800);
      return;
    }

    c.innerText = countdownValues[index];
    if (countdownValues[index] === "GO!") {
      c.classList.add("launch-blast");
    }

    index++;
    setTimeout(nextTick, 750); // Fast countdown
  }

  nextTick();
}

// User clicks "Start Terminal Boot"
function initIntro() {
  document.getElementById("beginIntro").style.display = "none";
  document.getElementById("bootLog").style.display = "block";
  document.getElementById("typewriter").style.display = "block";
  document.getElementById("countdown").style.display = "block";

  printBootLines();
  setTimeout(typeWriter, bootLines.length * 700 + 1000);
  setTimeout(startCountdown, bootLines.length * 700 + 5000);
}

// Select/deselect all scan types
function toggleAll(master) {
  document.querySelectorAll(".scan-option").forEach(opt => {
    opt.checked = master.checked;
  });
}

// Rocket animation and scan progress
function startScan() {
  const rocket = document.getElementById("rocketIcon");
  rocket.classList.remove("blastoff");
  rocket.classList.add("orbiting");

  const bar = document.getElementById("progressBar");
  const container = document.getElementById("progressContainer");
  container.style.display = "block";

  let width = 0;
  let interval = setInterval(() => {
    width += Math.random() * 5 + 2;
    if (width >= 100) {
      width = 100;
      rocket.classList.remove("orbiting");
      rocket.classList.add("blastoff");
      clearInterval(interval);
    }
    bar.style.width = width + "%";
    bar.innerText = Math.floor(width) + "%";
  }, 300);
}
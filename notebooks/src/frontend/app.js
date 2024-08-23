const connectionStatusElement = document.getElementById(
  "connection-status"
);
const logOutputElement = document.getElementById("log-output");
const transcriptOutputElement = document.getElementById(
  "transcript-output"
);

const textInputElement = document.getElementById("text-input");

function updateConnectionStatus(status, className) {
  connectionStatusElement.textContent = status;
  connectionStatusElement.className = className;
}

function logMessage(message) {
  const logEntry = document.createElement("div");
  logEntry.textContent = message;
  logOutputElement.appendChild(logEntry);
  logOutputElement.scrollTop = logOutputElement.scrollHeight;
}

const ws = new WebSocket("ws://localhost:8000/ws/");

ws.onopen = function () {
  updateConnectionStatus("Connected", "status-connected");
  logMessage("WebSocket is open now.");
};

ws.onmessage = function (event) {
  if (typeof event.data === "string") {
    logMessage("Received transcription: " + event.data);
    transcriptOutputElement.innerText = event.data;
  } else {
    logMessage("Received binary data of length: " + event.data.size);

    const audioBlob = new Blob([event.data], { type: "audio/wav" });
    const audioUrl = URL.createObjectURL(audioBlob);
    const audioElement = document.getElementById("audio-output");
    audioElement.src = audioUrl;

    audioElement
      .play()
      .then(() => {
        logMessage("Audio is playing.");
      })
      .catch((error) => {
        logMessage("Error playing audio: " + error);
      });
  }
};

ws.onclose = function () {
  updateConnectionStatus("Disconnected", "status-disconnected");
  logMessage("WebSocket is closed now.");
};

ws.onerror = function (error) {
  updateConnectionStatus("Error", "status-error");
  logMessage("WebSocket error observed: " + error);
};

function sendText() {
  const text = textInputElement.value.trim();
  if (text && ws.readyState === WebSocket.OPEN) {
    const message = {
      type: "text",
      text: text,
    };
    ws.send(JSON.stringify(message));
    logMessage("Sent text: " + text);
  } else if (ws.readyState !== WebSocket.OPEN) {
    logMessage("WebSocket is not open. ReadyState: " + ws.readyState);
  } else {
    logMessage("No text to send.");
  }
}

// Silence detection parameters
const silenceThreshold = 0.09; // Adjust the threshold according to your needs
const silenceTimeout = 1000; // Time in milliseconds to consider as silence
const minimumBufferDuration = 2000; // Minimum buffer duration in milliseconds

let audioContext;
let mediaRecorder;
let audioChunks = [];
let silenceTimer;
let bufferTimer;
let isRecording = false;

async function startMicrophone() {
  const stream = await navigator.mediaDevices.getUserMedia({
    audio: true,
  });
  audioContext = new (window.AudioContext ||
    window.webkitAudioContext)();
  const source = audioContext.createMediaStreamSource(stream);
  const analyser = audioContext.createAnalyser();
  analyser.fftSize = 2048;
  source.connect(analyser);

  mediaRecorder = new MediaRecorder(stream);

  mediaRecorder.ondataavailable = function (event) {
    if (event.data.size > 0) {
      audioChunks.push(event.data);
    }
  };

  mediaRecorder.onstop = function () {
    const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
    ws.send(audioBlob);
    logMessage("Sent audio data of size: " + audioBlob.size);
    audioChunks = [];
  };

  logMessage("Microphone is active and listening.");
  detectNoiseAndSilence(analyser);
}

function detectNoiseAndSilence(analyser) {
  const dataArray = new Uint8Array(analyser.fftSize);

  function checkNoiseLevel() {
    analyser.getByteTimeDomainData(dataArray);
    const maxAmplitude = Math.max(...dataArray) / 128 - 1;

    if (maxAmplitude >= silenceThreshold) {
      // Noise detected, start recording if not already recording
      if (!isRecording) {
        logMessage("Noise detected. Starting recording.");
        mediaRecorder.start();
        isRecording = true;
      }

      // Reset the silence timer if sound is detected
      if (silenceTimer) {
        clearTimeout(silenceTimer);
        silenceTimer = null;
      }

      // Reset the buffer timer to ensure minimum buffer duration
      if (bufferTimer) {
        clearTimeout(bufferTimer);
        bufferTimer = null;
      }
    } else if (isRecording) {
      // Detected silence after noise, start silence timer
      if (!silenceTimer) {
        silenceTimer = setTimeout(() => {
          logMessage(
            "Silence detected. Stopping recording after buffer."
          );

          // Continue recording for a minimum buffer duration after silence
          bufferTimer = setTimeout(() => {
            mediaRecorder.stop();
            isRecording = false;
            silenceTimer = null;
            bufferTimer = null;
          }, minimumBufferDuration);
        }, silenceTimeout);
      }
    }

    requestAnimationFrame(checkNoiseLevel);
  }

  checkNoiseLevel();
}

// Initialize the microphone and start detecting noise/silence
startMicrophone();

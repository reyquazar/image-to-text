// popup.js
const fileInput = document.getElementById("fileInput");
const runBtn = document.getElementById("runBtn");
const captureBtn = document.getElementById("captureBtn");
const statusEl = document.getElementById("status");
const resultEl = document.getElementById("result");
const canvas = document.getElementById("preview");
const ctx = canvas.getContext("2d");

let imageBase64 = null;

// Загрузка файла
fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = (e) => {
    const img = new Image();
    img.onload = () => {
      canvas.width = img.width;
      canvas.height = img.height;
      ctx.drawImage(img, 0, 0);
      imageBase64 = e.target.result.split(",")[1]; // только base64
    };
    img.src = e.target.result;
  };
  reader.readAsDataURL(file);
});

// Скриншот вкладки
captureBtn.addEventListener("click", () => {
  chrome.tabs.captureVisibleTab(null, { format: "png" }, (dataUrl) => {
    if (chrome.runtime.lastError) {
      alert("Ошибка: " + chrome.runtime.lastError.message);
      return;
    }

    const img = new Image();
    img.onload = () => {
      canvas.width = img.width;
      canvas.height = img.height;
      ctx.drawImage(img, 0, 0);
      imageBase64 = dataUrl.split(",")[1]; // только base64
    };
    img.src = dataUrl;
  });
});

// Запуск OCR
runBtn.addEventListener("click", async () => {
  if (!imageBase64) {
    alert("Сначала загрузите изображение или сделайте скриншот!");
    return;
  }

  statusEl.textContent = "Статус: отправка на сервер...";

  try {
    const response = await fetch("http://localhost:5000/ocr", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image: imageBase64 }),
    });

    const data = await response.json();
if (typeof data === 'string') {
    // Если бэкенд возвращает просто строку
    resultEl.textContent = data;
    statusEl.textContent = "Статус: готово ✅";
} else if (data.text) {
    // Если бэкенд возвращает объект {text: "..."}
    resultEl.textContent = data.text;
    statusEl.textContent = "Статус: готово ✅";
} else {
    resultEl.textContent = "Ошибка: неверный формат ответа";
    statusEl.textContent = "Статус: ошибка ❌";
}
  } catch (err) {
    resultEl.textContent = "Ошибка запроса: " + err.message;
    statusEl.textContent = "Статус: ошибка ❌";
  }
});

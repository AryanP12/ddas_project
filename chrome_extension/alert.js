// alert.js

document.addEventListener('DOMContentLoaded', () => {
    console.log("Alert script loaded successfully.");

    // 1. Get the data passed in the URL parameters
    const params = new URLSearchParams(window.location.search);
    const downloadId = parseInt(params.get('downloadId'));
    const filename = params.get('filename');
    const location = params.get('location');

    console.log("Params received:", filename, location);

    // 2. Display the info to the user
    const fileEl = document.getElementById('filename');
    const locEl = document.getElementById('location');

    if (fileEl) fileEl.textContent = filename || "Unknown File";
    if (locEl) locEl.textContent = location || "Unknown Location";

    // 3. Handle "Use Existing" (Delete/Cancel)
    document.getElementById('btn-existing').addEventListener('click', () => {
        chrome.runtime.sendMessage({ action: 'cancel_download', downloadId: downloadId });
        window.close();
    });

    // 4. Handle "Download Anyway"
    document.getElementById('btn-download').addEventListener('click', () => {
        chrome.runtime.sendMessage({ action: 'resume_download', downloadId: downloadId });
        window.close();
    });
});
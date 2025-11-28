// background.js - FINAL ROBUST VERSION

const API_ENDPOINT = 'http://127.0.0.1:5000/api/check_duplicate';

// 1. Listen for messages from our Alert Window
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'cancel_download') {
        // Search for the download to check its current state
        chrome.downloads.search({id: message.downloadId}, (results) => {
            if (!results || results.length === 0) return;
            
            const item = results[0];
            if (item.state === 'complete') {
                // If it finished downloading, DELETE the file
                chrome.downloads.removeFile(message.downloadId, () => {
                    console.log("Duplicate file deleted from disk.");
                });
                chrome.downloads.erase({id: message.downloadId}); // Remove from Chrome history
            } else {
                // If it's still running, CANCEL it
                chrome.downloads.cancel(message.downloadId);
                console.log("Download cancelled.");
            }
        });
    } else if (message.action === 'resume_download') {
        // Only resume if it's actually paused
        chrome.downloads.search({id: message.downloadId}, (results) => {
            if (results && results[0].state === 'in_progress') {
                 chrome.downloads.resume(message.downloadId);
            }
        });
    }
});

// 2. Intercept Downloads
chrome.downloads.onCreated.addListener((downloadItem) => {
    // Attempt to pause immediately
    chrome.downloads.pause(downloadItem.id, () => {
        // Whether pause succeeded or failed (due to speed), we check for duplicates
        checkForDuplicate(downloadItem);
    });
});

function checkForDuplicate(downloadItem) {
    const requestData = {
        source_url: downloadItem.url,
        partial_hash: 'check_by_url_only'
    };

    fetch(API_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestData),
    })
    .then(response => {
        if (response.status === 200) return response.json();
        // If not 200, ensure we resume if it was successfully paused
        chrome.downloads.search({id: downloadItem.id}, (r) => {
             if (r[0].state === 'in_progress' && r[0].paused) chrome.downloads.resume(downloadItem.id);
        });
        return null;
    })
    .then(data => {
        if (data && data.status === 'duplicate_found') {
            const existing = data.data;
            let locPath = "Unknown location";
            
            if (existing.known_locations && existing.known_locations.length > 0) {
                // Escape backslashes for the URL parameter to prevent errors
                locPath = existing.known_locations[0].path.replace(/\\/g, '\\\\');
            }

            const params = new URLSearchParams();
            params.append('filename', existing.original_filename);
            params.append('location', locPath);
            params.append('downloadId', downloadItem.id);

            chrome.windows.create({
                url: 'alert.html?' + params.toString(),
                type: 'popup',
                width: 450,
                height: 400,
                focused: true
            });
        }
    })
    .catch(err => {
        console.error("API Error", err);
        // Fail safe: ensure download continues
        chrome.downloads.resume(downloadItem.id);
    });
}
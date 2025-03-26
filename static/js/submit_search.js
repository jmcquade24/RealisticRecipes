// Submitting search by pressing enter
const searchInput = document.getElementById("searchbox");

searchInput.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        const query = searchInput.value.trim();
        if (query) {
            // Embeds query in url, then redirects to search page
            searchUrl = searchUrl + "?q=" + encodeURIComponent(query);
            window.location.href = searchUrl;
        }
    }
});

// Submit search called when pressing search button
function submitSearch () {
    const searchInput = document.getElementById("searchbox");

    const query = searchInput.value.trim();
    if (query) {
        searchUrl = searchUrl + "?q=" + encodeURIComponent(query);
        window.location.href = searchUrl;
    }
}
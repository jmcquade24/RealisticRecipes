document.addEventListener("DOMContentLoaded", function () {
    // Like Button Functionality
    const likeButton = document.getElementById("like-btn");
    if (likeButton) {
        likeButton.addEventListener("click", function (event) {
            event.preventDefault();
            const recipeSlug = likeButton.dataset.slug;
            const likeCountElement = document.getElementById("like-count");

            fetch(`/recipes/recipe/${recipeSlug}/like/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({})
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then(data => {
                console.log(data);
                likeCountElement.textContent = data.likes_count;
                likeButton.innerHTML = data.liked ? "Unlike" : "Like";
            })
            .catch(error => console.error("Error liking recipe:", error));
        });
    }

    // Favorite Button Functionality
    const favoriteButton = document.getElementById("favorite-btn");
    if (favoriteButton) {
        favoriteButton.addEventListener("click", function (event) {
            event.preventDefault();
            const recipeSlug = favoriteButton.getAttribute("data-slug");
            const favoriteStatus = document.getElementById("favorite-status");

            fetch(`/recipes/recipe/${recipeSlug}/favorite/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({})
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then(data => {
                favoriteStatus.textContent = data.favorited ? "Added" : "Add";
            })
            .catch(error => console.error("Error favoriting recipe:", error));
        });
    }

    // Add Review Form Submission (AJAX)
    const reviewForm = document.getElementById("review-form");
    if (reviewForm) {
        reviewForm.addEventListener("submit", function (event) {
            event.preventDefault();
            const formData = new FormData(this);
            const recipeSlug = document.querySelector("#like-btn").getAttribute("data-slug");

            fetch(`/recipes/recipe/${recipeSlug}/review/`, {
                method: "POST",
                headers: { "X-CSRFToken": getCSRFToken() },
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then(data => {
                const reviewsList = document.getElementById("reviews");
                const newReview = document.createElement("li");
                newReview.innerHTML = `<strong>${data.username}</strong>: (${data.rating}/5) - ${data.comment}`;
                reviewsList.appendChild(newReview);
                reviewForm.reset();
            })
            .catch(error => console.error("Error submitting review:", error));
        });
    }

    // CSRF Token Function
    function getCSRFToken() {
        let cookieValue = null;
        document.cookie.split(";").forEach(cookie => {
            let [name, value] = cookie.trim().split("=");
            if (name === "csrftoken") {
                cookieValue = decodeURIComponent(value);
            }
        });
        return cookieValue;
    }
});
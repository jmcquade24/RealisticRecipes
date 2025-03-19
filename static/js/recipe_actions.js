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
                if (data.success) {
                    const reviewsList = document.getElementById("reviews");

                    const newReview = document.createElement("li");
                    const username = document.createElement("strong");
                    username.textContent = data.review.username;
                    newReview.appendChild(username);

                    const rating = document.createElement("span");
                    rating.classList.add("rating");
                    for (let i = 1; i <= 5; i++) {
                        const star = document.createElement("i");
                        if (i <= data.review.rating) {
                            star.classList.add("fas", "fa-star");
                        } else {
                            star.classList.add("far", "fa-star");
                        }
                        rating.appendChild(star);
                    }
                    newReview.appendChild(rating);

                    const comment = document.createElement("p");
                    comment.classList.add("comment");
                    comment.textContent = data.review.comment;
                    newReview.appendChild(comment);
                    reviewsList.appendChild(newReview);
                    reviewForm.reset();
                }
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
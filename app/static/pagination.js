document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM fully loaded and parsed");

    const moviesPerPage = 8;
    let currentPage = 1;

    const movies = document.querySelectorAll(".movie-item");
    const prevButton = document.getElementById("prev-button");
    const nextButton = document.getElementById("next-button");

    if (!movies.length) {
        console.error("No movie items found");
        return;
    }

    if (!prevButton || !nextButton) {
        console.error("Navigation buttons not found");
        return;
    }

    console.log(`Total movies: ${movies.length}`);

    function showPage(page) {
        console.log(`Showing page: ${page}`);
        const start = (page - 1) * moviesPerPage;
        const end = start + moviesPerPage;

        movies.forEach((movie, index) => {
            if (index >= start && index < end) {
                movie.style.display = "block";
            } else {
                movie.style.display = "none";
            }
        });

        prevButton.disabled = page === 1;
        nextButton.disabled = page === Math.ceil(movies.length / moviesPerPage);
    }

    prevButton.addEventListener("click", () => {
        if (currentPage > 1) {
            currentPage--;
            showPage(currentPage);
        }
    });

    nextButton.addEventListener("click", () => {
        if (currentPage < Math.ceil(movies.length / moviesPerPage)) {
            currentPage++;
            showPage(currentPage);
        }
    });

    // Show the first page initially
    showPage(currentPage);


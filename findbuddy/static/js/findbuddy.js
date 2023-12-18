const cardsPerPage = 15;
let currentPage = 1;
let products = [];
let initialProducts = [];

const searchInput = document.getElementById("search-input");

searchInput.addEventListener("input", () => {
    const searchTerm = searchInput.value.toLowerCase();
    const searchResults = initialProducts.filter(product => product.fields.title.toLowerCase().includes(searchTerm));
    currentPage = 1;
    renderFilteredProducts(searchResults);
});

async function getProducts() {
    return fetch(`/findbuddy/get-book/`).then((res) => res.json());
}

function openModal(product) {
    const modal = document.getElementById("productModal");
    const modalImage = document.getElementById("modalImage");
    const modalTitle = document.getElementById("modalTitle");
    const modalAuthor = document.getElementById("modalAuthor");
    const modalDescription = document.getElementById("modalDescription");
    const modalPublisher = document.getElementById("modalPublisher");
    const modalPublishedDate = document.getElementById("modalPublishedDate");
    const modalPageCount = document.getElementById("modalPageCount");
    const modalCategories = document.getElementById("modalCategories");
    const modalAverageRating = document.getElementById("modalAverageRating");
    const modalLanguage = document.getElementById("modalLanguage");
    const modalBuyLink = document.getElementById("modalBuyLink");

    const closeModalBtn = document.querySelector(".close");

    modal.style.display = "block";
    modalImage.src = product.fields.thumbnail;
    modalImage.alt = product.fields.title;
    modalTitle.textContent = product.fields.title;
    modalAuthor.textContent = product.fields.authors;
    modalDescription.textContent = product.fields.description;
    modalPublisher.textContent = product.fields.publisher;
    modalPublishedDate.textContent = product.fields.published_date;
    modalPageCount.textContent = product.fields.page_count;
    modalCategories.textContent = product.fields.categories;
    modalAverageRating.textContent = product.fields.average_rating;
    modalLanguage.textContent = product.fields.languange;
    modalBuyLink.href = product.fields.buyLink;

    if (product.fields.average_ratings) {
        modalAverageRatings.textContent = product.fields.average_ratings;
    } else {
        modalAverageRating.textContent = "None";
    }

    closeModalBtn.addEventListener("click", () => {
        modal.style.display = "none";
    });

}


async function updateProductsByCategory(category) {
    const selectedCategory = category;
    if (selectedCategory) {
        const newProducts = initialProducts.filter(product => product.fields.categories === selectedCategory);
        currentPage = 1;
        renderFilteredProducts(newProducts);
    } else {
        currentPage = 1;
        renderFilteredProducts(initialProducts);
    }
}

function renderFilteredProducts(filteredProducts) {
    products = filteredProducts;
    renderCurrentPage();
    renderPagination();
}

function renderCurrentPage() {
    const cardContainer = document.getElementById("product_cards");
    cardContainer.innerHTML = "";

    const startIndex = (currentPage - 1) * cardsPerPage;
    const endIndex = startIndex + cardsPerPage;

    for (let i = startIndex; i < endIndex && i < products.length; i++) {
        const item = products[i];
        const authors = item.fields.authors.split(",");

        const card = document.createElement("div");
        card.className = "product-card";
        card.id = `product-card-${i}`; // Tambahkan id ke kartu

        card.innerHTML = `
            <img class="product-image" src="${item.fields.small_thumbnail}" alt="Book Cover">
            <div>
                <p>${item.fields.title}</p>
                <p><strong>Author:</strong> ${formatAuthors(authors)}</p>
                <p><strong>Description:</strong> ${truncateDescription(item.fields.description, 10)}</p>
            </div>
        `;
        cardContainer.appendChild(card);
        card.addEventListener("click", () => openModal(item)); // Tambahkan event listener
    }
}

function formatAuthors(authors) {
    if (authors.length === 1) {
        return authors[0];
    } else {
        return authors[0] + ", and more";
    }
}

function truncateDescription(description, wordCount) {
    const words = description.split(" ");
    if (words.length > wordCount) {
        return words.slice(0, wordCount).join(" ") + " ...";
    }
    return description;
}

function renderPagination() {
    const paginationContainer = document.getElementById("pagination");
    paginationContainer.innerHTML = "";

    const totalPages = Math.ceil(products.length / cardsPerPage);

    const pageBar = document.createElement("div");
    pageBar.className = "page-bar";

    if (currentPage > 1) {
        const prevButton = document.createElement("button");
        prevButton.className = "pagination-button";
        prevButton.innerText = "Previous";
        prevButton.addEventListener("click", () => {
            currentPage--;
            renderCurrentPage();
            scrollToTop();
            renderPagination();
        });
        pageBar.appendChild(prevButton);
    }

    const pageBarText = document.createElement("div");
    pageBarText.className = "page-bar-text";
    pageBarText.innerText = `Page ${currentPage} of ${totalPages}`;
    pageBar.appendChild(pageBarText);

    if (currentPage < totalPages) {
        const nextButton = document.createElement("button");
        nextButton.className = "pagination-button";
        nextButton.innerText = "Next";
        nextButton.addEventListener("click", () => {
            currentPage++;
            renderCurrentPage();
            scrollToTop();
            renderPagination();
        });
        pageBar.appendChild(nextButton);
    }

    paginationContainer.appendChild(pageBar);
}

function scrollToTop() {
    window.scrollTo(0, 0);
}

const categoryFilter = document.getElementById("category-filter");

categoryFilter.addEventListener("change", () => {
    updateProductsByCategory(categoryFilter.value);
});

const filterContainer = document.getElementById("filter-container");

getProducts().then((data) => {
    products = data;
    initialProducts = data;
    renderCurrentPage();
    renderPagination();
});

const requestButton = document.getElementById("request-button");
const bookForm = document.getElementById("book-form");

requestButton.addEventListener("click", function() {
    bookForm.style.display = "block"; // Menampilkan formulir ketika tombol ditekan
});

function addRequest() {

    fetch(`/findbuddy/add-request-ajax/`, {
        method: "POST",
        body: new FormData(document.getElementById("book-form"))
    }).then(refreshRequest)

    document.getElementById("book-form").reset()
}

document.getElementById("button_add").onclick = addRequest;

async function getRequest() {
    return fetch(`/findbuddy/get-request/`).then((res) => res.json())
    }

async function refreshRequest() {
    document.getElementById("form_table").innerHTML = ""
    const products = await getRequest()
    let htmlString = `<tr>
        <th>Title</th>
        <th>Author</th>
    </tr>`
    products.forEach((item) => {
        htmlString += `\n<tr>
        <td>${item.fields.title}</td>
        <td>${item.fields.author}</td>
    </tr>` 
    })
    
    document.getElementById("form_table").innerHTML = htmlString
}

refreshRequest();
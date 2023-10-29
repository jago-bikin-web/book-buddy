let chosenBook = null; // Variable to store the chosen book
let chosenBookId = null;

async function getBooks() {
  return fetch(`/reachbuddy/get-books/`).then((res) => res.json());
}

const searchInput = document.getElementById("search-input");

searchInput.addEventListener("input", function() {
  const searchValue = searchInput.value.toLowerCase();
  filterBooks(searchValue);
});

function filterBooks(searchText) {
  const rows = document.querySelectorAll(".row.pb-2");

  rows.forEach(function(row) {
    let hasMatchingBook = false;

    const bookCards = row.querySelectorAll(".kartu");
    searchText = searchText.trim().toLowerCase();

    bookCards.forEach(function(bookCard) {
      const bookTitle = bookCard.getAttribute("data-title").toLowerCase();
      if (bookTitle.includes(searchText)) {
          bookCard.style.display = "block"; // Show matching book cards
          hasMatchingBook = true;
      } else {
          bookCard.style.display = "none"; // Hide non-matching book cards
      }
    });

    if (hasMatchingBook) {
        row.style.display = "block"; // Show the row if it contains matching books
    } else {
        row.style.display = "none"; // Hide the row if it doesn't contain matching books
    }
  });
  if (searchText === ""){
    refreshCards()
  }
}

async function refreshCards() {
  const books = await getBooks();
  const bookCardContainer = document.getElementById("book_cards");

  bookCardContainer.innerHTML = "";

  let row = document.createElement("div");
  row.className = "row pb-2";
  let nomorBuku = 1;
  let count = 1;

  books.forEach((book, index) => {
    const bookCard = document.createElement("div");
    bookCard.className = "col-md-6";

    let slicedAuthors = "";
    if (book.fields.authors.length > 50) {
      slicedAuthors = book.fields.authors.slice(0, 50);
      slicedAuthors += "...";
    } else {
      slicedAuthors = book.fields.authors;
    }

    bookCard.innerHTML = `
      <div class="flex flex-col rounded-lg md:flex-row border-3 border-yellow-500 p-2 h-100 kartu" 
        data-title="${book.fields.title}" data-id="${book.pk}" onclick="chooseBook(this)" style="cursor: pointer;">
          <img class="w-16 h-24 object-cover rounded-lg md:h-32 md:w-32" src="${book.fields.thumbnail}" alt="${book.fields.title}" />
          <div class="flex flex-col p-2">
              <h5 class="mb-1 text-lg font-medium text-black">
                  ${nomorBuku}. ${book.fields.title}
              </h5>
              <p class="mb-1 text-sm text-black">
                  Author: ${slicedAuthors}
              </p>
              <p class="mb-1 text-sm text-black">
                  Published: ${book.fields.published_date}
              </p>
              <p class="mb-1 text-sm text-black">
                  Pages: ${book.fields.page_count}
              </p>
          </div>
      </div>
    `;

    row.appendChild(bookCard);
    count++;

    // Jika sudah ada 3 book cards pada satu baris, tambahkan baris tersebut ke dalam kontainer dan buat baris baru
    if (count > 2 || index === books.length - 1) {
      bookCardContainer.appendChild(row);
      row = document.createElement("div");
      row.className = "row pb-2";
      count = 1;
    }
    nomorBuku++;
  });
}

function getBooksById(id) {
  return fetch(`/reachbuddy/get_book_json_id/${id}/`).then((res) => res.json());
}

function chooseBook(card) {
  removeSelected();

  // Update the chosen book and modal title

  chosenBook = card.getAttribute("data-title");
  chosenBookId = card.getAttribute("data-id");
  const modalTitle = document.querySelector(".modal-title");
  modalTitle.textContent = `The chosen book is ${chosenBook}`;

  // Add 'bg-yellow-500' class to the clicked div
  card.classList.add('bg-yellow-500');
}

async function savedBook(){
  // diclick sama id="save_book"
  // mengisi content id="chosen_book" dengan identitas buku yang dipilih

  const book_data = await getBooksById(chosenBookId);
  const book = book_data[0]
  
  const chosenBookContainer = document.getElementById("chosen_book");
  chosenBookContainer.innerHTML = "";

  const bookContent = document.createElement("div");
  bookContent.className = "flex flex-col rounded-lg md:flex-row p-2 h-100"

  bookContent.innerHTML = `
  <img class="w-16 h-24 object-cover rounded-lg md:h-32 md:w-32" src="${book.fields.thumbnail}" />
  <div class="flex flex-col p-2">
      <h5 class="mb-1 text-lg font-medium text-black">
        Judul: ${book.fields.title}
      </h5>
      <p class="mb-1 text-sm text-black">
          Author: ${book.fields.authors}
      </p>
      <p class="mb-1 text-sm text-black">
          Published: ${book.fields.published_date}
      </p>
      <p class="mb-1 text-sm text-black">
          Pages: ${book.fields.page_count}
      </p>
  </div>
  `;

  chosenBookContainer.appendChild(bookContent);

  const tombolModal = document.querySelector("#tombol_pilih_buku")
  tombolModal.textContent = `Choose another`;
}

function removeSelected() {
  // Remove 'bg-yellow-500' class from previously selected div
  const previouslySelected = document.querySelector('.bg-yellow-500');
  if (previouslySelected) {
    previouslySelected.classList.remove('bg-yellow-500');
  }

  const modalTitle = document.querySelector(".modal-title");
  modalTitle.textContent = `Choose the desired book`;
}

refreshCards();

function addThread() {
  fetch(`/reachbuddy/create_thread_ajax/${chosenBookId}/`, {
      method: "POST",
      body: new FormData(document.querySelector('#form'))
  })
  .then(response => {
      if (response.ok) {
          // Reset the form
          document.getElementById("form").reset();
          
          // Redirect to a new URL
          window.location.href = `/reachbuddy/`;
      } else {
          console.log("Error creating thread.");
      }
  })
  .catch(error => {
      console.error("Error:", error);
  });

  return false;
}

document.getElementById("button_post").onclick = addThread;

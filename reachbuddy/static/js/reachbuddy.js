async function getThreads() {
  return fetch(`/reachbuddy/get-threads/`).then((res) => res.json());
}

function getBooksById(id) {
  return fetch(`/reachbuddy/get_book_json_id/${id}/`).then((res) => res.json());
}

function getProfileById(id) {
  return fetch(`/reachbuddy/get_profile_json_id/${id}/`).then((res) => res.json());
}

async function refreshCards() {
  const threads = await getThreads();
  const threadsCardContainer = document.getElementById("thread_cards");

  threadsCardContainer.innerHTML = "";

  threads.sort((a, b) => b.pk - a.pk);

  for (const thread of threads) {
    const threadContent = document.createElement("div");
    threadContent.className = "container my-2 py-2";

    const user_data = await getProfileById(thread.fields.user);
    const user = user_data[0];

    const book_data = await getBooksById(thread.fields.book);
    const book = book_data[0];

    const isLiked = thread.fields.likes.includes(parseInt(currentUserPk));

    threadContent.innerHTML = `
    <div class="row d-flex justify-content-center">
      <div class="col-md-12 col-lg-10 col-xl-8">
        <div class="card col-7 mx-auto border-warning border-3 border-radius rounded-4">
          <div class="card-header">
            <div class="flex flex-col rounded-lg md:flex-row p-2 h-100">
              <img class="w-16 h-24 object-cover rounded-lg md:h-32 md:w-32" src="${book.fields.thumbnail}" />
              <div class="flex flex-col p-2">
                <h5 class="mb-1 text-lg font-medium text-black text-left">
                  ${book.fields.title}
                </h5>
                <p class="mb-1 text-sm text-black text-left">
                  Author: ${book.fields.authors}
                </p>
                <p class="mb-1 text-sm text-black text-left">
                  Published: ${book.fields.published_date}
                </p>
                <p class="mb-1 text-sm text-black text-left">
                  Pages: ${book.fields.page_count}
                </p>
              </div>
            </div>
          </div>
          <div class="card-body">
            <div class="d-flex flex-start align-items-center">
              <div class="d-flex align-items-center">
                <img class="rounded-circle shadow-1-strong me-3"
                  src="${user.fields.profile_picture}" alt="avatar" width="60"
                  height="60" />
                <div>
                  <h6 class="fw-bold text-warning mb-1">
                    ${user.fields.full_name}
                  </h6>
                </div>
              </div>
              <p class="text-muted small mb-1 px-2">
                · ${thread.fields.date_added}
              </p>
              <div class="d-flex align-items-center ml-auto">
                <button type="submit" onclick="trashThread(${thread.pk})" class="trash-button">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                    <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5Zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5Zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6Z"/>
                    <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1v1ZM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118ZM2.5 3h11V2h-11v1Z"/>
                  </svg>
                </button>
              </div>
            </div>
            <p>${thread.fields.review}</p>
            <div class="small d-flex justify-content-start">
              <button type="submit" onclick="likeThread(${thread.pk})" class="d-flex align-items-center ml-4">
              ${isLiked 
                ? `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-5">
                  <path d="m11.645 20.91-.007-.003-.022-.012a15.247 15.247 0 0 1-.383-.218 25.18 25.18 0 0 1-4.244-3.17C4.688 15.36 2.25 12.174 2.25 8.25 2.25 5.322 4.714 3 7.688 3A5.5 5.5 0 0 1 12 5.052 5.5 5.5 0 0 1 16.313 3c2.973 0 5.437 2.322 5.437 5.25 0 3.925-2.438 7.111-4.739 9.256a25.175 25.175 0 0 1-4.244 3.17 15.247 15.247 0 0 1-.383.219l-.022.012-.007.004-.003.001a.752.752 0 0 1-.704 0l-.003-.001Z" />
                </svg>`
                : `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12Z" />
                </svg>`
              }
                </button>
              <span id="like-count-${thread.pk}">${thread.fields.likes.length}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    `;

    const trashButton = threadContent.querySelector(".trash-button");
    if (user.fields.full_name === currentUser) {
        trashButton.style.display = "block"; // Show the trash button
    } else {
        trashButton.style.display = "none"; // Hide the trash button
    }

    threadsCardContainer.appendChild(threadContent);
  };
}

refreshCards();

function trashThread(id) {
  fetch(`delete_thread_ajax/${id}`, {
      method: "DELETE"
  })
  .then(refreshCards)

  return false;
}

function likeThread(threadId) {
  fetch(`thread_like/${threadId}/`, {
    method: "POST"
  }).then(refreshCards)

}
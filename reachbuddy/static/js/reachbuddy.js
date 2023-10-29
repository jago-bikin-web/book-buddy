
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

  threadsCardContainer.innerHTML=""

  threads.sort((a, b) => b.pk - a.pk);

  //threads.forEach((thread) =>
  for (const thread of threads) {
    const threadContent = document.createElement("div");
    threadContent.className = "container my-2 py-2";

    threadContent.setAttribute("data-aos", "zoom-in");
    threadContent.setAttribute("data-aos-duration", "500");

    const user_data = await getProfileById(thread.fields.user);
    const user = user_data[0]

    const book_data = await getBooksById(thread.fields.book);
    const book = book_data[0]

    threadContent.innerHTML = `
    <div class="row d-flex justify-content-center ">
      <div class="col-md-12 col-lg-10 col-xl-8 ">
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
                <button type="submit" onclick="trashThread(${thread.pk})" class="trash-button"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                  <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5Zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5Zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6Z"/>
                  <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1ZM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118ZM2.5 3h11V2h-11v1Z"/>
                  </svg>
                </button>
            </div>

            </div>
            
              <p>${thread.fields.review}</p>

            <div class="small d-flex justify-content-start">
              <a href="#!" id="like_button" class="d-flex align-items-center ml-4">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart me-2" viewBox="0 0 16 16">
                  <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/>
                </svg>
              </a>

              <p>${thread.fields.likes}</p>
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
        // You can choose to hide the button or take another action
        trashButton.style.display = "none";
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

  return false
  }

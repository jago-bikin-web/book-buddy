async function getOwnBooks() {
  return fetch('/mybuddy/get-own-book/').then(res => res.json());
}

async function refreshOwnBooks() {
  const items = await getOwnBooks();
  let stringAdd = "";

  items.forEach((item) => {
    let ulasan = item.ulasan
    if (ulasan === "") {
      ulasan = "Anda belum menambahkan ulasan ..."
    }  

    stringAdd += `
    <article class="flex max-w-xl flex-col max-w-md shadow bg-white">
      <div class="h-48 w-full flex-none bg-cover rounded-t lg:rounded-t-none lg:rounded-l text-center overflow-hidden" style="background-image: url(${item.thumbnail});"></div>
      <div class="flex max-w-xl flex-col items-start justify-between p-3">
        <div class="flex items-center text-xs justify-between w-full">
          <p class="relative z-10 rounded-full bg-yellow-500 px-3 py-1.5 font-medium text-white hover:bg-gray-100">${item.status}</p>

          <div class="flex">
            <button class="bg-yellow-500 text-white font-bold text-md px-3 py-1.5 rounded-full hover:shadow-md outline-none"> - </button>
            <p class="bg-yellow-500 text-white mx-1 font-bold text-md px-3 py-1.5 rounded-full">
              ${item.page_track}
            </p>
            <button class="bg-yellow-500 text-white font-bold text-md px-3 py-1.5 rounded-full hover:shadow-md outline-none" type="button"> + </button>
          </div>
        </div>
        <div class="group relative">
          <h3 class="mt-3 text-lg font-semibold leading-6 text-gray-900">
            <span class="absolute inset-0"></span>
            ${item.title}
          </h3>
          <p class="mt-2 line-clamp-3 text-sm leading-6 text-gray-600">
            ${item.description}
          </p>
        </div>
        <div class="relative flex items-center">
          <div class="text-sm leading-6">
            <h5 class="mt-3 font-semibold leading-6 text-gray-900">
              <span class="absolute inset-0"></span>
              Ulasan
            </h5>
            <p class="text-gray-900 line-clamp-3">
              ${ulasan}
            </p>
          </div>
        </div>
        <div class="w-full mt-1">
          <button
            type="button"
            class="block w-full rounded bg-yellow-500 px-6 pb-2 pt-2.5 text-xs font-bold uppercase leading-normal text-white"
            onClick="showModal(${item.pk})">
            Ubah Koleksi
          </button>
        </div>
      </div>
    </article>
    `;
  });

  $(".bookshelf-mybuddy").html(stringAdd);
}

function showModal(id) {
  $(".modal-update").removeClass("hidden")
  fetch('/mybuddy/', {
    method: "PUT",
    body: JSON.stringify({
      pk: id
    }),
    headers: {
      'Content-type': 'application/json; charset=UTF-8',
    },
  }).then(res => console.log(res.json()))
}

function closeModal() {
  $(".modal-update").addClass("hidden")
  $(".page-track").val(0)
  $(".status").val("W")
  $(".ulasan").val("")
}

$(document).ready(()=>{
  $(".btn-close").click(() => {
    closeModal()
  })
  
  $(".btn-submit").click(() => {
    const form = document.querySelector("#form-update")
    const formData = new FormData(form);
    fetch("/mybuddy/update-own-book/", {
        method: "POST",
        body: formData
    }).then(res => {
      refreshOwnBooks();
      closeModal();
    })
  })

  $("#search-book").on("input", function() {
    const query = $(this).val();
    refreshBooks(query);
  });
})

async function getBooks(filter) {
  if (filter === "") filter = "get_random"
  return fetch("/api/search-books/?query=" + filter).then(res => res.json())
}

async function refreshBooks(filter) {
  const items = await getBooks(filter);
  let stringAdd = "";

  items.forEach((item) => {
    let title;
    let authors;
    let description;
    if (item.fields.title.length > 21) {
      title = item.fields.title.substring(0, 20) + "..."
    } else {
      title = item.fields.title
    }
    if (item.fields.description.length > 126) {
      description = item.fields.description.substring(0, 125) + "..."
    } else {
      description = item.fields.description
    }
    if (item.fields.authors.length > 21) {
      authors = item.fields.authors.substring(0, 20) + "..."
    } else {
      authors = item.fields.authors
    }

    stringAdd += `
      <div class="max-w-md w-full lg:flex shadow">
        <div class="relative h-48 lg:h-auto lg:w-48 flex-none bg-cover rounded-t lg:rounded-t-none lg:rounded-l text-center overflow-hidden" style="background-image: url('${item.fields.thumbnail}')">
          <button
            class="absolute right-2 bottom-2 rounded bg-yellow-500 px-3 pb-2 pt-2.5 text-xs font-medium leading-normal text-neutral-50 shadow" onclick="addBook(${item.pk})">
            Add
          </button>
        </div>
        <div class="border-r border-b border-l border-t border-grey-light lg:border-l-0 lg:border-t lg:border-grey-light bg-white rounded-b lg:rounded-b-none lg:rounded-r p-4 flex flex-col justify-between leading-normal">
          <div class="mb-8">
            <div class="text-black font-bold text-xl mb-2">${title}</div>
            <p class="text-grey-darker text-base">${description}</p>
          </div>
          <div class="flex items-center">
            <div class="text-sm">
              <p class="text-black leading-none"><strong>Author:</strong> ${authors}</p>
              <p class="text-grey-dark"><strong>${item.fields.published_date.substring(0,4)}</strong></p>
            </div>
          </div>
        </div>
      </div>
    `;
  });

  $(".bookshelf-addbuddy").html(stringAdd);
}

function addBook(id) {
  fetch('/mybuddy/add-buddy/', {
    method: "POST",
    body: JSON.stringify({
      pk: id
    }),
    headers: {
      'Content-type': 'application/json; charset=UTF-8',
    },
  }).then(res => {
    refreshBooks("");
  }).catch(err => {
    console.log(err);
    alert("Gagal menambah buku.");
  })
}

if (window.location.pathname.indexOf("mybuddy") != -1) {
  refreshOwnBooks();
}

if (window.location.pathname.indexOf("add-buddy") != -1) {
  refreshBooks("");
}


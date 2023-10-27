async function getBooks() {
  return fetch("/api/get-random/").then((res) => res.json());
}

async function refreshBooks() {
  const items = await getBooks();
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
      <div class="max-w-md w-full lg:flex" data-aos="fade-up">
        <div class="h-48 lg:h-auto lg:w-48 flex-none bg-cover rounded-t lg:rounded-t-none lg:rounded-l text-center overflow-hidden" style="background-image: url('${item.fields.thumbnail}')">
        </div>
        <div class="border-r border-b border-l border-grey-light lg:border-l-0 lg:border-t lg:border-grey-light bg-white rounded-b lg:rounded-b-none lg:rounded-r p-4 flex flex-col justify-between leading-normal gradient-custom">
          <div class="mb-8">
            <div class="text-black font-bold text-xl mb-2">${title}</div>
            <p class="text-grey-darker text-base">${description}</p>
          </div>
          <div class="flex items-center">
            <div class="text-sm">
              <p class="text-black leading-none">Author: ${authors}</p>
              <p class="text-grey-dark">${item.fields.published_date.substring(0,4)}</p>
            </div>
          </div>
        </div>
      </div>
    `;
  });

  $(".bookshelf").html(stringAdd);
}

if (window.location.href.indexOf("home") != -1) {
  refreshBooks();
}
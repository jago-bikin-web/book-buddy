
async function getEvents() {
    return fetch(`/eventbuddy/get-event/`).then((res) => res.json());
}

async function getBooksByID(id) {
    return fetch(`/eventbuddy/get-books-ID/${id}`).then((res) => res.json());
}

async function refreshEvent() {
    document.getElementById("event_cards").innerHTML = "";
    const events = await getEvents();
    let htmlString = "";

    for (const event of events) {
        const books_data = await getBooksByID(event.fields.book);
        const books = books_data[0];
        htmlString += `\n<div class="max-w-4xl border bg-white rounded relative">
            <a href="#"><img src="${books.fields.thumbnail}" alt="" class="h-[12.5rem] w-full object-cover" /></a>
            <div class="p-5">
                <a href="#">
                    <h5 class="font-NotoSansGeo mb-2 text-lg font-bold leading-normal md:text-xl">${event.fields.name}</h5>
                </a>
                <p class="mb-3 text-sm font-normal leading-normal text-gray-700 dark:text-gray-400">Date: ${event.fields.date}</p>
                <p class="mb-3 text-sm font-normal leading-normal text-gray-700 dark:text-gray-400">${event.fields.description}</p>
            </div>
            <div class="absolute top-40 left-0 bottom-0 m-4">
                <a href='edit-event/${event.pk}' class="rounded-md bg-yellow-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover-bg-yellow-500 focus-outline-none focus-ring-2 focus-ring-yellow-500 focus-ring-offset-2 focus-visible-outline-offset-2 focus-visible-outline-indigo-600">Edit</a>
                <a href='attendees/${event.pk}' class="rounded-md bg-yellow-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover-bg-yellow-500 focus-outline-none focus-ring-2 focus-ring-yellow-500 focus-ring-offset-2 focus-visible-outline-offset-2 focus-visible-outline-indigo-600">Attendees</a>
                <a href='regis-event/${event.pk}' class="rounded-md bg-yellow-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover-bg-yellow-500 focus-outline-none focus-ring-2 focus-ring-yellow-500 focus-ring-offset-2 focus-visible-outline-offset-2 focus-visible-outline-indigo-600">Reg</a>
            </div>
        </div>`;
    }

    document.getElementById("event_cards").innerHTML = htmlString;
}

function addEvent() {
    fetch((`/eventbuddy/create-event/`), {
        method: "POST",
        body: new FormData(document.querySelector('#formevent'))
    }).then(refreshEvent);

    document.getElementById("formevent").reset();
    closeModal();
    return false;
}

function closeModal() {
    $(".modal-update").addClass("hidden");
    document.getElementById("formevent").reset();
    return false;
}

function showModal() {
    $(".modal-update").removeClass("hidden");
    document.getElementById("formevent").reset();
    return false;
}

document.getElementById("button_add").onclick = addEvent;
document.getElementById("addevent").onclick = showModal;
document.getElementById("btn-close").onclick = closeModal;
refreshEvent();

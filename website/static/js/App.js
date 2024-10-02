function goToRoute(route, method) {
	if (method[0] == 'GET') {
		window.location.pathname = route
	} else {
		var data = method[1]
		const url = `${route}`
		fetch(url, {
			method: 'POST',
			headers: {'Content-Type': 'application/json'},
			body: JSON.stringify(data)
		})
		.then(response => response.text())
		.then(data => console.log(data))
	}
}
function renderComponent(element) {
	let content = element.textContent
	element.innerHTML = `${content}`
	console.log(`rendering component...\ndata: ${content}`)
}
function openNoteScreen(noteID) {
	loadScreen("22")
	let noteIsPremium = document.querySelector("#View-Note-Screen-is-premium")
	let noteDate = document.querySelector("#View-Note-Screen-date")
	let noteTime = document.querySelector("#View-Note-Screen-time")
	let noteTopic = document.querySelector("#View-Note-Screen-topic")
	let noteContent = document.querySelector(".View-Note-Screen-content")
	let noteTextbook = document.querySelector("#View-Note-Screen-textbook")
	let noteManual = document.querySelector("#View-Note-Screen-manual")
	let noteLecturer = document.querySelector("#View-Note-Screen-lecturer")

	fetch(`/get-note-data/${noteID}`)
	.then(response => response.json())
	.then(data => {
		console.log(data)
		noteIsPremium.innerHTML = (data.is_premium == "No") ? "This note is free." : "This note is exclusive to premium users."
		noteDate.innerHTML = data.datestamp
		noteTime.innerHTML = data.timestamp
		noteTopic.innerHTML = data.name
		noteContent.innerHTML = data.content
		noteTextbook.innerHTML = data.textbook
		noteManual.innerHTML = data.manual
		noteLecturer.innerHTML = data.lecturer

		console.log(noteIsPremium.textContent)
		noteContent.style.display = "none"

		
		if (N100PremiumStatus == 'True' && noteIsPremium.innerHTML == "This note is exclusive to premium users.") {
			noteContent.style.display = "block"
		} else if (noteIsPremium.innerHTML == "This note is free.") {
			noteContent.style.display = "block"
		} 
	})
	.catch(error => console.error('Error:', error))
}
// const loadingEvent = new Event('customLoadingEvent');

// window.addEventListener('load', () => {
//   document.dispatchEvent(loadingEvent);
// });

// document.addEventListener('customLoadingEvent', () => {
//   setTimeout(()=>{
//   	console.log('Internet is slow');
//   } , 10000)
// });
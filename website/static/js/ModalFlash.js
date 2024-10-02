function ModalFlashShow(title, content, category){
	const icon_folder_url = "../static/media/icons"
	document.querySelector("#ModalFlash-overlay").style.display = "block"
	document.querySelector("#ModalFlash-content").style.display = "flex"
	// document.querySelector("#ModalFlash-close-button").style.display = `${display_property}`
	try {
		document.querySelector("#ModalFlash-title").innerHTML = title
		document.querySelector("#ModalFlash-message").innerHTML = content
	} catch(e) {
		// statements
		console.log(`Using No Flash\n${e}`);
	}
	if (category[0] == "no-flash") {

		document.querySelector("#ModalFlash-content").innerHTML = ""
		document.querySelector("#ModalFlash-content").className = `modal-content-flash grid-container grid-parent-container-${category[1]}`
		document.querySelector("#ModalFlash-content").style.display = 'grid'
		const conent_title = document.createElement('h1')
		const grid_container_element = document.createElement('div')
		grid_container_element.className = `grid-container grid-container-${category[1]}`
		conent_title.className = `screen-header-text header-text-${category[1]}`
		document.querySelector("#ModalFlash-content").appendChild(conent_title)
		document.querySelector("#ModalFlash-content").appendChild(grid_container_element)

		document.querySelector(`.grid-container-${category[1]}`).innerHTML = content
		document.querySelector(`.header-text-${category[1]}`).innerHTML = title

		document.querySelector(`.grid-parent-container-${category[1]}`).style.height = '500px'
		document.querySelector(`.grid-parent-container-${category[1]}`).style.width = '80%'
		document.querySelector(`.grid-parent-container-${category[1]}`).style.placeItems = 'center'
		document.querySelector(`.grid-parent-container-${category[1]}`).style.overflowX = 'hidden'
		document.querySelector(`.grid-parent-container-${category[1]}`).style.overflowY = 'auto'

		document.querySelector(`.header-text-${category[1]}`).style.width = '100%'
		
		document.querySelector(`.grid-container-${category[1]}`).style.width = '100%'



	} if (category == 'info') {
		document.querySelector("#ModalFlash-icon").src = `${icon_folder_url}/myicon-info.png`
	} if (category == 'success') {
		document.querySelector("#ModalFlash-icon").src = `${icon_folder_url}/myicon-check.png`
	} if (category == 'error') {
		document.querySelector("#ModalFlash-icon").src = `${icon_folder_url}/myicon-cross.png`
	} 
}
function ModalFlashHide(){
	document.querySelector("#ModalFlash-overlay").style.display = 'none'
}
// ScreenManager.js
console.log(`[INFO]: Loaded page to screen ${current_screen}`)

const screen_definitions = {
	"1": ["home-screen", "home-tab"] ,
	"2": ["new-screen", "new-tab"] ,
	"3": ["profile-screen", "profile-tab"] ,
	"4": ["view-assignment-screen", ""],
	"5": ['hire-screen', ''],
	"6": ['go-pro-screen', ''],
	"7": ['notification-screen', 'notification-tab'],
	"8": ['view-notification-screen', ''],
	"9": ['broadcast-screen', 'broadcast-tab'],
	"10": ['users-screen', 'users-tab'],
	"11": ['new-quiz-screen', ''],
	"12": ['answer-quiz-screen', ''],
	"13": ['new-form-screen', ''],
	"14": ['answer-form-screen', ''],
	"15": ["learning-materials-screen", 'study-tab'],
	"16": ['user-forms', ''],
	"17": ['create-post-screen', ''],
	"18": ['study-files-screen', ''],
	"19": ['note-100-screen', ''],
	"20": ["calculator-screen", ""],
	"21": ['Note-100-Notes-List', ''],
	"22": ['View-Note-Screen', ''],
	"23": ['Note-100-Notes-List-Free', '']
}

function loadScreen(screen_id) {
	try {
		const screens = document.querySelectorAll(".screen")
		screens.forEach( screen => {
			screen.style.display = 'none'
		})
		const tabs = document.querySelectorAll(`.tab`)
		tabs.forEach( tab => {
			tab.className = "tab"
		})
		document.querySelector(`#${screen_definitions[screen_id][0]}`).style.display = 'block'
		try {
			document.querySelector(`#${screen_definitions[screen_id][1]}`).className = 'tab active-tab'
		} catch(e) {
			console.log(`Doesn't have a trigger button\n${e}`);
		}
		console.log(`[INFO]: Loaded page to screen 👇\nScreen ID: ${screen_id}\nScreen Name: ${screen_definitions[screen_id][0]}`)
	} catch(e) {
		console.log(`Invalid Screen ID\n${e}`);
	}
}

function goToScreen (element, screen_id, display_property) {
	const screens = document.querySelectorAll(".screen")
	screens.forEach( screen => {
		screen.style.display = 'none'
	})
	const tabs = document.querySelectorAll(`.${element.className}`)
	tabs.forEach( tab => {
		// tab.style.borderBottom = '0'
		tab.className = "tab"
	})
	document.querySelector(`#${screen_id}`).style.display = display_property.includes('-das') ? "block" : `${display_property}`
	// element.style.borderBottom = "2px solid #00a8f3"
	if (display_property.includes('-das')) {
		// nothing
	} else {
		element.className = "tab active-tab"
	}
}
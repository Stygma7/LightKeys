async function init() {
	const settings = {
		color: '#FF0000',
		colorW: 0,
		brightness: 100,
	}

	const inputRGB = document.getElementById('colorRGB')
	const inputW = document.getElementById('colorW')
	const inputBrightness = document.getElementById('brightness')

	inputRGB.addEventListener('change', function (e) {
		settings.color = e.target.value
	})

	const response = await fetch('./settings.json')
	const data = await response.json()

	inputRGB.value = data.colorRGB
	inputW.value = data.colorW
	inputBrightness.value = data.brightness

	showValueChange('colorRGB', 'span_RGB')
	showValueChange('colorW', 'span_W')
	showValueChange('brightness', 'span_brightness')
}

function showValueChange(elementValue, elementToShowValue) {
	document.getElementById(elementToShowValue).innerHTML =
		document.getElementById(elementValue).value
}

init()

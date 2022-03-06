const Gpio = require('onoff').Gpio

console.log('PaulaCam starting...')

const trigger = new Gpio(14, 'in', 'both');

trigger.watch((err, value) => triggerPressed(value))

const Ssd1351 = require('ssd1351').Ssd1351;
const oled = new Ssd1351();
oled.clearDisplay().then(r => console.log('CLR'))

function triggerPressed(value) {
    if (value == 1) {
        display().then(r => console.log('CLICK!'))
    }
}

async function display() {
    try {
        const startTime = Date.now();
        await oled.turnOnDisplay()
        while (Date.now() - startTime < 5 * 60 * 1000) {

            oled.clearDisplay();
            oled.drawLine(0, 0, 127, 127, Ssd1351.convertHexColourToRgb('#FF530D'));
            oled.drawLine(127, 0, 0, 127, Ssd1351.convertHexColourToRgb('#00FF00'));
            oled.drawLine(64, 0, 64, 127, Ssd1351.convertHexColourToRgb('#0000FF'));
            oled.drawLine(0, 64, 127, 64);
            oled.drawLine(0, 0, 127, 127, Ssd1351.convertHexColourToRgb('#FF530D'));
            await oled.updateScreen();

            await new Promise(resolve => setTimeout(resolve, 1000));
        }
        await oled.turnOffDisplay();
    } catch (e) {
        console.log(e)
    }

}
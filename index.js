'use strict'

console.log('PaulaCam starting...')

const jimp = require('jimp')

const GpioButtons = require('rpi-gpio-buttons')
const ScatteredStore = require('scattered-store')

const store = ScatteredStore.create('./data', (err) => {
    if (err) {
        // Oops! Something went wrong.
    } else {
        // Initialization done!
    }
})

let buttons = new GpioButtons({pins: [27]})

buttons.on('clicked', pin => {
    triggerPressed().then(r => {
        console.log("Photo has been taken")
    })
})

async function triggerPressed() {
    increaseCounterAndGet().then(counter => {
        let counterFormatted = (counter).toString().padStart(7, '0')
        const filename = `./pics/photo-${counterFormatted}.jpeg`
        console.log(`Taking photo ${filename}`)
        takePhoto(filename)
        // thumbnail(filename, `./thumbs/thumb-${counterFormatted}.jpeg`)
        console.log('CLICK!')
    })
}

async function increaseCounterAndGet() {
    let counter = await store.get('picture-counter')
    if (counter == null) {
        counter = 0
    }
    counter++
    store.set('picture-counter', counter)
    console.log(`Counter ${counter}`)
    return counter
}

function takePhoto(filename) {
    const cameraCommand = `
            libcamera-jpeg \\
                --camera 0 \\
                --output ${filename} \\
                --immediate \\
                --nopreview \\
                --timeout 1
        `
    exec(cameraCommand, (error, stdout, stderr) => {
        if (error) {
            console.log(`Doh! ${error.message}`)
            return
        }
        if (stderr) {
            console.log(`Doh! ${stderr}`)
            return
        }
        console.log(stdout)
    })
}


async function thumbnail(src, dest) {
    const image = await jimp.read(src)
    await image.resize(128, 128)
    await image.writeAsync(dest)
}

buttons.init().then(() => {
    console.log("Yeah!")
})


//const Ssd1351 = require('ssd1351').Ssd1351;
const {exec} = require("child_process");
const path = require("path");
const Jimp = require("jimp");
let timeOfLastUserAction = new Date();


/*process.on('SIGINT', _ => {
    console.log('Caught SIGINT - terminating...')
    trigger.unexport();
});*/

//const oled = new Ssd1351();
//oled.clearDisplay().then(r => console.log('CLR'))


setInterval(async () => {
    const now = new Date()
    if ((now.getTime() - timeOfLastUserAction.getTime()) / 1000 > 20) {
        console.log("Inactive")
        timeOfLastUserAction = now
        //await oled.turnOnDisplay()
        //await oled.turnOffDisplay()
    }
}, 1000)


/*async function display() {
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

}*/

/*
async function img() {
    await oled.turnOnDisplay()
    const Jimp = require("jimp");
    const height = 128, width = 128;
    let i = 0;
    let pixelsBuffer = Array.from({length: height * width * 2});
    const myImage = await Jimp.read(path.join(__dirname, "js.jpeg"));
    await myImage.rgba(false);
    myImage.resize(height, width)
        .scan(0, 0, height, width, function (x, y, idx) {
            const bytes = Ssd1351.convertRgbColourToRgb565(this.bitmap.data[idx + 0], this.bitmap.data[idx + 1], this.bitmap.data[idx + 2], this.bitmap.data[idx + 3]);
            pixelsBuffer[idx / 2] = bytes[0];
            pixelsBuffer[idx / 2 + 1] = bytes[1];
            if (0 === idx) {
                console.info('convert rgb colour to rgb 565 bit colour');
            } else if (height * width === idx / 4) {
                Promise.resolve(pixelsBuffer);
            }
        });

    console.info('draw image');
    oled.RawData = pixelsBuffer;

    pixelsBuffer = oled.RawData;

    await oled.setCursor(0, 0);
    await oled.updateScreen();
}*/

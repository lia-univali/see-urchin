def HTMLbegin(htmlFile):
    htmlFile.write('''
    <!DOCTYPE html>
    <style>
        html {
            padding: 0px;
            margin: 0px;
        }
        body {
            width: 80%;
            margin: auto;
            background-color: #ffffdd;
        }
        #title {
            height: 64px;
            width: 100%;
            text-align: center;
            font-family: Arial;
            font-size: 52;
            text-shadow: 0px 0px 3px;
            padding: 5px 25px 5px 25px;
        }
        #bigPictureBase {
            position: relative;
            display: inline-block;
            padding: 0px 0px 0px 0px;
            margin: 100px 5% 50px 5%;
            width: 39%;
            max-height: 1000px;
        }
        #bigPictureBase:hover #bigPicture {
            filter: brightness(0.8);
            z-index: 3;
        }
        #bigPictureBase:hover #infoTextBox {
            z-index: 2;
            padding: 5px 0px 0px 10px;
            position: absolute;
            display: inline-block;
            height: 80px;
            width: 200px;
        }
        #bigPicture {
            background-color: black;
            box-shadow: 0px 0px 10px 2px;
            display: inline-block;
            width: 100%;
            height: auto;
        }
        #imageAndInfoBar {
            background-color: aqua;
            display: block;
            height: 100px;
            width: 100%;
            padding: 0px 0px 20px 0px;
        }
        #imgBase {
            background-color: black;
            position: relative;
            display:inline-block;
            top: 15%;
            padding: 0px;
            margin: 0px 0px 10px 10px;
            height: 64px;
            width: 64px;
            box-shadow: 0px 0px 10px 2px;
        }
        #imgBase:hover #tinyPicture {
            opacity: 0.8;
        }
        #imgBase:hover #infoTextBox {
            z-index: 5;
            padding: 5px 0px 0px 10px;
            position: absolute;
            display: inline-block;
            height: 80px;
            width: 200px;
        }
        #tinyPicture {
            width: 64px;
            height: 64px;
        }
        #infoTextBox {
            font-family: Arial, Helvetica, sans-serif;
            display: none;
            height: 90%;
            width: 90%;
            position: relative;
            top: 15%;
            background-color: #ccc;
            opacity: 0.8;
        }
        #imageInfo {
            position: relative;
            margin: 0px;
        }
    </style>
    <body>
        <h1 id="title">
            Larvae Identification Process Report
        </h1>
    ''')

def HTMLBigPicture(htmlFile, pathName, imageInfo):
    htmlFile.write(f'''
    <div id="bigPictureBase">
        <img src="{pathName}" id="bigPicture">
        <div id="infoTextBox">
            <p id="imageInfo"> There are {imageInfo.numberOfLarvae} larvae</p>
            <p id="imageInfo"> in this image; </p>
            <p id="imageInfo"> {imageInfo.numberOfEggs} of them are eggs; </p>
            <p id="imageInfo"> {imageInfo.numberOfAdults} of them are adults. </p>
        </div>
    </div>
    ''')

def HTMLBar(htmlFile, imagePath, currentLarvae, larvaeNumber):
    htmlFile.write(f'''
    <div id=\"imgBase\">
        <img src="{imagePath}" id="tinyPicture">
        <div id="infoTextBox">
            <p id="imageInfo"> Larvae #{larvaeNumber}: </p>
            <p id="imageInfo"> Position: ({currentLarvae.x}, {currentLarvae.y}); </p>
            <p id="imageInfo"> Width: {currentLarvae.w}, Height: {currentLarvae.h}; </p>
            <p id="imageInfo"> Evolution stage: {currentLarvae.evolStage}. </p>
        </div>
    </div>
    ''')

def HTMLlineBreak(htmlFile):
    htmlFile.write('''<br>''')
        
def HTMLend(htmlFile):
    htmlFile.write('''
    </body>
    </html>
    ''')

def HTMLwrite(htmlFile, string):
    htmlFile.write(string)
def beginHTML(htmlFile):
    htmlFile.write('''
    <!DOCTYPE html>
    <style>
        html, body {
            padding: 0px;
            margin: 0px;
        }
        #title {
            height: 64px;
            width: 100%;
            text-align: center;
            font-family: Arial;
            font-size: 52;
            padding: 5px 25px 5px 25px;
        }
        #bigPicture {
            display: inline-block;
            height: 307px; /* 1536 */
            width: 409px; /* 2048 */
            margin: 100px 0px 50px 10px;
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
            margin: 0px 0px 0px 10px;
            height: 64px;
            width: 64px;
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

def makeHTMLBigPicture(htmlFile, pathName):
    htmlFile.write(f'''
    <img src="{pathName}" id="bigPicture">
    ''')

def makeHTMLBar(htmlFile, imagePath, currentLarvae, larvaeNumber):
    htmlFile.write(f'''
    <div id="imgBase">
        <img src="{imagePath}" id="tinyPicture">
        <div id="infoTextBox">
            <p id="imageInfo"> Larvae #{larvaeNumber}: </p>
            <p id="imageInfo"> Position: ({currentLarvae.x}, {currentLarvae.y}); </p>
            <p id="imageInfo"> Width: {currentLarvae.w}, Height: {currentLarvae.h}; </p>
            <p id="imageInfo"> Evolution stage: Unknown. </p>
        </div>
    </div>
    ''')
        
def endHTML(htmlFile):
    htmlFile.write('''
    </body>
    </html>
    ''')

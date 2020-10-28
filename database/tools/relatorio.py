
class HTML:
    @staticmethod
    def begin(arquivoHTML):
        arquivoHTML.write('''
        <!DOCTYPE html>
        <head>
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
                ::-webkit-scrollbar {
                    position: absolute;
                    width: 8px;
                    background-color: rgba(0, 0, 0, 0);
                }
                ::-webkit-scrollbar:hover {
                    background-color: rgba(0, 0, 0, 0.2);
                }
                ::-webkit-scrollbar-thumb {
                    background-color: rgba(0, 0, 0, 0.3);
                    width: 100px;
                    border-radius: 100px;
                }
                ::-webkit-scrollbar-thumb:hover{
                    background-color: rgba(0, 0, 0, 0.6);
                }
                p {
                    font-family: Arial;
                }
                a {
                    color: white;
                }
                #title {
                    height: 64px;
                    text-align: center;
                    font-family: Arial;
                    font-size: 52;
                    text-shadow: 0px 0px 2px;
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
                    transform: scale(1.1);
                    transition-duration: 200ms;
                }
                #bigPictureBase:hover #infoTextBox {
                    z-index: 2;
                    padding: 5px 0px 0px 10px;
                    position: absolute;
                    display: inline-block;
                    left: 105%;
                    height: 100px;
                    width: 200px;
                }
                #bigPicture {
                    background-color: black;
                    box-shadow: 0px 0px 10px 3px;
                    display: inline-block;
                    width: 100%;
                    height: auto;
                }
                #imgBase {
                    position: relative;
                    display:inline-block;
                    top: 15%;
                    padding: 0px;
                    margin: 0px 0px 10px 10px;
                    height: 68px;
                    width: 68px;
                }
                #imgBase:hover #tinyPicture {
                    z-index: 4;
                    transition-duration: 200ms;
                    transform: scale(1.2);
                    filter: brightness(0.8);
                }
                #imgBase:hover #infoTextBox {
                    z-index: 5;
                    padding: 5px 0px 0px 10px;
                    position: absolute;
                    display: inline-block;
                    height: 100px;
                    width: 200px;
                    left: -7px;
                    top: -91px;
                }
                #tinyPicture {
                    width: 64px;
                    height: 64px;
                    border-width: 2px;
                    border-style: solid;
                    box-shadow: 0px 0px 10px 3px;
                }
                #infoTextBox {
                    font-family: Arial, Helvetica, sans-serif;
                    display: none;
                    top: 15%;
                    background-color: #ccc;
                    opacity: 0.8;
                }
                #imageInfo {
                    position: relative;
                    margin: 0px;
                }
                footer {
                    width: 100%;
                    height: 100px;
                    background-color: #bb9;
                    position: absolute;
                    left: 0px;
                }
                #footerInfo {
                    color: white;
                    font-family: Arial, Helvetica, sans-serif;
                    width: 100%;
                    text-align: center;
                    font-size: x-small;
                    margin-bottom: 0px;
                    margin-top: 5px;
                    position: relative;
                    top: 60px;
                }
                #footerLogo {
                    height: 50px;
                    width: auto;
                    position: relative;
                    left: 10px;
                    top: 8px;
                    margin-right: 10px;
                }
                #footerLogo:hover {
                    filter: brightness(0.9);
                }
            </style>
            <link rel="icon" href="https://i.imgur.com/KpZnbS7.png">
        </head>
        <body>
            <h1 id="title">
                Larvae Identification Process Report
            </h1>
        ''')

    @staticmethod
    def bigPicture(arquivoHTML, caminho, infoImagem, numeroImagem):
        arquivoHTML.write(f'''
        <div id="bigPictureBase">
            <img src="{caminho}" id="bigPicture">
            <div id="infoTextBox">
                <p id="imageInfo"> Image #{numeroImagem}</p>
                <p id="imageInfo"> There are {infoImagem.numeroLarvas} larvae</p>
                <p id="imageInfo"> in this image; </p>
                <p id="imageInfo"> {infoImagem.numeroOvos} of them are eggs; </p>
                <p id="imageInfo"> {infoImagem.numeroAdultos} of them are adults. </p>
            </div>
        </div>
        ''')

    @staticmethod
    def bar(arquivoHTML, caminho, larvaAtual, numeroLarva):
        arquivoHTML.write(f'''
        <div id=\"imgBase\">
        ''')
        if(larvaAtual.estagioEvolutivo == "Egg"):
            arquivoHTML.write(f"<img src=\"{caminho}\" id=\"tinyPicture\" style=\"border-color: #ff7\">")
        elif(larvaAtual.estagioEvolutivo == "Larvae"):
            arquivoHTML.write(f"<img src=\"{caminho}\" id=\"tinyPicture\" style=\"border-color: #7ff\">")
        else:
            arquivoHTML.write(f"<img src=\"{caminho}\" id=\"tinyPicture\" style=\"border-color: #111\">")
        arquivoHTML.write(f'''
            <div id="infoTextBox">
                <p id="imageInfo"> Larvae #{numeroLarva}: </p>
                <p id="imageInfo"> Position: ({larvaAtual.x}, {larvaAtual.y}); </p>
                <p id="imageInfo"> Width: {larvaAtual.w}, Height: {larvaAtual.h}; </p>
                <p id="imageInfo"> Length: {larvaAtual.comprimento}px ({round((larvaAtual.comprimento / 90) * 100, 2)}µm); </p>
                <p id="imageInfo"> Evolution stage: {larvaAtual.estagioEvolutivo}. </p>
            </div>
        </div>
        ''')

    @staticmethod
    def lineBreak(arquivoHTML):
        arquivoHTML.write('''<br>''')

    @staticmethod
    def end(arquivoHTML):
        arquivoHTML.write('''
                <div style=\"margin: 100px 0px 50px 0px;\">
                    <div style=\"display: inline-block; border: solid 1px black; background-color: #7ff; width: 10px; height: 10px;\"></div>
                    <p style=\"display: inline\"> - Adult Larvae; </p>
                    <br>
                    <div style=\"display: inline-block; border: solid 1px black; background-color: #ff7; width: 10px; height: 10px;\"></div>
                    <p style=\"display: inline;\"> - Egg; </p>
                </div>
                <footer>
                    <p id="footerInfo">&copy Copyright <a href="https://github.com/lia-univali/See_Urchin">See_Urchin</a> Davi Mello</p>
                    <p id="footerInfo">In colaboration with <a href="https://www.univali.br">Univali - Universidade do Vale de Itajaí</a></p>
                    <a href="https://www.univali.br" style="color: rgba(0, 0, 0, 0)">
                        <img id="footerLogo" src="https://intranet.univali.br/intranet/wireless/ajuda/img/logo.png">
                    </a>
                    <a href="https://github.com/lia-univali/See_Urchin" style="color: rgba(0, 0, 0, 0)">
                        <img id="footerLogo" src="https://i.imgur.com/KpZnbS7.png">
                    </a>
                </footer>
            </body>
        </html>
        ''')

    @staticmethod
    def write(arquivoHTML, string):
        arquivoHTML.write(string)
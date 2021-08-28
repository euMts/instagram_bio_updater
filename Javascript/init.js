//github.com/euMts
const puppeteer = require('puppeteer');
const constants = require('./constants');

// - DEFININDO FUNÇÕES -
// x é y porcento de z
function percent(x, z){ // Ex. 585 dias é quanto porcento de 1440 dias? | percent(585, 1440) | output = 40.6 
  y = (x*100)/z;
  //console.log(String(x) + " é " + String(y.toFixed(1)) + "% de " + String(z))
  return y.toFixed(1);
}

// quantos dias já foram
function dateToDays(){
  let hoje = new Date();
  let diaAtual = String(hoje.getDate()).padStart(2, '0');
  let mesAtual = String(hoje.getMonth() + 1).padStart(2, '0'); //January is 0!
  let anoAtual = hoje.getFullYear();
  let diasRestantes = (diaAtual - 1) // comecei no dia 01/01/2020
  let mesesRestantes = (mesAtual - 1)*30; // convertendo para dias
  let anosRestantes = (anoAtual - 2020)*360; // convertendo para dias
  let jaPassaram = (diasRestantes + mesesRestantes + anosRestantes);
  return jaPassaram;
}

// editar bio instagram
async function editarBio(login, senha){ // logarInstagram
    let options = {
        headless: true, // true = não mostra o navegador, false mostra o navegador
        defaultViewport: {
          width: 400,
          height: 830,
        },
      };
    let texto = (`•FAG - Eng. Software ${percent(dateToDays(), 1440)}%\n•Toledo/Cascavel - PR\n•19y`);
    const browser = await puppeteer.launch(options);
    const page = await browser.newPage();
    const loginSelector = ('#loginForm > div > div:nth-child(1) > div > label > input');
    const senhaSelector = ('#loginForm > div > div:nth-child(2) > div > label > input');
    const botaoEntrarSelector = ('#loginForm > div > div:nth-child(3) > button');
    const bioTextAreaSelector = ('#pepBio');
    const botaoSalvarBioSelector = ('#react-root > section > main > div > article > form > div:nth-child(10) > div > div > button');
    const perfilSalvoSelector = ('body > div._-rjm > div > div > div > p');
    page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36');
    console.log("Entrando no instagram");
    await page.goto('https://www.instagram.com/');
    await page.waitForSelector(loginSelector); // espera o selector ficar disponivel
    console.log("Enviando login...")
    await page.type(loginSelector, login);
    console.log("Enviando senha...")
    await page.type(senhaSelector, senha);
    await page.click(botaoEntrarSelector);
    await page.waitForNavigation(); // espera a pag carregar
    console.log("Logado como " + String(login));
    await page.goto('https://www.instagram.com/accounts/edit/');
    console.log("Editando informações...");
    await page.waitForSelector(bioTextAreaSelector);
    await page.evaluate(bioTextAreaSelector => {document.querySelector(bioTextAreaSelector).value = "";}, bioTextAreaSelector); // limpando textarea
    await page.type(bioTextAreaSelector, texto);
    console.log("Salvando...");
    await page.click(botaoSalvarBioSelector);
    console.log("Salvo, deslogando...");
    await page.waitForSelector(perfilSalvoSelector);
    await page.goto('https://www.instagram.com/accounts/logout');
    await page.waitForSelector(loginSelector);
    console.log("Deslogado.");
    browser.close();
    console.log("Finalizado com sucesso.");
  }

editarBio(constants.loginInsta, constants.senhaInsta);
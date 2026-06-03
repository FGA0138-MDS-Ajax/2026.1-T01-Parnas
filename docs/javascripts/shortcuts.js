// Atalhos de teclado — CrediFab / Grupo Parnas

// "Ir para": tecla g seguida de...
const goTo = {
  h: "",                            // Home
  g: "sobre/",                      // o Grupo
  p: "produto/",                    // Produto
  v: "produto/visao/",              // documento de Visão
  a: "produto/arquitetura/",        // documento de Arquitetura
  q: "qualidade/",                  // Qualidade
  r: "qualidade/roteiro-testes/",   // Roteiro de testes
  t: "atas-reuniao/",               // aTas
};

let prefixOn = false;
let prefixTimer = null;

function siteRoot() {
  const logo = document.querySelector("a.md-logo");      // href = raiz do site
  return logo ? logo.href : location.origin + "/";       // respeita o subpath do GH Pages
}

keyboard$.subscribe(function (key) {
  if (key.mode !== "global") return;                     // ignora quando digitando na busca

  // 1) ativa o modo "ir para" ao apertar g
  if (!prefixOn && key.type === "g") {
    prefixOn = true;
    key.claim();
    clearTimeout(prefixTimer);
    prefixTimer = setTimeout(() => (prefixOn = false), 1500);
    return;
  }

  // 2) segunda tecla da sequência g + ?
  if (prefixOn) {
    prefixOn = false;
    clearTimeout(prefixTimer);
    const dest = goTo[key.type];
    if (dest !== undefined) {
      location.href = new URL(dest, siteRoot()).href;
      key.claim();
    }
    return;
  }

  // 3) atalhos diretos (teclas livres)
  if (key.type === "m") {                                // m = muda o tema
    const inputs = [...document.querySelectorAll(
      'form[data-md-component="palette"] input'
    )];
    const i = inputs.findIndex((el) => el.checked);
    const next = inputs[(i + 1) % inputs.length];
    if (next) { next.click(); key.claim(); }
  }

  if (key.type === "y") {                                // y = copia a URL da página
    navigator.clipboard?.writeText(location.href);
    key.claim();
  }
});

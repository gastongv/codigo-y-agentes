// GriftIA tipográfico (idea A, inspirada en el anuncio tipográfico del pollo): 1080x1920, ~16,5 s, sin voz, una palabra por golpe.
// Música: Tech Live (Kevin MacLeod, CC BY 4.0) desde el tramo de más energía (fuente/golpes.json). Paleta del manual; logo sin efectos.
// Guion "Agentes de IA" (aprobado 2026-11-03): agentes de IA que responden por WhatsApp e Instagram y agendan turnos, 24/7. Nada de pagos ni webchat.
// Uso: node fuente/build.mjs
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

const RAIZ = fileURLToPath(new URL("../", import.meta.url));
const W = 1080, H = 1920;
const C = { noche: "#0B1F3B", cian: "#00D1B2", celeste: "#2EC5FF", violeta: "#6C63FF", gris: "#F3F6F9" };
const { golpes } = JSON.parse(readFileSync(`${RAIZ}fuente/golpes.json`, "utf8"));
const B = (i) => +(golpes[i] ?? golpes.at(-1) + (i - golpes.length + 1) * 0.4875).toFixed(3);
const DUR = +(B(29) + 2.4).toFixed(2);

// Tarjetas: [id, golpe de entrada, golpe de salida, fondo, color de texto, contenido HTML, tipo]
const CI = (t) => "<span style='color:" + C.cian + "'>" + t + "</span>";
const T = [
  ["te", 0, 2, C.cian, C.noche, "¿TE<br/>ESCRIBEN", "letras"],
  ["3am", 2, 4, C.noche, "#fff", "A LAS<br/>" + CI("3 AM?"), "pal"],
  ["domingo", 4, 6, C.noche, C.cian, "¿UN<br/>DOMINGO?", "pal"],
  ["quien", 6, 8, C.cian, C.noche, "¿QUIÉN<br/>RESPONDE?", "eco"],
  ["logo", 8, 12, C.gris, C.noche, "", "logo"],
  ["agentes", 12, 14, C.noche, "#fff", "AGENTES<br/>" + CI("DE IA"), "pal"],
  ["responden", 14, 18, "#000", "#fff", "RESPONDEN", "patron"],
  ["whatsapp", 18, 19, C.cian, C.noche, "WHATSAPP", "golpe"],
  ["instagram", 19, 20, C.noche, C.cian, "INSTAGRAM", "golpe"],
  ["agendan", 20, 22, C.celeste, C.noche, "AGENDAN<br/>TURNOS", "pal"],
  ["247", 22, 23, C.noche, "#fff", CI("24/7"), "golpe"],
  ["vos", 23, 25, C.noche, C.cian, "", "vos"],
  ["hoy", 25, 27, C.cian, C.noche, "¡IMPLEMENTALO<br/>HOY!", "pal"],
  ["escribinos", 27, 28, C.noche, "#fff", "ESCRIBINOS", "golpe"],
  ["wa", 28, 29, C.cian, C.noche, "POR<br/>WHATSAPP", "golpe"],
  ["fin", 29, null, C.gris, C.noche, "", "fin"],
];

let nl = 0;
const letras = (s) => s.split("<br/>").map((parte) => [...parte].map((ch) => `<span class="l${ch === "¿" ? " ab" : ""}" id="l-${nl++}">${ch}</span>`).join("")).join("<br/>");
// El "¿" de Spartan cuelga bajo la línea: se sube para que no pise el renglón de abajo
const AB = (t) => t.replace(/¿/g, "<span class='ab'>¿</span>");
const tarjeta = ([id, , , fondo, color, crudo, tipo]) => {
  const html = tipo === "letras" ? crudo : AB(crudo);
  let dentro = "";
  if (tipo === "letras") dentro = `<div class="txt ajusta" id="tx-${id}">${letras(html)}</div>`;
  else if (tipo === "eco") dentro = [-2, -1, 1, 2].map((k) => `<div class="txt eco ajusta" id="eco-${k}" data-k="${k}">${html}</div>`).join("") + `<div class="txt ajusta" id="tx-${id}">${html}</div>`;
  else if (tipo === "logo") dentro = `<img id="logo-g" src="assets/logo/griftia-logo-vertical.svg" alt="GriftIA" />`;
  else if (tipo === "patron") dentro = `<video id="v-msj" class="clip" src="assets/clips/mensajes.mp4" muted playsinline data-start="${B(14)}" data-duration="${+(B(18) - B(14)).toFixed(3)}" data-track-index="2"></video><div id="oscuro"></div>`
    + Array.from({ length: 9 }, (_, r) => r === 4 ? "" : `<div class="fila" id="fila-${r}" style="top:${110 + r * 190}px">${"MENSAJE RESPONDIDO · ".repeat(4)}</div>`).join("")
    + `<div class="txt ajusta" id="tx-${id}">${html}</div>`;
  else if (tipo === "vos") dentro = `<div class="txt" id="vos-a">${AB("¿Y TU")}</div><div class="txt" id="vos-b">NEGOCIO?</div>`;
  else if (tipo === "fin") dentro = `<div id="fin-pila"><img id="fin-logo" src="assets/logo/griftia-logo-vertical.svg" alt="GriftIA" /><div id="fin-lema">Agentes de IA que responden<br/>y agendan, 24/7</div><div id="fin-wa">Escribinos por WhatsApp</div><div id="fin-url">griftia.com.ar</div></div>`;
  else dentro = `<div class="txt ajusta" id="tx-${id}">${html}</div>`;
  return `<div class="tarjeta" id="t-${id}"${tipo === "patron" || tipo === "eco" ? " data-layout-allow-overflow data-layout-allow-overlap" : ""} style="background:${fondo};color:${color}">${dentro}</div>`;
};

const html = `<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      @font-face { font-family: "Spartan"; src: url("assets/fonts/Spartan-Variable.ttf"); font-weight: 100 900; }
      @font-face { font-family: "Manrope"; src: url("assets/fonts/Manrope-latin.woff2"); font-weight: 200 800; }
      * { box-sizing: border-box; margin: 0; padding: 0; }
      html, body { width: ${W}px; height: ${H}px; background: #000; overflow: hidden; }
      #root { position: relative; width: ${W}px; height: ${H}px; overflow: hidden; background: ${C.noche}; font-family: "Spartan", sans-serif; }
      .tarjeta { position: absolute; inset: 0; opacity: 0; overflow: hidden; }
      .txt { position: absolute; left: 60px; right: 60px; top: 50%; text-align: center; font-weight: 900; line-height: 1.12; letter-spacing: -0.035em; text-transform: uppercase; white-space: nowrap; }
      .l { display: inline-block; }
      .ab { position: relative; top: -0.17em; }
      .eco { color: transparent; -webkit-text-stroke: 4px ${C.noche}; opacity: 0; }
      #logo-g { position: absolute; left: 190px; width: 700px; top: 620px; opacity: 0; }
      #v-msj { position: absolute; inset: 0; width: ${W}px; height: ${H}px; object-fit: cover; }
      #oscuro { position: absolute; inset: 0; background: rgba(4,9,20,0.55); }
      .fila { position: absolute; left: -400px; white-space: nowrap; font-weight: 900; font-size: 110px; letter-spacing: -0.02em; color: ${C.cian}; opacity: 0.9; }
      #tx-responden { color: #fff; text-shadow: 0 6px 40px rgba(0,0,0,0.6); }
      #vos-a { left: 80px; right: auto; top: 520px; font-size: 260px; text-align: left; }
      #vos-b { left: auto; right: 80px; top: 960px; font-size: 200px; text-align: right; }
      #fin-pila { position: absolute; left: 0; right: 0; top: 500px; display: flex; flex-direction: column; align-items: center; gap: 46px; }
      #fin-logo { width: 620px; opacity: 0; }
      #fin-lema { font-family: "Manrope", sans-serif; font-weight: 700; font-size: 50px; line-height: 1.25; text-align: center; color: ${C.noche}; opacity: 0; }
      #fin-wa { font-weight: 800; font-size: 62px; color: ${C.noche}; opacity: 0; }
      #fin-url { font-family: "Manrope", sans-serif; font-weight: 800; font-size: 48px; color: ${C.noche}; opacity: 0; padding: 10px 30px; border-radius: 40px; background: ${C.cian}; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="${DUR}" data-width="${W}" data-height="${H}">
      ${T.map(tarjeta).join("\n      ")}
      <audio id="bgm" src="assets/bgm/bgm.mp3" data-start="0" data-duration="${DUR}" data-track-index="20" data-volume="0.9"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {};
      // Ajuste determinista: cada palabra ocupa ~900 px de ancho (medido una vez, no depende del tiempo)
      for (const el of document.querySelectorAll(".ajusta")) {
        el.style.fontSize = "200px";
        const ancho = Math.max(...el.innerHTML.split(/<br\\s*\\/?>/i).map((parte) => { const s = document.createElement("span"); s.style.cssText = "position:absolute;visibility:hidden;white-space:nowrap;font:900 200px Spartan;letter-spacing:-0.035em"; s.innerHTML = parte; document.body.appendChild(s); const w = s.getBoundingClientRect().width; s.remove(); return w; }));
        const fs = Math.min(330, 200 * 920 / ancho);
        el.style.fontSize = fs + "px";
        const lineas = el.innerHTML.split(/<br\\s*\\/?>/i).length;
        el.style.marginTop = (-fs * 1.12 * lineas / 2 + fs * 0.06) + "px";
      }
      for (const el of document.querySelectorAll(".eco")) { const fs = parseFloat(el.style.fontSize), lineas = el.innerHTML.split(/<br\\s*\\/?>/i).length; el.style.marginTop = (parseFloat(el.style.marginTop) + (+el.dataset.k) * (fs * 1.12 * lineas + 24)) + "px"; }
      // "¿Y TU" / "NEGOCIO?": cada renglón entra en 900 px de ancho
      for (const el of document.querySelectorAll("#vos-a, #vos-b")) { const base = parseFloat(getComputedStyle(el).fontSize); const s = document.createElement("span"); s.style.cssText = "position:absolute;visibility:hidden;white-space:nowrap;font:900 " + base + "px Spartan;letter-spacing:-0.035em"; s.textContent = el.textContent; document.body.appendChild(s); const w = s.getBoundingClientRect().width; s.remove(); if (w > 900) el.style.fontSize = (base * 900 / w) + "px"; }
      const tl = gsap.timeline({ paused: true });
      const B = ${JSON.stringify(Array.from({ length: 34 }, (_, i) => B(i)))};
      const T = ${JSON.stringify(T.map(([id, a, b, , , , tipo]) => [id, a, b, tipo]))};
      for (const [id, a, b, tipo] of T) {
        const ta = B[a], tb = b === null ? ${DUR} : B[b];
        tl.set("#t-" + id, { opacity: 1 }, ta);
        if (b !== null) tl.set("#t-" + id, { opacity: 0 }, tb);
        const tx = "#tx-" + id;
        if (tipo === "letras") {
          tl.fromTo("#t-" + id + " .l", { y: 120 }, { y: 0, duration: 0.22, ease: "power3.out", stagger: 0.05, immediateRender: ta === 0 }, ta);
          tl.to("#t-" + id + " .txt", { scale: 1.08, duration: B[a + 1] - ta, ease: "none" }, ta);
        } else if (tipo === "pal" || tipo === "golpe" || tipo === "eco" || tipo === "patron") {
          tl.fromTo(tx, { scale: 1.35, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.14, ease: "power3.out", immediateRender: false }, ta);
          tl.to(tx, { scale: 0.94, duration: tb - ta - 0.14, ease: "none" }, ta + 0.14);
        }
        if (tipo === "eco") [1, -1, 2, -2].forEach((k, i) => tl.fromTo("#eco-" + k, { opacity: 0 }, { opacity: 1, duration: 0.05, immediateRender: false }, ta + 0.12 + i * 0.1));
        if (tipo === "logo") tl.fromTo("#logo-g", { opacity: 0 }, { opacity: 1, duration: 0.35, ease: "power1.out", immediateRender: false }, ta);
        if (tipo === "patron") for (let r = 0; r < 9; r++) if (r !== 4) tl.fromTo("#fila-" + r, { x: r % 2 ? -260 : 0 }, { x: r % 2 ? 0 : -260, duration: tb - ta, ease: "none", immediateRender: false }, ta);
        if (tipo === "vos") {
          tl.fromTo("#vos-a", { x: -120, opacity: 0 }, { x: 0, opacity: 1, duration: 0.16, ease: "power3.out", immediateRender: false }, ta);
          tl.fromTo("#vos-b", { x: 120, opacity: 0 }, { x: 0, opacity: 1, duration: 0.16, ease: "power3.out", immediateRender: false }, B[a + 1]);
        }
        if (tipo === "fin") {
          tl.fromTo("#fin-logo", { opacity: 0 }, { opacity: 1, duration: 0.35, immediateRender: false }, ta);
          tl.fromTo("#fin-lema", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.25, immediateRender: false }, B[a + 1]);
          tl.fromTo("#fin-wa", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.25, immediateRender: false }, B[a + 2]);
          tl.fromTo("#fin-url", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.25, immediateRender: false }, B[a + 3]);
        }
      }
      tl.set({}, {}, ${DUR});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
`;
writeFileSync(`${RAIZ}index.html`, html);
console.log(`index.html: ${T.length} tarjetas, ${DUR} s`);

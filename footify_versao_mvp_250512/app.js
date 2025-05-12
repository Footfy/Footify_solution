if (!localStorage.getItem("user_id")) {
  localStorage.setItem("user_id", crypto.randomUUID());
}
const userId = localStorage.getItem("user_id");


const submitBtn = document.getElementById("submitBtn");

const typingSound = new Audio("media/typing.mp3");
typingSound.volume = 0.3;
let typingSoundTimeout;

submitBtn.addEventListener("click", async (e) => {
  e.preventDefault();
  const descricao = document.getElementById("descricao").value.trim();
  if (!descricao) return;

  adicionarMensagem(descricao, "user");
  document.getElementById("descricao").value = "";

  const typingId = adicionarTyping("bot");

  try {
    const response = await fetch("http://127.0.0.1:5500/perguntar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mensagem: descricao, user_id: userId })

    });

    if (!response.ok) throw new Error("Erro na resposta da API.");
    const result = await response.json();

    removerTyping(typingId);
    renderizarCardsAnimados(result.resposta);

    if (result.mostrarImagem && result.imagem) {
      adicionarImagem(result.imagem);
    }
  } catch (error) {
    console.error(error);
    removerTyping(typingId);
    adicionarMensagem("⚠️ Erro ao consultar a IA. Tente novamente.", "bot");
  }
});

const descricaoInput = document.getElementById("descricao");
descricaoInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    submitBtn.click();
  }
});

function adicionarMensagem(texto, tipo) {
  const chat = document.getElementById("chat");
  const msg = document.createElement("div");
  msg.className = `message ${tipo}`;

  if (tipo === "bot") {
    msg.innerHTML = `
      <img src="image/bot_footify.png" alt="Bot" class="avatar">
      <div class="message-content">${texto}</div>
    `;
  } else {
    msg.innerHTML = `<div class="message-content user-content">${texto}</div>`;
  }

  chat.appendChild(msg);
  chat.scrollTop = chat.scrollHeight;
}

function adicionarImagem(src) {
  const chat = document.getElementById("chat");
  const imagem = document.createElement("img");
  imagem.src = src;
  imagem.alt = "Sugestão de tênis";
  imagem.style.maxWidth = "200px";
  imagem.style.margin = "10px 0";
  imagem.style.borderRadius = "12px";
  chat.appendChild(imagem);
  chat.scrollTop = chat.scrollHeight;
}

function adicionarTyping(tipo) {
  const chat = document.getElementById("chat");
  const msg = document.createElement("div");
  msg.className = `message ${tipo} typing`;

  msg.innerHTML = `
    <span class="typing-icon">💬</span>
    <span class="typing-dots">
      <span>.</span><span>.</span><span>.</span>
    </span>
  `;

  msg.id = `typing-${Date.now()}`;
  chat.appendChild(msg);
  chat.scrollTop = chat.scrollHeight;

  try {
    typingSound.currentTime = 0;
    typingSound.play();
    clearTimeout(typingSoundTimeout);
    typingSoundTimeout = setTimeout(() => {
      typingSound.pause();
      typingSound.currentTime = 0;
    }, 3000);
  } catch (e) {
    console.warn("Som de digitação bloqueado até interação do usuário.");
  }

  return msg.id;
}

function removerTyping(id) {
  const msg = document.getElementById(id);
  if (msg) msg.remove();

  typingSound.pause();
  typingSound.currentTime = 0;
  clearTimeout(typingSoundTimeout);
}

function renderizarCardsAnimados(texto, delay = 20) {
  const chat = document.getElementById("chat");
  const blocos = texto.split("\n\n---\n\n");

  let blocoIndex = 0;

  function renderizarBloco() {
    if (blocoIndex >= blocos.length) return;

    const bloco = blocos[blocoIndex].trim();
    if (!bloco) {
      blocoIndex++;
      renderizarBloco();
      return;
    }

    const wrapper = document.createElement("div");
    wrapper.className = "message bot";
    wrapper.innerHTML = `<img src="image/bot_footify.png" alt="Bot" class="avatar">`;

    const card = document.createElement("div");
    card.className = "card-bot";
    wrapper.appendChild(card);
    chat.appendChild(wrapper);
    chat.scrollTop = chat.scrollHeight;

    const linhas = bloco.split("\n\n");
    let linhaIndex = 0;

    function digitarLinha() {
      if (linhaIndex >= linhas.length) {
        blocoIndex++;
        setTimeout(renderizarBloco, 300);
        return;
      }

      const linha = linhas[linhaIndex];
      const linhaEl = document.createElement("div");

      linhaEl.className = linha.includes("🏷️") ? "card-header" : "card-produto";
      linhaEl.innerHTML = linha
        .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
        .replace(
          /\[(.+?)\]\((https?:\/\/[^\s]+?)\)/g,
          '<a href="$2" target="_blank" class="card-link">$1</a>'
        );

      linhaEl.style.animationDelay = `${linhaIndex * 100}ms`;
      card.appendChild(linhaEl);

      chat.scrollTop = chat.scrollHeight;

      linhaIndex++;
      setTimeout(digitarLinha, delay);
    }

    digitarLinha();
  }

  renderizarBloco();
}

// ✅ Resetar sessão e iniciar conversa ao carregar
window.addEventListener("DOMContentLoaded", async () => {
  const typingId = adicionarTyping("bot");

  try {
    // Resetar sessão
    await fetch("https://1051-189-78-76-133.ngrok-free.app/resetar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId , mensagem: "" }) 
    });

    // Iniciar conversa
    const response = await fetch("http://127.0.0.1:5500/resetar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, mensagem: "oi"  })
    });

    if (!response.ok) throw new Error("Erro ao iniciar conversa.");

    const result = await response.json();
    removerTyping(typingId);
    renderizarCardsAnimados(result.resposta);
  } catch (error) {
    console.error(error);
    removerTyping(typingId);
    adicionarMensagem("⚠️ Erro ao iniciar a conversa. Tente atualizar a página.", "bot");
  }
});

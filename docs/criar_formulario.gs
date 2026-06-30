function criarFormulario() {
  var form = FormApp.create("Vida em Movimento — Avaliação do Protótipo");

  form.setDescription(
    "Este questionário é parte de uma pesquisa acadêmica sobre o aplicativo " +
    "de exercícios assistidos por IA. Não há respostas certas ou erradas. " +
    "Suas respostas nos ajudarão a melhorar o aplicativo."
  );

  form.setCollectEmail(false);
  form.setShowLinkToRespondAgain(false);
  form.setConfirmationMessage(
    "Muito obrigado pela sua participação! Sua opinião é muito importante para nós."
  );

  // ── Pergunta 1 ──────────────────────────────────────────────────────────────
  form.addMultipleChoiceItem()
    .setTitle("1. Você conseguiu entender o que fazer na primeira tela do aplicativo, sem que ninguém precisasse explicar?")
    .setChoiceValues(["Sim", "Mais ou menos", "Não"])
    .setRequired(true);

  // ── Pergunta 2 ──────────────────────────────────────────────────────────────
  form.addMultipleChoiceItem()
    .setTitle("2. As letras e os botões eram grandes o suficiente para você ler com facilidade?")
    .setChoiceValues(["Sim", "Mais ou menos", "Não"])
    .setRequired(true);

  // ── Pergunta 3 ──────────────────────────────────────────────────────────────
  form.addMultipleChoiceItem()
    .setTitle("3. Você entendeu o que significa cada nível — Fácil, Médio e Difícil — antes de escolher?")
    .setChoiceValues(["Sim", "Mais ou menos", "Não"])
    .setRequired(true);

  // ── Pergunta 4 ──────────────────────────────────────────────────────────────
  form.addMultipleChoiceItem()
    .setTitle("4. Durante o exercício, você soube se estava fazendo o movimento certo ou errado?")
    .setChoiceValues(["Sim", "Mais ou menos", "Não"])
    .setRequired(true);

  // ── Pergunta 5 ──────────────────────────────────────────────────────────────
  form.addMultipleChoiceItem()
    .setTitle("5. O esqueleto que aparecia na câmera ajudou você a entender como mover o corpo?")
    .setChoiceValues(["Sim", "Mais ou menos", "Não"])
    .setRequired(true);

  // ── Pergunta 6 ──────────────────────────────────────────────────────────────
  form.addMultipleChoiceItem()
    .setTitle("6. Em algum momento você sentiu dor ou desconforto ao fazer os exercícios?")
    .setChoiceValues(["Não", "Sim"])
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle("6a. Se sentiu dor ou desconforto, pode nos dizer onde?")
    .setHelpText("Deixe em branco se respondeu 'Não' na pergunta anterior.")
    .setRequired(false);

  // ── Pergunta 7 ──────────────────────────────────────────────────────────────
  form.addMultipleChoiceItem()
    .setTitle("7. Você se sentiu seguro(a) usando o aplicativo sozinho(a), sem ajuda de outra pessoa?")
    .setChoiceValues(["Sim", "Mais ou menos", "Não"])
    .setRequired(true);

  // ── Pergunta 8 ──────────────────────────────────────────────────────────────
  form.addParagraphTextItem()
    .setTitle("8. Teve alguma parte do aplicativo que te deixou confuso(a) ou que você não soube o que fazer?")
    .setHelpText("Se não teve nenhuma parte confusa, pode escrever 'Nenhuma'.")
    .setRequired(true);

  // ── Pergunta 9 ──────────────────────────────────────────────────────────────
  form.addMultipleChoiceItem()
    .setTitle("9. Se você tivesse esse aplicativo em casa, você o usaria para se exercitar?")
    .setChoiceValues(["Sim", "Talvez", "Não"])
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle("9a. Pode nos dizer o motivo da sua resposta anterior?")
    .setRequired(false);

  // ── Pergunta 10 ─────────────────────────────────────────────────────────────
  form.addParagraphTextItem()
    .setTitle("10. O que você mudaria para deixar o aplicativo mais fácil de usar?")
    .setHelpText("Pode ser qualquer coisa: cor, tamanho das letras, sons, velocidade, etc.")
    .setRequired(false);

  // ── Resultado ───────────────────────────────────────────────────────────────
  var url = form.getPublishedUrl();
  var editUrl = form.getEditUrl();

  Logger.log("✅ Formulário criado com sucesso!");
  Logger.log("🔗 Link para responder: " + url);
  Logger.log("✏️  Link para editar:    " + editUrl);
}

# Confei — Manual da Administradora

---

## 1. Estrutura do app

O app é composto por **3 arquivos**. Sempre que atualizar, os 3 precisam ir juntos no Netlify.

| Arquivo | O que é |
|---|---|
| `index.html` | O app inteiro — telas, lógica, dados, estilo |
| `sw.js` | Controla o modo offline (service worker) |
| `manifest.json` | Informações do app instalável (nome, ícone, cor) |

---

## 2. Como publicar no Netlify (1ª vez)

1. Acesse **[netlify.com/drop](https://app.netlify.com/drop)**
2. Arraste a **pasta** com os 3 arquivos para a área cinza
3. O Netlify gera um link automático (ex: `https://amazing-mango-123.netlify.app`)
4. Esse é o link do seu app — salve ele

> **Dica:** O link gerado é aleatório e não é fácil de adivinhar, mas qualquer pessoa com o link consegue acessar a tela de código. Por isso os códigos de acesso existem.

---

## 3. Como atualizar o app (após editar)

1. Edite o `index.html` com as mudanças desejadas
2. Acesse **[app.netlify.com](https://app.netlify.com)** e faça login
3. Clique no seu site
4. Vá em **Deploys** → arraste a pasta atualizada na área "Drag and drop"
5. O Netlify publica a nova versão no mesmo link em segundos

> As testadoras já com o app instalado recebem a atualização automaticamente na próxima vez que abrirem com internet.

---

## 4. Códigos de acesso — como funcionam

### Onde ficam os códigos

Abra o `index.html` em qualquer editor de texto (Bloco de Notas, VS Code, TextEdit) e procure por:

```
var BETA_CODES = [
  'CONFEI-MINHA',
  'CONFEI-01', 'CONFEI-02', 'CONFEI-03', 'CONFEI-04', 'CONFEI-05',
  'CONFEI-06', 'CONFEI-07', 'CONFEI-08', 'CONFEI-09', 'CONFEI-10'
];
```

### Regras importantes

- **Cada código pode ser usado em vários dispositivos** — por isso, dê um código diferente para cada testadora
- **O código fica salvo no dispositivo** — a testadora só digita uma vez; o app lembra
- **Não é case-sensitive na entrada** — `confei-01` e `CONFEI-01` funcionam igual

### Como adicionar um código novo

1. Abra o `index.html`
2. Encontre o array `BETA_CODES`
3. Adicione a nova linha entre aspas e vírgula:
   ```
   'CONFEI-11',
   ```
4. Salve o arquivo e faça novo deploy no Netlify

### Como revogar acesso de uma testadora

1. Abra o `index.html`
2. Encontre o array `BETA_CODES`
3. **Apague a linha** com o código da pessoa
4. Salve e faça novo deploy
5. Na próxima vez que ela abrir o app (com internet), verá a tela de código novamente e não conseguirá mais entrar

> **Atenção:** A revogação só funciona quando a testadora abre o app com internet. Offline, o app continua funcionando enquanto estiver no cache do celular dela.

### Sugestão de controle — tabela de testadoras

Mantenha uma planilha simples:

| Código | Testadora | Contato | Status |
|---|---|---|---|
| CONFEI-MINHA | Você | — | Ativa |
| CONFEI-01 | Ana Silva | @anasilva | Ativa |
| CONFEI-02 | Maria Souza | (11) 9xxxx | Ativa |
| CONFEI-03 | — | — | Disponível |

---

## 5. Criar códigos personalizados (opcional)

Você pode usar qualquer texto como código, não precisa seguir o padrão `CONFEI-XX`. Exemplos válidos:

```
'BETA-ANA',
'TESTE-JULHO',
'DOCERIA-VIP',
```

A única regra é que o código no array deve estar em **letras maiúsculas** (a testadora pode digitar em minúsculo que funciona).

---

## 6. Dados das usuárias

- Cada testadora tem os **próprios dados isolados no celular dela** — nada é compartilhado entre dispositivos
- Você não tem acesso aos dados delas (não existe servidor)
- Se uma testadora desinstalar o app, ela perde os dados dela

---

## 7. Perguntas frequentes

**A testadora esqueceu o código. O que fazer?**
Ela pode entrar em contato com você. Se ainda tiver o código dela na tabela, reenvie. Se perdeu, crie um novo e dê para ela.

**Posso usar o mesmo link para a versão final (sem beta)?**
Sim. Quando o app estiver pronto para lançamento, basta remover todo o bloco do portão beta do `index.html` e fazer um novo deploy no mesmo site do Netlify.

**O Netlify é gratuito?**
Sim, para sites estáticos como esse. O plano gratuito inclui HTTPS, domínio personalizado e atualizações ilimitadas.

**Como editar o nome do app (Confei) ou a cor?**
No `manifest.json`, edite `"name"`, `"short_name"`, `"theme_color"` e `"background_color"`. No `index.html`, busque por `Confei` para encontrar os textos.

**O app funciona sem internet?**
Sim, após o primeiro acesso com internet, o app fica salvo no celular e funciona 100% offline.

---

## 8. Contato técnico

Para mudanças maiores no app (novas funcionalidades, mudança de visual, etc.), converse com quem desenvolveu o app com as especificações do que precisa.

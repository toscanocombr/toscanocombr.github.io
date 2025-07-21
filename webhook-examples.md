# GitHub Actions Webhooks - Exemplos de Uso

## 🕙 Atualização Diária Automática

O workflow `update-site.yml` executa automaticamente todos os dias às **10:00 AM (horário de Brasília)**.

### Funcionalidades:
- ✅ Execução automática diária
- ✅ Atualização da playlist de vídeos
- ✅ Commit automático das mudanças
- ✅ Deploy para GitHub Pages
- ✅ Logs detalhados

---

## 🔗 Webhook Manual/Externo

O workflow `webhook-trigger.yml` pode ser acionado via:

### 1. **Execução Manual** (via interface do GitHub)
- Vá em: `Actions` → `Webhook Trigger Update` → `Run workflow`
- Personalize a fonte e mensagem

### 2. **API do GitHub** (webhook externo)
```bash
curl -X POST \
  -H "Authorization: token SEU_GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/SEU_USUARIO/toscanocombr.github.io/dispatches \
  -d '{
    "event_type": "update-site-webhook",
    "client_payload": {
      "source": "external-api",
      "message": "Atualização via sistema externo"
    }
  }'
```

### 3. **Via workflow_dispatch** (execução manual)
```bash
curl -X POST \
  -H "Authorization: token SEU_GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/SEU_USUARIO/toscanocombr.github.io/actions/workflows/webhook-trigger.yml/dispatches \
  -d '{
    "ref": "main",
    "inputs": {
      "source": "api-call",
      "message": "Atualização programada via API"
    }
  }'
```

---

## 🔧 Configuração Necessária

### 1. **Habilitar GitHub Pages**
- Vá em: `Settings` → `Pages`
- Source: `Deploy from a branch`
- Branch: `gh-pages` / `/ (root)`

### 2. **Permissões do GitHub Token**
As permissões já estão configuradas nos workflows:
```yaml
permissions:
  contents: write
  pages: write
  id-token: write
```

### 3. **Variáveis de Ambiente** (opcional)
Se precisar de tokens ou chaves API:
- Vá em: `Settings` → `Secrets and variables` → `Actions`
- Adicione suas secrets

---

## 📝 Personalização

### Modificar horário da execução diária:
No arquivo `update-site.yml`, altere a linha:
```yaml
- cron: '0 10 * * *'  # 10:00 UTC = 07:00 Brasília
```

**Exemplos de horários:**
- `'0 13 * * *'` = 10:00 AM Brasília (horário padrão)
- `'0 12 * * *'` = 09:00 AM Brasília (horário de verão)
- `'30 14 * * *'` = 11:30 AM Brasília

### Adicionar mais atualizações:
Edite a seção "Update playlist videos" nos workflows para incluir:
- Atualização de dados externos
- Geração de conteúdo dinâmico
- Sincronização com APIs

---

## 🚀 Como Usar

1. **Commit os arquivos** para o repositório
2. **Aguardar execução automática** às 10h da manhã
3. **Ou acionar manualmente** via interface do GitHub
4. **Ou usar webhook** via API externa

### Verificar execuções:
- Vá em: `Actions` no GitHub
- Veja o histórico de execuções
- Verifique logs detalhados

---

## 🔍 Monitoramento

### Logs disponíveis:
- ✅ Timestamp de execução
- ✅ Mudanças detectadas
- ✅ Status do deploy
- ✅ Informações do trigger

### Arquivos gerados:
- `last_update.txt` - Timestamp da última atualização
- `webhook_update.log` - Log das atualizações via webhook
- Arquivos atualizados da playlist (se configurado)

---

## 🆘 Troubleshooting

### Workflow não executa:
- Verifique se o repositório está ativo
- Confirme que as Actions estão habilitadas
- Verifique permissões do token

### Deploy falha:
- Confirme configuração do GitHub Pages
- Verifique se a branch `gh-pages` existe
- Confirme permissões de escrita

### Webhook não funciona:
- Verifique o token do GitHub
- Confirme a URL do repositório
- Teste primeiro com execução manual
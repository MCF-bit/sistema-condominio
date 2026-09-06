# sistema-condominio
# Sistema de Gestão de Condomínio (sis_cond.py)

Sistema simples em Python, com banco de dados SQLite, para controle de pagamentos de condomínio de casas, incluindo histórico, pendências e movimentação de caixa.

## Funcionalidades

- **Listar casas**: exibe todas as casas cadastradas no condomínio.
- **Listar status de pagamento por mês**: consulta o status (PAGO, NÃO PAGO, PARCIALMENTE PAGO) e valor pago de todas as casas em um mês/ano específico.
- **Histórico de pagamento por casa**: mostra todo o histórico de pagamentos de uma casa específica.
- **Alterar status de pagamento**: registra o valor pago por uma casa em um determinado mês, atualizando automaticamente o status.
- **Listar pendências**: lista todas as casas com status "NÃO PAGO" ou "PARCIALMENTE PAGO".
- **Exibir valor total do caixa**: soma todas as movimentações registradas na tabela `caixa` e mostra o extrato.
- **Adicionar retirada/acréscimo pontual**: permite lançar entradas (+) ou saídas (-) manuais no caixa, com motivo obrigatório.

## Como funciona

Ao ser executado, o script:

1. Conecta (ou cria) o banco de dados `sis_cond_database.db` na mesma pasta do script.
2. Cria automaticamente uma tabela para cada casa (podendo ser adaptada no próprio script para quantidade de casas/apartamentos que quiser), a tabela `casas` (lista de casas) e a tabela `caixa` (movimentações financeiras).
3. Insere o mês atual (formato `MM/AA`) em cada casa com status inicial "NÃO PAGO", caso ainda não exista.
4. Exibe um menu interativo no terminal para o usuário escolher a ação desejada.

## Estrutura do banco de dados

| Tabela | Colunas | Descrição |
|---|---|---|
| `casas` | `casa_id` (PK) | Lista dos IDs das casas |
| `casaN` (uma por casa) | `mes_ano` (PK), `status`, `valor_cond` | Histórico mensal de pagamento de cada casa |
| `caixa` | `id` (PK, autoincrement), `motivo`, `caixa_valores` | Lançamentos financeiros do caixa do condomínio |

## Requisitos

- Python 3.x
- Bibliotecas padrão: `sqlite3`, `datetime`, `time`, `os`, `sys` (nenhuma dependência externa)

## Como executar

```bash
python sis_cond.py
```

O banco de dados `sis_cond_database.db` será criado automaticamente na primeira execução, na mesma pasta do script.

## Menu do sistema

```
(0) Sair do sistema
(1) Listar casas
(2) Listar status de pagamento em um determinado mês
(3) Listar histórico de pagamento de uma determinada casa
(4) Alterar status de pagamento de uma determinada casa
(5) Listar pendências de pagamento
(6) Exibir valor total do caixa
(7) Adicionar retirada/acréscimo pontual
```

## Observações e limitações conhecidas

- O valor fixo do condomínio está fixado em **R$ 50,00** (regras de status embutidas no código, porém, podendo ser adaptado para cada uso).
- O número de casas é fixo em **14** (`range(1, 15)`), sendo necessário alterar o código para adicionar/remover casas.
- Entradas de mês devem seguir estritamente o formato `MM/AA` (5 caracteres, com `/` na posição 3).
- Os nomes das tabelas de casas são montados via f-string (`casa{casa_id}`) a partir de valores internos controlados pelo próprio sistema, não de entrada livre do usuário.
- O sistema é executado inteiramente via terminal (linha de comando), sem interface gráfica.

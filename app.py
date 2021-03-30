import sys
from os import write
from datetime import datetime
import locale

def formatarNumeroDeInscricao(numero):
  numeroFormatado = numero[:2] + '.' + numero[2:5] + '.' + numero[5:8] + '/' + numero[8:12] + '-' + numero[12:]
  return numeroFormatado


if __name__ == '__main__':
  modeloName = sys.argv[1]
  relatorioName = sys.argv[2]

  modelo = open(modeloName, 'r')

  relatorio = open(relatorioName, 'w', encoding="utf-8")
  relatorio.write("""<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8">
    <title>Relatorio</title>
  </head>
  <body>
  """)

  formasDeLancamento = {
    '01': 'Crédito em Conta Corrente',
    '02': 'Cheque Pagamento / Administrativo',
    '03': 'DOC/TED (0) (1)',
    '04': 'Cartão Salário',
    '05': 'Crédito em Conta Poupança',
    '06': 'Liberação de Títulos HSBC',
    '07': 'Emissão de Cheque Salário',
    '08': 'Liquidação de Parcelas de Cobrança Não Registrada',
    '09': 'Arrecadação de Tributos Federais',
    '10': 'OP à Disposição',
    '11': 'Pagamento de Contas e Tributos com Código de Barras',
    '12': 'Doc Mesma Titularidade',
    '13': 'Pagamentos de Guias',
    '14': 'Crédito em Conta Corrente Mesma Titularidade',
    '16': 'Tributo - DARF Normal',
    '17': 'Tributo - GPS (Guia de Previdência Social)',
    '18': 'Tributo - DARF Simples',
    '19': 'Tributo - IPTU - Prefeituras',
    '20': 'Pagamento com Autenticação',
    '21': 'Tributo - DARJ'
  }

  header = ''
  nomeDoBanco = ''
  details = []
  formaDeLancamentoDescricao = ''

  for linha in modelo:
    if linha[7] == '0':
      nomeDoBanco = linha[102:132].strip()
    if linha[7] == '1':
      header = linha
      formaDeLancamentoDescricao = formasDeLancamento[linha[11:13]]
    if linha[7] == '3':
      details.append(linha)

  numeroDeInscricao = formatarNumeroDeInscricao(header[18:32])

  relatorio.write(f"""
    <table border="1px">
      <thead>
        <tr>
          <th>Nome da Empresa</th>
          <th>Numero de Inscricao da Empresa</th>
          <th>Nome do Banco</th>
          <th>Nome da Rua</th>
          <th>Numero do Local</th>
          <th>Nome da Cidade</th>
          <th>CEP</th>
          <th>Sigla do Estado</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>{header[72:102].strip()}</td>
          <td>{numeroDeInscricao}</td>
          <td>{nomeDoBanco}</td>
          <td>{header[142:172].strip()}</td>
          <td>{header[172:177].strip()}</td>
          <td>{header[192:212].strip()}</td>
          <td>{header[212:217]}-{header[217:220]}</td>
          <td>{header[220:222]}</td>
        </tr>
      </tbody>
    </table>
  """)

  relatorio.write("<br>")

  relatorio.write("""
    <table border="1px">
      <thead>
        <tr>
          <th>Nome do Favorecido</th>
          <th>Data de Pagamento</th>
          <th>Valor do Pagamento</th>
          <th>Numero do Documento Atribuido pela Empresa</th>
          <th>Forma de Lancamento</th>
        </tr>
      </thead>
      <tbody>
  """)

  for linhaDetalhe in details:

    dataFormatada = datetime.strptime(linhaDetalhe[93:101], '%d%m%Y').strftime('%d/%m/%Y')
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    moeda = linhaDetalhe[119:134]
    moedaFloat = float(moeda[:-2] + '.' + moeda[-2:])
    moedaFormatada = locale.currency(moedaFloat, grouping=True)

    relatorio.write(f"""
        <tr>
            <td>{linhaDetalhe[43:73].strip()}</td>
            <td>{dataFormatada}</td>
            <td>{moedaFormatada}</td>
            <td>{linhaDetalhe[73:93].strip()}</td>
            <td>{formaDeLancamentoDescricao}</td>
        </tr>
    """)

  relatorio.write("""
      </tbody>
    </table>
  </body>
</html>
  """)
  print("Relatorio gerado")
  modelo.close()
  relatorio.close()
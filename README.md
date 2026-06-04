## Ponderadas figurinhas

Para desenvolver a arquitetura do código eu decidi segui os seguintes princípios:

domain -> Responsável apenas por guardar a lógica de propriedades da entidade figurinhas, junto com as propriedades base de para criar atulizar e deletar entidades.

repository -> Implementa a interação com o banco de dados para persistir, atualizar e deletar informações de figurinhas do banco de dados 
    database -> Aqui coloquei os códigos puros de criação do ambiente do banco de dados e scripts de queries

services -> Orquestração do fluxo de dados das requicições recebidas pelo handler, validação dos dados recebidos e gestão da saudo do serviço durante a execução do processo dos dados visando consistência de dados por meio da utilização das interfaces, tanto para comunicar com o domain quanto para comunicar com o repository
    interfaces -> Aqui ficam os contratos que definem como o service se comunica com o repository e como o handler se comunica com o service. Decidi colocar aqui porque essas interfaces representam o que o service precisa e oferece.

handler -> Responsável apenas por receber as requisições HTTP, verificar se chegaram no formato esperado, como o Content-Type correto e o body presente, e repassar os dados para o service. Também é aqui que as exceções de domínio são capturadas e traduzidas para os status HTTP corretos, como 404 para figurinha não encontrada e 400 para dados inválidos

Essa foi a divisão final que cheguei. A atividade foi um bom exercício para praticar clean code e pensar em como dividir de forma consistente as responsabilidades de cada parte do projeto

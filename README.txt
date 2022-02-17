Home Sales Company

A Home Sales é uma imobiliária fictícia que trabalha com a compra e venda de imóveis. Buscamos, através da análise de características e dados dos imóveis, alcançar insights que possibilitam aquisições de imóveis mais vantajosas e seguras.
O objetivo desse projeto é relatar a análise de um conjunto de dados de imóveis e, por fim, destacar aqueles que são interessantes para compra.

1. Problema de negócio
A Home Sales é uma empresa fictícia especializada na compra e revenda de imóveis. Seu modelo de negócio consiste em, através da análise de regiões e características de imóveis, compra-los por preços vantajosos para revenda.
Atualmente, o objetivo da análise de dados é encontrar e filtrar aqueles imóveis com potencial de lucro de ao menos 10% sobre o valor de compra. O lucro estimado (profit_value) na compra de um imóvel é calculado através da divisão da mediana de preço do conjunto de imóveis (median_price) de cada região (zipcode) com o valor de compra (price) do respectivo imóvel.

2. Premissas de negócio
2.1 Da aquisição e venda dos imóveis
a) Somente casas com valores de compra abaixo da mediana de preço por código postal serão compradas;
b) Somente casas com em boas condições ("condition" >= 3) serão compradas;
c) As casas terão preço de revenda equivalente a 120% do seu preço de aquisição;

2.2 Da reestruturação de dados
a) Valores outliers serão excluídos;
b) Valores duplicados na coluna "ID" serão excluídos;

id: Código de identificação do imóvel
date: Data de inserção do imóvel em venda
price: Preço em que o imóvel foi anunciado
bedrooms: Número de quartos
bathrooms: Número de banheiros
sqft_living: Medida do espaço interior dos imóveis
sqft_lot: Medida do espaço do lote dos imóveis
floors: Número de andares dos imóveis
waterfront: Variável que indica vista para água (0: não, 1: sim)
view: Índice de 0 a 4 que indica qualidade da vista do imóvel (0: mais baixa, 4: mais alta)
condition: Índice de 1 a 5 que indica a condição do imóvel (1: mais baixa, 5: mais alta)
grade: dropar**
sqft_basement: Medida do espaço interior do porão dos imóveis
yr_built: Ano de construção dos imóveis
yr_renovated: Ano em que o imóvel foi reformado (se foi reformado)
zipcode: Região/código postal do imóvel
lat: Coordenada de latitude do imóvel
long: Coordenada de longitude do imóvel
sqft_livining15: dropar**
sqft_lot15: dropar**
is_winter: Variável que indica se a estação em que o imóvel foi anunciado é o inverno (0: não, 1: sim)
median_price: Mediana de preço de demais imóveis no mesmo código postal em que o imóvel está inserido
winter_median_price: Mediana de preço de demais imóveis durante o inverno no mesmo código postal em que o imóvel está inserido (somente para imóveis anunciados no inverno)
is_renovated: Variável que indica se o imóvel foi ou não reformado (0: não, 1: sim)
worth_buying: Variável que indica se o imóvel deve ser comprado, de acordo com as premissas de aquisição de imóveis assumidas.
profit_value: Valor que representa os 20% de acréscimo sobre o preço de aquisição dos imóveis.
selling_price: Preço de revenda dos imóveis.

3. Planejamento da solução
3.1 Importação dos dados do Kaggle (https://www.kaggle.com/shivachandel/kc-house-data);
3.2 Limpeza dos dados:
a) Utilização de métricas estatísticas de quartis para eliminação de outliers **(valores muito acima ou abaixo do normal)**
3.3 Reestruturação de dados:
a) Agrupamento dos imóveis por zipcode para determinação da mediana de preço (median_price);
b) Determinação de quais imóveis foram anunciados durante o inverno (Para verificar a condição: os imóveis são mais baratos no inverno, devido a baixa capacidade de locomoção?)
c) Agrupamento dos imóveis anunciados no inverno por zipcode para determinação da mediana de preço de inverno (winter_median_price);
d) Determinação dos imóveis que valem a pena serem comprados (worth_buying) e do valor de lucro (profit_value);
e) Criação do relatório de compras.
3.3 Análise exploratória dos dados;
3.4 Validação de insights.
3.5 Criação de dashboard interativo e hospedagem dos dados do site no Heroku.
3.6 Conclusão e análise de resultados

4. Os 3 principais insights de negócio
4.1 Casas vendidas no inverno são pelo menos 20% mais baratas, visto que não há muita mobilidade e as pessoas vendem na internet;
a) Aplicação: Torna a compra de casas em massa no inverno mais interessante diante da possibilidade de um desconto maior no valor dessas casas;
4.2 Casas reformadas são ao menos 30% mais caras que casas que não passaram por reformas;
a) Aplicação: Informa se a compra de casas não reformadas é viável para revenda caso seja possível aplicar uma pequena reforma na casa e ganhar no valor de venda final;
4.3 Casas com vista em frente à rios ou ao mar são pelo menos 20% mais caras;
a) Aplicação: Permite estudar a melhor oportunidade para comprar casas com vista de frente para rios ou mares e revender.

# 5. Resultados financeiros para o negócio e conclusão
Após limpeza, análise e reestruturação dos dados, foi possível destacar com eficácia os imóveis vantajosos para compra e revenda, permitindo também visualização dinâmica desses imóveis, com recursos gráficos de comparação de preços, visualização de localização geográfica e filtros aplicáveis para melhor refinamento da amostra de imóveis para compra.
Através desses resultados, os imóveis vantajosos para compra foram listados em um documento contendo a identificação (id) do imóvel, preço de compra (price), preço de venda (selling_price).
Foi gerado também um aplicativo, utilizando Heroku, disponível para acessar o banco de dados e seus gráficos em qualquer plataforma. 
O lucro estimado resultante da venda dos imóveis é de U$777.552.813,2, evidenciando a possibilidade de bons resultados para um ótimo retorno financeiro.

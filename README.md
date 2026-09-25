# airflow
O projeto foi desenvolvido python 3.7 (padrão do container airflow), e suas bibliotecas pandas, streamlit, psycopg2-binary, python-dotenv.
Link do app -> https://airflow-cs-teste-tecnico.streamlit.app/

# Estrutura das pastas    
Segui com o padrão semelhante ao MVC, para melhor visualização e compreensão, com a ressalva de alguns ajustes devido a linguagem.

Airflow/
├── docker-compose.yaml               # Compose padrão do airflow, com mudanças referentes ao demais containers integrados nele (Postgres e Redis), pois como no meu ambiente docker eu ja tenho ambos, so adicionei o airflow no mesmo network para comunicação das partes. 
├── README.md                         # Documentação
├── requirements.txt                  # Dependências Python do projeto
│
├── dags/
│   └── OT Trans/
│       ├── sqlite.py                 # Script relacionado ao SQLite, onde gero o demanda.db em 'core'
│       ├── docs/
│       │   ├── arquivos_brutos/      # Onde ficam os dados brutos baixados, gerar uma automação onde fosse baixados automaticamente os arquivos seria um pouco mais complexo e demorado, por isso optei por seguir no modelo padrão, onde é inserido o arquivo manualmente na pasta e o sistema lê. 
│       │   └── arquivos_limpos/     # Onde ficariam os dados tratados e limpos, acabei não tendo tempo para completar essa parte (já que a logica seria que depois dos arquivos tratados seriam salvos novamente nessa pasta) então optei por não seguir por com essa parte por enquanto.
│       │
│       ├── src/
│       │   ├── index_dag.py          # DAG principal do Airflow
│       │   ├── app/
│       │   │   ├── components/       # Componentes reutilizáveis
│       │   │   └── views/            # Views / páginas / renderização
│       │   │
│       │   ├── Config/
│       │   │   └── config.py         # Configurações da aplicação, onde configuro o nome do arquivo que vai ser tratado
│       │   │
│       │   ├── core/
│       │   │   ├── db_connection.py  # Conexão com banco de dados
|       |   |   └── demanda.db        # Onde fica meu dados do SQLite
│       │   │
│       │   └── functions/
│       │       ├── function.py       # Onde fica as funções de 'index_dag'
│       │       └── function_app.py   # Onde fica as funções de 'index_app' (No caso as querys)
│       │
│       └── tests/
│           └── teste.py              # Testes do projeto
│
|
│
└── .env                              # Variáveis de ambiente

# Decisões tecnicas
O projeto foi desenvolvido no container airflow, utilizando tanto o postgres quando o sqlite para o banco de dados e a biblioteca pandas para manuseio dos dados pelo sistema. Pela necessidade do deploy publico online foi necessario ser utilizado o sqlite para armazenamento de dados interno no sistema para que o mesmo não pare sua aplicação online no Streamlit community, ja que como meu container postgres é local, não haveria conexão logo não exibindo a aplicação de maneira correta.

O projeto inicialmente foi desenvolvido somente para postgres já que o mesmo tem muita versatilidade para suportar consultas vetoriais, OLTP e OLAP, porém como falei acima, devido a 'necessidade' dele rodar offline, foi adicionado o sqlite, e por que o sqlite e não o duckdb? em uma simples resposta, por que o sistema (da forma atual), não se compoe de analises complexas e alta carga de linhas e colunas, entretanto, não descartei a ideia de usar o duckdb nesse projeto.

A escolha ente o Streamlit e o Dash, foi um pouco mais facil devido o Streamlite ter como fazer deploy facil com o git e uma curva de aprendizado bem mais simples que a do Dash, com isso em mente decidir optar pelo Streamlit mesmo.

# Limitações e melhorias futuras
Os documentos para serem tratados tem que ser adicionados manualmente em 'config.py', ja que não foi desenvolvida de forma que ja busco tudo que tem na pasta e valide o que ja foi tratado e o que não foi. (melhoria futura)
Os logging não foi criados, fora as infos que o usuasrio teria na interface do airflow e os logs do proprio airflow, não foi desenvolvida a camada com logging interno. (melhoria futura)

# Instalação
Para rodar a aplicação, voce ja deve ter os containers postgres e redis instalados (podem ser criados no mesmo compose, se esse for o caso, usar o compose padrão disponibilizado pelo site do airflow). 
Para não ficar aparecendo como se houvesse erros no codigo, acessei o dev containers tool do vscode e acessei meu proprio container, ja que o ambiente ja é configurado la (com a versão padrão airflow do python e etc), mas não é uma regra isso.
E para rodar o Streamlit local, deves rodar o comando 'streamlit run src/app/views/index_app.py' se estiver na pasta main (OT Trans) ou somente 'streamlit run index_app.py' se estiver na pasta 'views'.


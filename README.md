# Urbanizze

## Requisitos
* Python 3+
* Postgres 10
* PostGis
* Gdal, talvez seja esse o comando `apt-get install python-gdal`. Se for mac um `brew install gdal` é suficiente.

## Configurações do DB
Primeiro de tudo configurar o Postgres através do comando `psql -U postgres`:

```sql
CREATE USER urbanizze WITH PASSWORD 'XXXXX';
CREATE DATABASE urbanizze;
GRANT ALL PRIVILEGES ON DATABASE urbanizze to urbanizze;
ALTER USER urbanizze CREATEDB;
ALTER USER urbanizze SUPERUSER;
\c urbanizze
CREATE EXTENSION postgis;
```

## Ambiente de desenvolvimento
Depois clonar o repositório e rodar os comandos abaixo:

```console
git clone git@github.com:medeirosthiago/urbanizze.git
cd urbanizze
python -m venv .urbanizze
source .urbanizze/bin/activate
pip install -r requirements-dev.txt
cp .env-sample .env
```

Preencha as informações do `.env` e rode os seguintes comandos:
> Caso não tenha todas as informações para o `.env`, copie as configurações que estão no servidor.
```console
python manage.py migrate
python manage.py test
```
Se algum teste falhou pode ser alguma dependência esteja faltando.
Verifique o *log* pra se informar sobre o erro.

Se os testes rodaram com sucesso é necessário importar os dados para o mapa e zonas.
```console
psql -f urbanizze/map/data/sql/map_zona.sql -d urbanizze
psql -f urbanizze/map/data/sql/map_setor.sql -d urbanizze
psql -f urbanizze/map/data/sql/map_codurbanismo.sql -d urbanizze
```

É preciso coletar os arquivos estáticos:
```console
python manage.py collectstatic
```

Criar um super user, esse será o admin do sistema:
```console
python manage.py createsuperuser
```

Iniciar o servidor do urbanizze:
```console
python manage.py runserver
```

Você pode acessar o sistema pelo http://127.0.0.1:8000/. :tada:

## Configurações para deploy
Para fazer o deploy das atualizações desenvolvidas, você vai precisar adicionar o `remote`
no seu *git* e realizar o push para o remote que deseja, no caso do Urbanizze, chamamos o remote
produção de **live** e mantemos o **origin** apenas para armazenar o código no GitHub.

Por isso, apenas faça `git push live master` se você tem certeza das novas mudanças/features que você realizou,
faça testes, por favor :pray:.

Para acessar o servidor, vai utilizar o `ssh` e então irá restartar o serviço do apache.
Feito isso as novas atualizações já estarão rodando em produção.

```console
git remote add live ssh://[user]@[server]/root/urbanizze/live.git
ssh [user]@[server]
sudo /etc/init.d/apache2 restart
```

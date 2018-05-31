from database.TinyDB_DB import TinyDB_DB
# tiny = TinyDB_DB.init_from_json('tinydb_with_feats.json','scraping/castro_clean.json')
# tiny.update_all_feats()
import click
import server

@click.group()
def cli():
    pass

@cli.command()
@click.argument("code")
def server(code):
   server.main()

if __name__ == '__main__':
    cli()

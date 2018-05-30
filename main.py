from database.TinyDB_DB import TinyDB_DB
# tiny = TinyDB_DB.init_from_json('tinydb_with_feats.json','scraping/castro_clean.json')
# tiny.update_all_feats()
import click

@click.group()
def cli():
    pass

@cli.command()
@click.argument("code")
def server(code):
    print("{code}: I am a teapot".format(code=code))

if __name__ == '__main__':
    cli()
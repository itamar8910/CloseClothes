from database.TinyDB_DB import TinyDB_DB,TINYDB_PATH
# tiny = TinyDB_DB.init_from_json('tinydb_with_feats.json','scraping/castro_clean.json')
import click
import server as server_module
""" Collection of the main commands for the backend. to run a command run `python main.py COMMAND_NAME`
Run `python main.py -h` to see all avalible commands"""
@click.group()
def cli():
    pass

@cli.command()
def server():
    """Runs the back-end socket based server"""
    server_module.main()

db_class = TinyDB_DB
@cli.command()
@click.argument("json_paths", nargs=-1)  # varidic argument
@click.option("-o","--output_path" ,default=TINYDB_PATH)
@click.option('--update_feats/--dont_update_feats',default=False)
def init_db(output_path,json_paths,update_feats):
    """ Create a database from the scrapes given as json arguments, and update the db """
    tiny = db_class.init_from_json(output_path,*json_paths)
    if update_feats:
        update_db(tiny)

def update_db(db):
    db.update_all_feats()
    db.init_knn()

@cli.command('create_knn')
@click.option("-db","--db_path" ,default=TINYDB_PATH)
def create_knn_cmd(db_path):
    init_knn(db_path)
    
@cli.command("update_db")
@click.option("-db","--db_path" ,default=TINYDB_PATH)
def update_db_cmd(db_path):
    tiny = db_class(db_path)
    update_db(tiny)


def init_knn(db_path):
    tiny = db_class(db_path)
    tiny.init_knn()

if __name__ == '__main__':
    cli()

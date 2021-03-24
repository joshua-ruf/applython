import click
from applython import applython
from database import database

@click.group()
def cli():
    pass

@cli.command()
@click.option('-i', '--in-file', default='cover-letter', show_default=True,
    help="Which markdown template in templates/ to render.")
@click.option('-o', '--out-file', default='CoverLetter.pdf', show_default=True,
    help="Name of the output file.")
def build(markdown_file, out_file):
    ap = applython()
    ap.load_markdown()
    ap.render_template()
    ap.build_pdf(out_file)

@cli.command()
@click.option('--n', default=10, show_default=True,
    help="Number of (most recent) results to display.")
@click.option('--company', default=None,
    help="Limit search to specific company.")
@click.option('--position', default=None,
    help="Limit search to specific position.")
def list(n, company, position):
    DB = database()
    DB.list_applications(n, company, position)
    DB.db.close()

if __name__ == '__main__':
    cli()
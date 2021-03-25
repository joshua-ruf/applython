import click
from applython import applython
from database import database
import os

@click.group()
def cli():
    pass

@cli.command()
@click.option('-i', '--in-file', default='cover-letter', show_default=True,
    help="Which markdown template in templates/ to render.")
@click.option('-o', '--out-file', default='CoverLetter.pdf', show_default=True,
    help="Name of the output file.")
def build(in_file, out_file):
    ap = applython()
    ap.load_markdown(markdown_file=in_file)
    ap.render_template()
    ap.build_pdf(out_file)

@cli.command()
@click.option('-n', default=10, show_default=True,
    help="How many of the most recent applictions to list.")
@click.option('--company', default=None,
    help="Limit search to specific company.")
@click.option('--position', default=None,
    help="Limit search to specific position.")
@click.option('--to-csv/--to-console', default=False,
    help="If --to-csv is used then the results are saved to %Y%m%d%H%M%SapplythonExport.csv" +
    ", otherwise prints to console.")
def list(n, company, position, to_csv):
    DB = database()
    DB.list_applications(n, company, position, to_csv)
    DB.db.close()

if __name__ == '__main__':
    cli()
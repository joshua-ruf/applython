from flask import Flask, render_template
from flask_flatpages import FlatPages
from flask_frozen import Freezer

from datetime import datetime
from database import database

import pdfkit
import tempfile
import shutil
import os

class applython:
    def __init__(self):

        ### make temporary directory to store frozen build
        temp_dir = tempfile.mkdtemp()

        app = Flask(__name__)
        flatpages = FlatPages(app)
        app.config['FLATPAGES_EXTENSION'] = '.md'
        app.config['FLATPAGES_ROOT'] = 'cover-letters'
        app.config['FREEZER_DESTINATION'] = temp_dir
        freezer = Freezer(app)

        ### initialize the sqlite database
        DB = database()

        self.DB = DB
        self.app = app
        self.flatpages = flatpages
        self.freezer = freezer
        self.temp_dir = temp_dir

    def list_letters(self):
        """
        Print the available cover letter markdown files in the cover-letters folder.
        """
        posts = [p for p in self.flatpages]
        for i, p in enumerate(posts):
            print(i, p.path)

    def load_markdown(self, markdown_file='cover-letter', update_database=True):
        """
        Parse the YAML header from the selected markdown file.

        Args:
            markdown_file (str, optional): extension-less file name to use in rendering.
            Defaults to 'cover-letter'.
            update_database (bool, optional): Whether to add this application to the database.
            Defaults to True.
        """
        print('parsing markdown...')

        # remove extension
        markdown_file = os.path.splitext(markdown_file)[0]

        posts = [p for p in self.flatpages if p.path == markdown_file]
        
        ### check if the selected markdown_file exists
        if len(posts)==0:
            print(markdown_file, 'not found in cover-letters/')
            print('Try again with one of the following letters:')
            self.list_letters()
            exit()
        elif len(posts)==1:
            posts = posts[0]
        else:
            print('Error: multiple files found matching', markdown_file)
            exit()

        company = posts.meta['company']
        position = posts.meta['position']
        today = datetime.today().strftime('%Y-%m-%d')

        ### check if an application has already been submitted
        already_applied = self.DB.applied(company=company, position=position)

        ### if applied, ask to continue
        if already_applied[0]:
            print(f'You have already applied to the {position} position at {company} on {already_applied[1]}')
            continue_ = input('Would you like to continue? [y/n] ')
            if continue_ == 'n':
                print('Goodbye!')
                exit()

        ### upload to database
        if update_database:
            self.DB.insert(company=company, position=position, date=today)

        self.posts = posts
        self.today = today

    def render_template(self):
        """
        Render the html template via .temp-template, an intermediate hidden file.
        """
        print('rendering template...')

        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, dir='templates')
        self.temp_file = temp_file

        @self.app.route("/main.html")
        def main():
            ### prerender to use the markdown yaml content in the markdown file
            # html_file = open("templates/.temp-template","w")
            temp_file.write(render_template("template.html", post=self.posts, now=self.today))
            temp_file.close()
            # html_file.close()

            return render_template(os.path.basename(temp_file.name), post=self.posts)

    def build_pdf(self, out_file = 'CoverLetter.pdf'):
        """
        Build the PDF Cover Letter.

        Args:
            out_file (str, optional): Name for the output pdf file. Defaults to 'CoverLetter.pdf'.
        """
        print('saving to', out_file)
        
        ### freeze flask app
        self.freezer.freeze()

        ### convert html to pdf
        options={
            '--allow':self.temp_dir + '/static/',
            'quiet':''
        }
        pdfkit.from_file(self.temp_dir + '/main.html', out_file, options=options) 

        ### cleanup temp_dir and temp_file
        shutil.rmtree(self.temp_dir)
        os.remove(self.temp_file.name)

if __name__ == "__main__":

    ap = applython()
    # ap.list_letters()

    ap.load_markdown()
    ap.render_template()
    ap.build_pdf()
    
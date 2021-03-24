# applython

Efficiently and dynamically render cover letters for job applications with markdown! Makes use of Flask (Flatpages and Frozen) alongside the wkhtmltopdf conversion tool.

### Installation
1. install wkhtmltopdf with `brew install wkhtmltopdf` on mac and `apt-get install wkhtmltopdf` on linux. Follow [this link](https://docs.brew.sh/Installation) for an install guide for brew.
2. install the necessary python packages from requirements.txt with `pip3 install -r requirements.txt`.

### Use
1. edit the cover-letter.md file with your personal cover letter and the specific details of the job to which you are applying. In the markdown file you can use the `{{ post.parameter }}` syntax to include dynamic content.
2. run `python3 applython.py` to render the html and convert to a pdf file called CoverLetter.pdf

### Notes

- The templates/template.html file contains a header block with the company, job title, and current date.
- The static/main.css file formats the resulting pdf file, feel free to edit that to give your cover letter a personal flare!
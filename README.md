# applython

Efficiently and dynamically render cover letters for job applications with markdown! Makes use of Flask (Flatpages and Frozen) alongside the wkhtmltopdf conversion tool.

### Installation
1. install wkhtmltopdf with `brew install wkhtmltopdf` on mac and `apt-get install wkhtmltopdf` on linux. Follow [this link](https://docs.brew.sh/Installation) for an install guide for brew.
2. from within the applython directory, install applython as a python package with `pip3 install .`

### Use
By default applython chooses the cover-letters/cover-letter.md file as its template, edit this file to make it your own. You can add another file to the cover-letters folder and cycle between them with an option in the `build` command. In the markdown files use the `{{ post.parameter }}` syntax to include dynamic content.

To generate a cover letter:

```sh
applython build -i myawesomecoverletter.md -o MyAwesomeCoverLetter.pdf
```

Here, the `-i` and `-o` options are optional, defaulting to `cover-letter.md` and `CoverLetter.pdf` respectively. Remember that `myawesomecoverletter.md` must be in the cover-letters/ folder.


To list your five most recent applications run:

```sh
applython list -n 5
```

Here, `-n`, the number of results to print to console, defaults to 10. You can also save these results to a csv file to analyze your progress with the `--to-csv` option.


### Notes

- The templates/template.html file contains a header block with the company, job title, and current date.
- The static/main.css file formats the resulting pdf file, feel free to edit that to give your cover letter a personal flare!


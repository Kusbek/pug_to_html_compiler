# pug_to_html_compiler
This is a converter of a file with pug extension to html file. 
## Tags
It can handle standard tags, hierarchy of tags,
standard and custom self closing tags, block expansion.

## Attributes
Attributes can be single and multiline

## Error Handling
It reports two types of error:
-Nested self closing error
-Custom self closing syntax error

## How to use
In the project directory run by cmd
>\>python PugToHtml.py -f "test.pug" -o "output.html" 

Two additional pug files \"testWithNestedSelfClosingError.pug\" and \"testWithSelfClosingSyntaxError.pug\" can be tested as well

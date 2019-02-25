# pug_to_html_compiler
This is a converter of a file with pug extension to html file. 
## Tags
It can handle standard tags, hierarchy of tags,
standard and custom self closing tags, block expansion.

## Attributes
Attributes can be single and multiline

## Error Handling
It reports two types of error: Nested self closing error and Custom self closing syntax error

## How to use
In the project directory run by cmd
>\>python PugToHtml.py -f "test.pug" -o "output.html" 

Two additional pug files \"testWithNestedSelfClosingError.pug\" and \"testWithSelfClosingSyntaxError.pug\" can be tested as well

## Example of pug file 

```
html
	body	
		div(id = "imageControl", class = "jay", name = "gavnyuk")/ Self Closing
		ul(class = "card", name = "Beka")
			li(id = "1") Item A
				div
			li(id = "2") Item B
				div
			li(id = "3") Item C
				div
		ul( id = "1"): div(
				type='checkbox'
				name='agreement'
				checked
			)
			input(
				id = "2"
			)	
			div(class = "divka"): a
				img
		div
			input(
				type='checkbox'
				name='agreement'
				checked
			)
			input(
				type='button'
				name='Beka'
			)

```


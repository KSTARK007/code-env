# API Sheet 

## 1) /getfile/`<search>` [GET]
input: `<search>` string
output: JSON file

`{	`


`"0":{
		"title": "...",
		"data" : "...",
		"code" : "...",
	    "link" : "..."
		},`
    
    
`"1":{
		"title": "...",
		"data" : "...",
		"code" : "...",
	    "link" : "..."
		}`
    
    
`}`



## 2) /postfile/   [POST]

Run the index.html page
input : all the attributes in the form
output: nothing
service : addeds the article to the database.


## Prerequisite:
- `pip install flask` 

## Usage:
Run - 
- `python app.py`

for post request open `index.html`

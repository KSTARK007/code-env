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



## 2) /postfile/<data>   [GET]


input : `<title>;<data>;<code>;<link>` strings
output: nothing
service : adds the article to the database.


## Usage:
Run - 
- `python app.py`

API call -
`	/postfile/testtitle;testdata;;testlink `
in this the code field is not avalable
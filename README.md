# bank-statement-parser

This is an app that will read all banking statement pdfs in the `/pdfs` directory and return one csv file. 

## To run
1. Move your credit card banking PDF statements to `/pdfs` folder in this project locally.
2. Go to `/dist` folder and run the `main`executable. 
3. A resulting file will get saved in the directory you ran the executable from `temp_transactions.csv`. 

At the moment this only parses through RBC credit card statements as a supported format.
#!/bin/bash

pandoc -s --output=content.txt --from=docx --to=plain I\ lik\ thangs.docx;
echo "You are an expert editor. Proofread the following document. Make only necessary corrections.  
Rules:  
1. Do not add extra explanations outside the text.  
2. Preserve the original text structure.  
3. Only correct errors or improve clarity.  
Text to proofread: $(cat content.txt)" | ollama run mistral > corrections_made.txt; pandoc corrections_made.txt -o edited_document.docx ; diff content.txt corrections_made.txt >> corrections_made.txt; rm content.txt

#!/bin/bash

pandoc -s --output=content.txt --from=docx --to=plain I\ lik\ thangs.docx;
echo "You are an expert editor. Proofread the following document. Make only necessary corrections.  
Rules:  
1. Do not add extra explanations outside the text.  
2. Keep comments concise.  
3. Preserve the original text structure.  
4. Only correct errors or improve clarity.  
Text to proofread: $(cat content.txt)" | ollama run mistral > corrected_document.txt; diff content.txt corrected_document.txt >> corrected_document.txt; pandoc corrected_document.txt -o corrected_document.docx; rm content.txt

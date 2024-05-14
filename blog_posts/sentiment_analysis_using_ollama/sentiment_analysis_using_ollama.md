# ---- This post is a work in progress ----

# Intro

This is an exploration of analyzing sentiment from documents using large language models (LLMs) run with Ollama. This project is in several parts
1. I scrape the Federal Reserve website for Federal Open Market Committee (FOMC) press releases. These are in the form of PDFs released roughly every two months. I chose these as a data source because the PDFs are quite structured and dense - there are always several topics written about in the press releases so each document will have multiple opportunities for sentiment analysis. I also find the press releases interesting, as they can hint the future policy of the Federal Reserve (I'm not using this for any predictive analysis or anything, but it may help me stay informed)
2. I extract and clean the text from the PDFs
3. I pass the text into an LLM using Ollama

Ollama is an incredible program that allows you to run LLMs locally on your computer. I'm specifically using the Ollama Python API, ollama-python, to pass text into the model. 
# The Project

[Link to the GitHub repo](https://github.com/JustinSmethers/fomc-documents) 
# Working with Ollama

# The results

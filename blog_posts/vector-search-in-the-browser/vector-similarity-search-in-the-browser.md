---
title: Vector Similarity Search in the Browser - With DuckDB!
description: WIP - Exploring vector similarity search in the browser using DuckDB-WASM
thumbnail: duckdb-in-the-browser.webp
tags:
  - wip
---
### ---- This post is a work in progress ----

# What is this?
This is a post about exploring vector similarity search in the browser using DuckDB-WASM. It is a work in progress and I will be updating it as I go. I personally want to learn more about using DuckDB-WASM, but I also think it's useful to explore the utility of vector similarity search in the browser for fun projects, but also for more useful applications.

### Why DuckDB?
DuckDB is a lightweight, embedded analytical database that is super easy to use. I've written about [using DuckDB here](https://justinsmethers.com/blog/post/1-billion-row-challenge-in-python/). It also has a WebAssembly version that can run in the browser, [duckdb-wasm](https://duckdb.org/docs/api/wasm/overview.html), which means we can run DuckDB in the browser and use (most) all of its features, such as it's vector similarity search extension, [vss](https://duckdb.org/2024/05/03/vector-similarity-search-vss.html). Using this, we can perform vector similarity search in the browser!

### What's the goal?
The goal is to add a search bar to this blog such that you can search for sections of posts which are related to the input search term. This will be done by embedding DuckDB-WASM in the browser and using the vss extension to search for the most similar text in the blog. I know there are easier ways to do "search" for this blog, but I think this is a fun way to explore DuckDB-WASM and should give some interesting results.
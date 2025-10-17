---
title: Building a new feature entirely on my phone with Codex
description: How I built a new feature for this website using only my phone, OpenAI's Codex, and GitHub Mobile
thumbnail: code-thumbnail.png
tags:
  - post
date: 2025-10-10
---

# Building a New Feature Entirely on My Phone with Codex

I recently decided to revamp this website by adding some small features to make it fun to write on and browse. This time, I'm adding tags to posts, "Post", "WIP", "Talk" and "Notes". Honestly, I only wanted to do this because agentic tools are at a point where I can fire off a few requests and have a working feature (who wants to relearn Django). This felt like a perfect time to add a feature entirely with codex using only the mobile app for ChatGPT and GitHub. 

First off, Codex is buggy. It didn’t appear in the sidebar of my ChatGPT app despite Redditor's insistence it should be there. Turns out, you first need to send a request with Codex in the web app. There, I worked through the UI (you couldn’t even scroll down to see the conversation history! I could only see half of each conversation entry on my iPhone 16 Pro). I was able to send off a simple prompt after connecting to GitHub and choosing my repository:

> Create a plan to implement tagging on posts. These should be pill-style text colored tags which are “post”, “WIP”, “talk”, “notes”.

At first, I was impressed. It returned a 5 step plan with a button on each step to “Start task”. Each task seemed to work pretty well, but I realized I wanted to be more specific with the implementation

> Create a plan to implement tagging on posts. These should be pill-style text colored tags which are “post”, “WIP”, “talk”, “notes”. In parts of the code, I take the title and description etc from the blog post md files and process those to display on the posts, use that model to take tags from the Md file properties section and apply it to the post. The tag types should be configured as tests, either pre-commit or otherwise, to standardize tags

This is where the bugs really started. I added the new requirements in one of the tasks’ conversation thread. This resulted in the thread getting stuck hanging and not allowing me to interrupt. OK, I thought, I’ll add this in the main conversation thread instead. Same result, unfortunately. 

Ok, I thought again, I’ll send the new prompt in a new codex task instead. I hear it’s better to treat agents as slot machines by spinning again rather than trying to steer the output of a thread. For the life of me, I couldn’t remember how to get it to spit out a plan with the actionable steps. Instead, it output plan.md files with design specs for the feature. No problem, I’ll just paste the design spec into yet another new codex thread. This time, it made the changes in a single go by modifying 15 files and running the Django app in a container. A little unwieldy, but cool!

From there, Codex displayed a button with the GitHub logo allowing me to create a PR (or draft PR) with a concise description. Reviewing the PR on the GitHub mobile app was surprisingly easy!

In the end, this website now supports tagging posts, and this was a fun glimpse into the world of agentic coding. I didn’t write a line of code and saw this feature completed end-to-end while in the passenger seat of a car. Feels genuinely revolutionary in some ways. If I tightened the development loop (maybe by automating more tests and finding a way for Codex to show me the changes in a dev environment), this would a viable workflow for some serious development work.

Side note: this could make folding phones more useful. Might be nice to review code on a larger screen.

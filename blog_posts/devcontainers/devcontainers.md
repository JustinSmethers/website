---
title: Devcontainers
description: Experimenting with devcontainers for Codex and day-to-day development
thumbnail: thumbnail.png
tags:
  - post
date: 2025-12-22
---

# Devcontainers

I've recently been experimenting with devcontainers with the goal of running Codex in --yolo mode. So far, it's awesome and also tricky to set up. Here are some notes on my experience.

## Why do this?
Codex and Claude Code have gotten to the point that they can handle basically all simple implementations and bug fixes on their own. However, they constantly need approval for commands they want to run in the terminal. As I scale up my agent usage, this is becoming a bottleneck. I wanted to be able to setup a git worktree for a feature, include any context on the task, and let the agent run until completion. Both Codex and Claude Code have flags to run without asking for permissions (--yolo for Codex and --dangerously-skip-permissions), but you might surmise from the names, these modes come with serious risks: they can do anything on your machiine, including deleting files, exfiltrating data, changing system settings, etc.

Enter devcontainers. devcontainers are isolated development environments that run in containers. By running Codex in a devcontainer, I can limit the potential damage it can do to my host machine. If something goes wrong, I can simply delete the container and start fresh. This also just *feels right* in the ethos of working with agents: when the entire environment is disposable and quick to spin up, you can easily pull the lever on the Codex slot machine and let it run wild. 

## My setup so far
I have a couple different setups for devcontainers right now. I have a "base" setup in my dotfiles repo that I use for day-to-day development - [link](https://github.com/JustinSmethers/dotfiles). This includes a python environment with mounts to my Codex and uv configs. I also have Claude Code mounts but I have that in an example file since mounts will error if the files don't exist on the host mahcine - I haven't figured out an ergonomic way to handle that yet. There's also some messy leftover bits from when I was trying to have a configurable firewall for network access, but I haven't fully implemented that yet.

I have another setup for this website which essentially creates a website-in-a-box. It has everything needed to run the site, including a postgres database, and mounts to my blog post drafts. This way, I can let Codex run wild developing this website. Even cooler, the devcontaienr has playwright installed, so Codex can visually inspect changes as it goes. This has been a huge unlock in having Codex be totally autonomous in developing the site. Link to the repo [here](https://github.com/JustinSmethers/website).

## What's next?
I plan to keep iterating on my devcontainer setups. Some things I want to explore:
- a full data-stack-in-a-box for data projects. This would include a database (duckdb) and the ability to connect to cloud data warehouses (snowflake) for source data.
- More ergonomic handling of config files for different agents
- Better dev setup for VSCode with more extentions and settings
- A shell script to automate the creation of git worktrees, devcontainers, and context gathering from Jira/tickets/PRs. I have a git worktree script already, but I haven't cracked the worktree + devcontainer setup so that it has access to the right .git, so I'm having to manually set that up for now.

## Note
The thumbnail feels accurate for what I'm trying to do here with simple tasks, and also the thought of handing AI my job is anxiety inducing. But I do think this is the future of development. Now how do I make sure I have a job in that future...
---
title: Fluent Python Notes Part 3 (Chapter 11)
description: Consolidated notes from Fluent Python part 3 covering chapter 11
thumbnail: thumbnail.png
tags:
  - notes
date: 2025-09-08
---

# Fluent Python Notes Part 3

## Chapter 11 - A Pythonic Object

This chapter covers implementing the special methods in a class in Python in order for your user-defined object to behave Pythonically, and that is to use the built-in operators and to inherit language behavior of things like equality and hashability and things like that. It's really mostly useful, seemingly, for defining libraries and modules that other programmers will use just to make it more simple to use and more compatible with standard operations like equality and hashability and putting objects into sets and things like that. Some notes that's interesting, it covers the use of static methods and class methods, particularly stating that class methods are useful for providing alternative constructors for classes. It covers hashability and making a class mutable by implementing the hash function within a class. It discusses the slots attribute to save memory when defining a class, but again, probably only useful when building libraries. It discusses the use of private attributes by using double underscores, which Python then does “name mangling” to rename the private variable, so it's still accessible by the mangled name, which is _classname__attributename. And the alternative convention of just putting a single underscore, which is more disrespected by developers rather than mangled by the interpreter itself.

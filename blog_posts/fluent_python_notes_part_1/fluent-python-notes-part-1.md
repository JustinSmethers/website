---
title: Fluent Python notes part 1 (chapters 1-6)
description: Consolidated notes from Fluent Python part 1 covering chapters 1 through 6
thumbnail: thumbnail.png
tags:
  - notes
date: 2025-08-17
---

# Fluent Python Notes Part 1

## Chapter 1 - The Python Data Model

Voice note:
> Chapter 1 covers the Python data model and extending built-in functions for particular data types, in particular, how to define functions that you might use to override default methods when defining a class, for example, using functions to overwrite built-in functions for vectors, such as representing a vector with the REPR dunder function to give instead a formatted string value, so when you print the vector object, you get a nicely formatted return, or the absolute value function, which you would return the hypotenuse of the vector in order to get the absolute value of the vector itself, or summing a vector, where you overwrite the dunder add function to add the x values and the y values of two respective vectors in order to get an actual vector addition. It then goes over string representation in more detail using the REPR or dunder STR function. It talks briefly about Boolean values and the Collection API, which maps out all of the built-in internal functions for collections in Python. It talks about why length is not a method, because it uses CPython objects assigned to objects, which is just a faster way to retrieve the length rather than having to call a method every time. Note that the len() function is called, and it also lists the method names for all the different categories of collections or special methods in Python.

Summary:
### Fluent Python – Chapter 1 Notes

### Overview
Chapter 1 introduces Python's **data model** and how to make custom objects integrate seamlessly with built-in language features by implementing special ("dunder") methods.

### Key Topics

### Python Data Model
- Python uses **special methods** (e.g. `__repr__`, `__abs__`, `__add__`) to enable custom behavior for built-in functions and operators.
- By implementing these in user-defined classes, objects can behave more like built-in types.

### Example: Custom Vector Class
- **`__repr__`**: Customize how objects are represented in the console (used by `repr()` and in interactive sessions).
- **`__str__`**: Used by `print()` to return a readable string representation.
- **`__abs__`**: Override to define what `abs(my_vector)` should return — e.g., Euclidean norm (hypotenuse).
- **`__add__`**: Enable vector addition via `+` by returning a new vector with summed components.

### String Representation
- Prefer implementing `__repr__` over `__str__` for debugging.
- `__repr__` should ideally return a string that can recreate the object (`eval(repr(obj)) == obj`).

### Boolean Evaluation
- Objects can define **truthiness** using `__bool__()` or `__len__()`.
- Falsy if `__bool__()` returns `False` or `__len__()` returns `0`.

### Collections API
- Python collections rely on special methods:
  - `__len__()` for `len()`
  - `__getitem__()` for indexing
  - `__iter__()` for iteration
  - Others: `__contains__()`, `__reversed__()`, `__setitem__()`, etc.

### Why `len()` is Not a Method
- `len(obj)` is faster than `obj.len()` due to internal C-level optimizations (CPython uses a slot in the object structure).

### Collection Categories
- Lists, tuples, dicts, sets, and user-defined collections implement different combinations of special methods to provide:
  - Sequence behavior
  - Mapping behavior
  - Mutable/immutable variants

## Takeaways
- Implementing special methods makes your classes more Pythonic.
- Think in terms of interfaces (how objects should behave) rather than inheritance.
- The data model is central to idiomatic, elegant Python.

## Chapter 2 - An Array of Sequences

In Python, the built-in sequences consist of container sequences, which can hold different types of objects within themselves. These are lists, tuples, collections.dq, are some examples. And there are also flat sequences that can only hold one simple type. These are like strings, bytes, and array.array, for example. In addition, there are other waste group sequences, which are immutability. Some examples of immutable sequences are lists, arrays.arrays, collections.dq. There are immutable sequences, for example, tuples, strings, and bytes. The chapter talks about list comprehensions and generator expressions. List comprehensions I am pretty familiar with, I suppose, although I could always use more practice. Something I didn't know is the scope of comprehensions. You can use the walrus operator, which is the colon equal operator, to make variables accessible outside of list comprehensions. Unless you use the local and global flags, local1 will contain it to the list comprehension. It goes into using list comprehensions for Cartesian products. Lists also gets into generator expressions. These are expressions like the function tuple, where you wrap a for loop in the tuple function, or in array.array to produce or generate one of those data types. The advantage of this is it doesn't have to first create a list for use with certain operations. For example, it has an advantage over using a list comprehension to take the Cartesian product of two lists of a thousand elements each, because that would produce a list of a million elements before doing some operation within the loop. Instead, you can use a generator expression to not create an overall object to hold all those. One fascinating thing that I had never thought about was using tuples as not just immutable lists, but as records. The idea being that tuples are records without field names, where each element is a field. Since you know the length is going to be the same and that the values can represent certain ideas, it can act as a table that doesn't have field names.

It covers unpacking as it pertains to unpacking an object, say a list or iterable, and assigning the values to variables. It covers using unpacking characters, i.e. the asterisk symbol, to unpack values returned from a function or to pass values into a function while unpacking them. It also covers using the undercase as ignoring values returned from some sort of function in Python and how those values don't actually get assigned. It can also do asterisk extra, which assigns the extra values as a list with zero more items, which is crazy. That seems like a bit much. It also covers match case, which seems to be just a cleaner, more readable way to do a series of matching inputs to a series of outputs. It gives the example of matching latitude and longitude to a certain value by using match case statements, which is cleaner than the if-else. It also gives the disclaimer that when pattern matching in this way, like with match case, you can't iterate over string bytes and byte arrays because this could lead to unintended bugs in those records where you match too many records.

It discusses slicing and how it can be used to iterate through and replace objects in an iterable object, primarily lists. It also discusses the different way to sort arrays and lists, really lists, which I'm aware of already. And it mentions MemoryViews, which is a built-in class which I hadn't heard of, which is essentially a generalized numpy array structure in Python itself, which allows sharing memory between data structures without first copying, which is important for large datasets.

Some other highlights to remember, slicing is very powerful when used with different objects and can even support named slices, which is useful for just readability, it also discusses numpy and pandas a bit, just to highlight other libraries that support different collections, although I don't use numpy much since I use DuckDB or just other things, so I'm not too worried about that, although the collections library itself has a lot of different options. I think mastering, unpacking, this comprehensions and generators would be very useful.



### ChatGPT summarized notes
Here’s your **structured summary** of your notes, followed by a **gap analysis** comparing them against the full chapter text.

---

## **Structured Summary of Your Notes**

### 1. **Types of Built-in Sequences**

- **Container sequences** – hold different object types (e.g., `list`, `tuple`, `collections.deque`).
    
- **Flat sequences** – hold one simple type (e.g., `str`, `bytes`, `array.array`).
    
- **Immutable sequences** – `tuple`, `str`, `bytes`.
    
- **Mutable sequences** – `list`, `bytearray`, `array.array`, `collections.deque`.
    

---

### 2. **List Comprehensions**

- Familiar concept; useful for building lists concisely.
    
- **Scope**: variables inside comprehensions are local to them, except variables created via the **walrus operator (`:=`)** which can escape to outer scope.
    
- **Cartesian products**: can combine multiple sequences (e.g., `[(color, size) for color in colors for size in sizes]`).
    
- **Good practice**: use for producing lists only, avoid if not storing the result.
    

---

### 3. **Generator Expressions**

- Similar syntax to list comprehensions but use parentheses.
    
- Useful for initializing other sequence types (`tuple`, `array.array`) without first building an intermediate list.
    
- More memory-efficient, especially for large Cartesian products.
    

---

### 4. **Tuples**

- Not just immutable lists — also useful as **records without field names** (position in tuple conveys meaning).
    
- Can be unpacked easily.
    
- Advantage: **clarity** (fixed length) and **performance** (smaller memory footprint, possible optimizations).
    

---

### 5. **Unpacking**

- Works for sequences and general iterables.
    
- Can use `*` to capture excess values.
    
- `_` conventionally used to ignore values (not bound in `match` patterns).
    
- Supports nested unpacking.
    
- `*extra` binds extras to a list; `*_` ignores extras.
    

---

### 6. **Pattern Matching (`match` / `case`)**

- Cleaner alternative to multiple `if/elif` checks.
    
- Matches sequences by structure and optionally type.
    
- Strings, bytes, bytearrays treated as atomic in matches (not iterated).
    
- Supports variable binding with `as`.
    
- Guards (`if`) filter matches.
    

---

### 7. **Slicing**

- Can replace parts of sequences in-place (for mutable sequences).
    
- Named slices improve readability.
    
- MemoryView — built-in type for memory sharing (avoids copying).
    
- Slice step can be negative for reversed order.
    
- Useful in multi-dimensional contexts (NumPy, pandas).
    

---

### 8. **Other Highlights**

- **Collections library** provides additional sequence-like containers.
    
- Unpacking, comprehensions, and generators are key tools to master.
    
- NumPy/pandas mentioned as external tools for advanced slicing and collections handling.
    

---

## **Gap Analysis – Missing or Underdeveloped in Your Notes**

From the chapter content, here are key areas **not covered or only lightly covered** in your notes:

1. **Performance & Storage Model of Sequences**
    
    - Memory diagrams comparing **container** vs **flat sequences**.
        
    - Per-item object header overhead in Python objects vs raw C array storage.
        
    - Comparison of `list` vs `tuple` performance and allocation strategy.
        
2. **map/filter vs list comprehensions**
    
    - Readability and performance comparison.
        
    - Example showing list comprehensions can be faster.
        
3. **Tuple Mutability Caveat**
    
    - Tuples are immutable in references, not in contained mutable objects.
        
    - How to check if an object is fully immutable (`hash` check).
        
4. **Advanced Unpacking**
    
    - Function call unpacking with multiple `*` or `**` unpacking.
        
    - Rare use-case of unpacking into a list for enforcing record count from queries.
        
5. **Pattern Matching – More Complex Features**
    
    - Type constraints in patterns (e.g., `case [str(name), *_, (float(lat), float(lon))]`).
        
    - `_` wildcard can appear multiple times.
        
    - Using `as` for binding parts of a match.
        
    - Example from `lis.py` interpreter refactoring.
        
6. **Slicing Details**
    
    - Why Python slices/ranges exclude the last index (Dijkstra’s argument).
        
    - `slice` objects for naming ranges (like spreadsheet ranges).
        
    - Ellipsis (`...`) usage in slicing.
        
7. **Sequence Operations**
    
    - `+` and `*` behavior for mutable vs immutable sequences.
        
    - Pitfalls when multiplying sequences containing mutable items (`[['_']]*3` problem).
        
    - Augmented assignment (`+=`, `*=`) differences between mutable/immutable sequences.
        
8. **Special Gotchas**
    
    - `A += B` puzzle where tuples containing mutable elements both mutate and throw `TypeError`.

## Chapter 3 - Dictionaries and Sets

The chapter talks about dict comprehensions and going over those, which are very much similar to list comprehensions, just in dictionary format. It gets a bit more into unpacking mappings, and I did some additional reading to make sure I understood the args and kwargs arguments, as well as the syntax around using single asterisks and double asterisks, which I didn't understand that the asterisks are the important part, that the single asterisk, when used in a function call, collects arguments into a tuple, and a double asterisk collects arguments into a dictionary, into keyword arguments, so if they're specified as keywords, and that the double asterisk has to be used last in a function to collect everything else into the dictionary, the single asterisk has to be used before that if you use both. So the chapter talks about unpacking dictionaries with double asterisks, so the flip side of using it in functions where using it to unpack will pull keys and values out of a dictionary with mapping running for it. It also talks about merging mappings with the pipe operator and the pipe equals operator, where merging will merge two mappings together, typically by overwriting the first mapping called with the second, so if they contain the same key, then the key in the second mapping will be the one that survives the merging operation. It also talks about pattern matching with match case, and one distinction between pattern matching with mappings versus structures like strings and lists in the last chapter is that you don't have to specify all keys in a match case as long as it matches the keys you do specify, which might have had to be a little bit more specific with how you match, but it also allows a little more flexibility.

It covers briefly what is hashable, which is something that has a consistent ID or hash value, no matter if it's mutated or not. So, lists will change when they're modified, so they're not hashable. And that dicts can't have mutable values as keys.

There are several ways to handle missing keys in dictionaries. One way is to use the DefaultDict method, which is another version of Dict. Seemingly, what you can do is counter DefaultDict. You can use the DefaultDict method to counter a copy of the dictionary. You shouldn't DefaultDict. DefaultDict doesn't exist in the dictionary. So there's a lot of issues around switching up keys that don't exist inside a standard dictionary copy of the dictionary.

It also covers sets in Python, which is a way to store unique values. It requires only hashable items within the set. There's also FrozenSet, which is hashable because it is immutable. It covers the set operations, so the union, intersection, the symmetrical intersection, and other things, and how those set operations can also be used on dictionaries. It talks about instantiating a set and how you have to use either the curly braces for a set itself or the constructor for a set. FrozenSet only has a constructor. It also talks a bit about dictionary views and how referencing dictionary keys, values, and items creates a view, which is more limited on what kind of methods can be used on them, but reduces memory on referencing those objects.

## Chapter 4 - Unicode Text versus Bytes

I didn't really take much away from the encoding and decoding chapter. A couple notes around, you can encode string into bytes, and you can decode bytes into string. There are different encoding formats. But I've not really worked with encoded text before. Or, it seems like it might be useful if you're dealing with emojis, for one thing, because they have Unicode byte representations. Or text with accents, or non-English characters. One useful pattern, it seemed, that I took away was the encoding sandwich. As soon as you process bytes, decode them to strings, process data with the string representation, and then when you go to output, encode them back into bytes.

## Chapter 5 - Data Class Builders

The chapter mainly covers three different types of data class builders, the collections named tuple object, the typing named tuple object, and the data class feature of Python, which is declared by having a annotation above a class, which specifies it's a data class. Classic named tuples from the collections object seems just outdated, and seems to be used for demonstration purposes. Typed named tuples and data classes seem to cover a lot of the same ground. Data classes seem to be the more ideal implementation, and the more readable, in my mind. So, I think I would use data classes. Talks about the difference between instance variables and class variables, and workarounds in data classes to declare these. That is, variables that are attributes of an instance declared of that class, and attributes available to the class itself, and not to the instance. These are declared using the init var and class var functions within data classes library. It also covers data classes as a code smell, the idea that data classes can be indicative of poor system design, where instead there's probably behavior that also belongs to the data class, which should instead be implemented in just a full-blown class, not a data class specifically. So, it can indicate refactoring is needed, where behavior is pulled back into the data class as functions to make a regular class. It also briefly touches on pattern matching class instances, with different ways to do that, which specifies with simple class patterns, keyword class patterns, and positional class patterns, really just matching variables using keyword patterns seems to be the most readable and usable. I assume pattern matching will be covered more later. The author notes it’s probably more important to know how to use classes in this way rather than write them

## Chapter 6 - Object References, Mutability, and Recycling

The chapter covers immutable and mutable objects equality references, so checking if A == B. For immutable objects, it's checking the IDs, so it can be safe, but for mutable objects, it's checking the values. It talks about simple assignments of variables that don't create copies of objects, but if you do a plus equals or times equals, it will create a new object on the left-hand side if it's bound to an immutable object, but it may modify mutable objects in place. It talks about if there's an existing value, it does not change the object previously bound to it, because that's called rebinding. The variable is now bound to a different object. Once there are zero references to an object, then it will be garbage collected and deleted, which the del operator removes references. It doesn't necessarily delete unless the reference count is zero. Function parameters are passed as aliases, which means that the function may change any mutable object received as an argument, so you need to be very careful when processing things like lists, where you need to create a copy of the list before processing or modifying it. There's no way to prevent that except create local copies or using immutable objects, so passing a tuple instead of a list. Using mutable objects as defaults for a function parameter is dangerous, because if the default is modified, then every future call of that function relies on that default, which will now reference the modified object instead of the empty list as default or whatever default you actually assigned. The author makes the point that this chapter would not be necessary if all Python objects were immutable. This is just like the edge cases around having immutable and mutable objects. References languages like Elixir, where all data types are immutable by default to avoid some of these. Immutable objects are the main reason why programming threads is so hard to get right. Threads mutating objects without proper synchronization produce corrupted data. However, excessive synchronization, on the other hand, causes deadlocks, which I'm sure will be covered in later chapters.

# TO DO: Replace readme placeholders with actual content
# EXPAT (used as 'expat <command> <etc>')

This program does...

This program supports...

Additional features include...

## Installation
Download the files and install locally with pip. Requires Python 3 and the `click` package (this should be installed automatically because it's a required package).

`pip install .`

Once installed, run `expat -h` or `expat --help` in the terminal for usage instructions.

## Usage
This is what the help screen shows.
```
TERMINAL USAGE OUTPUT HERE
```

If using the Stanford CoreNLP pipeline, the recommended script to start the CoreNLP Server is:
``` sh
java -mx6g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000 -annotators tokenize,ssplit,pos,lemma,ner,truecase,parse,depparse
```
Otherwise, the NLTK annotator does PoS tagging, lemmatising (maybe?), and basic NER and has no external dependencies outside NLTK.

## Important info re: patterns
- Patterns cannot end on an optional word, meaning the final word in a pattern must have a minimum of 1 or more (not zero). Instead, just make a copy of the pattern with that as required with a different weight value if the optional parameter is important.

## To-do

- [x] XML Spec and DTD done
- [x] Create classes for the XML elements
- [x] Read and parse XML file
- [x] Check that default values are working
- [x] Connect to Stanford NLP Server
- [x] Main Processing class to parse sentence
- [x] Remove WordGroup
- [ ] Main command-line interface to select annotators, search algorithms, give instructions, input and output
- [ ] Make the graph generation into a class (strategy pattern) rather than baked into the Pattern class. Probably aren't going to be many ways to build a graph but it's safer this way.
- [ ] Refactoring (comment cleanup, code-analysis)
- [ ] Refactoring (file rearranging, namespace cleanup and removing circular dependencies)
- [ ] More tests (edge cases like 1-word patterns, lots of optionals, empty sentences, really bad annotators where everything is None...etc)

## Examples
Using the sample files, an example is:

`EXAMPLE`

This example does _a thing_.

## Further Notes
- Does x.
- Has y.
- Default w is z.


## Pattern File Description
``` xml
EXPAT Template Description

Structural Hierarchy:
<root>
  <patterngroup>
    <pattern>
      <word />
      <word />
      ...
    ...

  DTD Spec for Validation:
  <!DOCTYPE patterngroup [
    <!-- Pattern Group Element -->
    <!ELEMENT patterngroup (pattern)+>
    <!ATTLIST patterngroup version CDATA #REQUIRED>
    <!ATTLIST patterngroup label CDATA "">

    <!-- Pattern Element -->
    <!ELEMENT pattern (word)+>
    <!ATTLIST pattern name ID #REQUIRED>
    <!ATTLIST pattern description CDATA "">
    <!ATTLIST pattern class CDATA #REQUIRED>
    <!ATTLIST pattern weight CDATA "1">
    <!ATTLIST pattern label CDATA "">

    <!-- Word element -->
    <!ELEMENT word EMPTY>
    <!ATTLIST word min CDATA "1">
    <!ATTLIST word max CDATA "1">
    <!ATTLIST word contextual CDATA "false">
    <!ATTLIST word label CDATA "">
    <!-- Specific Word Matching -->
    <!ATTLIST word lemma CDATA "">
    <!ATTLIST word word CDATA "">
    <!-- Parts of Speech -->
    <!ATTLIST word pos CDATA "*">
    <!ATTLIST word expos CDATA "">
    <!-- Dependencies -->
    <!ATTLIST word deps CDATA "*">
    <!ATTLIST word exdeps CDATA "">
    <!ATTLIST word depnum CDATA "1">
    <!-- Additional Type -->
    <!ATTLIST word type CDATA "*">
    <!ATTLIST word extype CDATA "">
    <!ATTLIST word typenum CDATA "1">
  ]>

  Notes:
  - A * own matches anything.
  - The star can be used to match anything starting with a character, so
    VB* matches VBD, VBG and VBZ. *S would match NNS and NNPS.
  - A missing attribute is like a * in most cases. The assumption is that
    if the attibute was not specified, skip all the associated checks.
```

``` perl
  Elements and Attributes:
    <root>
    # Root element. Some version in the future may add other elements that
    # aren't patterns, so <patterngroup> is not the root element.
    - version : float/string
      # e.g. 1.0.
      # This would let the XML interpreter/parser know what elements and
      # structure we are looking for (in a standardised way).
  
    <patterngroup>
    # Only one of these. Container element for patterns.
    - label : string
      # An optional attribute that helps in arranging and debugging.
      # If using multiple files, this allows groups to have a different
      # label to tell them apart.
  
    <pattern>
    # A collection of words that make up a pattern.
    - name : string
      # The unique name of the pattern.
    - description : string
      # A short description or more detailed name of what the pattern is.
    - class : string
      # The class/category that the pattern belongs to, i.e. 'noun-group' or 'prp-phrase'
    - weight : numeric
      # Allows patterns to be ordered or sorted based on
    - label : string
      # More descriptive metadata. Non-operative.

    <word>
    # An item that matches N words that meet its criteria.
    - min : numeric
      # The minimum number of tokens that this word should match.
    - max : numeric
      # The maximum number of tokens that this word should match.

    - pos : string
      # The part(s) of speech to match. Multiple values are comma-delimited.
      # Supports * character.
    - expos : string
      # Parts of speech to exclude. Easier to specify a few in here rather than
      # specify dozens in the allowed.
    
    - deps : string
      # The dependencies to match. Multiple values are comma-delimited.
      # The dependency requires the Governor and Dependent to be specified as a suffix.
      # The following formats are acceptable:
      #   - 'conj-d' for the dependent of a conj.
      #   - 'conj-g' for the governor of a conj.
      #   - 'conj*' or 'conj-*' for either the dependent or governer of a conj.
    - exdeps : string
      # The dependencies to exclude. Multiple values are comma-delimited.
      # Supports the same dependency relationship suffixes.
      # Has the same suffix requirements as 'deps'
      # Supports * character.
    - depnum : numeric
      # The required number of dependencies. If 2 dependencies are specified,
      # a depnum of 1 would be a logical OR while a depnum of 2 would be a logical AND.

    - type : string
      # The word types or categories that the word belongs to. Multiple values
      # are comma-delimited. Supports * character.
    - extype: string
      # The word types or categories to exclude. Multiple values are comma-delimited.
      # Supports * character.
    - typenum : string
      # The number of types or categories the word needs to belong to. If 2, the
      # word must have 2 of the required types (and none of the excluded types if 
      # applicable) for it to match.
    
    - contextual : boolean
      # If True, the word is needed to match the pattern but it is not part of
      # the pattern itself, e.g. to match an adjective that precedes a noun,
      # the adjective is what the pattern should find, but it also needs to find
      # the noun for the pattern to be correct. Therefore, we add the noun to the
      # pattern, but mark it as contextual.
      # Default is False, which means the word is essential to the pattern.

    - lemma and word : string
      # Match lemmas and/or words. Not recommended except in very rare cases
      # because it's not flexible and has the same disadvantages of hardcoded values.
      # Supports the * character.

    - label : string
      # Descriptive metadata for a word. Non-operative.
```
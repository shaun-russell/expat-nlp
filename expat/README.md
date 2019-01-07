# EXPAT (used as 'expat <command> <etc>')

Expat is an NLP command-line application that uses word patterns to identify important elements in sentences.

## Introduction to Concepts
Word patterns are XML objects that specify a sequence of words or word attributes.

### What are word attributes?
Word attributes can be word forms (lemmas), types and categories (part of speech, word extension type), or dependencies. These allow for flexible patterns, as a pattern can simply look for a noun, a verb or adverb, anything with an nmod dependency, or something that is classified as 'animal' by an extension tagger.

An annotator is first run on the sentence to give each word a Part of Speech tag and a Lemma.
Other annotators like the Stanford CoreNLP annotator will add dependencies to each word.
The Extension Type annotator reads an extension file (a text file) which contains a path to a word file, the name of the words' category, the part of speech tags they should be restricted to, and a hint for the lemmatiser (usually 'n' or 'v').

### What are word patterns?
A word pattern is a sequence. Words in this sequence can have a minimum and maximum value, allowing for optional words or up to x number of word occurences.
The default values will match anything, so only the important attributes need to be added in XML.

For a pattern to match, the sentence must contain all the non-optional words. A pattern that looks for a **determiner/article followed by a noun** would match 'a dog', but would not match 'a big dog' (big is an adjective). The adjective could instead be added as an optional word (minimum of 0), and the pattern would match both 'a dog', 'a big dog', 'the house'...etc

Here's an example of how patterns and attributes work:

Our sentence is "I walked to the shops." and we have a single word pattern that looks for a verb with a 'motion-verb' type, followed by an optional adverb, and the word 'to'.
```xml
<pattern name="example-pattern" class="examples">
  <word pos="VB*" type="motion-verb" />
  <word pos="RB*" min="0" />
  <word word="to" />
</pattern>
```
The 'VB*' will match anything that starts with 'VB'. Further uses of stars are described later.
The 'type' attribute requires that word to have been found in the list of words with the 'motion-verb' category. This category would be provided by the user as an extension type. Types are lemmatised and stemmed, so the list only needs one form of 'walk', rather than needing 'walking', 'walks', and 'walked'.
The 'word' attribute will match if the word is 'to', and the lemma attribute works in the same way (just using the lemma instead).

In the sentence "I walked to the shops.", the example pattern would match "walked to". If we had a comprehensive list of motion-verbs, we could also match "strolled to", "roamed to", and "scampered to" with this pattern. It would not match "walked a long way to", because our pattern requires the verb to be directly followed by either a 'to' or an adverb.

## Installation
Download the files and install locally with pip. Requires Python 3 and the necesary packages should be fetched on installation.

`pip install .`

Once installed, run `expat -h` or `expat --help` in the terminal for usage instructions.

## Usage
This is what the help screen shows.
```
Usage: expat [OPTIONS] IN_FILE PATTERN_FILE EXTENSION_FILE

  The main annotation program called from the command line.

Options:
  -a, --annotator [nltk|corenlp]  The annotator to use for tagging.
  -s, --selector [none|containing]
                                  Which type of selection algorithm to use to
                                  focus the patterns.
  -u, --corenlp-url TEXT          The url of the CoreNLP server.
  -x, --export-matrix FILENAME    A filename to export the pattern matrix to.
  -g, --debug-pattern TEXT        A pattern to run full verbose output on.
  --heading TEXT                  The heading to use for the sentence output.
                                  Default is "sentence", but override this is
                                  there is more than 1 column in the sentences
                                  file.
  --stepwise Manually cycle through the sentences to scan what is matched. 
  -v, --verbose Enables information-dense terminal output. 

  --version Shows the version and exits.

  -h, --help Shows the help text (this) and exits.
```

If using the Stanford CoreNLP pipeline, the recommended script to start the CoreNLP Server is:
``` sh
java -mx6g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000 -annotators tokenize,ssplit,pos,lemma,ner,truecase,parse,depparse
```
Otherwise, the NLTK annotator does PoS tagging, lemmatising (maybe?), and basic NER and has no external requirements.

The biggest differences between Stanford CoreNLP and NLTK is that CoreNLP finds the word dependencies, whereas NLTK does not, but CoreNLP annotation requires the not-so-lightweight CoreNLP server to be running.

# How to run the program
If you are unfamiliar with command line help syntax, the program usage will be explained further here.

### Main Commands

```Usage: expat [OPTIONS] IN_FILE PATTERN_FILE EXTENSION_FILE```

To run this program (once installed) you need the following things.

**expat** is the name of the program you are running)

**IN_FILE** is a file containing a list of sentences your are wanting to process. These should each be on a new line. If each line has both a sentence and results from previous classifiers, make sure that: (a) the file has a TAB delimiter, or (b) the sentence is wrapped in double quotes: "sentence like this".
**IMPORTANT NOTE** If you are using both double quotes and single quotes _in a CSV_, the program _will not read your file correctly_. Normal sentences can contain commas, but the double quote is needed to determine which commas are part of the sentence and which are part of the file structure.

**PATTERN FILE** is the .xml file containing the patterns. Please keep the DOCTYPE definition as this provides validation and default values for the Pattern. Defaults are not hard-coded, which means you can make custom defaults in your pattern files. Expat will parse your pattern file and should tell you if and where it encounters any errors in your XML file. External XML validators will do this for you and may be more convenient.

**EXTENSION FILE** is where Expat finds extension types. This has a semicolon delimited format that _should not be changed_ (otherwise the program won't work).
Lines starting with a # are comments and are ignored. Patterns can be easier to write with shorter type names, so comments are recommended.
An example type extension line is: ```motion-verb;VB*;path/to/motion-verbs.txt;v```. The first column is the type name (motion-verb), the second column is the parts of speech it is restricted to (supports stars and comma lists), followed by the path to the file, and ending with a hint for the lemmatiser. Since the words in a file have no context to infer parts of speech, this must be provided. Verbs should have a 'v', and all others can have an 'n'.

### Options
  `-a, --annotator [nltk|corenlp]` The annotator to use for tagging. If corenlp, provide the --corenlp-url of the server.

  `-u, --corenlp-url TEXT` The url of the CoreNLP server.

  `-s, --selector [none|containing]` Which type of selection algorithm to use to focus the patterns.
  
  `-x, --export-matrix FILENAME` filename to output the pattern matrix to. The pattern matrix has columns for the sentence and the results of each pattern for that sentence.

  `-g, --debug-pattern TEXT` Specify a pattern name to run full verbose output on it. Use this if you have a pattern that doesn't seem to be matching correctly and it will show the key steps that the program is taking to match this pattern.

  `--heading TEXT` The heading to use for the sentence output. Default is 'sentence', but it is the column name for the text being annotated in the final output. Override this if there is more than 1 column in the sentences file, e.g. sentence,class1,class2

  `--stepwise` Manually cycle through the sentences to scan what is matched. Use this when debugging a pattern as it pauses the program after each sentence, allowing you to look at each result (to debug or investigate).

  `-v, --verbose` Enables information-dense terminal output. This is dense output and is useful for higher level debugging, seeing what patterns have matched, and what the annotated sentence looks like.

  `--version` Show the version and exit.

  `-h, --help` Show this message and exit.

## Important info regarding patterns
- Patterns cannot end on an optional word, meaning the final word in a pattern must have a minimum of 1 or more (not zero). Instead, just make a copy of the pattern with that as required with a different weight value if the optional parameter is important.
- At this stage, contextual does nothing. Its future purpose is to represent part of a pattern that is needed for matching, but is ignored once matched. An example would be if a verb pattern needs a noun to match, but the output should only be the verb (the noun is left out because it is _contextual_).

## Writing word attributes
A word attribute supports both globbing (the star \*), and list notation. For example to match any noun, instead of writing `pos="NN,NNS,NNP,NNPS"` for every pattern, the star \* allows you to just write `pos="NN*"` instead. This matches anything _starting with_ 'NN'.

Other examples of star use are:
- `"*"` matches anything and everything
- `"*ing"` matches anything _ending with_ 'ing', like many verb forms.
- `"A*ed"` matches _starting with_ 'A' and _ending with_ 'ed'.
- `"*in*"` matches anything which contains the letters 'in'.

List notation uses commas to separate match criteria. Using the examples above, a word that needs to end with 'ing', start with 'A' and end with 'ed', or contain 'in' would be notated as `"*ing,A*ed,*in*"`. This is useful for checking multiple part of speech tags.

A word can require a certain number of these listed match criteria by using the 'typenum' and 'depnum' attribute for types and dependencies, respectively. There is no 'posnum' because a word can only have 1 part of speech tag (though this can be changed in a custom implementation).

```xml
<word type="has-legs,flies,eats-veges" typenum="2" />
```
The word pattern above would look for an animal name that _has two of the specified types_. If we assume the type categories are correct and comprehensive, a seagull would match as it has legs, flies (2/3). A snail eats veges, but cannot fly and has no legs (1/3) and therefore would not match this word pattern.


## Example Files
Example files are provided in the `sample_files` folder. The sample files contain geospatial vocab lists, an extension file, a pattern file, and some sentences.

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
      # Allows patterns to be ordered or sorted based on how the user ranks their effectiveness/importance
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
      # NOT IMPLEMENTED YET
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
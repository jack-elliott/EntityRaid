# EntityResolutionSNA
Developing methods for Entity Resolution through text-based, phonetic, and sub-network similarity measures in Python.

EntityRAID (Entity Resolution for Ambiguous Interaction Data) significantly reduced resource requirement for large scale SNA. EntityRAID is written
in very basic code and is intended to be user friendly. 

  EntityRAID's input:

    - Raw interaction data produced via name-generator surveys in .csv
    - Optionally, a school roster with participant information in .csv

  EntityRAID's output:

    - Fully resolved interaction data in .csv
    - Adjacency Matrix in .csv

EntityRAID resolves references in the data in stepwise stages, starting with references that can be resolved with highest confidence first:

  STAGE 1: Identify High Confidence Identities
    - Compile a numbered key of 'high-confidence' identities (self-reported names and names from the roster) and school numbers (if applicable)
  STAGE 2: Resolve High Confidence Identities
    - Resolve exact instances of high-confidence key names in the interaction data
  STAGE 3: Identify and Resolve High Confidence Variants
    - Identify names in the interaction data that could be variants of high-confidence identities and compare them to key names via
      the Levenshtein distance and the Levenshtein distance of the respective double metaphone algorithm key codes
  STAGE 4: Identify and Resolve Low/No Confidence Identities
    - Identify non-participant full name references to create a low-confidence key. Use this key to resolve such references
    - Identify and resolve first name-only references to a number with no confidence
    
  Data manipulation uses pandas for .csv data manipulation, and pythonic indexing throughout. Please see the example file for how your interaction data
  and initialized key should be organized. 




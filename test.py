from fuzzywuzzy import fuzz
from fuzzywuzzy import process

ratio = fuzz.partial_ratio(
    "fuzzy", "International Journal of Fuzzy Logic and Intelligent Systems"
)

print(ratio)

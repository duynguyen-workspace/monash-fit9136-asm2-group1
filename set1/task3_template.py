from typing import Tuple, List


def get_vocabs_simple(text: str) -> Tuple[Tuple[str], Tuple[int]]:
    pass


def get_vocabs(text: str) -> Tuple[Tuple[str], Tuple[int]]:
    pass

# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    the_example_str = "you are good at python , and you will be master of programming ."
    print(get_vocabs_simple(the_example_str))
    print(get_vocabs(the_example_str))
#from Project1.logic import *
from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# A says "I am both a knight and a knave."
# A diz: "Sou um cavaleiro e um patife"

knowledge0 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Implication(AKnight, And(AKnight, AKnave) ),
    Implication(AKnave, Not(And(AKnight, AKnave)) ),

)



# Puzzle 1
# A says "We are both knaves."
# B says nothing.

#A diz: “Nós dois somos uns canalhas.”
#B não diz nada.
knowledge1 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave))),
)


# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
#A diz: “Somos da mesma espécie.”
#B diz: “Somos de tipos diferentes.”
knowledge2 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    Implication(
        AKnight,
        Or(
            And(AKnight, BKnight),
            And(AKnave, BKnave)
        )
    ),
    Implication(
        AKnave,
        Not(
            Or(
                And(AKnight, BKnight),
                And(AKnave, BKnave)
            )
        )
    ),

    Implication(
        BKnight,
        Or(
            And(AKnight, BKnave),
            And(AKnave, BKnight)
        )
    ),
    Implication(
        BKnave,
        Not(
            Or(
                And(AKnight, BKnave),
                And(AKnave, BKnight)
            )
        )
    ),
)


# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
#A diz: “Sou um cavaleiro.” ou “Sou um patife.”
#B diz: “A disse: ‘Sou um patife.’” e “C é um patife.”
#C diz: “A é um cavaleiro.”
knowledge3 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),
    Or(
        A_said_knight := Symbol("A said 'I am a Knight'"),
        A_said_knave := Symbol("A said 'I am a Knave'")
    ),
    Or(
        And(A_said_knight, Not(A_said_knave)),
        And(Not(A_said_knight), A_said_knave)
    ),
    Implication(AKnight, Biconditional(A_said_knight, AKnight)),
    Implication(AKnave, Biconditional(A_said_knight, Not(AKnight))),
    Implication(AKnight, Biconditional(A_said_knave, AKnave)),
    Implication(AKnave, Biconditional(A_said_knave, Not(AKnave))),
    Implication(BKnight, A_said_knave),
    Implication(BKnave, Not(A_said_knave)),
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight))
)




def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()

# Install: pip install z3-solver

from z3 import *

# ------------------------------------------------------------
# Domains / Sorts
# ------------------------------------------------------------
Participant = DeclareSort("Participant")
Field       = DeclareSort("Field")
Purpose     = DeclareSort("Purpose")
Agent       = DeclareSort("Agent")
System       = DeclareSort("System")

# Time is represented as integers: 0, 1, 2, ...
Time = IntSort()

# ------------------------------------------------------------
# Variables
# ------------------------------------------------------------
p       = Const("p",       Participant)
f       = Const("f",       Field)
rho     = Const("rho",     Purpose)
A       = Const("A",       Agent)
S       = Const("S",       System)
t       = Int("t")
t_prime = Int("t_prime")

# ------------------------------------------------------------
# Predicates
# ------------------------------------------------------------
Cap      = Function("Cap",      Participant,              BoolSort())
Info     = Function("Info",     Participant,              BoolSort())
Vol      = Function("Vol",      Participant,              BoolSort())

Withdraw =     Function("Withdraw", System, Participant, Time, BoolSort())
ConsentValid = Function("ConsentValid", Participant, Time, BoolSort())
Collect = Function("Collect", System, Field, Participant, Time, BoolSort())
UseData = Function("UseData", System, Participant, Time, BoolSort())

IdentifyingField = Function("IdentifyingField", Field,              BoolSort())
Necessary        = Function("Necessary",        Field, Purpose,     BoolSort())

Fair          = Function("Fair",          System, BoolSort())
BiasMitigated = Function("BiasMitigated", System, BoolSort())
Discriminate =  Function("Discriminate", System, Participant, Time, BoolSort())
Responsible   = Function("Responsible",   System, BoolSort())
Supervises =    Function("Supervises", Agent, System, BoolSort())
Ethical       = Function("Ethical",       Agent, BoolSort())

# ------------------------------------------------------------
# Deontic encoding notes:
# O(phi) = phi must hold (encoded as the formula itself)
# F(phi) = Not(phi)      (phi is forbidden)
# A -> B = Implies(A, B) (necessary condition)
# ------------------------------------------------------------
constraints = []

# ------------------------------------------------------------
# (a1) Valid consent requires capacity, information, voluntariness
# Paper: O(ConsentValid(p,t) -> (Cap(p) /\ Info(p) /\ Vol(p)))
# If consent is valid, all three conditions must hold.
# ------------------------------------------------------------
C1= ForAll([p, t],
        Implies(
            ConsentValid(p, t),
            And(Cap(p), Info(p), Vol(p))
        )
    ) 
# constraints.append(C1)

# ------------------------------------------------------------
# (a2) Withdrawal invalidates consent at all future times
# # Paper: O(Withdraw(S,p,t) -> G_{t'>t} -ConsentValid(p,t'))
# ------------------------------------------------------------
C2 = ForAll([S, p, t, t_prime],
    Implies(
        And(Withdraw(S, p, t), t_prime > t),
        Not(ConsentValid(p, t_prime))
    )
)

# ------------------------------------------------------------
# (b) Forbidden to use data without valid consent
# Paper Eq(3): # O((Collect(S,f,p,t) \/ UseData(S,p,t)) -> ConsentValid(p,t))
# Equivalent to: F((Collect \/ UseData) /\ -ConsentValid)
# ------------------------------------------------------------
C3 = ForAll([S, f, p, t],
    Not(
        And(
            Or(Collect(S, f, p, t), UseData(S, p, t)),
            Not(ConsentValid(p, t))
        )
    )
)
# constraints.append(C3)

# ------------------------------------------------------------
# (c) Forbidden to collect unnecessary identifying fields
# Paper: # Paper: F(Collect(S,f,p,t) /\ IdentifyingField(f) /\ -Necessary(f,rho))
# ------------------------------------------------------------
C4 = ForAll([S, f, p, t, rho],
        Not(And(
            Collect(S, f, p, t),
            IdentifyingField(f),
            Not(Necessary(f, rho))
        ))
    )

# constraints.append(C4)

# ------------------------------------------------------------
# Paper Eq(5): O(Responsible(S) -> Fair(S) /\ BiasMitigated(S) /\ ForAll p,t -Discriminate(S,p,t))
# Uses Implies to encode -> (necessary condition)
# If system is responsible, it must satisfy these conditions.
# Additional criteria such as transparency may also be required.
# ------------------------------------------------------------
C5 = ForAll([S],
        Implies(
            Responsible(S),
            And(
                Fair(S),
                BiasMitigated(S),
                Not(Exists([p, t], Discriminate(S, p, t)))
            )
        )
    )
# constraints.append(C5)

# ------------------------------------------------------------
# Ethical Agent Definition: necessary condition
# Paper Eq(6): Ethical(A) -> ForAll S: Supervises(A,S) -> Responsible(S)
# C1-C5 globally asserted above cover the remaining conjuncts of Eq(6)
#  C1–C5 collectively constitute Constraints(S)\text{Constraints}(S)
# Constraints(S).
# ------------------------------------------------------------
C6 = ForAll([A, S],
    Implies(
        And(Ethical(A), Supervises(A, S)),
        Responsible(S)
    )
)

constraints.extend([C1, C2, C3, C4, C5, C6])




# ------------------------------------------------------------
# Helper function
# ------------------------------------------------------------
def check_case(name, s, extra_constraints=None, expected=None):
    s.push()

    if extra_constraints is not None:
        if isinstance(extra_constraints, list):
            s.add(*extra_constraints)
        else:
            s.add(extra_constraints)

    result = s.check()

    expected_str = f" | expected: {expected}" if expected else ""
    match = ""
    if expected:
        match = " ✓" if str(result) == expected else " ✗ MISMATCH"

    print(f"{name}: {result}{expected_str}{match}")

    if result == sat:
        print(s.model())
    elif result == unsat:
        print("Unsat core:", s.unsat_core())

    print("-" * 70)

    s.pop()



    

if __name__ == "__main__":

    s = Solver()

    for i, c in enumerate(constraints):
        s.assert_and_track(c, f"C{i}")

    result = s.check()
    print("Global satisfiability:", result)

    if result == sat:
        print("No internal conflict found.")
        print(s.model())
    elif result == unsat:
        print(s.unsat_core())
        print("There is a conflict among the constraints.")
    else:
        print("Z3 could not determine satisfiability.")

    # ------------------------------------------------------------
# Verification via counterexamples
# ------------------------------------------------------------

# Eq. (1): Consent validity requires capacity, information, and voluntariness

    check_case(
        "Eq. (1a): Counterexample - valid consent without capacity",
        s,
        extra_constraints=[
            ConsentValid(p, t),
            Not(Cap(p))
        ],
        expected="unsat"
    )

    check_case(
        "Eq. (1b): Counterexample - valid consent without information",
        s,
        extra_constraints=[
            ConsentValid(p, t),
            Not(Info(p))
        ],
        expected="unsat"
    )

    check_case(
        "Eq. (1c): Counterexample - valid consent without voluntariness",
        s,
        extra_constraints=[
            ConsentValid(p, t),
            Not(Vol(p))
        ],
        expected="unsat"
    )

    # Eq. (2): Withdrawal invalidates future consent

    check_case(
        "Eq. (2): Counterexample - consent remains valid after withdrawal",
        s,
        extra_constraints=[
            Withdraw(S, p, t),
            t_prime > t,
            ConsentValid(p, t_prime)
        ],
        expected="unsat"
    )

    # Eq. (3): Data must not be collected or used without valid consent

    check_case(
        "Eq. (3a): Counterexample - collect without valid consent",
        s,
        extra_constraints=[
            Collect(S, f, p, t),
            Not(ConsentValid(p, t))
        ],
        expected="unsat"
    )

    check_case(
        "Eq. (3b): Counterexample - use data without valid consent",
        s,
        extra_constraints=[
            UseData(S, p, t),
            Not(ConsentValid(p, t))
        ],
        expected="unsat"
    )
     # Eq. (4): Identifying fields must not be collected unless necessary

    check_case(
        "Eq. (4): Counterexample - collect unnecessary identifying field",
        s,
        extra_constraints=[
            Collect(S, f, p, t),
            IdentifyingField(f),
            Not(Necessary(f, rho))
        ],
        expected="unsat"
    )

    # Eq. (5): Responsible systems must be fair, bias-mitigated, and non-discriminatory

    check_case(
        "Eq. (5a): Counterexample - responsible system is not fair",
        s,
        extra_constraints=[
            Responsible(S),
            Not(Fair(S))
        ],
        expected="unsat"
    )

    check_case(
        "Eq. (5b): Counterexample - responsible system has unmitigated bias",
        s,
        extra_constraints=[
            Responsible(S),
            Not(BiasMitigated(S))
        ],
        expected="unsat"
    )

    check_case(
        "Eq. (5c): Counterexample - responsible system discriminates",
        s,
        extra_constraints=[
            Responsible(S),
            Discriminate(S, p, t)
        ],
        expected="unsat"
    )

    # Eq. (6): Ethical agent cannot supervise a system that violates Constraints(S)
# In your code, C6 directly checks responsibility of supervised systems.

    check_case(
        "Eq. (6): Counterexample - ethical agent supervises irresponsible system",
        s,
        extra_constraints=[
            Ethical(A),
            Supervises(A, S),
            Not(Responsible(S))
        ],
        expected="unsat"
    )

    # Positive test — collecting necessary identifying field with consent
    check_case(
        "Eq. (3)(4): Positive - collect necessary field with consent (permitted)",
        s,
        extra_constraints=[
            Collect(S, f, p, t),
            IdentifyingField(f),
            Necessary(f, rho),
            ConsentValid(p, t),
            Cap(p), Info(p), Vol(p)
        ],
        expected="sat"
    )
    
    



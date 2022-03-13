from Footy.MatchStates import (MatchState, 
                                Drawing, 
                                TeamLeadByOne, 
                                TeamExtendingLead,
                                TeamLosingLead,
                                TeamDeficitOfOne,
                                TeamExtendingDeficit,
                                TeamLosingDeficit)

matchState = MatchState(0, 0)

matchState = matchState.FindState()
print(matchState)
assert(isinstance(matchState, Drawing))

matchState = matchState.GoalScored(1, 0)
print(matchState)
assert(isinstance(matchState, TeamLeadByOne))

matchState = matchState.GoalScored(2, 0)
print(matchState)
assert(isinstance(matchState, TeamExtendingLead))

matchState = matchState.GoalScored(3, 0)
print(matchState)
assert(isinstance(matchState, TeamExtendingLead))

matchState = matchState.GoalScored(3, 1)
print(matchState)
assert(isinstance(matchState, TeamLosingLead))

matchState = matchState.GoalScored(3, 2)
print(matchState)
assert(isinstance(matchState, TeamLosingLead))

matchState = matchState.GoalScored(3, 3)
print(matchState)
assert(isinstance(matchState, Drawing))

matchState = matchState.GoalScored(3, 4)
print(matchState)
assert(isinstance(matchState, TeamDeficitOfOne))

matchState = matchState.GoalScored(3, 5)
print(matchState)
assert(isinstance(matchState, TeamExtendingDeficit))

matchState = matchState.GoalScored(3, 6)
print(matchState)
assert(isinstance(matchState, TeamExtendingDeficit))

matchState = matchState.GoalScored(4, 6)
print(matchState)
assert(isinstance(matchState, TeamLosingDeficit))

matchState = matchState.GoalScored(5, 6)
print(matchState)
assert(isinstance(matchState, TeamLosingDeficit))

matchState = matchState.GoalScored(6, 6)
print(matchState)
assert(isinstance(matchState, Drawing))

matchState = matchState.GoalScored(8, 6)
print(matchState)
assert(isinstance(matchState, TeamExtendingLead))


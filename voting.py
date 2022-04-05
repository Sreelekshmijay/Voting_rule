

from collections import Counter
import copy

#Task 1
#Function Generatepreference

def generatePreferences (values):

    """"
    
    Input:
    A set of numerical values
    that the agents have for different alternatives
    
    Output: 
    A preference profile- a set of  n preference orderings, one for every agent.
    
    """

    agentList = [] #list which contains the agents
    preferenceList = [] #list of lists which contain preference order of each agent
    a = 0

    for row in values.rows:
        preferenceOrdering = [] #list to store preference value on descending order
        preferences = [] #list to store preference value as per given order for each agent
        for cell in row:
            preferences.append(cell.value)
            #Arrange preference value in descending order  
            preferenceOrdering = preferences.copy()      
            preferenceOrdering.sort(reverse = True)
        indexList = [] #list to store index of preference value in given data for each agent.

    #generating a list which contain index value of the preferences by each agent
        for i in preferenceOrdering:   
                count = 0        
                for j in preferences:
                    count = preferences.count(j)
                    #Checking whether any agent assigned same value for different alternatives
                    if count > 1:
                        if i == j:
                            #storing index of preference value if duplicates are present
                            allindexList = [index+1 for index, element in enumerate(preferences) if element ==j]
                            allindexList.sort(reverse = True)
                            x = allindexList[0]
                            preferences[x - 1]  = 0
                            indexList.append(x)     
                    #if no duplicate values are present              
                    else: 
                        if i == j:
                            x = preferences.index(j) +1
                            preferences[preferences.index(j)]  = 0
                            indexList.append(x)                      

        
    #generating a list of list containing preference order of each agents.        
        preferenceList.append(indexList) 
        a+=1
        agentList.append(a)
    #Creating dictionary
    output = dict(zip(agentList, preferenceList))
    return output

#Function for dictatorship Rule
def dictatorship(preferenceProfile, agent):

    """
    Input: 
    Preference profile

    Output: 
    An agent is selected and
    The winner is the alternative that this agent ranks first.

    """

    if agent in preferenceProfile:
        for key in preferenceProfile:            
            if key == agent:
                x = preferenceProfile.get(agent)
                winner = x[0]
        return winner
    else:
        print("The given agent is not present in the preference profile")
            
   
#Function for scoringrule
def scoringRule(preferences, scoreVector, tieBreak):

    """

    Input: 

    A preference profile represented by a dictionary.
    A score vector of length m, i.e., equal to the number of alternatives,
     i.e., a list of length  containing positive floating numbers. 
    An option for the tie-breaking among possible winners.

    Output:

    Alternative with the highest total score,
    using the tie-breaking option to distinguish between 
    alternatives with the same score

    """

    finalScoreDict = {}
    for lst in preferences.values():
        if len(scoreVector) != len(lst):
            print("Incorrect input")
            return False

        else:
            #Arranging score vector in descending order
            scoreVector.sort(reverse = True)    
            for key in preferences:                
                a = preferences[key]    
                #Creating a dictionary with agent as key and corresponding score vector as values            
                scoreDictionary = dict(zip(a, scoreVector))   
                #Incrementing the value of score vector in each loop             
                finalScoreDict = dict(Counter(finalScoreDict) + Counter(scoreDictionary))                          
            max_score =max(finalScoreDict.values())
            alternative = [k for k, v in finalScoreDict.items() if v == max_score]            
            if len(alternative) > 1:
                tieBreakRule(tieBreak,alternative, preferences)
            else:
                winner = alternative[0]
                return winner

#Function Plurality
def plurality(preferences, tieBreak):

    """
    
    Input: 
    A preference profile represented by a dictionary as described above.
    An option for the tie-breaking among possible winners 

    Output: 
    winner is the alternative that appears the most times 
    in the first position of the agents' preference orderings.

    """


    a = list(preferences.values()) #list of list with preference ordering of each agent
    b = [] #List to append with the alternative that appears first
    for ele in a:
        b.append(ele[0])

        #Creating a dictionary to count how many times an alternative appeared first.
        counter_dict = {i:b.count(i) for i in b}    
    #find maximum value        
    max_value =max(counter_dict.values())
    alternative = [k for k, v in counter_dict.items() if v == max_value]
    if len(alternative) > 1:
        return tieBreakRule(tieBreak,alternative, preferences)
    else:
        winner = alternative[0]
        print(winner)
        return winner

def veto (preferences, tieBreak):

    """
    Rule:
    Every agent assigns 0 points to the alternative 
    that they rank in the last place of their preference orderings, 
    and 1 point to every other alternative.

    Input: 
    a preference profile represented by a dictionary..
    An option for the tie-breaking among possible winners

    Output: 
    winner is the alternative with the most number of points.

    """

    final_dict = {}
    for agent in preferences:
        b = preferences[agent]
        c = []   

        #loop for assigning score as per rule     
        for i in b:
            if i == b[-1]:
                c.append(0)
            else:
                c.append(1)
        #creating dictionary 
        new_dict = dict(zip(b,c))        
        for ele in b:
            if ele in final_dict:
                print(final_dict[ele])
                final_dict[ele] += new_dict[ele]
            else:
                final_dict[ele] = new_dict[ele]
    #finding maximum score
    max_score =max(final_dict.values())
    alternative = [k for k, v in final_dict.items() if v == max_score]           
    if len(alternative) > 1:
        tieBreakRule(tieBreak,alternative, preferences)
    else:
        winner = alternative[0]
        return winner




def borda (preferences, tieBreak):

    """
    Rule:

    Every agent assigns a score of 0 to the their least-preferred 
    alternative (the one at the bottom of the preference ranking), 
    a score of 1 to the second least-preferred alternative, ... , 
    and a score of m-1 to their favourite alternative.
    the alternative ranked at position j receives a score of m-j .

    Input: 
    a preference profile represented by a dictionary..
    An option for the tie-breaking among possible winners

    Output: 
    winner is the alternative with the most number of points.

    """

    final_dict = {}
    for agent in preferences:
        b = preferences[agent]
        c = []

        #loop for assigning score as per rule
        for i in b:
            d = len(b) - 1
            e = d - b.index(i)
            c.append(e)
            #Creating dictionary
            zip_iterator = zip(b,c)
            new_dict = dict(zip_iterator)
        for ele in b:
            if ele in final_dict:
                final_dict[ele] += new_dict[ele]
            else:
                final_dict[ele] = new_dict[ele]   

    #finding maximum value  
    max_score =max(final_dict.values())
    alternative = [k for k, v in final_dict.items() if v == max_score]         
    if len(alternative) > 1:
        tieBreakRule(tieBreak,alternative, preferences)
    else:
        winner = alternative[0]
        return winner

def harmonic(preferences, tieBreak):

    """
    Rule:
    
    Every agent assigns a score of (1/m) to the their least-preferred 
    alternative (the one at the bottom of the preference ranking), 
    a score of (1/(m-1)) to the second least-preferred alternative, ... , 
    and a score of 1 to their favourite alternative.
    the alternative ranked at position j receives a score of (1/m-j) .

    Input: 
    a preference profile represented by a dictionary..
    An option for the tie-breaking among possible winners

    Output: 
    winner is the alternative with the most number of points.

    """

    final_dict = {}
    for agent in preferences:
        b = preferences[agent]
        c = []

        #loop for assigning score as per rule
        for i in b:
            d = 1 / (b.index(i) + 1)
            c.append(d)

            #Creating dictionary
            new_dict = dict(zip(b,c))     
        for ele in b:
            if ele in final_dict:
                final_dict[ele] += new_dict[ele]
            else:
                final_dict[ele] = new_dict[ele]

    #finding maximum value  
    max_score =max(final_dict.values())
    alternative = [k for k, v in final_dict.items() if v == max_score]        
    if len(alternative) > 1:
        tieBreakRule(tieBreak,alternative, preferences)
    else:
        winner = alternative[0]
        return winner

def STV(preferences, tieBreak):

    """
    Rule:
    
    The voting rule works in rounds. 
    In each round, the alternatives that appear 
    the least frequently in the first position of 
    agents' rankings are removed, and the process is repeated.

    Input: 
    a preference profile represented by a dictionary..
    An option for the tie-breaking among possible winners

    Output: 
    When the final set of alternatives is removed (one or possibly more), 
    then this last set is the set of possible winners.

    """

    preferencescopy = copy.deepcopy(preferences)
    while len(preferencescopy[1]) != 0:
        print(len(preferencescopy[1]))
        a = (preferencescopy.values())
        b = []
        for item in a:
            b.append(item[0])
        counter_dict = {i:b.count(i) for i in b}

        #Removing alternative which does not appear at first position at all
        if len(counter_dict) != len(item):
            x = []
            for element in item:
                if element not in counter_dict.keys():
                    x.append(element)
                    mini_dict = {i:x.count(i) for i in x}
                    min_count = min(mini_dict.values())
                    alternative = [k for k, v in mini_dict.items() if v == min_count] 

        #Removing alternative that appeared least at the first position
        else:
            min_count = min(counter_dict.values())
            alternative = [k for k, v in counter_dict.items() if v == min_count] 
        for agent in preferencescopy:
            for index in alternative:
                preferencescopy[agent].remove(index)
    if len(alternative) == 1:
        winner = alternative[0]
    else:
        tieBreakRule(tieBreak,alternative, preferences)
    return winner


def rangeVoting(values, tieBreak):

    """

    Input: 
    A worksheet corresponding to an xlsx file, see Task 1 for the details.
    An option for the tie-breaking among possible winners.

    Output: 
    Alternative that has the maximum sum of valuations, 
    i.e., the maximum sum of numerical values in the xlsx file, 
    using the tie-breaking option to distinguish between possible winners.

 

    """

    sum_of_valuations = []
    x = []
    for valuations in values.iter_cols(values.min_column, values.max_column, values.min_row, values.max_row):
        column_Data = []
        #finding sum of values assigned by agents to a particular alternative
        for r in valuations:
            column_Data.append(r.value)        
            sum_of_valuations = sum(column_Data)
        #making a list of sum
        x.append(sum_of_valuations)

    #Finding maximum score    
    max_score = max(x)
    
    alternative = [index +1 for index, element in enumerate(x) if element == max_score ]
    
    if len(alternative) > 1: 
        tieBreakRule(tieBreak, alternative,preferences)
    else:
        winner = alternative[0]
 
    return winner

    

def tieBreakRule(tieBreak,possibleWinners,preferences):

    """

    Input: 

    Option for the tieBreak input of above functions

    ie: max: Among the possible winning alternatives,
             select the one with the highest number.
        min: Among the possible winning alternatives, 
             select the one with the lowest number.
        agent i : Among the possible winning alternatives, 
            select the one that agent i ranks the highest in his/her preference ordering. 

    possibleWinners : list generated at the end of above functions 
    with possible winning alternatives

    preferences: Dictionary

    Output: 

    Winner as per the value of tieBeak
 

    """



    y = []
    if tieBreak == "max":
        winner = max(possibleWinners)
        return winner
    elif tieBreak == "min":
        winner = min(possibleWinners)
        return winner
    else:
        if tieBreak not in preferences.keys():
            print("Input a valid agent")
        else:
                agent_preference = preferences[tieBreak]

                for i in possibleWinners:
                    y.append(agent_preference.index(i))
                    #finding most preferred
                preferred_index = min(y)
                winner = agent_preference[preferred_index]
        return winner



    



    




    
            
            


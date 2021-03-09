# -*- coding: utf-8 -*-
"""StanfordCS221Lecture7.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/161yQiBuLgLlOtKPD7LIJNvex0J4muGus
"""

#Lecture 7
'''
Tram Search Problem framed as a Markov Decision Processes (MDP):
Imagine streets with blocks are numbered from 1 to n. 
Walking from block s to block s+1 takes 1 minute
Taking a magic tram from block s to block 2s takes 2 minutes
Tram fails with probability of 0.5

Question: How to travel from 1 to n in the least time?
Solution for MDP is going to be a policy 
(a policy essentially tells the action to take when in a particular state)
'''

#MODEL
#Formalized as MDP
#Reason why this is a MDP is because tram can fail with probablity of 0.5

class TransportationProblemMDP(object):
  def __init__(self,N):
    self.N=N
  def startState(self):
    return 1
  def isEnd(self,state):
    if state==self.N:
      return True
  def actions(self,state):
    #For the state you are currently in, return possible actions
    result=[]
    if state+1<=self.N:
      result.append(('walk'))
    if state*2<=self.N:
      result.append(('tram'))
    return result
  def succProbReward(self,state,action):
    #Return (newstate,probability of new state occurring,reward)
    result=[]
    if action=='walk':
      result.append((state+1,1,-1))
    elif action=='tram':
      failProb=.5
      result.append((state*2,failProb,-2))
      result.append((state,failProb,-2))
    return result
  def discount(self):
    return 1
  def states(self):
    return range(1,self.N+1)

mdp=TransportationProblemMDP(10)

print(mdp.actions(3))
print(mdp.actions(9))

print(mdp.succProbReward(3,'walk'))
print(mdp.succProbReward(5,'tram'))

import os

#INFERENCE
#Policy Evaluation: Given a policy, evaluate value of policy at every state
#Value Iteration: Get the BEST optimal policy at every state
#Note: Value of policy is the EXPECTED utility from following that policy

def valueIteration(mdp):

  #initialize
  V={}
  for state in mdp.states():
    V[state]=0

  def Q(state,action):
    return sum(transitionProb*(reward+mdp.discount()*V[newState]) for newState,transitionProb,reward in mdp.succProbReward(state,action))
  while True:
    #compute new values (Vnew) given the old values (Vold)
    newV={}
    for state in mdp.states():
      if mdp.isEnd(state):
        newV[state]=0
      else:
        newV[state]=max(Q(state,action) for action in mdp.actions(state))

    #check for convergence
    if max(abs(newV[state]-V[state]) for state in mdp.states())<1e-10:
      break
    V=newV

    #Print out policy during each iteration
    policy={}
    for state in mdp.states():
      if mdp.isEnd(state):
        policy[state]='none'
      else:
        policy[state]=max((Q(state,action),action) for action in mdp.actions(state))[1]

    os.system('clear')
    print('{:15} {:15} {:15}'.format('s','V(s)','pi(s)'))
    for state in mdp.states():
      print('{:15} {:15} {:15}'.format(state,V[state],policy[state]))
    input()

valueIteration(mdp)

#Next steps:
#Play around with failProb variable. Try to change the value, and see how the policy changes as a result. Note, failProb must be between [0,1]
#It turns out, when you set the failProb to 0, you will get the SAME results as you had in the standard search problem (check out Lecture6 found in same Github repo)

#Key Takeaway: 
#Essentially, having a MDP with transition probabilities of 0 (ie no randomness) will convert the problem back into a standard search
#MDPs deal with uncertainties
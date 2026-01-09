from abc import ABC, abstractmethod
from state import State
from action import Action
from typing import List

class Problem(ABC): 
  def __init__(self, initialState: State): 
  	self.initialState = initialState
  @abstractmethod 
  def goalState(self, state: State) -> bool: pass 
  @abstractmethod
  def getStateActions(self, state: State) -> List[Action]: pass
  @abstractmethod
  def childState(self, state: State, action: Action) -> State: pass

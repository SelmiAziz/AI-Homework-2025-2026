from abc import ABC, abstractmethod

class State(ABC): 
  @abstractmethod
  def __lt__(self, other) -> bool: pass
  @abstractmethod
  def print(slef): pass
  

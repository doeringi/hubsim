from abc import ABC, abstractmethod


class AbstractPlanner(ABC):
    # takes in agents summary description and summary of previous day
    # creates a rough plan for the day (5 to 8 chunks) and saves this plan to memory
    # recursively creates finer-grained plans for each chunk e.g. 1 hour chunks
    # recursively creates finer-grained plans for each chunk e.g. 5-15 minute chunks
    # Reacting and Updating Plans: At every time step in the simulation prompt the language model to decide whether to update the plan or not

    @abstractmethod
    def plan(self):
        raise NotImplementedError('Abstract method "plan" must be implemented')

    @abstractmethod
    def react():
        raise NotImplementedError('Abstract method "react" must be implemented')

    @abstractmethod
    def update_plan():
        raise NotImplementedError('Abstract method "update_plan" must be implemented')

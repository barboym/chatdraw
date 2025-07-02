
from chatdraw.tutorial_creator_sketchagent import load_tutorial
from typing import List, Optional


class SketchAgentGuide:
    def __init__(self, concept: str, tutorial_steps: List[str]):
        """
        Initialize the SketchAgentGuide with a drawing context and steps.

        Args:
            context: The subject being drawn (e.g., "giraffe")
            tutorial_steps: List of step-by-step instructions
        """
        assert len(tutorial_steps) > 0
        self.tutorial_steps = tutorial_steps
        self.curr_step = 0
        self.concept = concept
        # Track state for API integration
        self.is_completed = False
        self.current_message = ""

    @classmethod
    def from_path(cls,tutorial_path: str):
        """
        Create a SketchAgentGuide from a tutorial file.

        Args:
            tutorial_path: Path to the tutorial JSON file

        Returns:
            SketchAgentGuide: Initialized guide ready to use in API
        """
        concept, tutorial = load_tutorial(tutorial_path)
        return cls(concept, tutorial)


    def start(self) -> str:
        """
        Start the tutorial and return the welcome message.

        Returns:
            str: The initial welcome message
        """
        welcome_message = f"Hello. I'll teach you to paint {self.concept} in {len(self.tutorial_steps)} strokes"
        self.current_message = welcome_message
        return welcome_message

    def get_current_step(self) -> Optional[str]:
        """
        Get the current tutorial step without advancing.

        Returns:
            str: Current step instructions or None if tutorial is completed
        """
        if self.curr_step >= len(self.tutorial_steps): 
            return None
        return self.tutorial_steps[self.curr_step]

    def next_step(self, retry: bool = False) -> str:
        """
        Advance to the next step or retry current step based on user choice.
        Designed to be called from API endpoints.

        Args:
            retry: Whether to retry the current step
        Returns:
            str: The next instruction or completion message
        """
        if self.is_completed:
            return self.current_message

        if not retry and self.curr_step < len(self.tutorial_steps):
            self.curr_step += 1

        if self.curr_step >= len(self.tutorial_steps):
            self.is_completed = True
            completion_message = f"That's it. You finished the tutorial. You now know how to draw a {self.concept}"
            self.current_message = completion_message
            return completion_message

        current_step = self.tutorial_steps[self.curr_step]
        self.current_message = current_step
        return current_step

    def get_progress(self) -> dict:
        """
        Get the current progress of the tutorial.

        Returns:
            dict: Progress information for API responses
        """
        return {
            "current_step": self.curr_step + 1,
            "total_steps": len(self.tutorial_steps),
            "is_completed": self.is_completed,
            "context": self.context,
            "current_message": self.current_message
        }

    def reset(self) -> str:
        """
        Reset the tutorial to the beginning.

        Returns:
            str: Reset confirmation message
        """
        self.curr_step = 0
        self.is_completed = False
        return self.start()


    

if __name__ == "__main__":
    # Interactive console mode
    concept, tutorial = load_tutorial("/home/mos/exercises/SketchAgent/results/test/giraffe/experiment_log.json")
    guide = SketchAgentGuide(concept, tutorial)

    print(guide.start())

    while not guide.is_completed:
        print(guide.get_current_step())
        print("Do you want to try this step again? (y/n)")
        retry = input().lower() in ['y', 'yes']
        guide.next_step(retry=retry)

    print(guide.current_message)

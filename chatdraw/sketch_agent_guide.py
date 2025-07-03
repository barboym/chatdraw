
from chatdraw.tutorial_creator_sketchagent import load_tutorial


def response(response_type: str, response_data: str, concept: str, current_step: int) -> str:
    """
    Process user response (image or text) and provide feedback.

    Args:
        response_type: "image" or "text"
        response_data: Image data or text input from user
        concept: The relevant concept
        current_step: Override the current step if needed

    Returns:
        str: Feedback message based on response
    """
    tutorial = load_tutorial(concept)
    
    curr_step = tutorial[current_step]
    next_step = tutorial[current_step+1]

    if response_type == "image":
        # Process image response
        # For simplicity, we'll just acknowledge receipt of the image
        return f"I see your drawing for step {curr_step + 1}. Let's continue."

    elif response_type == "text":
        # Process text response
        if response_data.lower() in ["next", "continue"]:
            return next_step
        if response_data.lower() in ["retry", "repeat"]:
            return curr_step
        else:
            # Default behavior for unrecognized text
            return "I'm not sure what you mean. Type 'next' to continue or 'retry' to repeat this step."


if __name__ == "__main__":
    # Interactive console mode
    concept, tutorial = load_tutorial("/home/mos/exercises/SketchAgent/results/test/giraffe/experiment_log.json")

    print(guide.start())

    while not guide.is_completed:
        print(guide.get_current_step())
        print("Do you want to try this step again? (y/n)")
        retry = input().lower() in ['y', 'yes']
        guide.next_step(retry=retry)

    print(guide.current_message)

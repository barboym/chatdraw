
from chatdraw.tutorial_creator_sketchagent import load_tutorial


# def response(response_type: str, response_data: str, concept: str, current_step: int) -> str:
#     """
#     Process user response (image or text) and provide feedback.

#     Args:
#         response_type: "image" or "text"
#         response_data: Image data or text input from user
#         concept: The relevant concept
#         current_step: Override the current step if needed

#     Returns:
#         str: Feedback message based on response
#     """
#     tutorial = load_tutorial(concept)

#     if response_type == "image":
#         # Process image response
#         # For simplicity, we'll just acknowledge receipt of the image
#         return f"I see your drawing for step {current_step + 1}. Let's continue."

#     elif response_type == "text":
#         # Process text response
#         if response_data.lower() in ["next", "continue"]:
#             return "next_step"
#         if response_data.lower() in ["retry", "repeat"]:
#             return "curr_step"
#         else:
#             # Default behavior for unrecognized text
#             return "I'm not sure what you mean. Type 'next' to continue or 'retry' to repeat this step."
#     else:
#         return "wrong message type"


def tutorial_response(response_data: list[tuple[int,int]], step: int,  tutorial: str|list) -> tuple[str,int]:
    """
    Process user response (image or text) and provide feedback.

    Args:
        response_data: Image data in the form of 
        tutorial: The relevant concept or the preloaded tutorial
        step: Override the current step if needed

    Returns:
        str: Feedback message based on response
    """
    if isinstance(tutorial,str):
        tutorial = load_tutorial(tutorial)
    if step>=len(tutorial):
        return (
            "You succesfully completed the tutorial.\n", 
            step+1
        )
    # TODO: calculate distance measures. 
    # if step>0: 
    #     pass
    #     strokes = pixels_to_strokes(tutorial)
    #     draw_stroke = strokes[step]

    draw_step = tutorial[step]
    return (
        f"""Draw the {draw_step['name']} next.\n""",
        step+1
    )

if __name__ == "__main__":
    print(
        tutorial_response(response_data=[], step=1, tutorial="monkey")
    )

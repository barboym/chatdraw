
from chatdraw.tutorial_creator_sketchagent import load_tutorial
from chatdraw.utils import pixels_to_strokes
import numpy as np
from scipy.interpolate import interp1d

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


def tutorial_response(response_data: list[(int,int)], step: int,  tutorial: str|list) -> (str,int):
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
    draw_step = tutorial[step]
    # TODO: calculate distance measures. 
    return (
        f"""Draw the {draw_step['name']} next.\n""",
        step+1
    )

def make_smooth_stroke(draw_stroke):
    draw_stroke = np.array(draw_stroke)
    n=len(draw_stroke)
    interp_method=None
    if n in [1,2]:
        return draw_stroke
    elif n==3:
        interp_method='quadratic'
    else:
        interp_method='cubic'
    return np.c_[
        interp1d(np.linspace(0,1,len(draw_stroke)),draw_stroke[:,0],kind=interp_method)(np.linspace(0,1,100)), 
        interp1d(np.linspace(0,1,len(draw_stroke)),draw_stroke[:,1],kind=interp_method)(np.linspace(0,1,100))
    ]

if __name__ == "__main__":
    print(
        tutorial_response(response_data=[], step=1, tutorial="monkey")
    )

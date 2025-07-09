
from chatdraw.tutorial_creator_sketchagent import load_tutorial
import numpy as np
from scipy.interpolate import interp1d


# def tutorial_response(response_data: list[(int,int)], step: int,  tutorial: str|list) -> (str,int):
#     """
#     Process user response (image or text) and provide feedback.

#     Args:
#         response_data: Image data in the form of 
#         tutorial: The relevant concept or the preloaded tutorial
#         step: Override the current step if needed

#     Returns:
#         str: Feedback message based on response
#     """
#     if isinstance(tutorial,str):
#         tutorial = load_tutorial(tutorial)
#     if step>=len(tutorial):
#         return (
#             "You succesfully completed the tutorial.\n", 
#             step+1
#         )
#     draw_step = tutorial[step]
#     # TODO: calculate distance measures. 
#     return (
#         f"""Draw the {draw_step['name']} next.\n""",
#         step+1
#     )

    

# def response(state: str, message: str) -> tuple[str, str]:
#     state_data = dialogue(state)

#     next_state = state_data["transitions"].get(message.lower())

#     if next_state:
#         return next_state, dialogue[next_state]["message"]
#     else:
#         return state, "Invalid input. " + state_data["message"]



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
    pass
    # print(
    #     tutorial_response(response_data=[], step=1, tutorial="monkey")
    # )

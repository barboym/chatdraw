from typing import List, Tuple
from chatdraw.sketches.svg_utils import render_tutorial_to_pil
from transformers import AutoImageProcessor, AutoModel
import torch

processor = AutoImageProcessor.from_pretrained('facebook/dinov2-small')
model = AutoModel.from_pretrained('facebook/dinov2-small')

def get_dino_v2_score(user_points: List[List[Tuple[int, int]]], system_points: List[List[Tuple[int, int]]]) -> float:
    image1 = render_tutorial_to_pil(user_points)
    image2 = render_tutorial_to_pil(system_points)
    with torch.no_grad():
        inputs = processor(images=[image1,image2], return_tensors="pt")
        outputs = model(**inputs)
        last_hidden_states = outputs.last_hidden_state
    score = torch.nn.CosineSimilarity(dim=-1)(last_hidden_states[0].mean(dim=1),last_hidden_states[1].mean(dim=1))
    return score

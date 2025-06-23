
from ready_tutorials.tutorial_creator_sketchagent import load_tutorial


class SketchAgentGuide:
    def __init__(self, context:str, tutorial_steps:list):
        assert len(tutorial_steps) > 0
        self.tutorial_steps = tutorial_steps
        self.curr_step = 0
        self.context = context

    def start(self):
        print(f"""Hello. Ill teach you to paint {self.context} in {len(self.tutorial_steps)} strokes""")
        self.next_step()
    
    def next_step(self):
        tutorial_step = self.tutorial_steps[self.curr_step]
        print(tutorial_step)
        print("Do you want to try this step again?(y/n)")
        if input() not in ['y','Y']:
            self.curr_step+=1
        if self.curr_step >= len(self.tutorial_steps): 
            self.end()
            return
        self.next_step()

    def end(self):
        print(f"Thats it. You finished the tutorial. You now know how to draw a {self.context}")


if __name__=="__main__":
    concept, tutorial = load_tutorial("/home/mos/exercises/SketchAgent/results/test/giraffe/experiment_log.json")
    SketchAgentGuide(concept,tutorial).start()




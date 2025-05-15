#!/usr/bin/env python3

class SketchTutorialBot:
    def __init__(self):
        self.tutorials = {
            "apple": [
                {
                    "step": 1,
                    "title": "Basic Shape",
                    "instruction": "Start by drawing a circle that's not perfectly round - apples are typically slightly taller than they are wide. Draw lightly so you can refine the shape later.",
                    "tip": "Hold your pencil loosely and use your whole arm, not just your wrist, to create smooth curves."
                },
                {
                    "step": 2,
                    "title": "Add the Stem and Leaf",
                    "instruction": "At the top of your apple, draw a small stem. It can be straight or slightly curved. Next to it, add a small leaf using simple curved lines.",
                    "tip": "The stem doesn't need to be centered - apples in nature have stems that are often off to one side."
                },
                {
                    "step": 3, 
                    "title": "Add the Dip and Bottom",
                    "instruction": "Add a small dip at the top where the stem connects. Then, add a subtle dip at the bottom of the apple.",
                    "tip": "Look at real apples for reference - they have characteristic indentations at both the top and bottom."
                },
                {
                    "step": 4,
                    "title": "Add Dimension",
                    "instruction": "Darken the outline of your apple. Then add a curved line to represent the side of the apple, giving it a 3D appearance.",
                    "tip": "Imagine a light source coming from one direction and think about which parts of the apple would catch the light."
                },
                {
                    "step": 5,
                    "title": "Add Basic Shading",
                    "instruction": "Add some light shading to give your apple volume. Shade one side darker than the other to create a sense of depth.",
                    "tip": "Use the side of your pencil and build up the shading gradually with light pressure."
                },
                {
                    "step": 6,
                    "title": "Add Final Details",
                    "instruction": "Add some light texture or spots to make your apple look more realistic. You can also darken some areas for contrast.",
                    "tip": "Real apples often have small spots or variations in color - adding these subtle details makes your drawing more lifelike."
                }
            ]
            # More tutorials can be added here in the future
        }
        self.current_tutorial = None
        self.current_step = 0
        
    def start(self):
        """Start the chatbot interface"""
        print("=" * 60)
        print("Welcome to the Sketch Tutorial Bot!")
        print("I'll guide you through sketching various objects step by step.")
        print("=" * 60)
        
        self.main_menu()
    
    def main_menu(self):
        """Display the main menu"""
        while True:
            print("\nWhat would you like to sketch today?")
            print("1. Apple")
            print("2. Exit")
            
            choice = input("\nEnter your choice (1-2): ")
            
            if choice == "1":
                self.start_tutorial("apple")
            elif choice == "2":
                print("Thank you for using Sketch Tutorial Bot. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def start_tutorial(self, tutorial_name):
        """Start a specific tutorial"""
        if tutorial_name in self.tutorials:
            self.current_tutorial = tutorial_name
            self.current_step = 0
            print(f"\nGreat! Let's learn how to sketch an {tutorial_name}.")
            print("I'll guide you through each step. Take your time and enjoy the process!")
            print("Press Enter when you're ready to start.")
            input()
            self.next_step()
        else:
            print(f"Sorry, I don't have a tutorial for {tutorial_name} yet.")
    
    def next_step(self):
        """Show the next step in the current tutorial"""
        if not self.current_tutorial:
            print("No tutorial selected. Please choose a tutorial first.")
            return
        
        tutorial = self.tutorials[self.current_tutorial]
        
        if self.current_step < len(tutorial):
            step = tutorial[self.current_step]
            
            print("\n" + "=" * 60)
            print(f"STEP {step['step']}: {step['title']}")
            print("=" * 60)
            print(step['instruction'])
            print("\nTIP: " + step['tip'])
            
            if self.current_step < len(tutorial) - 1:
                input("\nPress Enter when you're ready for the next step...")
                self.current_step += 1
                self.next_step()
            else:
                print("\nCongratulations! You've completed all steps for sketching an apple.")
                print("Would you like to see all the steps again or return to the main menu?")
                print("1. See all steps again")
                print("2. Return to main menu")
                
                choice = input("\nEnter your choice (1-2): ")
                if choice == "1":
                    self.current_step = 0
                    self.next_step()
                else:
                    self.main_menu()
    
    def run(self):
        """Run the chatbot"""
        try:
            self.start()
        except KeyboardInterrupt:
            print("\n\nThanks for using Sketch Tutorial Bot. Goodbye!")


if __name__ == "__main__":
    bot = SketchTutorialBot()
    bot.run()
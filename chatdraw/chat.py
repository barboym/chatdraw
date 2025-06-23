#!/usr/bin/env python3

class SketchTutorialBot:
    def __init__(self):
        self.tutorials = {
            "apple": 
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
            print(f"\nGreat! Let's learn how to sketch: {tutorial_name}.")
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
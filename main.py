from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import warnings
import logging

# Suppress warnings
warnings.filterwarnings('ignore')
logging.getLogger('absl').setLevel(logging.ERROR)

# Load environment variables
load_dotenv()

class FinancialAdvisor:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            convert_system_message_to_human=True
        )

    def analyze_budget(self, income, fixed_expenses, discretionary_expenses):
        total_fixed = sum(fixed_expenses.values())
        total_discretionary = sum(discretionary_expenses.values())
        
        # Calculate ideal allocations (50/30/20 rule)
        ideal_needs = income * 0.5
        ideal_wants = income * 0.3
        ideal_savings = income * 0.2
        
        current_savings = income - total_fixed - total_discretionary
        savings_percentage = (current_savings / income) * 100
        
        prompt = f"""
        As a financial advisor, please provide a detailed budget analysis using this information:

        CURRENT SITUATION:
        Monthly Income: ${income:,.2f}
        
        Fixed Expenses (Total: ${total_fixed:,.2f}):
        {self._format_expenses(fixed_expenses)}
        
        Discretionary Expenses (Total: ${total_discretionary:,.2f}):
        {self._format_expenses(discretionary_expenses)}
        
        Current Allocations:
        - Fixed Expenses: {(total_fixed/income)*100:.1f}% of income
        - Discretionary: {(total_discretionary/income)*100:.1f}% of income
        - Available for Savings: {savings_percentage:.1f}% of income (${current_savings:,.2f})
        
        IDEAL ALLOCATIONS (50/30/20 Rule):
        - Needs (50%): ${ideal_needs:,.2f}
        - Wants (30%): ${ideal_wants:,.2f}
        - Savings (20%): ${ideal_savings:,.2f}

        Please provide:
        1. A clear analysis of the current budget structure
        2. Specific areas where spending differs from the 50/30/20 rule
        3. Three actionable recommendations to optimize the budget
        4. Potential savings opportunities with estimated monthly savings
        
        Format the response with clear headers and bullet points for readability.
        """
        
        try:
            response = self.llm.invoke(prompt).content
            return self._format_output(response)
        except Exception as e:
            return f"Error generating analysis: {str(e)}"

    def _format_expenses(self, expenses):
        return "\n".join([f"- {name}: ${amount:,.2f}" for name, amount in expenses.items()])

    def _format_output(self, text):
        # Add some visual formatting to the output
        sections = text.split('\n')
        formatted_sections = []
        
        for section in sections:
            if section.strip():
                if section.startswith('**'):
                    formatted_sections.append(f"\n{section}")
                elif section.startswith('-'):
                    formatted_sections.append(f"  {section}")
                else:
                    formatted_sections.append(section)
        
        return "\n".join(formatted_sections)

def main():
    # Clear the terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("💰 Finance Chatbot: Budget Planner 💰")
    print("=" * 50)
    print("Let's analyze your financial situation!")
    
    try:
        # Get monthly income
        while True:
            try:
                income = float(input("\n📈 What is your monthly income? $").strip())
                if income > 0:
                    break
                print("Income must be greater than 0.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Get fixed expenses
        fixed_expenses = {}
        print("\n🏠 Enter your fixed expenses (rent, utilities, etc.)")
        print("Type 'done' when finished")
        
        while True:
            expense = input("\nExpense name (or 'done'): ").strip()
            if expense.lower() == 'done':
                break
            try:
                amount = float(input("Amount: $").strip())
                if amount > 0:
                    fixed_expenses[expense] = amount
                else:
                    print("Amount must be greater than 0.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Get discretionary expenses
        discretionary_expenses = {}
        print("\n🎮 Enter your discretionary expenses (entertainment, hobbies, etc.)")
        print("Type 'done' when finished")
        
        while True:
            expense = input("\nExpense name (or 'done'): ").strip()
            if expense.lower() == 'done':
                break
            try:
                amount = float(input("Amount: $").strip())
                if amount > 0:
                    discretionary_expenses[expense] = amount
                else:
                    print("Amount must be greater than 0.")
            except ValueError:
                print("Please enter a valid number.")

        print("\n🔄 Analyzing your financial information...")
        advisor = FinancialAdvisor()
        analysis = advisor.analyze_budget(income, fixed_expenses, discretionary_expenses)
        
        print("\n📊 Your Personalized Budget Analysis:")
        print("=" * 50)
        print(analysis)
        print("=" * 50)
        print("\n💡 Thank you for using the Finance Chatbot!")

    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        print("Please try again or contact support if the problem persists.")

if __name__ == "__main__":
    main()
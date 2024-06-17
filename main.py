import os
import pandas as pd
import warnings
from dotenv import load_dotenv, find_dotenv
from financial_statement_downloader import download_financial_statement
from langchain.agents import AgentType
from langchain.agents.agent_types import AgentType
from langchain_community.chat_models import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI, OpenAI
from langchain.schema import SystemMessage
from nemoguardrails import RailsConfig, LLMRails
from verifier import NIM_verifier

# Removes future deprecation warnings
warnings.filterwarnings("ignore")
_ = load_dotenv(find_dotenv())

# Load environment variables
api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
nvapi_key = os.getenv('NVIDIA_API_KEY')

# Initialize AI API
llm = ChatOpenAI(temperature=0)

# Invokes the power of llms to sort the initial query into one of the 3 financial statements based on context for future correct API calls, even if none are explicitly mentioned
def determine_statement_type(query):
    prompt = f"Given the financial query '{query}', determine which financial statement is needed: income statement, balance sheet, or cash flow statement. Respond with only one of these options."
    messages = [SystemMessage(content=prompt)]
    response = llm(messages)
    statement = response.content.lower().strip()

    # Indicates which statement the answer is in, then notifies the process is continuing to the API call to acquire it 
    print(f"This information can best be found in the: {statement}, I will get that financial document now.")
    if "income statement" in statement:
        return "INCOME_STATEMENT"
    elif "balance sheet" in statement:
        return "BALANCE_SHEET"
    elif "cash flow" in statement:
        return "CASH_FLOW"
    else:
        return None


# Define the main function to run the agent
def run_agent(query, ticker):
    # Determine the statement type
    statement_type = determine_statement_type(query)
    if not statement_type:
        return "Unable to determine the financial statement type from the query."

    # Download the financial statement
    csv_filepath = download_financial_statement(ticker, statement_type, api_key)

    #Load the downloaded CSV into a DataFrame
    df = pd.read_csv(csv_filepath)

    # Create the agent with the downloaded CSV file
    agent = create_csv_agent(
        llm=OpenAI(temperature=0), # Reduces randomness of the llm responses by bringing this to 0
        path=csv_filepath,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
    )


    # Run the agent with the query
    result = agent.run(query)
    return result
    

# Change the ticker to any publically traded company stock ticker for your AI Agent fundamental analysis
ticker = "NVDA"
# This system supports queries on any of the three primary financial statements from a 10-K, spanning back up to 15 years, provided they are fundamentally based.
# Refrain from posing questions related to chart movements or price fluctuations, as these are not covered by the financial statements.
# For complex inquiries requiring data from multiple financial statements, approach sequentially: address each statement individually and integrate the resultant data into a comprehensive final analysis.
# Leveraging advanced LLMs, the LangChain AI Agent possesses a robust understanding of financial terminology and mathematical principles, enabling it to execute precise calculations with needing it in the query!
query = "Has the gross margin been increasing or decreasing over the last 5 years? What does this say about management and the competition?"
response = (run_agent(query, ticker))

# Output is generated progressively as follows:
# 1. Identifies the type of financial statement required.
# 2. Retrieves the statement via API call, ensuring successful integration into a DataFrame for subsequent operations.
# 3. Analyzes the necessary computational logic to be applied on the DataFrame contents to address the query.
# 4. Demonstrates the processing steps: highlights relevant columns and data points, extracts numerical values, and executes calculations utilizing python_repl_ast.
# 5. Upon completing the calculations, leverages LLM logic to verify accuracy, culminating in a structured response labeled as "Final Answer:".
print(response)

# The NVIDIA NIM, utilizing the model="meta/llama3-70b-instruct", meticulously evaluates whether the "Final Answer" appropriately addresses the query and, if valid, confirms its accuracy.
# Should the NVIDIA NIM verification fail, it proposes an alternative phrasing of the query, optimized for interpretation by LangChain's CSV AI Agent that specializes in DataFrame calculations.
# # This mechanism permits the inquirer to re-submit the query for another shot at analysis if desired.
verification_result = NIM_verifier(query, response)
print("NIM Verification Result:", verification_result)


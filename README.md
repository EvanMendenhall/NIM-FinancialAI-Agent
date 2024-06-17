NVIDIA NIM LangChain Financial AI Agent

Overview

The purpose is for fundamental value analyses of publicly traded companies in the United States.

For the non-speculator investor who seeks to understands companies rather than charts, and discover the value in the operations of a business I created this AI Agent to go deeper than surface level readily-available quantitative data. While this is not going to
replace DCF modeling, it will give specific answers like effective tax rate, changes in debt-to-equity or debt-to-asset values over whatever period of time you want to look at. You can ask it the change in gross margin over a time period, and what that indicates about
that company's management team's ability and their competition. It can suggest if a company's dividend seems sustainable based on free cash flows, and almost any variety of interesting questions as long as they pertain to a single financial statement and
don't bounce between them in the same question. Maybe 2.0 can solve that.

API KEY Requirements

You'll need three API_KEYs to make this work:
1. It will require an NVIDIA key to access their NIM llama3-70b-instruct model. https://build.nvidia.com/explore/retrieval
2. OpenAI to run the main LangChain AI Agent sequences, this consumes considerable token usage. Somewhere between 8-10,000 tokens per query due to the Agents continued adjustments and logic checks on financial formulas, then mathematical operations, and code to carry them out. https://openai.com/api/pricing/ (Don't run GPT4 unless you want to spend $0.10 a question)
3. Alpha Vantage offers a free API to get the isolated financial statements for personal use from the SEC, which this code relies on. You can get yours here https://www.alphavantage.co/support/#api-key

Setup your keys in a .env file and import them using dotenv as the requirements.txt shows


Features

Harnessing the reasoning ability of LLMs, the user's query is funneled through a surface level prompt, designed to firstly identify the information sought and immediately secondary, to classify which of the three financial statements the answer could potentially be found in.
Once this is known, an API call specific to that financial statement, either Income Statement, Balance Sheet, or Cash Flow Statement is downloaded in a CSV format temporarily. This is more machine readable than human readable, and no effort was made to adjust that in this code.
The data is then moved from CSV to a Pandas dataFrame using the LangChain CSV agent specifically, with several customizations. The financial formulas are identified from the original query, then it goes to work extracting the numbers in order to perform mathematical operations.
Python_repl_ast is used, so I recommend keeping the model as OpenAI and not ChatOpenAI, as the Chat version, while more conversational, often mistypes its own internal prompts and the repl functions are seen as dialog rather than functions to be carried out. With the model
temperatures at a low of 0, there is often high reliability in it's understanding and operations to correctly solve multi-step questions. Upon given the output, it is run through a final separate NVIDIA NIM Verifier, which either likes the output or suggests a better query.

Contribution Guidelines

This project could best benefit from:
1. Embedding common financial formulas which could be referenced during the AI Agent's chain for accuracy and to reduce token consumption.
2. Or perhaps designing a search API in the LangChain Chain that would go seek out the formula based on the context from https://www.investopedia.com/
3. Through expanding the project considerably, multiple financial statements could be queried for very advanced and complex evaluations, then saved in a vector storage for later recall giving the Agent even higher ability such as accuracy in determining changes in FCF Yield through first determining Enterprise Value etc etc.
4. Addition of saving the outputs to files (though I had this originally I did not want to clutter up folders for the user and found it quite helpful on one question at a time)
5. Creating a looping operation that might find something like increasing operating margins for each company in a list of 50 companies within an industry to compare their relative efficiency by their managements to reduce costs.
6. Whatever else you think may be interesting! It's been a very helpful tool for me and I hope for you too.

Tests

Because much of it is powered by the intelligence of a non-deterministic agent, not every answer is correct. The NIM verification step should help get to a query that is appropriately answered, but when in doubt, these are financial research and math questions, and can be checked by hand to ensure the code is functioning as it should.

MIT License
Copyright (c) 2024 Evan Mendenhall

Permissions: 
Commercial use
Modification
Distribution
Private use

Acknowledgements

Andrew Ng and Harrison Chase's LangChain courses on https://www.deeplearning.ai
Isa Fulford for her course on LLM Prompt Engineering
Eddie Shu for selecting me as an alpha tester of Andrew Ng's new courses in 2023
Gabe Abinante for exceptional dedication to tutoring me in Python and Linux over several sessions
Elan Bechor for informing me of the developments of AI all the way back in 2016 and 2017
Mentors like Andy Pilara who taught me value investing for the long term is a worthwhile study

The AI Mindscape Academy, a closed membership club of AI enthusiasts I heard constant news and developments from since Feb 2023
Members: Gabe Abinante, Elan Bechor, Jacob Farneth, Zach Scott, David Wilson, and Evan Mendenhall.

Aidan Allchin, who mirrored my interest in AI, and along with his father, had endless profound insights into the discipline. 

ArcherTech LLC, DBA Archer Technologies of South Dakota
All NVIDIA staff for producing incredible hardware which powers this, and the innovation that brought NIMs to the big GTC Jensen reveal!

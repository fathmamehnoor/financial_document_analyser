## Importing libraries and files
from crewai import Task
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from crewai_tools import SerperDevTool
from tools import read_financial_document, analyze_investment, assess_risk

# Create search tool instance
search_tool = SerperDevTool()

## Creating a task to analyze financial documents
analyze_financial_document = Task(
    description="""
    Analyze the financial document provided at the file path and respond to the user's query: {query}
    
    Your analysis should include:
    1. Extract and summarize key financial metrics from the document
    2. Identify important trends and patterns in the financial data
    3. Assess the financial health and performance of the entity
    4. Provide relevant market context using current information
    5. Address the specific query asked by the user
    
    Use the financial document reading tool to extract data from: {file_path}
    Search for current market information if relevant to provide context.
    """,

    expected_output="""
    A comprehensive financial analysis report containing:
    - Executive Summary of key findings
    - Detailed analysis of financial metrics and ratios
    - Identification of strengths, weaknesses, and opportunities
    - Market context and industry comparison
    - Direct response to the user's specific query
    - Professional recommendations based on the analysis
    
    All recommendations should be backed by data from the document and include appropriate disclaimers.
    """,

    agent=financial_analyst,
    tools=[read_financial_document, search_tool],
    async_execution=False,
)

## Creating an investment analysis task
investment_analysis = Task(
    description="""
    Based on the financial document analysis, provide investment recommendations for: {query}
    
    Your analysis should:
    1. Review the financial health and performance metrics
    2. Assess investment potential and risks
    3. Compare with industry benchmarks and market conditions
    4. Provide specific, actionable investment recommendations
    5. Include appropriate risk warnings and disclaimers
    """,

    expected_output="""
    A structured investment recommendation report including:
    - Investment thesis based on financial analysis
    - Specific investment recommendations with rationale
    - Risk assessment for each recommendation
    - Portfolio allocation suggestions if applicable
    - Timeline and monitoring recommendations
    - Important disclaimers and risk warnings
    """,

    agent=investment_advisor,
    tools=[analyze_investment, search_tool],
    async_execution=False,
)

## Creating a risk assessment task
risk_assessment = Task(
    description="""
    Conduct a comprehensive risk assessment based on the financial document and user query: {query}
    
    Your assessment should:
    1. Identify key financial and operational risks
    2. Quantify risks where possible using financial ratios
    3. Assess market and industry-specific risks
    4. Provide risk mitigation strategies
    5. Create a risk matrix or scoring system
    """,

    expected_output="""
    A detailed risk assessment report containing:
    - Risk identification and categorization
    - Risk quantification and scoring
    - Impact and probability analysis
    - Risk mitigation strategies and recommendations
    - Monitoring and review procedures
    - Risk tolerance recommendations
    """,

    agent=risk_assessor,
    tools=[assess_risk, search_tool],
    async_execution=False,
)

## Creating a document verification task
verification = Task(
    description="""
    Verify the financial document provided and ensure it contains valid financial information.
    
    Your verification should:
    1. Confirm the document is readable and contains financial data
    2. Validate key financial statements are present
    3. Check for data consistency and completeness
    4. Identify any potential issues or missing information
    """,

    expected_output="""
    A verification report stating:
    - Document type and format confirmation
    - Summary of financial information found
    - Data quality and completeness assessment
    - Any issues or concerns identified
    - Recommendations for additional information if needed
    """,

    agent=verifier,
    tools=[read_financial_document],
    async_execution=False
)
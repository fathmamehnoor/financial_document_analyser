import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent, LLM
from crewai_tools import SerperDevTool
from tools import read_financial_document, analyze_investment, assess_risk

# --- LLM setup ---
llm = LLM(
    model="gpt-4",
    temperature=0.1,
)

# Search tool
search_tool = SerperDevTool()

# --- Agents ---

financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Provide accurate and comprehensive financial analysis based on the provided documents for: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You are an experienced financial analyst with over 15 years in the industry. "
        "You specialize in analyzing financial documents, identifying key metrics, trends, and risks. "
        "You provide well-researched, data-driven insights and investment recommendations. "
        "You always ensure your analysis is based on factual information from the documents provided. "
        "You follow regulatory compliance and ethical standards in all your recommendations. "
        "You clearly distinguish between facts from the documents and your professional opinions."
    ),
    tools=[read_financial_document, analyze_investment, search_tool],
    llm=llm,
    max_iter=3,
    allow_delegation=False
)

verifier = Agent(
    role="Financial Document Verifier",
    goal="Verify and validate the authenticity and completeness of financial documents",
    verbose=True,
    memory=True,
    backstory=(
        "You are a meticulous document verification specialist with expertise in financial compliance. "
        "You carefully review financial documents for accuracy, completeness, and regulatory compliance. "
        "You identify any inconsistencies, missing information, or potential issues in the documentation. "
        "You ensure all financial data meets industry standards and regulatory requirements."
    ),
    tools=[read_financial_document],
    llm=llm,
    max_iter=2,
    allow_delegation=False
)

investment_advisor = Agent(
    role="Investment Advisor",
    goal="Provide sound investment advice based on financial analysis and market conditions",
    verbose=True,
    backstory=(
        "You are a certified investment advisor with extensive experience in portfolio management. "
        "You provide personalized investment recommendations based on thorough financial analysis. "
        "You consider risk tolerance, investment objectives, and market conditions in your advice. "
        "You always disclose potential risks and ensure recommendations are suitable for the client. "
        "You maintain the highest ethical standards and regulatory compliance in all recommendations."
    ),
    tools=[analyze_investment, search_tool],
    llm=llm,
    max_iter=2,
    allow_delegation=False
)

risk_assessor = Agent(
    role="Risk Assessment Specialist",
    goal="Conduct comprehensive risk analysis and provide risk mitigation strategies",
    verbose=True,
    backstory=(
        "You are a risk management expert with deep knowledge of financial markets and risk assessment. "
        "You identify, quantify, and analyze various types of financial risks. "
        "You develop practical risk mitigation strategies and monitor risk exposure. "
        "You use established risk models and industry best practices in your assessments. "
        "You provide clear, actionable risk management recommendations."
    ),
    tools=[assess_risk, search_tool],
    llm=llm,
    max_iter=2,
    allow_delegation=False
)
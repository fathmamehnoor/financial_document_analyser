import os
from dotenv import load_dotenv
load_dotenv()

from crewai.tools import tool
from langchain_community.document_loaders import PyPDFLoader
from pypdf import PdfReader

@tool
def read_financial_document(path: str = 'data/sample.pdf') -> str:
    """Tool to read data from a pdf file from a path
    
    Args:
        path (str, optional): Path of the pdf file. Defaults to 'data/sample.pdf'.
        
    Returns:
        str: Full Financial Document content
    """
    
    try:
        # Check if file exists
        if not os.path.exists(path):
            return f"Error: File not found at path: {path}"
        
        # Try using PyPDFLoader first
        try:
            loader = PyPDFLoader(path)
            documents = loader.load()
            
            full_report = ""
            for doc in documents:
                content = doc.page_content
                
                # Clean and format the document content
                while "\n\n" in content:
                    content = content.replace("\n\n", "\n")
                
                full_report += content + "\n"
            
            return full_report.strip()
            
        except Exception as e1:
            # Fallback to PyPDF2 if PyPDFLoader fails
            try:
                full_report = ""
                with open(path, 'rb') as file:
                    pdf_reader = PdfReader(file)
                    
                    for page_num in range(len(pdf_reader.pages)):
                        page = pdf_reader.pages[page_num]
                        content = page.extract_text()
                        
                        # Clean and format the content
                        while "\n\n" in content:
                            content = content.replace("\n\n", "\n")
                        
                        full_report += content + "\n"
                
                return full_report.strip()
                
            except Exception as e2:
                return f"Error reading PDF file: {str(e2)}"
                
    except Exception as e:
        return f"Error processing file: {str(e)}"

@tool
def analyze_investment(financial_document_data: str) -> str:
    """Analyze investment opportunities from financial document data
    
    Args:
        financial_document_data (str): The financial document content
        
    Returns:
        str: Investment analysis results
    """
    
    if not financial_document_data or financial_document_data.strip() == "":
        return "No financial data provided for investment analysis"
    
    try:
        # Process and clean the data
        processed_data = financial_document_data.strip()
        
        # Remove excessive whitespace
        while "  " in processed_data:
            processed_data = processed_data.replace("  ", " ")
        
        # Basic analysis 
        analysis_results = {
            "data_length": len(processed_data),
            "contains_numbers": any(char.isdigit() for char in processed_data),
            "contains_financial_keywords": any(keyword in processed_data.lower() 
                for keyword in ["revenue", "profit", "loss", "assets", "liabilities", 
                              "cash flow", "balance sheet", "income statement"]),
            "processed_data_sample": processed_data[:200] + "..." if len(processed_data) > 200 else processed_data
        }
        
        return f"Investment Analysis Results: {analysis_results}"
        
    except Exception as e:
        return f"Error in investment analysis: {str(e)}"

@tool
def assess_risk(financial_document_data: str) -> str:
    """Create risk assessment from financial document data
    
    Args:
        financial_document_data (str): The financial document content
        
    Returns:
        str: Risk assessment results
    """
    
    if not financial_document_data or financial_document_data.strip() == "":
        return "No financial data provided for risk assessment"
    
    try:
        # Process the financial data
        processed_data = financial_document_data.strip()
        
        # Basic risk indicators
        risk_indicators = {
            "data_available": bool(processed_data),
            "debt_mentioned": "debt" in processed_data.lower() or "liability" in processed_data.lower(),
            "loss_mentioned": "loss" in processed_data.lower() or "deficit" in processed_data.lower(),
            "cash_flow_mentioned": "cash flow" in processed_data.lower(),
            "risk_keywords_found": [keyword for keyword in ["risk", "uncertainty", "volatile", "fluctuation"]
                                  if keyword in processed_data.lower()]
        }
        
        return f"Risk Assessment Results: {risk_indicators}"
        
    except Exception as e:
        return f"Error in risk assessment: {str(e)}"
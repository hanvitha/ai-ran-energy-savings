
import os
from dotenv import load_dotenv
import numpy as np
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from langchain_community.llms.vllm import VLLMOpenAI
from langchain.prompts import PromptTemplate


load_dotenv()
MODEL_URL = os.environ['MODEL_URL']
MODEL_ACCESS_KEY = os.environ['MODEL_ACCESS_KEY']
# prometheus from which metrics are to be fetched
PROM_URL = os.environ.get('PROM_URL')
PROM_ACCESS_TOKEN = os.environ.get('PROM_ACCESS_TOKEN')
# Load the model (replace this with your Merlinite model if it's a custom model)
MODEL_NAME = os.environ['MODEL_NAME']  
# Helper function to generate a response from the llm
def generate_response(user_input, metrics, predictions, predictive_model):
    # print(user_input, metrics,predictions, predictive_model)

    # LLM definition
    llm = VLLMOpenAI(           # We are using the vLLM OpenAI-compatible API client. But the Model is running on OpenShift AI, not OpenAI.
        openai_api_key = MODEL_ACCESS_KEY,   # And that is why we don't need an OpenAI key for this.
        openai_api_base= f"{MODEL_URL}/v1",
        model_name=MODEL_NAME,
        top_p=0.92,
        temperature=0.01,
        max_tokens=300,
        presence_penalty=1.03,
        streaming=False,
        frequency_penalty=0.8  # Further control repetitive use of common phrases
        # callbacks=[StreamingStdOutCallbackHandler()]
    )
    # Define a PromptTemplate for Classification
     # Use LLM to interpret metrics data
    # analysis_prompt = (
    #     f"You are Kepler Bot.Based on the following Prometheus query results:\n{metrics}\n"
    #     f"Provide a human-readable analysis for the query: '{user_input}'"
    #     f"If you do not know answer, provide natural chat respectfully"
    # )
    classification_prompt = f"""
        Classify the following query into one of these categories: 
        1. Metrics-related (queries about specific metrics like energy usage, power consumption,Node metrics etc.)
        2. Prediction-related (queries about predict, forecasts, trends, or predictive models like ARIMA or LSTM)
        3. General (other queries unrelated to metrics or predictions)

        Query: "{user_input}"

        Category:
    """
    classification_response = llm.generate(prompts=[classification_prompt])
    classification = classification_response.generations[0][0].text.strip().lower()
    print("Category: "+classification)
    # Example: Analyze Metrics
    if classification == "metrics-related":
         # Define a PromptTemplate for Metrics-Related Analysis
        metrics_prompt_template = PromptTemplate(
            input_variables=["metrics", "user_input"],
            template=f"""
                You are Kepler Bot, an AI Power Savings Tool specialized in analyzing energy consumption metrics and providing actionable insights.

                ### **Prometheus Metrics on Energy Consumption of Nodes, RAN Distributed Units:**
                {metrics}

                ### **User Query:**
                {user_input}

                ### **Instructions:**
                Analyze the provided Prometheus metrics above :
                1. Identify high or low usage time patterns or potential areas for energy savings.
                2. Do not ask any further questions unless needed.
                3. respond to the user's query in a short, concise, and human-readable manner. Focus on clarity and actionable insights on saving energy.
            """ 

        )
        input_data = {"metrics": metrics, "user_input": user_input}
        print("im in metrics")
        metrics_chain = metrics_prompt_template | llm
        response = metrics_chain.invoke(input_data)
    

    # Example: Analyze Predictions
    elif classification == "prediction-related":
        # Define a PromptTemplate for Prediction-Related Analysis
        # Scale and prepare predictions
        predictive_model.eval()
        scaling_factor = 100
        predictions *= scaling_factor
        adjusted_predictions = np.clip(predictions, 0, 500)
        predictions_text = "\n".join([f"Time {i+1}: {pred}" for i, pred in enumerate(adjusted_predictions)])

        prediction_prompt_template = PromptTemplate(
            input_variables=["predictions_text", "metrics", "user_input"],
            template=f"""
                You are Kepler Bot, an AI Power Savings Tool specialized in analyzing metrics and providing actionable insights. Given the provided data, you should directly answer the user's question without asking for additional information.

                ### **Predicted Energy Consumption or Predictions generated based on historical prometheus metrics of energy consumption of nodes:**
                {predictions_text}

                ### **Prometheus Metrics on Energy Consumption of Nodes, RAN Distributed Units:**
                {metrics}

                ### **User Query:**
                {user_input}

                ### **Instructions:**
                Based on the predicted values and historical data provided above, please:
                1. Analyze the energy consumption trends.
                2. Identify high or low usage time patterns or potential areas for energy savings.
                2. Do not ask any further questions unless needed.
                4. Provide clear and concise predictions and forecast recommendations to optimize energy usage like shut down schedule etc.
                **Please present your response in bullet points for easy readability.**
            """ 
        
        )
        input_data={"predictions_text":predictions_text, 
               "metrics":metrics,
               "user_input":user_input}
        predictions_chain = prediction_prompt_template | llm
        response = predictions_chain.invoke(input_data)
   

    # Example: Handle General Queries
    else:
        # Define a PromptTemplate for General Queries
        general_prompt_template = PromptTemplate(
            input_variables=["user_input"],
            template=f"""
                You are Kepler Bot, an AI Power Savings Tool specialized in analyzing energy consumption metrics and providing actionable insights.

                ### **User Query:**
                {user_input}

                ### **Instructions:**
                Respond as a regular chatbot for a generic query. You can provide lot of insights into the energy consumption patterns in RAN Distributed Units to help Telco Admins take actions based on the patterns.
            """ 

        )
        # print("im here1")
        # Create a runnable sequence
        general_chain = general_prompt_template | llm
        input_data={"user_input":user_input}
        response = general_chain.invoke(input_data)        
    
    response = response.replace(user_input,"").strip()  # Remove leading and trailing whitespaces
    return response

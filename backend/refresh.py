
import os
from os import listdir
from os.path import isfile, join
import warnings
warnings.filterwarnings("ignore")
import pandas as pd

from prometheus_api_client import PrometheusConnect, MetricsList, MetricSnapshotDataFrame
from prometheus_api_client.utils import parse_datetime
from datetime import datetime, timedelta

# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
# from langchain.prompts import PromptTemplate
from langchain_community.llms import VLLMOpenAI
# from langchain import agents
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

# prometheus from which metrics are to be fetched
PROM_URL = os.environ.get('PROM_URL')
PROM_ACCESS_TOKEN = os.environ.get('PROM_ACCESS_TOKEN')

from datetime import datetime, timedelta
def refreshPromData():
    try:
        prom = PrometheusConnect(
            url=PROM_URL,
            disable_ssl=True,
            headers={"Authorization": f"bearer {PROM_ACCESS_TOKEN}"},
        )
        start_time = parse_datetime("7d") 
        end_time = parse_datetime("now") 
        chunk_size = timedelta(hours=1) 
        metric_data = prom.get_metric_range_data(metric_name='kepler_node_platform_joules_total',
                                                start_time=start_time, 
                                                end_time=end_time, 
                                                chunk_size=chunk_size)
        metric_df = MetricSnapshotDataFrame(metric_data)
        # metric_df.to_csv("kepler_data.csv", index=False)
        return metric_df
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying Prometheus: {e}")

import logging
import os
import io
import azure.functions as func
import pandas as pd
from azure.storage.blob import BlobServiceClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('write_conf function was triggered')    
    
    req_body = req.get_json()
    file_name = req_body.get('file_name')
    file_partition = req_body.get('file_partition')
    config_file = req_body.get('config_file')

    
    # creating sample data: 
    # conf_data = {'Name': ['Tom', 'nick', 'krish', 'jack'], 'Age': [20, 21, 19, 18]}
    # Create DataFrame with the conf content
    # df = pd.DataFrame(conf_data)    

    # get the connection string of the account to save data in
    cs = os.environ['PARQUET_CS']    
    parquet_file = io.BytesIO()
    # using blob client to read/write
    blob_service_client = BlobServiceClient.from_connection_string(cs)
    conf_container = os.environ['CONF_CONTAINER']
    
    # used for reading an existing csv file
    csv_blob_client = blob_service_client.get_blob_client(container = conf_container, blob = config_file)
    # read the csv into a df
    df = read_config(csv_blob_client)
    parquet_container = os.environ['CONF_PARQUET']
    # change this to the partition scheme required
    parquet_conf_path = f'{file_partition}/{file_name}'
    # create the blob clietn and write to it
    parquet_blob_client = blob_service_client.get_blob_client(container = parquet_container, blob = parquet_conf_path)
        
    df.to_parquet(parquet_file, engine = 'pyarrow')
    # after the load of the df, need to move it back to zero
    parquet_file.seek(0)
    parquet_blob_client.upload_blob(data = parquet_file)
    return func.HttpResponse(f"File, {config_file} was processed and saved to {parquet_conf_path}.")


def read_config(blob_client_instance):
    # get a handle to stream
    download_stream = blob_client_instance.download_blob()         
    # first read all the blob content into the stream, then use the stream as an input for pandas
    return pd.read_csv(io.BytesIO(download_stream.readall()), encoding='utf8', sep=",")
import streamlit as st
import boto3
import json

# Initialize a session using Amazon DynamoDB
session = boto3.Session(
    aws_access_key_id='AKI***********',
    aws_secret_access_key='I4y32dfd*************',
    region_name='eu-north-1'
)
lambda_client = session.client('lambda', region_name='eu-north-1') 
# Function to invoke the AWS Lambda function to process and store the post
def invoke_lambda_process_post(post_text, hashtags):
    payload = {
        'text': post_text,
        'hashtags': hashtags
    }
    response = lambda_client.invoke(
        FunctionName='hashtag',  
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )
    response_payload = json.loads(response['Payload'].read())
    return response_payload

# Function to invoke the AWS Lambda function to get trending hashtags
def invoke_lambda_get_trending_hashtags():
    response = lambda_client.invoke(
        FunctionName='hashtag',  
        InvocationType='RequestResponse',
        Payload=json.dumps({})
    )
    response_payload = json.loads(response['Payload'].read())
    return response_payload

# Streamlit User Interface
st.title("Social Media Post Publisher")

# Post composition area
post_text = st.text_area("Compose your post", height=150)
hashtags = st.text_input("Enter hashtags (comma-separated)")
hashtags_list = [tag.strip() for tag in hashtags.split(',')] if hashtags else []

# Post button
if st.button("Post"):
    if post_text:
        response_payload = invoke_lambda_process_post(post_text, hashtags_list)
        if response_payload['statusCode'] == 200:
            st.success("Post submitted successfully!")
        else:
            st.error("Failed to submit post.")
    else:
        st.warning("Post text cannot be empty.")

# Trending hashtags button
if st.button("Show Trending Hashtags"):
    response_payload = invoke_lambda_get_trending_hashtags()
    if response_payload['statusCode'] == 200:
        trending_hashtags = json.loads(response_payload['body'])
        st.subheader("Trending Hashtags:")
        for hashtag, count in trending_hashtags:
            st.write(f"{hashtag}: {count} times")
    else:
        st.error("Failed to retrieve trending hashtags.")

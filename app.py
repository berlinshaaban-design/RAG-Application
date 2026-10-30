import os
os.environ["AWS_ACCESS_KEY_ID"] = "AKIAW3XR4NNCICOGLTVU"
os.environ["AWS_SECRET_ACCESS_KEY"] = "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"
os.environ["AWS_DEFAULT_REGION"] = "eu-north-1"
from flask import Flask, render_template, request
import boto3
from botocore.exceptions import BotoCoreError, ClientError

app = Flask(__name__)

# =========================
# FILL THESE VALUES
# =========================
AWS_REGION = "us-east-1"
KNOWLEDGE_BASE_ID = "NNWWCOSUYL"
MODEL_ARN = "amazon.nova-lite-v1:0"

bedrock_agent_runtime = boto3.client(
    "bedrock-agent-runtime",
    region_name=AWS_REGION
)

def ask_knowledge_base(question: str):
    response = bedrock_agent_runtime.retrieve_and_generate(
        input={
            "text": question
        },
        retrieveAndGenerateConfiguration={
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": KNOWLEDGE_BASE_ID,
                "modelArn": MODEL_ARN
            }
        }
    )

    answer = response.get("output", {}).get("text", "")

    citations = []
    for citation in response.get("citations", []):
        refs = citation.get("retrievedReferences", [])
        for ref in refs:
            location = ref.get("location", {})
            s3_loc = location.get("s3Location", {})
            uri = s3_loc.get("uri", "")
            if uri and uri not in citations:
                citations.append(uri)

    return answer, citations


@app.route("/", methods=["GET", "POST"])
def home():
    answer = ""
    question = ""
    citations = []
    error = ""

    if request.method == "POST":
        question = request.form.get("question", "").strip()

        if not question:
            error = "Please enter a question."
        else:
            try:
                answer, citations = ask_knowledge_base(question)
                if not answer:
                    answer = "No answer returned from Bedrock."
            except (ClientError, BotoCoreError) as e:
                error = f"AWS error: {str(e)}"
            except Exception as e:
                error = f"Unexpected error: {str(e)}"

    return render_template(
        "index.html",
        question=question,
        answer=answer,
        citations=citations,
        error=error
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
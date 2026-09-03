# Import libraries
from langchain_core.messages import HumanMessage
from agent import workflow


# Create chat response function
def generate_response(data):

    # Stream graph updates
    for event in workflow.stream(
        {
            "messages": [HumanMessage(content=data.messages)],
            "mental_health_score": data.mental_health_score,
            "user_data": data.user_data,
            "question_category": "general advice",
            "score_analysis": "",
            "advisor_context": "",
            "response": ""
        },
        config={
            "configurable": {
                "thread_id": data.thread_id
            }
        },
        stream_mode="updates"
    ):

        # Send only final response
        if "generate_guidance" in event:
            yield event["generate_guidance"]["response"]
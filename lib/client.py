from openai import OpenAI
import main
import secret
Open_AI_API_KEY=secret.OPEN_AI_API_KEY
client = OpenAI(api_key=Open_AI_API_KEY)
def streamAi(prompt:str):
    prompt=f"{prompt},give output in small chunks like sentence by sentence"
    buffer=""
    with client.responses.stream(
        model="gpt-5-mini",
        input=prompt
    ) as stream:
        for event  in stream:
            if event.type=="response.output_text.delta":
                chunk=event.delta
                buffer+=chunk
                if buffer.strip().endswith((".","?","!")):
                    line=buffer.strip()
                    print(line)
                    main.speak(line)
                    buffer=""
    # final_response=stream.get_final_response()
def getAiOutput(prompt:str):
    response= client.responses.create(
        model="gpt-5-nano",
        tools=[{"type":"web_search"}],
        input=prompt
    )
    output=response.output_text
    return output
if __name__=="__main__":
    streamAi("Tell me about UN")


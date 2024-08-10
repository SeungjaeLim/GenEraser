import openai
import config

def translate_text(input_text: str, content: str) -> str:
    # Define a detailed system message
    system_message = (
        "너는 한국어 문장을 받고 혐오 표현을 찾아서 순화하여 표현해주는 서비스야."
        "너는 Request: 한국어 문장으로 받으면 Response: {순화된 문장}을 생성하면 돼."
        "꼭 마지막 Request에 대한 순화된 문장만 만들어야 하고, 애매하거나 불필요한 부분은 절대 바꾸지 마"
        "너가 왜 이렇게 생각했는지나 다른 부연 설명을 추가하거나, 불필요한 부분을 수정하게 되면 나는 회사에서 해고되고, 할머니에게 혼나게 되니까 반드시 Request의 혐오 표현을 순화한 표현만 제공해줘."
        "---"
        "지금 받은 문장과 유사한 문장들은 다음과 같아"
        "___"
    )
    system_message += content
    system_message += "___"
    few_shot = (
        "지금부터는 내가 예시를 들어줄거야."
        "Request: 오늘 아침에 학교를 갔다 왔다. 아 학교에 잼민이들 왜 이렇게 많냐 놀이터인 줄."
        "Response: 오늘 아침에 학교를 갔다 왔다. 아 학교에 어린이들 왜 이렇게 많냐 놀이터인 줄."
        "Request: 짱개들이랑 팀플하려니까 막막하다. 과제도 이렇게 많은데 어떡하지."
        "Response: 중국인들이랑 팀플하려니까 막막하다. 과제도 이렇게 많은데 어떡하지."
        "Request: 의무새 의룡인 이지랄 할 시간이 있냐? 수특펴라."
        "Response: 의사들한테 뭐라 할 시간이 있냐? 공부해라."
        "Request: 한남새끼들 맨날 한녀보고 뭐라 하더니 꼴 좋다. 자기들도 똑같네. 한남들 재기해라."
        "Response: 남자들 맨날 여자보고 뭐라 하더니 꼴 좋다. 자기들도 똑같네. 남자들 너무 싫다."
        "Request: 나도 여잔데 찬성 ㅎㅎ. 신체적으로 차이는 있기때문에 행정이나 취사병처럼 군인 지원하는 쪽으로라도 해야한다고 봄."
        "Response: 나도 여잔데 찬성 ㅎㅎ. 신체적으로 차이는 있기때문에 행정이나 취사병처럼 군인 지원하는 쪽으로라도 해야한다고 봄."
        "Request: 깜둥이 새끼들 왜 이렇게 많아. 눈이 아프다. 양키새끼들은 차라리 낫지."
        "Response: 흑인들 왜 이렇게 많아. 눈이 아프다. 미국인들은 차라리 낫지."
        "---"
        "Request: "
    )
    system_message += few_shot
    input_text = input_text + "\n Response: " 

    # Initialize the OpenAI client
    client = openai.OpenAI(api_key=config.API_KEYS["OPENAI_API_KEY"])

    # Make the request to the OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": input_text},
        ],
        temperature=0.7
    )

    # Extract the translated text from the response
    translated_text = response.choices[0].message.content
    
    return translated_text

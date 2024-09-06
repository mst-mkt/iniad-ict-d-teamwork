from typing import Literal

from langchain.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from config.settings import VECTOR_DB_DIR_PATH

from ..constants import OPENAI_API_BASEURL
from .grourmet import generate_gourmet_info
from .maps import generate_place_info

embedding_function = OpenAIEmbeddings(openai_api_base=OPENAI_API_BASEURL)
db = Chroma(persist_directory=VECTOR_DB_DIR_PATH, embedding_function=embedding_function)
retriever = db.as_retriever(search_kwargs={"k": 3})

llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0,
    openai_api_base=OPENAI_API_BASEURL,
    verbose=True,
)


class DatePlanStepModel(BaseModel):
    type: Literal["spot", "restaurant"] = Field(description="Type of the step")
    id: str = Field(description="ID of the spot or restaurant")
    from_time: str = Field(description="Start time of the step")
    to_time: str = Field(description="End time of the step")
    comment: str = Field(description="Comment of the step")


class DatePlanModel(BaseModel):
    title: str = Field(description="Title of the date plan")
    message: str = Field(description="Message of the date plan")
    steps: list[DatePlanStepModel]
    advice: str = Field(description="Advice for the date plan")


def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])


def create_date_plan_with_rag(
    spots, restaurants, all_spots, all_restaurants, weather_info, query
):
    template = """
    # 以下のcontextをデートの失敗談に関する情報が含まれています。この情報を元に、デートプランを作成してください。
    ```context
    {context}
    ```

    ## また、以下のユーザーの要望を満たすようにしてください。
    ### 要望:
    {query}
    ### 興味のあるデートスポット:
    {spots}
    ### 飲食店:
    {restaurants}
    ### 天気情報:
    {weather}
    ### steps数:
    4 ~ 6
    ### 文量
    #### message:
    長め
    #### advice:
    長め
    #### comment:
    短め

    ## 選択肢が不足している場合は以下の飲食店やデートスポットを参考にしてください。
    ### 飲食店:
    {all_restaurants}
    ### デートスポット:
    {all_spots}

    ## デートプランは以下の形式に**絶対に**従い、JSON形式で出力してください。
    ### 出力形式:
    ```output_format
    class DatePlanStepModel(BaseModel):
        type: Literal["spot", "restaurant"] = Field(description="Type of the step")
        id: str = Field(description="ID of the spot or restaurant")
        from_time: str = Field(description="Start time of the step")
        to_time: str = Field(description="End time of the step")
        comment: str = Field(description="Comment of the step")


    class DatePlanModel(BaseModel):
        title: str = Field(description="Title of the date plan")
        message: str = Field(description="Message of the date plan")
        steps: list[DatePlanStepModel]
        advice: str = Field(description="Advice for the date plan")
    ```
    """

    prompt = ChatPromptTemplate.from_template(
        template,
        partial_variables={
            "spots": "\n\n".join([generate_place_info(spot) for spot in spots]),
            "restaurants": "\n\n".join(
                [generate_gourmet_info(restaurant) for restaurant in restaurants]
            ),
            "all_spots": "\n\n".join([generate_place_info(spot) for spot in all_spots]),
            "all_restaurants": "\n\n".join(
                [generate_gourmet_info(restaurant) for restaurant in all_restaurants]
            ),
            "weather": weather_info["weather"][0]["description"],
        },
    )

    chain = (
        {
            "context": retriever | format_docs,
            "query": RunnablePassthrough(),
        }
        | prompt
        | llm.with_structured_output(DatePlanModel, method="json_mode")
    )

    res = chain.invoke(query)

    return res

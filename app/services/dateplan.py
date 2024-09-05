from typing import Literal

from langchain.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from config.settings import VECTOR_DB_DIR_PATH

from ..constants import OPENAI_API_BASEURL

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
    message: str = Field(description="Message of the date plan")
    steps: list[DatePlanStepModel]


def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])


def create_date_plan_with_rag(spots, restaurants, weather_info, query):
    template = """以下のcontextのみに基づいて質問にできるだけ詳しくjson形式で答えなさい。:
    {context}

    質問: {question}
    出力形式:
    ```
    class DatePlanStepModel(BaseModel):
        type: Literal["spot", "restaurant"] = Field(description="Type of the step")
        id: str = Field(description="ID of the spot or restaurant")
        from_time: str = Field(description="Start time of the step")
        to_time: str = Field(description="End time of the step")
        comment: str = Field(description="Comment of the step")


    class DatePlanModel(BaseModel):
        message: str = Field(description="Message of the date plan")
        steps: list[DatePlanStepModel]
    ```
    """

    prompt = ChatPromptTemplate.from_template(template, partial_variables={})

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm.with_structured_output(DatePlanModel, method="json_mode")
    )

    res = chain.invoke(query)

    return res

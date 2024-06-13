import os
from typing import List, Tuple

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import AIMessage, HumanMessage
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.runnables import RunnableParallel

class YAMRChainFactory:
    SEPARATOR = "|"
    SYSTEM_PROMPT_TEMPLATE = """As a movie and series recommender, your role is to provide personalized recommendations. Based on the following questionnaire, which includes various questions related to the user’s movie preferences, humor, age, and personality traits, generate three tailored recommendations. These recommendations should be available on the specified Video-On-Demand (VOD) platforms mentioned by the user.

    <QUESTIONNAIRE>
    {questionnaire}
    </QUESTIONNAIRE>

    Three recommendations, NAMES AND YEARS OF PRODUCTION IN PARENTHESES ONLY, without quotation marks, separated by a '""" + SEPARATOR + "':"

    OPENAI_MODEL_NAME = os.environ.get("OPENAI_MODEL_NAME")

    def create(self):
        inputs = RunnableParallel(
            {
                "questionnaire": lambda x: self._format_questionnaire(x.questions_answers),
            }
        ).with_types(input_type=YAMRChainInput)

        answer_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.SYSTEM_PROMPT_TEMPLATE),
                MessagesPlaceholder(variable_name="questionnaire"),
            ]
        )

        llm = ChatOpenAI(
            model_name=self.OPENAI_MODEL_NAME,
            streaming=False,
            max_tokens=128,
            temperature=0
        )

        chain = inputs | answer_prompt | llm | StrOutputParser()
        return chain

    def _format_questionnaire(self, questions_answers: List[Tuple[str, str]]):
        buffer = []
        for i, (question, answer) in enumerate(questions_answers, start=1):
            buffer.append(AIMessage(content=f"Question {i}: {question}"))
            buffer.append(HumanMessage(content=f"Answer {i}: {answer}"))
        return buffer

# User input
class YAMRChainInput(BaseModel):
    questions_answers: List[Tuple[str, str]]

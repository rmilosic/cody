import asyncio

from dotenv import load_dotenv
from langsmith import aevaluate

load_dotenv()

from agent.graph.graph import graph


def accuracy(outputs: dict, reference_outputs: dict) -> float:
    human_vykony = reference_outputs["vykony"]
    llm_vykony = outputs["vykony"]

    human_kody = set(v["code"] for v in human_vykony)
    llm_kody = set(v["code"] for v in llm_vykony)

    true_positives = human_kody & llm_kody

    precision = len(true_positives) / len(llm_kody) if len(llm_kody) != 0 else 0.0
    recall = len(true_positives) / len(human_kody) if len(human_kody) != 0 else 0.0

    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall != 0.0
        else 0.0
    )

    return [
        {"score": precision, "key": "precision"},
        {"score": recall, "key": "recall"},
        {"score": f1, "key": "f1"},
    ]


async def main():
    await aevaluate(
        graph | (lambda x: {"vykony": x.get("diagnosis", {}).get("vykony", [])}),
        data="rakathon-oncoders-hard",
        evaluators=[accuracy],
        max_concurrency=5,
    )


if __name__ == "__main__":
    asyncio.run(main())

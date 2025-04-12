import asyncio
import json

from dotenv import load_dotenv
from langsmith import aevaluate

from agent.graph import graph

load_dotenv()


def correct(outputs: dict, reference_outputs: dict) -> bool:
    expected_vykony = json.loads(reference_outputs["vykony"])
    expected_materialy = json.loads(reference_outputs["materialy"])

    actual_vykony = outputs.get("vykony")
    actual_materialy = outputs.get("materialy")

    return actual_vykony == expected_vykony and actual_materialy == expected_materialy


async def main():
    await aevaluate(
        graph, data="rakathon-oncoders", evaluators=[correct], max_concurrency=20
    )


if __name__ == "__main__":
    asyncio.run(main())

#!/bin/python3

from typing import List


class Result:
    def __init__(self, job_id: str, result: float) -> None:
        self.job_id: str = job_id
        self.type: str = ""
        self.result: float = result
        self.runtime: float = 0.0

    @staticmethod
    def to_csv_list(results: List["Result"]) -> List[str]:
        csv_lines = ["job_id,type,result,runtime"]
        for r in results:
            line = f"{r.job_id},{r.type},{r.result},{r.runtime}"
            csv_lines.append(line)
        return csv_lines

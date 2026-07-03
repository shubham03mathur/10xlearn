from llama_index.core.workflow import (
    Workflow,
    StartEvent,
    StopEvent,
    Event,
    step,
    WorkflowValidationError
)
from llama_index.utils.workflow import draw_all_possible_flows
import random
import asyncio


class ProcessingEvent(Event):
    intermediate_result: str

    def get_final_answer(self):
        return self.intermediate_result


class LoopEvent(Event):
    loop_output: str


class MultiStepWorkFlowWithLoop(Workflow):
    """
    Here we simulate the desicion making process and workflow decides if
    It should re-processs (loop-back) or move to the next step, for brevity,
    I am using random() method to simulate the desicion factor
    """

    @step
    async def FirstStep(
        self, ev: StartEvent | LoopEvent
    ) -> ProcessingEvent | LoopEvent:
        if random.randint(0, 1) == 0:
            """Found error loop back"""
            return LoopEvent(loop_output="go back to Step 1")
        else:
            """All good, We can proceed..."""
            return ProcessingEvent(intermediate_result="Process Completed!")

    @step
    async def FinalStep(self, ev: ProcessingEvent) -> StopEvent:
        result = ev.get_final_answer()
        return StopEvent(result=result)


async def main():
    try:
        print("starting Multi Step Workflow with loop...")
        w = MultiStepWorkFlowWithLoop(timeout=10, verbose=False)
        #This will generate HTML file to visualize the Workflow
        draw_all_possible_flows(w, "flow.html")
        res = await w.run()
        print(res)
    except WorkflowValidationError as wve:
        print(f"Workflow execution failed with WorkflowValidationError: {repr(wve)}")


if __name__ == "__main__":
    asyncio.run(main())

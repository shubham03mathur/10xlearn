import asyncio

from llama_index.core.workflow import Workflow, StartEvent, StopEvent, step, Event

class ProcessingEvent(Event):
    intermidate_result: str
    #perform some action here
    def change_to_uppercase(self)->str:
        return self.intermidate_result.upper()
    

class MultiStepWorkFlow(Workflow):
    @step
    async def first_step(self, ev: StartEvent)-> ProcessingEvent:
        return ProcessingEvent(intermidate_result="This workflow is working!")
    @step
    async def final_step(self, ev:ProcessingEvent)->StopEvent:
        intermidiate_result = ev.intermidate_result
        processed_result = ev.change_to_uppercase()
        final_result = f"Result from Step 1: {intermidiate_result}\nFinal result: {processed_result}"
        return StopEvent(final_result)
    
async def main():
    print("Executing the workflow...")
    w = MultiStepWorkFlow(timeout=10, verbose=False)
    response = await w.run()
    print(response)

if __name__=="__main__":
    asyncio.run(main())
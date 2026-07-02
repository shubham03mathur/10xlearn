from llama_index.core.workflow import StartEvent, StopEvent, Workflow, step
import asyncio

class MyWorkflow(Workflow):
    @step
    async def first_step(self, ev: StartEvent) -> StopEvent:
        return StopEvent(result="Step 1 completed")


async def main():
    w = MyWorkflow(timeout=10, verbose=False)
    result = await w.run()
    print(result)


# 3. Use the execution guard to run the event loop safely
if __name__ == "__main__":
    print("Starting workflow...")
    asyncio.run(main())
    print("Done!")

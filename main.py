from fastapi import FastAPI

from api.router import router as interview_router


app = FastAPI(title="AI Interviewer")
app.include_router(interview_router)


def main():
    print("FastAPI app created: AI Interviewer")


if __name__ == "__main__":
    main()

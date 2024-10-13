import os
from typing import Optional, List, Union

from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator

from typing_extensions import Annotated
from fastapi.middleware.cors import CORSMiddleware

from bson import ObjectId
import motor.motor_asyncio
from pymongo import ReturnDocument

app = FastAPI(
    title="Student Course API",
    summary="A sample application showing how to use FastAPI to add a ReST API to a MongoDB collection.",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:8000"],  # Multiple specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGODB_URL = os.environ.get("MONGODB_URL", "mongodb+srv://test:test@fairsight.fuef7.mongodb.net/?retryWrites=true&w=majority&appName=FairSight&tlsAllowInvalidCertificates=true")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client.fair_sight
video_collection = db.get_collection("video")
analysis_collection = db.get_collection("analysis")
fake_news_collection = db.get_collection("fake_news")

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


class VideoModel(BaseModel):
    """
    Container for a single student record.
    """

    # The primary key for the StudentModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    link: str = Field(...)
    #email: EmailStr = Field(...)
    #course: str = Field(...)
    #gpa: float = Field(..., le=4.0)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "link": "https://www.youtube.com/watch?v=rInpN0eQ4WA"
            }
        },
    )


class UpdateVideoModel(BaseModel):
    """
    A set of optional updates to be made to a document in the database.
    """

    link: Optional[str] = None
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "link": "https://www.youtube.com/watch?v=rInpN0eQ4WA"
            }
        },
    )


class VideoCollection(BaseModel):
    """
    A container holding a list of `StudentModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    videos: List[VideoModel]


@app.post(
    "/videos/",
    response_description="Add new video",
    response_model=VideoModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_video(video: VideoModel = Body(...)):
    """
    Insert a new video record.

    A unique `id` will be created and provided in the response.
    """
    new_video = await video_collection.insert_one(
        video.model_dump(by_alias=True, exclude=["id"])
    )
    created_video = await video_collection.find_one(
        {"_id": new_video.inserted_id}
    )
    return created_video


@app.get(
    "/videos/",
    response_description="List all videos",
    response_model=VideoCollection,
    response_model_by_alias=False,
)
async def list_videos():
    """
    List all of the video data in the database.

    The response is unpaginated and limited to 1000 results.
    """
    return VideoCollection(videos=await video_collection.find().to_list(1000))


@app.get(
    "/videos/{id}",
    response_description="Get a single video",
    response_model=VideoModel,
    response_model_by_alias=False,
)
async def show_video(id: str):
    """
    Get the record for a specific video, looked up by `id`.
    """
    if (
        video := await video_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return video

    raise HTTPException(status_code=404, detail=f"Video {id} not found")


@app.put(
    "/videos/{id}",
    response_description="Update a video",
    response_model=VideoModel,
    response_model_by_alias=False,
)
async def update_video(id: str, video: UpdateVideoModel = Body(...)):
    """
    Update individual fields of an existing video record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    video_update = {
        k: v for k, v in video.model_dump(by_alias=True).items() if v is not None
    }

    if len(video_update) >= 1:
        update_result = await video_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": video_update},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Video {id} not found")

    # The update is empty, but we should still return the matching document:
    if (existing_video := await video_collection.find_one({"_id": ObjectId(id)})) is not None:
        return existing_video

    raise HTTPException(status_code=404, detail=f"Video {id} not found")


@app.delete("/videos/{id}", response_description="Delete a video")
async def delete_video(id: str):
    """
    Remove a single video record from the database.
    """
    delete_result = await video_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Video {id} not found")

class AnalysisModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    videoId: PyObjectId = Field(...)
    summary: str = Field(...)
    fake_news_counter: int = Field(...)
    fake_newsId: Optional[PyObjectId] = Field(default=None)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "videoId": "5f85f36d70ff2b2b1c991234",
                "summary": "This video discusses...",
                "fake_news_counter": 3,
                "fake_newsId": "5f85f36d70ff2b2b1c995678"
            }
        },
    )

class UpdateAnalysisModel(BaseModel):
    videoId: Optional[PyObjectId] = None
    summary: Optional[str] = None
    fake_news_counter: Optional[int] = None
    fake_newsId: Optional[PyObjectId] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "summary": "Updated summary...",
                "fake_news_counter": 5
            }
        },
    )

class FakeNewsModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    number: int = Field(...)
    title: str = Field(...)
    description: str = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "number": 1,
                "title": "Misleading Claim",
                "description": "This claim is false because..."
            }
        },
    )

class UpdateFakeNewsModel(BaseModel):
    number: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "title": "Updated Misleading Claim",
                "description": "Updated description..."
            }
        },
    )

class AnalysisCollection(BaseModel):
    analyses: List[AnalysisModel]

class FakeNewsCollection(BaseModel):
    fake_news: List[FakeNewsModel]

# Analysis CRUD operations
@app.post(
    "/analyses/",
    response_description="Add new analysis",
    response_model=AnalysisModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_analysis(analysis: AnalysisModel = Body(...)):
    new_analysis = await analysis_collection.insert_one(
        analysis.model_dump(by_alias=True, exclude=["id"])
    )
    created_analysis = await analysis_collection.find_one(
        {"_id": new_analysis.inserted_id}
    )
    return created_analysis

@app.get(
    "/analyses/",
    response_description="List all analyses",
    response_model=AnalysisCollection,
    response_model_by_alias=False,
)
async def list_analyses():
    return AnalysisCollection(analyses=await analysis_collection.find().to_list(1000))

@app.get(
    "/analyses/{id}",
    response_description="Get a single analysis",
    response_model=AnalysisModel,
    response_model_by_alias=False,
)
async def show_analysis(id: str):
    if (analysis := await analysis_collection.find_one({"_id": ObjectId(id)})) is not None:
        return analysis
    raise HTTPException(status_code=404, detail=f"Analysis {id} not found")

@app.put(
    "/analyses/{id}",
    response_description="Update an analysis",
    response_model=AnalysisModel,
    response_model_by_alias=False,
)
async def update_analysis(id: str, analysis: UpdateAnalysisModel = Body(...)):
    analysis_update = {
        k: v for k, v in analysis.model_dump(by_alias=True).items() if v is not None
    }

    if len(analysis_update) >= 1:
        update_result = await analysis_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": analysis_update},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Analysis {id} not found")

    if (existing_analysis := await analysis_collection.find_one({"_id": ObjectId(id)})) is not None:
        return existing_analysis

    raise HTTPException(status_code=404, detail=f"Analysis {id} not found")

@app.delete("/analyses/{id}", response_description="Delete an analysis")
async def delete_analysis(id: str):
    delete_result = await analysis_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Analysis {id} not found")

# Fake News CRUD operations
@app.post(
    "/fake-news/",
    response_description="Add new fake news",
    response_model=FakeNewsModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_fake_news(fake_news: FakeNewsModel = Body(...)):
    new_fake_news = await fake_news_collection.insert_one(
        fake_news.model_dump(by_alias=True, exclude=["id"])
    )
    created_fake_news = await fake_news_collection.find_one(
        {"_id": new_fake_news.inserted_id}
    )
    return created_fake_news

@app.get(
    "/fake-news/",
    response_description="List all fake news",
    response_model=FakeNewsCollection,
    response_model_by_alias=False,
)
async def list_fake_news():
    return FakeNewsCollection(fake_news=await fake_news_collection.find().to_list(1000))

@app.get(
    "/fake-news/{id}",
    response_description="Get a single fake news",
    response_model=FakeNewsModel,
    response_model_by_alias=False,
)
async def show_fake_news(id: str):
    if (fake_news := await fake_news_collection.find_one({"_id": ObjectId(id)})) is not None:
        return fake_news
    raise HTTPException(status_code=404, detail=f"Fake news {id} not found")

@app.put(
    "/fake-news/{id}",
    response_description="Update a fake news",
    response_model=FakeNewsModel,
    response_model_by_alias=False,
)
async def update_fake_news(id: str, fake_news: UpdateFakeNewsModel = Body(...)):
    fake_news_update = {
        k: v for k, v in fake_news.model_dump(by_alias=True).items() if v is not None
    }

    if len(fake_news_update) >= 1:
        update_result = await fake_news_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": fake_news_update},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Fake news {id} not found")

    if (existing_fake_news := await fake_news_collection.find_one({"_id": ObjectId(id)})) is not None:
        return existing_fake_news

    raise HTTPException(status_code=404, detail=f"Fake news {id} not found")

@app.delete("/fake-news/{id}", response_description="Delete a fake news")
async def delete_fake_news(id: str):
    delete_result = await fake_news_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Fake news {id} not found")

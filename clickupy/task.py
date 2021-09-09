from typing import Optional, List, Any
from pydantic import BaseModel,  ValidationError, validator, Field
from clickupy.customfield import CustomField
from clickupy.status import Status
from clickupy.creator import Creator
from clickupy import client
from clickupy import attachment
from clickupy.priority import Priority

import ntpath

import os

class ClickupList(BaseModel):
    id: str = None


class Folder(BaseModel):
    id: str = None


class Space(BaseModel):
    id: str = None


class Task(BaseModel):
    id: str = None
    custom_id: None = None
    name: str = None
    text_content: str = None
    description: str = None
    status: Status = None
    orderindex: str = None
    date_created: str = None
    date_updated: str = None
    date_closed: None = None
    creator: Creator = None
    task_assignees: List[Any] = Field(None, alias="assignees")
    task_checklists: List[Any] = Field(None, alias="checklists")
    task_tags: List[Any] = Field(None, alias="tags")
    parent: str = None
    priority: Optional[Priority]
    due_date: str = None
    start_date: str = None
    time_estimate: str = None
    time_spent: Optional[str] = None
    custom_fields: List[CustomField] = None
    list: ClickupList
    folder: Folder
    space: Folder
    url: str

    @validator('priority')
    def check_status(cls, v):

        if v =="":
            v = 4
        
            return v


    def build_task(self):
        return Task(**self)

    def upload_attachment(self, file_path: str, client_instance:client):
        from clickupy import client
        if os.path.exists(file_path):

            f = open(file_path, 'rb')
            files = [
                ('attachment', (f.name, open(
                    file_path, 'rb')))
            ]
            data = {'filename': ntpath.basename(f.name)}
            model = "task/" + self.id
            uploaded_attachment = client_instance._post_request(
                model, data, files, True, "attachment")

            if uploaded_attachment:
                final_attachment = attachment.build_attachment(uploaded_attachment)
            return final_attachment

    
class Tasks(BaseModel):
    tasks: List[Task] = None

    def build_tasks(self):
        return Tasks(**self)
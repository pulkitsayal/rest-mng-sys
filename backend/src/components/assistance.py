from fastapi import APIRouter

router = APIRouter()

@router.get("/assistances")
async def view_assistances():
    with open("data_files/assist_queue.txt", "r") as file_object:
        assistance_queue = [line.strip().split() for line in file_object]
    return assistance_queue

@router.post("/assistances/add/{table_num}")
async def add_assistances(table_num: int, assistance_type: str):
    with open("data_files/assist_queue.txt", "r") as file_object:
        # Check if table number already exists in the file
        if str(table_num) in file_object.read().splitlines():
            return {"message": f"Table {table_num} is already awaiting assistance"}
    
    # Append table number and assistance type to the file
    with open("data_files/assist_queue.txt", "a") as file_object:
        file_object.write(f"{table_num} {assistance_type}\n")

    return {"message": f"Table {table_num} successfully added to the assistance queue"}

@router.post("/assistances/finish/{table_num}")
async def finish_assistances(table_num: int, assistance_type: str):
    request = f"{table_num} {assistance_type}"

    # Use a context manager to open the file for reading
    with open("data_files/assist_queue.txt", "r") as file_object:
        # Check if the assistance request exists in the file
        if request in file_object.read().splitlines():
            # Remove the line with the assistance request
            with open("data_files/assist_queue.txt", "r") as file:
                lines = file.readlines()

            with open("data_files/assist_queue.txt", "w") as file:
                for line in lines:
                    if line.strip("\n") != request:
                        file.write(line)

            return {"message": f"Table {table_num} has been removed from the assistance queue"}
        else:
            return {"message": f"Table {table_num} is not in the assistance queue"}

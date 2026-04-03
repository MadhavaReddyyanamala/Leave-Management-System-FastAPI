from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
import crud
from database import engine, Base, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Leave Management System")


@app.get("/")
def root():
    return {"message": "Leave Management System API is running"}


@app.post("/employees/", response_model=schemas.EmployeeResponse)
def add_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db, employee)


@app.get("/employees/", response_model=list[schemas.EmployeeResponse])
def list_employees(db: Session = Depends(get_db)):
    return crud.get_employees(db)


@app.post("/leaves/", response_model=schemas.LeaveResponse)
def apply_leave(leave: schemas.LeaveCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_leave(db, leave)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/leaves/", response_model=list[schemas.LeaveResponse])
def list_all_leaves(db: Session = Depends(get_db)):
    return crud.get_all_leaves(db)


@app.get("/employees/{employee_id}/leaves", response_model=list[schemas.LeaveResponse])
def list_employee_leaves(employee_id: int, db: Session = Depends(get_db)):
    return crud.get_employee_leaves(db, employee_id)


@app.put("/leaves/{leave_id}", response_model=schemas.LeaveResponse)
def edit_leave(leave_id: int, leave_update: schemas.LeaveUpdate, db: Session = Depends(get_db)):
    try:
        updated = crud.update_leave(db, leave_id, leave_update)
        if not updated:
            raise HTTPException(status_code=404, detail="Leave request not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/leaves/{leave_id}")
def remove_leave(leave_id: int, db: Session = Depends(get_db)):
    try:
        deleted = crud.delete_leave(db, leave_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Leave request not found")
        return {"message": "Leave request deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/leaves/{leave_id}/approve", response_model=schemas.LeaveResponse)
def approve_leave(leave_id: int, db: Session = Depends(get_db)):
    try:
        approved = crud.approve_leave(db, leave_id)
        if not approved:
            raise HTTPException(status_code=404, detail="Leave request not found")
        return approved
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/leaves/{leave_id}/reject", response_model=schemas.LeaveResponse)
def reject_leave(leave_id: int, db: Session = Depends(get_db)):
    try:
        rejected = crud.reject_leave(db, leave_id)
        if not rejected:
            raise HTTPException(status_code=404, detail="Leave request not found")
        return rejected
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
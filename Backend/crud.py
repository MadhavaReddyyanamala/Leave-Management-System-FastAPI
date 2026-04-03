from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import and_
import models
import schemas


def create_employee(db: Session, employee: schemas.EmployeeCreate):
    db_employee = models.Employee(name=employee.name, email=employee.email)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def get_employees(db: Session):
    return db.query(models.Employee).all()


def is_overlapping_leave(db: Session, employee_id: int, start_date: date, end_date: date, exclude_leave_id: int = None):
    query = db.query(models.LeaveRequest).filter(
        models.LeaveRequest.employee_id == employee_id,
        models.LeaveRequest.status.in_(["Pending", "Approved"]),
        and_(
            models.LeaveRequest.start_date <= end_date,
            models.LeaveRequest.end_date >= start_date
        )
    )

    if exclude_leave_id:
        query = query.filter(models.LeaveRequest.id != exclude_leave_id)

    return db.query(query.exists()).scalar()


def create_leave(db: Session, leave: schemas.LeaveCreate):
    today = date.today()

    if leave.start_date < today or leave.end_date < today:
        raise ValueError("Cannot apply leave for past dates")

    if is_overlapping_leave(db, leave.employee_id, leave.start_date, leave.end_date):
        raise ValueError("Overlapping leave request exists")

    db_leave = models.LeaveRequest(
        employee_id=leave.employee_id,
        leave_type=leave.leave_type,
        start_date=leave.start_date,
        end_date=leave.end_date,
        reason=leave.reason,
        status="Pending"
    )
    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)

    return {
        "id": db_leave.id,
        "employee_id": db_leave.employee_id,
        "employee_name": db_leave.employee.name,
        "leave_type": db_leave.leave_type,
        "start_date": db_leave.start_date,
        "end_date": db_leave.end_date,
        "reason": db_leave.reason,
        "status": db_leave.status
    }


def get_all_leaves(db: Session):
    leaves = db.query(models.LeaveRequest).all()

    result = []
    for leave in leaves:
        result.append({
            "id": leave.id,
            "employee_id": leave.employee_id,
            "employee_name": leave.employee.name,
            "leave_type": leave.leave_type,
            "start_date": leave.start_date,
            "end_date": leave.end_date,
            "reason": leave.reason,
            "status": leave.status
        })

    return result


def get_employee_leaves(db: Session, employee_id: int):
    leaves = db.query(models.LeaveRequest).filter(
        models.LeaveRequest.employee_id == employee_id
    ).all()

    result = []
    for leave in leaves:
        result.append({
            "id": leave.id,
            "employee_id": leave.employee_id,
            "employee_name": leave.employee.name,
            "leave_type": leave.leave_type,
            "start_date": leave.start_date,
            "end_date": leave.end_date,
            "reason": leave.reason,
            "status": leave.status
        })

    return result


def update_leave(db: Session, leave_id: int, leave_update: schemas.LeaveUpdate):
    db_leave = db.query(models.LeaveRequest).filter(models.LeaveRequest.id == leave_id).first()

    if not db_leave:
        return None

    if db_leave.status != "Pending":
        raise ValueError("Only pending requests can be updated")

    today = date.today()
    if leave_update.start_date < today or leave_update.end_date < today:
        raise ValueError("Cannot apply leave for past dates")

    if is_overlapping_leave(
        db,
        db_leave.employee_id,
        leave_update.start_date,
        leave_update.end_date,
        exclude_leave_id=leave_id
    ):
        raise ValueError("Overlapping leave request exists")

    db_leave.leave_type = leave_update.leave_type
    db_leave.start_date = leave_update.start_date
    db_leave.end_date = leave_update.end_date
    db_leave.reason = leave_update.reason

    db.commit()
    db.refresh(db_leave)

    return {
        "id": db_leave.id,
        "employee_id": db_leave.employee_id,
        "employee_name": db_leave.employee.name,
        "leave_type": db_leave.leave_type,
        "start_date": db_leave.start_date,
        "end_date": db_leave.end_date,
        "reason": db_leave.reason,
        "status": db_leave.status
    }


def delete_leave(db: Session, leave_id: int):
    db_leave = db.query(models.LeaveRequest).filter(models.LeaveRequest.id == leave_id).first()

    if not db_leave:
        return None

    if db_leave.status != "Pending":
        raise ValueError("Only pending requests can be deleted")

    db.delete(db_leave)
    db.commit()
    return True


def approve_leave(db: Session, leave_id: int):
    db_leave = db.query(models.LeaveRequest).filter(models.LeaveRequest.id == leave_id).first()

    if not db_leave:
        return None

    if db_leave.status != "Pending":
        raise ValueError("Only pending requests can be approved")

    db_leave.status = "Approved"
    db.commit()
    db.refresh(db_leave)

    return {
        "id": db_leave.id,
        "employee_id": db_leave.employee_id,
        "employee_name": db_leave.employee.name,
        "leave_type": db_leave.leave_type,
        "start_date": db_leave.start_date,
        "end_date": db_leave.end_date,
        "reason": db_leave.reason,
        "status": db_leave.status
    }


def reject_leave(db: Session, leave_id: int):
    db_leave = db.query(models.LeaveRequest).filter(models.LeaveRequest.id == leave_id).first()

    if not db_leave:
        return None

    if db_leave.status != "Pending":
        raise ValueError("Only pending requests can be rejected")

    db_leave.status = "Rejected"
    db.commit()
    db.refresh(db_leave)

    return {
        "id": db_leave.id,
        "employee_id": db_leave.employee_id,
        "employee_name": db_leave.employee.name,
        "leave_type": db_leave.leave_type,
        "start_date": db_leave.start_date,
        "end_date": db_leave.end_date,
        "reason": db_leave.reason,
        "status": db_leave.status
    }